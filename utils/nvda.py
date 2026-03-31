# utils/nvda.py

import pathlib
import pandas as pd
from nicegui import ui
from utils.project import project
from utils.project_extention import extention
import shutil

from utils.storage import get_user_nvda_dir, get_user_projects_dir, ensure_user_directories


def add_characters_to_nvda():
    """Adds the characters from the language file to the NVDA symbols file"""
    print("adding symbols to nvda for", project.project_name)
    projects_dir = get_user_projects_dir()
    language_file = pd.read_csv(projects_dir / f"filtered_{project.project_name}.csv")

    nvda_dir = get_user_nvda_dir()
    nvda_symbols_file = open(nvda_dir / "symbols.dic", "a+", encoding="utf8")
    nvda_symbols_file.write("\n#" + project.project_name + "\n")

    for index, row in language_file.iterrows():
        new_line = str(row[project.project_character_column]) + "\t" + str(row["Name"]) + "\tmost\talways\n"
        nvda_symbols_file.write(new_line)

    nvda_symbols_file.write("#End " + project.project_name + "\n\n")
    nvda_symbols_file.close()
    print("symbols added to nvda for", project.project_name)


def generate_locale_file():
    """Generates a nvda locale file for the language"""
    print("generating nvda locale file for", project.project_name)
    projects_dir = get_user_projects_dir()
    language_file = pd.read_csv(projects_dir / f"filtered_{project.project_name}.csv")

    nvda_dir = get_user_nvda_dir()
    new_folder = nvda_dir / project.project_language_code
    new_folder.mkdir(parents=True, exist_ok=True)

    # characterDescriptions.dic for letters
    with open(new_folder / "characterDescriptions.dic", "w", encoding="utf8") as f:
        f.write(f"""#{project.project_name} characterDescriptions.dic
#A part of NonVisual Desktop Access (NVDA)
#URL: http://www.nvda-project.org/
#Copyright (c) 2024 Matthew Yeater and Paul Geoghegan.
#This file is covered by the GNU General Public License.

""")
        language_file[project.project_name_column] = language_file[project.project_name_column].apply(format_names)
        for index, row in language_file.loc[(language_file["Type"] == "letter")].sort_values(by=[project.project_name_column]).iterrows():
            new_line = str(row[project.project_character_column]) + "\t" + str(row["Name"]) + "\n"
            f.write(new_line)

    # symbols.dic for non-letters
    if not language_file.loc[(language_file["Type"] != "letter")].empty:
        with open(new_folder / "symbols.dic", "w", encoding="utf8") as f:
            f.write(f"""#{project.project_name} symbols.dic
#A part of NonVisual Desktop Access (NVDA)
#URL: http://www.nvda-project.org/
#Copyright (c) 2024 Matthew Yeater and Paul Geoghegan.
#This file is covered by the GNU General Public License.

""")
            for index, row in language_file.loc[(language_file["Type"] != "letter")].sort_values(by=[project.project_name_column]).iterrows():
                new_line = str(row[project.project_character_column]) + "\t" + str(row["Name"]) + "\tmost\talways\n"
                f.write(new_line)

    print("Generated Locale files for NVDA for", project.project_name)


