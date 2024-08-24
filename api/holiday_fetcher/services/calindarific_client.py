from datetime import datetime
import pytz

import requests
from config import settings
from requests.exceptions import HTTPError, Timeout, RequestException


class CalendarificClient:
    """
        A client for interacting with the Calendarific API to fetch holiday data.
    """

    def __init__(self):
        """
                Initializes the CalendarificClient with API key and base URL from settings.
        """

        self.api_key = settings.CALENDARIFIC_API_KEY
        self.base_url = settings.BASE_URL

    def get_holidays(self, country_code: str, year: int, month: int = None, day: int = None):
        """
                Fetches holidays for a specific country and year, optionally filtering by month and day.

                Args:
                    country_code (str): The country code (e.g., 'us' for the United States).
                    year (int): The year for which to fetch holidays.
                    month (int, optional): The month for which to fetch holidays. Defaults to None.
                    day (int, optional): The day for which to fetch holidays. Defaults to None.

                Returns:
                    dict: The JSON response containing holiday data.

                Raises:
                    HTTPError: If the HTTP request returned an unsuccessful status code.
                    Timeout: If the request timed out.
                    RequestException: For any other request-related issues.
        """

        params = {
            'api_key': self.api_key,
            'country': country_code,
            'year': year,
            **({'month': month} if month is not None else {}),
            **({'day': day} if day is not None else {})
        }

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()  # Will raise an HTTPError for bad responses
        except HTTPError as e:
            raise HTTPError(f"HTTP error occurred while fetching holidays: {str(e)}")
        except Timeout as e:
            raise Timeout(f"Request timed out while fetching holidays: {str(e)}")
        except RequestException as e:
            raise RequestException(f"Error occurred while fetching holidays: {str(e)}")

        return response.json()

    def get_holidays_in_range(self, countries_list: list, start_time: datetime, end_time: datetime):
        """
                Fetches holidays for multiple countries within a specified date range.

                Args:
                    countries_list (list): List of country codes for which to fetch holidays.
                    start_time (datetime): The start date of the range.
                    end_time (datetime): The end date of the range.

                Returns:
                    list: A list of holidays within the specified date range.

                Raises:
                    RuntimeError: If there is an error fetching holidays for a specific country or date range.
        """

        holidays_in_range = []

        for country in countries_list:
            current_year = start_time.year
            end_year = end_time.year

            if current_year == end_year:
                try:
                    holidays = self.get_holidays(country_code=country, year=current_year)
                    holidays_in_range.extend(
                        CalendarificClient.filter_holidays_by_date_range(holidays, start_time, end_time))
                except Exception as e:
                    raise RuntimeError(f"Error fetching holidays for {country} in year {current_year}: {str(e)}")
            else:
                try:
                    holidays = self.get_holidays(country_code=country, year=current_year)
                    holidays_in_range.extend(CalendarificClient.filter_holidays_by_date_range(holidays, start_time, datetime(current_year, 12, 31)))

                    for year in range(current_year + 1, end_year):
                        holidays = self.get_holidays(country_code=country, year=year)
                        holidays_in_range.extend(holidays['response']['holidays'])

                    holidays = self.get_holidays(country_code=country, year=end_year)
                    holidays_in_range.extend(CalendarificClient.filter_holidays_by_date_range(holidays, datetime(end_year, 1, 1), end_time))
                except Exception as e:
                    raise RuntimeError(
                        f"Error fetching holidays for {country} in range {current_year}-{end_year}: {str(e)}")

        return holidays_in_range

    @staticmethod
    def filter_holidays_by_date_range(holidays: dict, start_date: datetime, end_date: datetime):
        """
                Filters holidays to include only those within the specified date range.

                Args:
                    holidays (dict): The JSON response containing holiday data.
                    start_date (datetime): The start date of the range.
                    end_date (datetime): The end date of the range.

                Returns:
                    list: A list of holidays within the specified date range.

                Raises:
                    ValueError: If there is an error parsing the holiday date.
                    KeyError: If an expected field is missing in the holiday data.
        """

        start_date = start_date.astimezone(pytz.UTC)
        end_date = end_date.astimezone(pytz.UTC)

        filtered_holidays = []
        for holiday in holidays['response']['holidays']:
            try:
                holiday_date = datetime.fromisoformat(holiday['date']['iso']).astimezone(pytz.UTC)
                if start_date <= holiday_date <= end_date:
                    filtered_holidays.append(holiday)
            except ValueError as e:
                raise ValueError(f"Error parsing holiday date: {str(e)}")
            except KeyError as e:
                raise KeyError(f"Missing expected field in holiday data: {str(e)}")
        return filtered_holidays
