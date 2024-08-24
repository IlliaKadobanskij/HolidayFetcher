from pydantic import BaseModel, Field
from datetime import datetime

from typing import List, Dict


class DateDetails(BaseModel):
    """
        Represents detailed date information.
        """

    year: int = Field(..., description="Year of the date. Example: 1992.")
    month: int = Field(..., description="Month of the date. Example: 8.")
    day: int = Field(..., description="Day of the date. Example: 24.")


class HolidayDate(BaseModel):
    """
        Represents the date of the holiday.
        """

    iso: str = Field(..., description="Date in ISO 8601 format. Example: 1992-08-24.")
    datetime: DateDetails = Field(..., description="Detailed date information including year, month, and day.")

    def model_dump(self, date_format: str = "%Y-%m-%dT%H:%M:%S%z", *args, **kwargs) -> Dict[str, str]:
        """
        Custom method to serialize the model instance to a dictionary with a customizable date format.

        Args:
            date_format (str): The format for the date field. Default is ISO 8601.

        Returns:
            Dict[str, str]: The serialized model as a dictionary with formatted date.
        """
        base_dict = super().model_dump(*args, **kwargs)
        base_dict['datetime'] = self.datetime.strftime(date_format)

        return base_dict


class Country(BaseModel):
    """
        Represents a country where the holiday is observed.
        """

    id: str = Field(..., description="Country code. Example: 'ua'.")
    name: str = Field(..., description="Name of the country. Example: 'Ukraine'.")


class Holiday(BaseModel):
    """
        Represents a holiday with all related details.
    """

    name: str = Field(..., description="The name of the holiday.")
    description: str = Field(..., description="Description of the holiday.")
    country: Country = Field(..., description="Country where the holiday is observed.")
    date: HolidayDate = Field(..., description="Date of the holiday.")
    type: List[str] = Field(..., description="Types of the holiday.")
    primary_type: str = Field(..., description="Primary type of the holiday.")
    canonical_url: str = Field(..., description="Canonical URL for the holiday.")
    urlid: str = Field(..., description="URL identifier for the holiday.")
    locations: str = Field(..., description="Locations where the holiday is observed.")
    states: str = Field(..., description="States where the holiday is observed.")


class CountryHolidaysRequest(BaseModel):
    """
    Represents a request to fetch holidays for a list of countries within a specified date range.
    """

    countries_list: List[str] = Field(..., description="List of country codes for which to retrieve holidays. Example: ['UA', 'US'].")
    start_time: datetime = Field(..., description="The start time for the range of holidays to retrieve in ISO 8601 format. Example: 2024-05-24T10:16:48.147Z.")
    end_time: datetime = Field(..., description="The end time for the range of holidays to retrieve in ISO 8601 format. Example: 2024-08-24T10:16:48.147Z.")

    class Config:
        json_schema_extra = {
            'example':
                {
                      "countries_list": [
                        "UA", "FR"
                      ],
                      "start_time": "2024-06-24T11:26:23.588Z",
                      "end_time": "2024-09-24T11:26:23.588Z"
                }
        }