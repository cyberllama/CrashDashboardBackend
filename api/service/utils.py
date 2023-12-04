import csv
from pathlib import Path
from typing import List

# Returns a CSV as a list of dicts
def csv_to_dicts(filepath: str) -> List[dict]:
    path = Path(filepath)
    with open (path, 'r') as file:
        return [d for d in csv.DictReader(file)]

# Filters a list of dicts to only include the given fields
def filter_for_fields(data: List[dict], *fields):
    filtered_data = []
    for entry in data:
        filtered_entry = {f: entry[f] for f in fields}
        filtered_data.append(filtered_entry)
    return filtered_data