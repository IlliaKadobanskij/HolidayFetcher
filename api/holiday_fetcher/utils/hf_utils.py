import json

from typing import List, Dict
from pathlib import Path

from holiday_fetcher.schemas import Holiday


def save_holidays_to_file(country_code: List[str], holidays: Dict[str, List[Holiday]]):
    """
        Saves holiday data to a JSON file.

        Args:
            country_code (List[str]): List of country codes used to name the file.
            holidays (Dict[str, List[Holiday]]): Dictionary where keys are country codes and values are lists of `Holiday` objects.

        Returns:
            None

        Raises:
            IOError: If there is an error opening or writing to the file.
    """

    data_dir = Path(__file__).resolve().parent.parent.parent / 'data'
    data_dir.mkdir(parents=True, exist_ok=True)

    file_path = data_dir / f"{'_'.join(country_code)}_holidays.json"

    holidays_dict = {
        country: [holiday.model_dump() for holiday in holiday_list]
        for country, holiday_list in holidays.items()
    }

    try:
        with file_path.open('w', encoding='utf-8') as f:
            json.dump(holidays_dict, f, ensure_ascii=False, indent=4)
    except IOError as e:
        raise IOError(f"Error writing to file: {str(e)}")
