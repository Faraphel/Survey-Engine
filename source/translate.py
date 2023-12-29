import warnings
from typing import Optional


Translatable = dict[str, str]

current_language_code: str = "en"


def set_language(language_code: str) -> None:
    """
    Set the current language of the application
    :param language_code: the new language code
    """

    global current_language_code
    current_language_code = language_code


def get_language() -> str:
    """
    Get the current language of the application
    :return: the current language of the application
    """

    return current_language_code


def translate(language_data: Translatable) -> str:
    """
    Get the translation of a text to the current set language
    :param language_data: a dictionary with every translation associated to the language
    :return: the translation for the current language
    """

    translation: Optional[str] = language_data.get(current_language_code)

    if translation is None:
        warnings.warn(f"No translation for language {current_language_code!r} for text {language_data!r}")
        translation = language_data.get("en")

    if translation is None:
        raise Exception(f"No translation available for text {language_data!r}")

    return translation
