# utils/braille.py

import os
from pathlib import Path
import warnings
import pandas as pd
import json
from utils.project import project
from utils.storage import get_user_projects_dir, get_user_braille_dir, get_user_tests_dir
from nicegui import ui


# Load braille conversion files (shared across functions)
try:
    with open("utils/braille_converter.json", encoding="utf8") as f:
        braille_object = json.load(f)
    with open("utils/braille_test_converter.json", encoding="utf8") as f:
        braille_test_object = json.load(f)
    with open("utils/braille_to_numbers.json", encoding="utf8") as f:
        braille_numbers_object = json.load(f)
except Exception as ex:
    print(f"ERROR loading braille JSON files: {ex}")
    braille_object = {}
    braille_test_object = {}
    braille_numbers_object = {}


def create_braille_table(include_metadata=True):
    print("creating table for Liblouis")

    if not project.project_name:
        ui.notify("Please select a project.", type="negative")
        return

    projects_dir = get_user_projects_dir()
    filtered_path = projects_dir / f"filtered_{project.project_name}.csv"

    if not filtered_path.exists():
        ui.notify(f"Filtered CSV not found: {filtered_path}", type="negative")
        return

    braille = pd.read_csv(filtered_path)

    braille_folder = get_user_braille_dir()
    braille_folder.mkdir(parents=True, exist_ok=True)

    if include_metadata:
        output_filename = f"{project.project_language_code}.utb"
    else:
        output_filename = f"{project.project_language_code}_nometa.utb"
    output_path = braille_folder / output_filename

    braille[project.project_braille_column] = braille[project.project_braille_column].apply(braille_to_numbers)

    with open(output_path, "w", encoding="utf-8") as braille_table:
        if include_metadata:
            braille_table.write(f"""
# liblouis: {project.project_name}
#
""")

            if project.project_display_name:
                braille_table.write(f"#-display-name: {project.project_display_name}\n")
            else:
                braille_table.write(f"#-display-name: {project.project_name} uncontracted\n")

            if project.project_index_name:
                braille_table.write(f"#-index-name: {project.project_index_name}\n")
            else:
                braille_table.write(f"#-index-name: {project.project_name} uncontracted\n")

            if project.project_supported_braille_languages:
                for language in project.project_supported_braille_languages:
                    braille_table.write(f"#+language: {language}\n")
            else:
                braille_table.write(f"#+language: {project.project_language_code}\n")

            braille_table.write(f"""#+type:literary
#+contraction:no
#+system:{project.project_language_system_code}
#+dots:6

#-license: lgpl-2.1

# This file is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this file; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

""")

            if project.project_language_information or project.project_contributors:
                braille_table.write(str(project.project_language_information or "") + str(project.project_contributors or ""))

        braille = braille.sort_values(["Type", project.project_character_column])
        previous_char = ""

        for index, row in braille.iterrows():
            if row["Type"] != previous_char:
                braille_table.write(f"\n# {row['Type']} op code characters\n")
                previous_char = row["Type"]

            if len(str(row[project.project_braille_column])) > 0:
                if str(row[project.project_character_column]).isspace():
                    new_line = f"{row['Type']} \\s {row[project.project_braille_column]}  # space\n"
                else:
                    new_line = f"{row['Type']} {row[project.project_character_column]} {row[project.project_braille_column]}  # {row[project.project_name_column]}\n"
                braille_table.write(new_line)
            else:
                warnings.warn(f"Missing braille for character: {row[project.project_character_column]}")

        if project.project_included_braille_tables:
            braille_table.write("\n# Include additional braille tables\n")
            for table in project.project_included_braille_tables:
                braille_table.write(f"include {table}\n")

    ui.notify(f"Braille Table for {project.project_name} has been Generated.")
    print("Braille table created successfully")
    ui.download(output_path, output_filename)


