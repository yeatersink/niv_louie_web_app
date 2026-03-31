# utils/project_extention.py

from nicegui import app, events, ui
import json
import os
from pathlib import Path

from utils.storage import get_user_nvda_dir, ensure_user_directories


# Function to load extentions from JSON file
def load_extentions(nvda_dir=None):
    try:
        if nvda_dir is None:
            ensure_user_directories()
            nvda_dir = get_user_nvda_dir()
        
        extentions_file = nvda_dir / "extentions_file.json"
        if not extentions_file.exists():
            extentions_file.parent.mkdir(parents=True, exist_ok=True)
            with open(extentions_file, "w", encoding="utf-8") as file:
                json.dump([], file, ensure_ascii=False, indent=4)
            print(f"LOG: Created empty extentions_file.json for new user")
            return []
        
        with open(extentions_file, "r", encoding="utf-8") as file:
            data = json.load(file)
            print(f"LOG: Loaded {len(data)} extensions from {extentions_file}")
            return data
    except FileNotFoundError:
        return []  
    except Exception as ex:
        print(f"LOG: Error loading extentions: {ex}")
        return []


class Extention:
    def __init__(self):
        self.extention_name = None
        self.extention_summary = None
        self.extention_description = None
        self.extention_author = None
        self.extention_version = None
        self.extention_minimum_version = None
        self.extention_last_tested_version = None
        self.extention_locale = None
        self.extention_included_projects = None
        
        self.extentions = []
        self.extentions_list = []
        self.nvda_dir = None

    def set_user_storage(self, nvda_dir):
        """Called from pages to set the correct user folder."""
        self.nvda_dir = Path(nvda_dir)
        self.nvda_dir.mkdir(parents=True, exist_ok=True)
        print(f"LOG: Extention now using user nvda storage: {self.nvda_dir}")
        
        # Reload extensions with the correct path
        self.reload_extentions()

    def reload_extentions(self):
        """Reload extensions from the current user folder"""
        if self.nvda_dir is None:
            self.nvda_dir = get_user_nvda_dir()
        self.extentions = load_extentions(self.nvda_dir)
        self.extentions_list = [addon["name"] for addon in self.extentions]
        print(f"LOG: Reloaded {len(self.extentions)} extensions")

    def update_extentions_list(self):
        self.extentions_list = [addon["name"] for addon in self.extentions]

    def update_extention_name(self, e: events.ValueChangeEventArguments):
        self.extention_name = e.value

    def update_extention_summary(self, e: events.ValueChangeEventArguments):
        self.extention_summary = e.value

    def update_extention_description(self, e: events.ValueChangeEventArguments):
        self.extention_description = e.value

    def update_extention_author(self, e: events.ValueChangeEventArguments):
        self.extention_author = e.value
        
    def update_extention_version(self, e: events.ValueChangeEventArguments):
        self.extention_version = e.value

    def update_extention_minimum_version(self, e: events.ValueChangeEventArguments):
        self.extention_minimum_version = e.value

    def update_extention_last_tested_version(self, e: events.ValueChangeEventArguments):
        self.extention_last_tested_version = e.value

    def update_extention_locale(self, e: events.ValueChangeEventArguments):
        self.extention_locale = e.value

    def update_extention_included_projects(self, e: events.ValueChangeEventArguments):
        self.extention_included_projects = e.value

    def save_extention(self):
        error = False
        if self.extention_name is None:
            ui.notify("Name is required", type="negative")
            error = True
        if self.extention_summary is None:
            ui.notify("Summary is required", type="negative")
            error = True
        if self.extention_description is None:
            ui.notify("Description is required", type="negative")
            error = True
        if self.extention_author is None:
            ui.notify("Author is required", type="negative")
            error = True
        if self.extention_version is None:
            ui.notify("Version is required", type="negative")
            error = True
        if self.extention_minimum_version is None:
            ui.notify("Minimum version is required", type="negative")
            error = True
        if self.extention_last_tested_version is None:
            ui.notify("Last tested version is required", type="negative")
            error = True
        if self.extention_locale is None:
            ui.notify("Locale is required", type="negative")
            error = True
        if self.extention_included_projects is None:
            ui.notify("Included projects is required", type="negative")
            error = True

        for addon in self.extentions:
            if self.extention_name.lower() == addon["name"].lower():
                ui.notify("An extention with that name already exists.", type="negative")
                error = True

        if error:
            return

        extention_object = {
            "name": self.extention_name,
            "summary": self.extention_summary,
            "description": self.extention_description,
            "author": self.extention_author,
            "version": self.extention_version,
            "minimum_version": self.extention_minimum_version,
            "last_tested_version": self.extention_last_tested_version,
            "locale": self.extention_locale,
            "included_projects": self.extention_included_projects
        }
        self.extentions.append(extention_object)
        self.update_extentions_list()

        # Use user-specific directory
        nvda_dir = self.nvda_dir or get_user_nvda_dir()
        extentions_file = nvda_dir / "extentions_file.json"
        with open(extentions_file, "w", encoding="utf-8") as file:
            json.dump(self.extentions, file, ensure_ascii=False, indent=4)

        self.reload_extentions()   # Refresh the list immediately

        ui.navigate.to("/nvda_extention_builder")
        ui.notify("Extention Saved.", close_button="Ok.")

    def set_fields(self):
        for addon in self.extentions:
            if self.extention_name == addon["name"]:
                self.extention_summary = addon["summary"]
                self.extention_description = addon["description"]
                self.extention_author = addon["author"]
                self.extention_version = addon["version"]
                self.extention_minimum_version = addon["minimum_version"]
                self.extention_last_tested_version = addon["last_tested_version"]
                self.extention_locale = addon["locale"]
                self.extention_included_projects = addon["included_projects"]
                break

    def save_changes(self, old_extention_name):
        updated = False
        if self.extention_name != old_extention_name and self.extention_name in self.extentions_list:
            ui.notify("You have an Extention with that Name Already!")
            return

        for addon in self.extentions:
            if addon["name"] == old_extention_name:
                addon["name"] = self.extention_name
                addon["summary"] = self.extention_summary
                addon["description"] = self.extention_description
                addon["author"] = self.extention_author
                addon["version"] = self.extention_version
                addon["minimum_version"] = self.extention_minimum_version
                addon["last_tested_version"] = self.extention_last_tested_version
                addon["locale"] = self.extention_locale
                addon["included_projects"] = self.extention_included_projects
                self.update_extentions_list()

                nvda_dir = self.nvda_dir or get_user_nvda_dir()
                extentions_file = nvda_dir / "extentions_file.json"
                with open(extentions_file, "w", encoding="utf-8") as file:
                    json.dump(self.extentions, file, ensure_ascii=False, indent=4)

                # Rename files in user folder
                old_source = nvda_dir / (old_extention_name + "-nvda-addon-source")
                new_source = nvda_dir / (self.extention_name + "-nvda-addon-source")
                old_addon = nvda_dir / (old_extention_name + ".nvda-addon")
                new_addon = nvda_dir / (self.extention_name + ".nvda-addon")

                if old_source.exists():
                    old_source.rename(new_source)
                if old_addon.exists():
                    old_addon.rename(new_addon)

                updated = True
                break

        self.reload_extentions()   # Refresh list after save

        if updated:
            ui.notify("Addon has been Updated!")
        else:
            ui.notify("Failed to Update!")

    def remove_extention(self):
        nvda_dir = self.nvda_dir or get_user_nvda_dir()
        for addon in self.extentions[:]:   # copy to avoid modification during iteration
            if addon["name"] == self.extention_name:
                self.extentions.remove(addon)
                self.update_extentions_list()
                extentions_file = nvda_dir / "extentions_file.json"
                with open(extentions_file, "w", encoding="utf-8") as file:
                    json.dump(self.extentions, file, ensure_ascii=False, indent=4)

                # Remove files from user folder
                source_dir = nvda_dir / (self.extention_name + "-nvda-addon-source")
                addon_file = nvda_dir / (self.extention_name + ".nvda-addon")

                if source_dir.exists():
                    import shutil
                    shutil.rmtree(source_dir, ignore_errors=True)
                if addon_file.exists():
                    addon_file.unlink()

                self.reload_extentions()
                ui.notify("Extention has been Removed!")
                return


extention = Extention()