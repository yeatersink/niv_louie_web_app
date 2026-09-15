# utils/csv.py

import json
import pandas as pd
from utils.project import project
from utils.storage import get_user_projects_dir
from utils.project_errors import ProjectCsvError, format_header_list

try:
    with open("utils/braille_to_numbers.json", encoding="utf8") as f:
        braille_numbers_object = json.load(f)
except Exception as ex:
    print(f"ERROR loading braille_to_numbers.json: {ex}")
    braille_numbers_object = {}


def get_source_path():
    """Helper to get the source CSV path for the current project."""
    projects_dir = get_user_projects_dir()
    source_dir = projects_dir / "source"
    source_dir.mkdir(parents=True, exist_ok=True)
    return source_dir / f"{project.project_name}.csv"


def _strip_columns(df):
    df.columns = [str(c).replace("\ufeff", "").strip() for c in df.columns]
    return df


def _cell_str(value):
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass
    return str(value)


def _is_blank(value):
    text = _cell_str(value).strip()
    return text == "" or text.lower() == "nan"


def _issue_line(row_number, column, problem, value):
    return f'row {row_number}, column {column}: {problem} in "{_cell_str(value)}"'


def _space_problems(value):
    if _is_blank(value):
        return []
    text = _cell_str(value)
    problems = []
    if text[:1].isspace():
        problems.append("leading space")
    if text[-1:].isspace():
        problems.append("trailing space")
    if "  " in text.strip():
        problems.append("extra space")
    return problems


def _build_csv_quality_report(filtered_language, char_col, hex_col, type_col, name_col, braille_col):
    extra_spaces = []
    missing_hex = []
    missing_braille = []
    non_braille = []
    missing_always = []
    extra_plus = []
    hex_wrong_length = []
    missing_columns = []

    required_cols = [char_col, hex_col, type_col, name_col, braille_col]
    space_cols = [char_col, hex_col, type_col, braille_col]
    missing_covered = {hex_col, braille_col}

    for index, row in filtered_language.iterrows():
        for col in space_cols:
            for problem in _space_problems(row[col]):
                extra_spaces.append(_issue_line(index, col, problem, row[col]))

        for col in required_cols:
            if col in missing_covered:
                continue
            if _is_blank(row[col]):
                missing_columns.append(_issue_line(index, col, "missing value", row[col]))

        if _is_blank(row[hex_col]):
            missing_hex.append(_issue_line(index, hex_col, "missing value", row[hex_col]))
        else:
            hex_text = _cell_str(row[hex_col])
            hex_stripped = hex_text.strip()
            if "++" in hex_stripped:
                extra_plus.append(_issue_line(index, hex_col, "extra plus", hex_text))
            parts = [part.strip() for part in hex_stripped.split("+")]
            for part in parts:
                if len(part) != 4:
                    hex_wrong_length.append(
                        f'row {index}, column {hex_col}: part "{part}" is {len(part)} characters, expected 4'
                    )
            if "+" in hex_stripped and _cell_str(row[type_col]).strip().lower() != "always":
                missing_always.append(
                    _issue_line(
                        index,
                        type_col,
                        "Hex contains + but Type is not always",
                        row[type_col],
                    )
                )

        if _is_blank(row[braille_col]):
            missing_braille.append(_issue_line(index, braille_col, "missing value", row[braille_col]))
        else:
            braille_text = _cell_str(row[braille_col])
            if any((not char.isspace()) and char not in braille_numbers_object for char in braille_text):
                non_braille.append(
                    _issue_line(index, braille_col, "non-braille character", braille_text)
                )

    stripped_hex = filtered_language[hex_col].map(
        lambda value: "" if _is_blank(value) else _cell_str(value).strip()
    )
    duplicate_mask = stripped_hex.ne("") & stripped_hex.duplicated(keep=False)
    duplicate_hex = [
        _issue_line(index, hex_col, "duplicate value", row[hex_col])
        for index, row in filtered_language.loc[duplicate_mask].iterrows()
    ]

    sections = [
        ("Extra spaces or leading/trailing spaces", extra_spaces),
        ("Missing Hex", missing_hex),
        ("Missing Braille", missing_braille),
        ("Non-braille characters in Braille", non_braille),
        ("Hex contains + but Type is not always", missing_always),
        ("Duplicate Hex values", duplicate_hex),
        ("Hex contains ++", extra_plus),
        ("Hex part is not 4 characters", hex_wrong_length),
        ("Missing required column value", missing_columns),
    ]

    lines = [
        f"Report for {project.project_name}",
        f"Generated on {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}",
    ]
    issue_count = 0
    for title, rows in sections:
        if not rows:
            continue
        issue_count += len(rows)
        lines.append("")
        lines.append(f"**{title}**")
        lines.extend(rows)

    if issue_count == 0:
        lines.append("No errors found.")

    return "\n".join(lines) + "\n", issue_count


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

    char_col = project.project_character_column
    hex_col = project.project_unicode_column
    type_col = project.project_type_column
    name_col = project.project_name_column
    braille_col = project.project_braille_column
    needed = [char_col, hex_col, type_col, name_col, braille_col]

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

    name_column = filtered_language[[name_col]].copy()
    name_column[name_col] = name_column[name_col].astype(str)
    new_name_column = name_column[name_col].apply(format_names)
    filtered_language[name_col] = new_name_column
    filtered_language.index = range(2, 2 + len(filtered_language))

    report_text, issue_count = _build_csv_quality_report(
        filtered_language, char_col, hex_col, type_col, name_col, braille_col
    )

    filtered_language = filtered_language.sort_values(by=[hex_col], key=lambda x: x.astype(str).str.len(), ascending=False)

    filtered_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        filtered_language.to_csv(filtered_path, index=False)
    except Exception as ex:
        raise ProjectCsvError(
            "The filtered spreadsheet could not be saved",
            str(ex),
            "Check that the project folder is writable, then try Save project again.",
        ) from ex
    print("Spreadsheet Generated")

    project_name = str(project.project_name)
    report_filename = f"{project_name}_csv_report.txt"
    report_path = projects_dir / report_filename
    report_bytes = report_text.encode("utf-8")
    try:
        report_path.write_bytes(report_bytes)
        print(f"LOG: CSV report written {report_path} issues={issue_count}")
    except Exception as ex:
        print(f"LOG: Could not write CSV report file {report_path}: {ex}")

    return report_bytes, report_filename


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