def get_braille_from_text(text):
    if str(text) == "nan" or not text:
        return "nan"

    text = str(text)

    if any(char.isdigit() for char in text):
        new_text = ""
        for char in text:
            if char.isdigit():
                new_text += "⠼" + char
            else:
                new_text += char
        text = new_text

    braille = ""
    for char in text:
        if char in braille_object:
            braille += braille_object[char]
        else:
            braille += char

    return braille


def braille_to_numbers(text):
    if str(text) == "nan" or not text:
        return ""

    text = str(text).lower()
    braille = ""
    for char in text:
        if char in braille_numbers_object:
            braille += braille_numbers_object[char] + "-"
        else:
            braille += char + "-"

    if braille.endswith("-"):
        braille = braille[:-1]
    return braille


def load_filtered_project_csv(projects_dir, project_name):
    """Load filtered_{name}.csv. Notify and return None if missing."""
    filtered_path = Path(projects_dir) / f"filtered_{project_name}.csv"
    if not filtered_path.exists():
        ui.notify(f"Filtered CSV not found: {filtered_path}", type="negative")
        print(f"DEBUG: Missing filtered CSV: {filtered_path}")
        return None
    return pd.read_csv(filtered_path, encoding="utf-8")


def sort_replacements_longest_first(df, char_col):
    """Sort so longer matches win. Prefer Hex length; fall back to Character length."""
    if df is None or df.empty:
        return df
    if "Hex" in df.columns:
        return df.sort_values(by=["Hex"], key=lambda s: s.astype(str).str.len(), ascending=False)
    return df.sort_values(by=[char_col], key=lambda s: s.astype(str).str.len(), ascending=False)


def apply_replacements_in_order(text, df, char_col, braille_col):
    """Replace print with braille by walking the already-sorted DataFrame. Never use dict order."""
    if df is None or df.empty:
        return text
    for _, row in df.iterrows():
        needle = str(row[char_col])
        repl = str(row[braille_col])
        if needle and needle != "nan" and repl != "nan" and needle in text:
            text = text.replace(needle, repl)
    return text


def _included_braille_table_names(included_tables):
    if not included_tables:
        return []
    if isinstance(included_tables, str):
        return [part.strip() for part in included_tables.replace(";", ",").split(",") if part.strip()]
    return list(included_tables)


