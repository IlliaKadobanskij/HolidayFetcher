from fastapi import APIRouter
from holiday_fetcher.controllers.hf_controllers import get_holidays
from holiday_fetcher.schemas.hf_schemas import CountryHolidaysRequest

router = APIRouter()


@router.post(
    "/holidays/",
    summary="Fetch Holidays",
    description="Retrieves holidays for the specified countries and date range from the Calendarific API. Returns the holiday data for each country within the provided date range. Uses the `CountryHolidaysRequest` schema to validate and process the input request.",
    response_description="Returns a dictionary where the keys are country codes and the values are lists of holidays for each country. Each holiday contains detailed information including the name, description, date, and more."
)
def get_holidays_handler(request: CountryHolidaysRequest):
    """
    Handles POST requests to fetch holidays based on the given input parameters.

    This endpoint processes the request to fetch holidays data for the specified countries and date range.
    It delegates the task to the `get_holidays` function from `hf_controllers`, which interacts with the
    Calendarific API to retrieve the required data.

    Args:
        request (CountryHolidaysRequest): The request body containing the list of countries and the date range
                                          for which holidays need to be fetched.

    Returns:
        CountryHolidaysRequest: The response containing the requested holidays data structured according to
                                the `CountryHolidaysRequest` schema.

    Raises:
        HTTPException: If there is an HTTP error, request timeout, invalid data format, or other exceptions.
    """
    return get_holidays(request)