def create_nvda_extention():
    """Creates a new extension for NVDA"""
    print("Creating Extension for NVDA")
    extention.set_fields()

    nvda_dir = get_user_nvda_dir()
    source_folder = nvda_dir / (extention.extention_name + "-nvda-addon-source")
    source_folder.mkdir(parents=True, exist_ok=True)

    locale_folder = source_folder / "locale" / extention.extention_locale
    locale_folder.mkdir(parents=True, exist_ok=True)

    # Create manifest.ini
    with open(source_folder / "manifest.ini", "w", encoding="utf-8") as f:
        f.write(f"""name = {extention.extention_name}
summary = "{extention.extention_summary}"
description = "{extention.extention_description}"
author = "{extention.extention_author}"
version = {extention.extention_version}
minimumNVDAVersion = {extention.extention_minimum_version}
lastTestedNVDAVersion = {extention.extention_last_tested_version}

[symbolDictionaries]
""")
        for language in extention.extention_included_projects:
            project.set_project_name(language)
            project.set_all_fields()
            f.write(f"[[{project.project_language_code}]]\n")
            f.write(f"displayName = {project.project_display_name}\n")
            f.write("mandatory = false\n")
            add_characters_to_nvda_extention(source_folder)

    # === FIXED: Reliable .nvda-addon creation on Windows ===
    final_name = f"{extention.extention_name}.nvda-addon"
    final_path = nvda_dir / final_name
    zip_path = nvda_dir / f"{extention.extention_name}.zip"

    # Clean old files
    for p in [final_path, zip_path]:
        if p.exists():
            try:
                p.unlink()
            except Exception as e:
                print(f"DEBUG: Failed to delete old {p}: {e}")

    # Create zip (make_archive adds .zip)
    shutil.make_archive(str(nvda_dir / extention.extention_name), 'zip', root_dir=source_folder)

    # Rename .zip to .nvda-addon
    if zip_path.exists():
        try:
            zip_path.rename(final_path)
            print(f"DEBUG: Renamed successfully to {final_path}")
        except Exception as e:
            print(f"DEBUG: Rename failed ({e}), using copy fallback")
            shutil.copy2(zip_path, final_path)
    else:
        print("DEBUG: Zip file was not created!")

    ui.notify("Extension Generated!")
    print(f"DEBUG: Final .nvda-addon created at {final_path}")

    # === Download with content (reliable for web/IP access) ===
    try:
        if final_path.exists():
            with open(final_path, "rb") as f:
                content = f.read()
            ui.notify(f"Downloading {final_name}", type="positive")
            ui.download.content(content, filename=final_name, media_type="application/zip")
            print(f"DEBUG: Download triggered for {final_path}")
        else:
            ui.notify("Extension created, but download file missing", type="warning")
    except Exception as e:
        print(f"DEBUG: Download error: {e}")
        ui.notify("Extension created - check folder manually", type="warning")


def add_characters_to_nvda_extention(source_folder):
    """Adds characters to the NVDA extension"""
    print("generating nvda Character Set for", project.project_name)
    projects_dir = get_user_projects_dir()
    language_file = pd.read_csv(projects_dir / f"filtered_{project.project_name}.csv")

    ui.notify("Adding Characters to NVDA Extension for " + project.project_name)

    character_set_path = source_folder / "locale" / extention.extention_locale / f"symbols-{project.project_language_code}.dic"

    with open(character_set_path, "w", encoding="utf-8") as f:
        f.write(f"""#{project.project_name} symbols.dic
#Copyright (c) 2024 Matthew Yeater and Paul Geoghegan.
#This file is covered by the GNU General Public License.

symbols:\n""")

        language_file[project.project_name_column] = language_file[project.project_name_column].apply(format_names)

        for index, row in language_file.sort_values(by=[project.project_name_column]).iterrows():
            new_line = str(row[project.project_character_column]) + "\t" + str(row["Name"]) + "\tnone\n"
            f.write(new_line)

    print("Generated Character Set file for NVDA extension for", project.project_name)


def generate_character_set():
    """Generates a locale file for the language"""
    print("generating nvda Character Set for", project.project_name)
    projects_dir = get_user_projects_dir()
    language_file = pd.read_csv(projects_dir / f"filtered_{project.project_name}.csv")

    nvda_dir = get_user_nvda_dir()
    new_folder = nvda_dir / "character_sets" / project.project_language_code
    new_folder.mkdir(parents=True, exist_ok=True)

    with open(new_folder / "symbols.dic", "w", encoding="utf8") as f:
        f.write(f"""#{project.project_name} symbols.dic
#A part of NonVisual Desktop Access (NVDA)
#URL: http://www.nvda-project.org/
#Copyright (c) 2024 Matthew Yeater and Paul Geoghegan.
#This file is covered by the GNU General Public License.

""")

        language_file[project.project_name_column] = language_file[project.project_name_column].apply(format_names)

        for index, row in language_file.sort_values(by=[project.project_name_column]).iterrows():
            new_line = str(row[project.project_character_column]) + "\t" + str(row["Name"]) + "\tmost\talways\n"
            f.write(new_line)

    print("Generated Character Set file for NVDA for", project.project_name)


def format_names(name):
    """Removes unwanted characters from the name of the character"""
    if not isinstance(name, str):
        name = str(name)
    return name.strip().lower()