def create_braille_tests(selected_projects=None, include_metadata=True):
    """Create YAML test file for Liblouis"""
    if not selected_projects:
        ui.notify("No projects selected for test generation", type="negative")
        return

    print("Creating braille tests")

    projects_dir = get_user_projects_dir()
    tests_dir = get_user_tests_dir()
    tests_dir.mkdir(parents=True, exist_ok=True)

    first_project = selected_projects[0]
    project.set_project_name(first_project)
    project.set_all_fields()

    test_csv_path = tests_dir / f"{project.project_language_code}.csv"
    if include_metadata:
        yaml_filename = f"{project.project_language_code}.yaml"
    else:
        yaml_filename = f"{project.project_language_code}_nometa.yaml"
    yaml_path = tests_dir / yaml_filename

    if not test_csv_path.exists():
        ui.notify(f"Test CSV not found: {test_csv_path}", type="negative")
        print(f"DEBUG: Missing test CSV: {test_csv_path}")
        return

    language_file = load_filtered_project_csv(projects_dir, first_project)
    if language_file is None:
        return

    if len(selected_projects) > 1:
        for project_name in selected_projects[1:]:
            print(project_name)
            extra = load_filtered_project_csv(projects_dir, project_name)
            if extra is None:
                continue
            language_file = pd.concat([language_file, extra])

    if project.project_included_braille_tables:
        for table in _included_braille_table_names(project.project_included_braille_tables):
            table_code = str(table).split(".")[0]
            for language in project.languages:
                if table_code == language.get("language_code"):
                    print("found language " + str(language.get("language_code")))
                    extra = load_filtered_project_csv(projects_dir, language.get("name"))
                    if extra is None:
                        continue
                    language_file = pd.concat([language_file, extra])

    char_col = project.project_character_column
    braille_col = project.project_braille_column
    language_file = sort_replacements_longest_first(language_file, char_col)

    test_csv = pd.read_csv(test_csv_path, encoding="utf-8")
    report = {
        "non_braille_characters_in_braille_section": [],
        "extra_spaces": [],
    }

    with open(yaml_path, "w", encoding="utf-8") as test_yaml:
        if include_metadata:
            test_yaml.write(f"""
# Yaml Test For {project.project_name}

# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved. This file is offered as-is,
# without any warranty.

""")

            if project.project_test_display_type:
                test_yaml.write(f"display: {project.project_test_display_type}\n")
            else:
                test_yaml.write("display: unicode.dis\n")

            test_yaml.write(f"""table:
  language: {project.project_language_code}
  __assert-match: {project.project_language_code}.utb
flags: {{ testmode: forward }}
tests:
""")
        else:
            test_yaml.write("tests:\n")

        for _, row in test_csv.iterrows():
            braille_test = str(row["Text"])

            if any(char.isdigit() for char in braille_test):
                new_text = ""
                previous_was_number = False
                for char in braille_test:
                    if char.isdigit() and not previous_was_number:
                        new_text += "⠼" + char
                        previous_was_number = True
                    else:
                        new_text += char
                        previous_was_number = False
                braille_test = new_text

            braille_test = apply_replacements_in_order(
                braille_test, language_file, char_col, braille_col
            )

            for char in list(braille_test):
                if char in braille_test_object:
                    braille_test = braille_test.replace(char, braille_test_object[char])

            if any(char not in braille_numbers_object for char in braille_test):
                warning_msg = (
                    "This test contains a character that is not in the braille object. "
                    "This may be a mistake in your test."
                )
                warnings.warn(warning_msg)
                print(warning_msg + f' "{row["Text"]}": "{braille_test}"')
                report["non_braille_characters_in_braille_section"].append(
                    f'"{row["Text"]}": "{braille_test}"'
                )

            if " " in braille_test:
                report["extra_spaces"].append(f'"{row["Text"]}": "{braille_test}"')

            test_yaml.write(f'  - ["{row["Text"]}", "{braille_test}"]\n')

    ui.notify(f"Braille Test for {first_project} has been Generated.")
    print(f"Done creating braille tests for {first_project}")
    ui.download(yaml_path, yaml_filename)

    if report["non_braille_characters_in_braille_section"]:
        ui.notify(
            "Some tests contain characters not in braille_to_numbers.json. See test report.txt.",
            type="warning",
        )

    try:
        report_path = tests_dir / "test report.txt"
        with open(report_path, "w", encoding="utf-8") as report_file:
            report_file.write(f"Report for {project.project_name}\n")
            report_file.write(f"Generated on {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            if report["non_braille_characters_in_braille_section"]:
                report_file.write("\n**Non Braille Characters in Braille Section**\n")
                for item in report["non_braille_characters_in_braille_section"]:
                    report_file.write(item + "\n")
            if report["extra_spaces"]:
                report_file.write("\n**Extra Spaces**\n")
                for item in report["extra_spaces"]:
                    report_file.write(item + "\n")
        ui.download(report_path, "test report.txt")
    except Exception as ex:
        print(f"Could not write or download test report.txt: {ex}")


def get_braille_from_text_in_source():
    print("converting text to braille")

    projects_dir = get_user_projects_dir()
    source_path = projects_dir / "source" / f"{project.project_name}.csv"

    if not source_path.exists():
        ui.notify("Source file not found", type="negative")
        return

    language_file = pd.read_csv(source_path)

    new_braille_column = language_file[project.project_braille_column].apply(get_braille_from_text)

    language_file["Braille"] = new_braille_column

    language_file.to_csv(source_path, index=False)
    print("done converting text to braille")
    ui.notify("Text converted to braille in source file.")