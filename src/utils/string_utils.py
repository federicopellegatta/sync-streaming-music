from re import sub
import difflib


def string_similarity(str1, str2):
    if str1 is None and str2 is None:
        return 1.0
    elif str1 is None or str2 is None:
        return 0.0
    else:
        result = difflib.SequenceMatcher(a=str1.lower(), b=str2.lower())
        return result.ratio()


def remove_parenthesis_content(string):
    return string.split("(")[0] if string is not None else None


def get_string_before_dash(string):
    return string.split("-")[0] if string is not None else None


def snake_case(str):
    return '_'.join(
        sub('([A-Z][a-z]+)', r' \1',
            sub('([A-Z]+)', r' \1',
                str.replace('-', ' '))).split()).lower()


def title_case(str):
    return ' '.join(
        sub('([A-Z][a-z]+)', r' \1',
            sub('([A-Z]+)', r' \1',
                str.replace('_', ' '))).split()).title()
