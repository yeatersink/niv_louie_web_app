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


def create_braille_table():
    print("creating table for lib louis")

    projects_dir = get_user_projects_dir()
    filtered_path = projects_dir / f"filtered_{project.project_name}.csv"

    braille = pd.read_csv(filtered_path)

    braille_folder = get_user_braille_dir()
    braille_folder.mkdir(parents=True, exist_ok=True)

    output_path = braille_folder / f"{project.project_language_code}.utb"

    braille[project.project_braille_column] = braille[project.project_braille_column].apply(braille_to_numbers)

    with open(output_path, "w", encoding="utf-8") as braille_table:
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
    ui.download(output_path, f"{project.project_language_code}.utb")


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


def create_braille_tests(selected_projects=None):
    """Create YAML test file for Liblouis"""
    if not selected_projects:
        ui.notify("No projects selected for test generation", type="negative")
        return

    print("Creating braille tests")

    projects_dir = get_user_projects_dir()
    tests_dir = get_user_tests_dir()
    tests_dir.mkdir(parents=True, exist_ok=True)

    for proj_name in selected_projects:
        # Load the correct project context
        project.set_project_name(proj_name)
        project.set_all_fields()

        test_csv_path = tests_dir / f"{project.project_language_code}.csv"
        yaml_path = tests_dir / f"{project.project_language_code}.yaml"

        if not test_csv_path.exists():
            ui.notify(f"Test CSV not found for {proj_name} (expected {test_csv_path.name})", type="negative")
            print(f"DEBUG: Missing test CSV: {test_csv_path}")
            continue

        language_file = pd.read_csv(projects_dir / f"filtered_{proj_name}.csv", encoding="utf-8")
        test_csv = pd.read_csv(test_csv_path, encoding="utf-8")

        with open(yaml_path, "w", encoding="utf-8") as test_yaml:
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

                for _, lang_row in language_file.iterrows():
                    char = str(lang_row[project.project_character_column])
                    braille_char = str(lang_row[project.project_braille_column])
                    if char in braille_test and braille_char != "nan":
                        braille_test = braille_test.replace(char, braille_char)

                for char in list(braille_test):
                    if char in braille_test_object:
                        braille_test = braille_test.replace(char, braille_test_object[char])

                test_yaml.write(f'  - ["{row["Text"]}", "{braille_test}"]\n')

        ui.notify(f"Braille Test for {proj_name} has been Generated.")
        print(f"Done creating braille tests for {proj_name}")
        
        ui.download(yaml_path, f"{project.project_language_code}.yaml")


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