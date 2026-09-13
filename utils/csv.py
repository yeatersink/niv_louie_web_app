# utils/csv.py

import pandas as pd
import warnings
from utils.project import project
from utils.storage import get_user_projects_dir
from utils.project_errors import ProjectCsvError, format_header_list


def get_source_path():
    """Helper to get the source CSV path for the current project."""
    projects_dir = get_user_projects_dir()
    source_dir = projects_dir / "source"
    source_dir.mkdir(parents=True, exist_ok=True)
    return source_dir / f"{project.project_name}.csv"


def _strip_columns(df):
    df.columns = [str(c).replace("\ufeff", "").strip() for c in df.columns]
    return df


def create_filtered_csv():
    """
    This function creates a filtered csv file that only contains the characters, names, and braille codes for the language    
    """
    print("Generating", project.project_name, "Spreadsheet")

    source_path = get_source_path()
    projects_dir = get_user_projects_dir()
    filtered_path = projects_dir / f"filtered_{project.project_name}.csv"

    language_file = pd.read_csv(source_path, encoding="utf-8-sig")
    _strip_columns(language_file)
    headers = list(language_file.columns)

    if not headers:
        raise ProjectCsvError(
            "No header row found",
            "The spreadsheet has no column names, so it cannot be filtered.",
            "Open the file, put headers in the first row, save as CSV, then upload it again.",
        )

    mappings = [
        ("Character column", project.project_character_column),
        ("Character name column", project.project_name_column),
        ("Unicode / Hex column", project.project_unicode_column),
        ("Type column", project.project_type_column),
        ("Braille column", project.project_braille_column),
    ]

    missing_required = [label for label, value in mappings if value is None]
    if missing_required:
        raise ProjectCsvError(
            "Column matching incomplete",
            (
                "A required mapping is empty: "
                + ", ".join(missing_required)
                + f". Headers in the file: {format_header_list(headers)}."
            ),
            "Match each list to a column in your file, including Braille. Then save again.",
        )

    missing_in_file = [
        f'{label} ("{value}")' for label, value in mappings if value not in language_file.columns
    ]
    if missing_in_file:
        raise ProjectCsvError(
            "A mapped column is not in the file",
            (
                "These mapped columns were not found: "
                + ", ".join(missing_in_file)
                + f". Headers in the file: {format_header_list(headers)}."
            ),
            "Your first row is the headers. One header has a space before Character. "
            "Re-save the CSV without leading spaces, or pick the header that JAWS reads with the space.",
        )

    hex_col = project.project_unicode_column
    type_col = project.project_type_column
    needed = [
        project.project_character_column,
        hex_col,
        type_col,
        project.project_name_column,
        project.project_braille_column,
    ]

    try:
        filtered_language = language_file[needed].copy()
    except KeyError as ex:
        raise ProjectCsvError(
            "A mapped column is missing",
            (
                f"Could not find one of the mapped columns ({ex}). "
                f"Headers in the file: {format_header_list(headers)}."
            ),
            "Your first row is the headers. One header has a space before Character. "
            "Re-save the CSV without leading spaces, or pick the header that JAWS reads with the space.",
        ) from ex

    name_column = filtered_language[[project.project_name_column]].copy()
    name_column[project.project_name_column] = name_column[project.project_name_column].astype(str)
    new_name_column = name_column[project.project_name_column].apply(format_names)
    filtered_language[project.project_name_column] = new_name_column

    hex_as_str = filtered_language[hex_col].astype(str)
    if filtered_language[(hex_as_str.str.contains(r"\+", na=False)) & (filtered_language[type_col] != "always")].shape[0] > 0:
        warnings.warn("There are characters with multiple hex values that are not set to always")
        print(filtered_language[(hex_as_str.str.contains(r"\+", na=False)) & (filtered_language[type_col] != "always")])

    if filtered_language.duplicated(keep=False, subset=[hex_col]).sum() > 0:
        warnings.warn("There are duplicates in the language file")
        print(filtered_language[filtered_language.duplicated(keep=False, subset=[hex_col])])

    filtered_language = filtered_language.sort_values(by=[hex_col], key=lambda x: x.astype(str).str.len(), ascending=False)

    filtered_path.parent.mkdir(parents=True, exist_ok=True)
    filtered_language.to_csv(filtered_path, index=False)
    print("Spreadsheet Generated")


def format_names(name):
    """
    This function removes unwanted characters from the name of the character
    """
    if not isinstance(name, str):
        name = str(name)

    if project.project_replace is not None:
        for phrase in project.project_replace:
            if phrase in name:
                name = name.replace(phrase, "").strip()
    return name


def regenerate_characters_using_hex():
    """
    This function regenerates the characters in the language file from the Hex column
    """
    print("Regenerating characters from Hex")

    source_path = get_source_path()

    language_file = pd.read_csv(source_path, encoding="utf-8-sig")
    _strip_columns(language_file)

    hex_col = project.project_unicode_column or "Hex"
    language_file[project.project_character_column] = language_file[hex_col].apply(generate_characters)

    language_file.to_csv(source_path, index=False)
    print("Characters regenerated")


def generate_characters(hex_str):
    """
    Converts hex (possibly with +) to actual characters
    """
    if not isinstance(hex_str, str):
        hex_str = str(hex_str)

    new_char = ""
    if "+" in hex_str:
        for part in hex_str.split("+"):
            try:
                new_char += chr(int(part.strip(), 16))
            except ValueError:
                new_char += part  # fallback
    else:
        try:
            new_char = chr(int(hex_str.strip(), 16))
        except ValueError:
            new_char = hex_str  # fallback
    return new_char


def regenerate_hex_using_characters():
    """
    This function regenerates the Hex column from the character column
    """
    print("Regenerating Hex from characters")

    source_path = get_source_path()

    language_file = pd.read_csv(source_path, encoding="utf-8-sig")
    _strip_columns(language_file)

    hex_col = project.project_unicode_column or "Hex"
    language_file[hex_col] = language_file[project.project_character_column].apply(generate_hex_from_character)

    language_file.to_csv(source_path, index=False)
    print("Hex regenerated from characters")


def generate_hex_from_character(char):
    """
    Converts a character to its Unicode hex representation
    """
    if not isinstance(char, str) or len(char) == 0:
        return ""

    # For multi-character cases we join with +
    hex_values = []
    for c in char:
        hex_values.append(f"{ord(c):04X}")

    return "+".join(hex_values)


document = None  # not used in this file
