import json
import yaml
from datetime import datetime


def load_data_from_json(path: str) -> dict:
    """Extract data from JSON file.

    Args:
        path (str): Path to the JSON file.
    """
    with open(path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
    return data


def load_data_from_yaml(path: str) -> dict:
    """Extract data from YAML file.
    Args:
        path (str): Path to the YAML file.
    """
    with open(path, "r", encoding="utf-8") as yaml_file:
        data = yaml.safe_load(yaml_file)
    return data


def timedelta_in_months(start_date: datetime, end_date: datetime | None = None) -> int:
    """Get date difference in months.

    Args:
        start_date (datetime): Starting date.
        end_date (datetime | None): End date. If None uses real-time date.
    """
    if end_date is None:
        end_date = datetime.now()
    return 12 * (end_date.year - start_date.year) + (end_date.month - start_date.month)
