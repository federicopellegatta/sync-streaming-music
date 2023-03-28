import json


def read_file(path: str) -> str:
    """
    Reads a file and returns its content.

    Parameters
    ----------
    path : str
        The path to the file.

    Returns
    -------
    str
        The content of the file.
    """
    with open(path, mode="r", encoding="utf-8") as file:
        return file.read()


def get_json_from_file(path: str) -> json:
    """
    Returns the JSON object from a json file.

    Parameters
    ----------
    path : str
        The path to the file.

    Returns
    -------
    dict
        The JSON from the file.
    """
    return json.loads(read_file(path))
