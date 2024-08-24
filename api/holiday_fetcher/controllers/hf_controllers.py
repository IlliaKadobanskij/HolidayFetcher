from fastapi import HTTPException

from holiday_fetcher.schemas.hf_schemas import CountryHolidaysRequest, Holiday, Country, HolidayDate, DateDetails
from holiday_fetcher.services import CalendarificClient
from requests.exceptions import HTTPError, Timeout, RequestException

from holiday_fetcher.utils.hf_utils import save_holidays_to_file

client = CalendarificClient()


def get_holidays(request: CountryHolidaysRequest):
    """
        Fetches and returns holidays for the specified countries and date range.

        This endpoint retrieves holiday data from the Calendarific API based on the given countries and date range,
        processes the data into a structured format, and saves it to a file. It also handles various exceptions that
        may occur during the process.

        Args:
            request (CountryHolidaysRequest): Request body containing the list of countries and the date range
                                              for which holidays need to be fetched.

        Returns:
            Dict[str, List[Holiday]]: A dictionary where the keys are country codes and the values are lists of
                                      `Holiday` objects representing the holidays in each country.

        Raises:
            HTTPException: If there is an HTTP error, request timeout, invalid data format, or other exceptions.
    """

    holidays_data = {}
    countries_list = request.countries_list

    try:
        holidays_in_range = client.get_holidays_in_range(
            countries_list=countries_list,
            start_time=request.start_time,
            end_time=request.end_time
        )

        if not holidays_in_range:
            raise HTTPException(status_code=404, detail="No holidays found in the given date range.")

        for country_code in countries_list:
            country_holidays = [Holiday(
                name=holiday['name'],
                description=holiday['description'],
                country=Country(
                    id=holiday['country']['id'],
                    name=holiday['country']['name']
                ),
                date=HolidayDate(
                    iso=holiday['date']['iso'],
                    datetime=DateDetails(
                        year=holiday['date']['datetime']['year'],
                        month=holiday['date']['datetime']['month'],
                        day=holiday['date']['datetime']['day']
                    )
                ),
                type=holiday['type'],
                primary_type=holiday['primary_type'],
                canonical_url=holiday['canonical_url'],
                urlid=holiday['urlid'],
                locations=holiday['locations'],
                states=holiday['states']
            ) for holiday in holidays_in_range if holiday['country']['id'] == country_code.lower()]

            holidays_data[country_code] = country_holidays

        if holidays_data:
            save_holidays_to_file(countries_list, holidays_data)

    except HTTPError as e:
        raise HTTPException(status_code=500, detail=f"HTTP error occurred: {str(e)}")
    except Timeout as e:
        raise HTTPException(status_code=504, detail=f"Request timed out: {str(e)}")
    except RequestException as e:
        raise HTTPException(status_code=500, detail=f"Request error occurred: {str(e)}")
    except KeyError as e:
        raise HTTPException(status_code=500, detail=f"Missing expected data in response: {str(e)}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid data format: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

    return holidays_data
