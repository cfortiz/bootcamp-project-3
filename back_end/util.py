import csv
from functools import lru_cache as memoized


def load_utf8_csv(filename, *, has_headers=True):
    """Load data from a UTF-8 encoded CSV file.
    
    Args:
        filename: Name of the CSV file as a string
        has_headers: If true, the CSV file has headers in the first row
            (default: True)
    
    Returns:
        A `list[dict[str,str]]` if the CSV file has headers; otherwise, a
        `list[list[str]]`.
    
    """
    with open(filename, 'r', encoding='utf-8-sig') as csv_file:
        reader = csv.reader(csv_file)
        data = list(reader)
    if has_headers:
        headers, rows = data[0], data[1:]
        data = [
            dict(zip(headers, row))
            for row in rows
        ]
    return data


def rename_fields(source_data, renamed_fields):
    """Rename fields in a dictionary
    
    Args:
        source_data: A dict or list of dicts
    
    Returns:
        A dict or list of dicts, where each such dict has its fields renamed if
        an old-to-new name mapping is found in `renamed_fields`.
    
    """
    def rename_dict_fields(source_dict):
        return {
            renamed_fields.get(field, field): value
            for field, value in source_dict.items()
        }

    if isinstance(source_data, list):
        return list(map(rename_dict_fields, source_data))
    elif isinstance(source_data, dict):
        return rename_dict_fields(source_data)
    else:
        raise TypeError('source_data must be a dict oor list of dicts')
