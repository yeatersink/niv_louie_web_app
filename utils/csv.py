# utils/csv.py

import pandas as pd
import warnings
from utils.project import project
from utils.storage import get_user_projects_dir
from nicegui import ui


def get_source_path():
    """Helper to get the source CSV path for the current project."""
    projects_dir = get_user_projects_dir()
    source_dir = projects_dir / "source"
    source_dir.mkdir(parents=True, exist_ok=True)
    return source_dir / f"{project.project_name}.csv"


def create_filtered_csv():
    """
    This function creates a filtered csv file that only contains the characters, names, and braille codes for the language    
    """
    print("Generating", project.project_name, "Spreadsheet")

    source_path = get_source_path()
    projects_dir = get_user_projects_dir()
    filtered_path = projects_dir / f"filtered_{project.project_name}.csv"

    # The language file is read in to pandas
    language_file = pd.read_csv(source_path)

    # selects the columns that are needed for the filtered csv file
    filtered_language = language_file[[project.project_character_column, "Hex", "Type", project.project_name_column, project.project_braille_column]].copy()

    # Gets the name column and clean it
    name_column = filtered_language[[project.project_name_column]].copy()
    name_column[project.project_name_column] = name_column[project.project_name_column].astype(str)
    new_name_column = name_column[project.project_name_column].apply(format_names)
    filtered_language[project.project_name_column] = new_name_column

    # Checks if there are rows where there is a plus in the Hex column and the Type is not set to always
    if filtered_language[(filtered_language["Hex"].str.contains(r"\+")) & (filtered_language["Type"] != "always")].shape[0] > 0:
        warnings.warn("There are characters with multiple hex values that are not set to always")
        print(filtered_language[(filtered_language["Hex"].str.contains(r"\+")) & (filtered_language["Type"] != "always")])

    # Checks if there are duplicates in the language file
    if filtered_language.duplicated(keep=False, subset=["Hex"]).sum() > 0:
        warnings.warn("There are duplicates in the language file")
        print(filtered_language[filtered_language.duplicated(keep=False, subset=["Hex"])])

    filtered_language = filtered_language.sort_values(by=["Hex"], key=lambda x: x.str.len(), ascending=False)

    # Save filtered file
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

    language_file = pd.read_csv(source_path)

    # Regenerate character column from Hex
    language_file[project.project_character_column] = language_file["Hex"].apply(generate_characters)

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

    language_file = pd.read_csv(source_path)

    # Regenerate Hex column from character column
    language_file["Hex"] = language_file[project.project_character_column].apply(generate_hex_from_character)

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