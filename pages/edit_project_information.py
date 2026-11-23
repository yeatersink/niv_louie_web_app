# pages/06_edit_project_information.py

from nicegui import events, ui
from utils.i18n import back_button, dashboard_button, heading, language_switcher, prepare_page, t
from utils.storage import ensure_user_directories
from utils.project import project
from utils.project_utils import save_and_create_existing_csv
from utils.project_errors import show_project_error

# Add these missing imports so the regenerate functions are available
from utils.csv import regenerate_characters_using_hex, regenerate_hex_using_characters
from utils.braille import get_braille_from_text_in_source


def init_user_storage():
    try:
        ensure_user_directories()
        project.set_user_storage()   # Reloads languages and project data
        print("LOG: User storage + project reloaded from edit_project_information page")
    except Exception as e:
        print(f"LOG: Could not init user storage: {e}")


def save_project_edits(regenerate_characters, regenerate_hex, generate_braille, old_project_name):
    try:
        if regenerate_characters:
            regenerate_characters_using_hex()
        if regenerate_hex:
            regenerate_hex_using_characters()
        if generate_braille:
            get_braille_from_text_in_source()
        save_and_create_existing_csv(old_project_name)
    except KeyError as e:
        headers = list(project.project_text.columns) if project.project_text is not None else []
        show_project_error(
            t("errors.missing_column_title"),
            t("errors.missing_column_message", error=e, headers=", ".join(f'"{c}"' for c in headers)),
            t("errors.missing_column_fix"),
        )
    except ValueError as e:
        show_project_error(
            t("errors.save_title"),
            str(e),
            t("errors.save_fix"),
        )


@ui.page("/edit_project_information")
def edit_project_information():
    prepare_page("edit.title")
    init_user_storage()
    regenerate_characters = False
    regenerate_hex = False
    generate_braille = False
    old_project_name = project.project_name

    with ui.column().classes('w-full max-w-3xl mx-auto p-8 gap-8'):

        with ui.row().classes('w-full items-center justify-between'):
            back_button()
            language_switcher()
            dashboard_button()

        heading("h1", "text-3xl font-bold text-primary", "edit.title")

        if project.project_name is not None:
            project.set_all_fields()
            try:
                project.load_language_source()
            except Exception as ex:
                show_project_error(
                    t("errors.read_title"),
                    t("errors.read_message", error=ex),
                    t("errors.read_fix"),
                )

            with ui.card().classes('w-full p-8'):
                heading("h2", "text-2xl font-semibold mb-6 text-primary", "edit.basic")

                ui.input(label=t("info.name"),
                        value=project.project_name,
                        on_change=project.update_project_name).classes('w-full')

                ui.input(label=t("info.iso"),
                        value=project.project_language_code,
                        on_change=project.update_project_language_code).classes('w-full')

                ui.input(label=t("info.system"),
                        value=project.project_language_system_code,
                        on_change=project.update_project_language_system_code).classes('w-full')

        if project.project_text is not None:
            cols = [str(c).replace("\ufeff", "").strip() for c in project.project_text.columns]
            project.project_text.columns = cols

            def select_value(saved):
                if saved is None:
                    return None
                saved_name = str(saved).replace("\ufeff", "").strip()
                if saved_name in cols:
                    return saved_name
                return None

            with ui.card().classes('w-full p-8'):
                heading("h2", "text-2xl font-semibold mb-4 text-primary", "info.columns")
                ui.label(t("info.columns_help")).classes('mb-6 text-gray-700')

                ui.select(label=t("info.col_character"),
                         options=cols,
                         value=select_value(project.project_character_column),
                         on_change=project.update_project_character_column).classes('w-full')

                ui.select(label=t("info.col_name"),
                         options=cols,
                         value=select_value(project.project_name_column),
                         on_change=project.update_project_name_column).classes('w-full')

                ui.select(label=t("info.col_unicode"),
                         options=cols,
                         value=select_value(project.project_unicode_column),
                         on_change=project.update_project_unicode_column).classes('w-full')

                ui.select(label=t("info.col_type"),
                         options=cols,
                         value=select_value(project.project_type_column),
                         on_change=project.update_project_type_column).classes('w-full')

                ui.select(label=t("info.col_braille"),
                         options=cols,
                         value=select_value(project.project_braille_column),
                         on_change=project.update_project_braille_column).classes('w-full')

            with ui.card().classes('w-full p-8'):
                heading("h2", "text-2xl font-semibold mb-6 text-primary", "edit.additional")

                ui.input(label=t("info.language_codes"),
                        value=project.project_supported_braille_languages,
                        on_change=project.update_project_supported_braille_languages).classes('w-full')

                ui.input(label=t("info.explanation"),
                        value=project.project_language_information,
                        on_change=project.update_project_language_information).classes('w-full')

                ui.input(label=t("info.contributors"),
                        value=project.project_contributors,
                        on_change=project.update_project_contributors).classes('w-full')

                ui.input(label=t("info.other_tables"),
                        value=project.project_included_braille_tables,
                        on_change=project.update_project_included_braille_tables).classes('w-full')

                ui.input(label=t("info.direction"),
                        value=project.project_test_display_type,
                        on_change=project.update_project_test_display_type).classes('w-full')

                ui.input(label=t("info.remove_text"),
                        value=project.project_replace,
                        on_change=project.update_project_replace).classes('w-full')

                # Regeneration options
                heading("h3", "text-xl font-semibold mt-8 mb-4 text-primary", "edit.regen")

                def update_regenerate_characters(e: events.ValueChangeEventArguments):
                    nonlocal regenerate_characters
                    regenerate_characters = e.value

                ui.checkbox(text=t("edit.regen_characters"),
                           value=regenerate_characters,
                           on_change=update_regenerate_characters).classes('mb-3')

                def update_regenerate_hex(e: events.ValueChangeEventArguments):
                    nonlocal regenerate_hex
                    regenerate_hex = e.value

                ui.checkbox(text=t("edit.regen_unicode"),
                           value=regenerate_hex,
                           on_change=update_regenerate_hex).classes('mb-3')

                ui.checkbox(text=t("edit.regen_braille"),
                           value=generate_braille).classes('mb-3')

        ui.button(t("edit.save"),
                 on_click=lambda: save_project_edits(regenerate_characters, regenerate_hex, generate_braille, old_project_name)
        ).props('size=lg color=accent').classes('w-full mt-8')
