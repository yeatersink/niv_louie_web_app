# pages/05_project_information.py

from nicegui import ui
from utils.i18n import back_button, dashboard_button, heading, language_switcher, prepare_page, t
from utils.storage import ensure_user_directories
from utils.project import project
from utils.project_utils import save_and_create_csv


def init_user_storage():
    try:
        ensure_user_directories()
        print("LOG: User storage initialized from project_information page")
    except Exception as e:
        print(f"LOG: Could not init user storage: {e}")


@ui.page("/project_information")
def project_information():
    prepare_page("info.title")
    init_user_storage()

    if project.project_text is None:
        ui.notify(t("project.upload_csv_first"))
        ui.navigate.to("/create_project")
        return

    cols = [str(c).replace("\ufeff", "").strip() for c in project.project_text.columns]
    project.project_text.columns = cols

    def select_value(saved):
        if saved is None:
            return None
        saved_name = str(saved).replace("\ufeff", "").strip()
        if saved_name in cols:
            return saved_name
        return None

    with ui.column().classes('w-full max-w-3xl mx-auto p-8 gap-8'):

        with ui.row().classes('w-full items-center justify-between'):
            back_button()
            language_switcher()
            dashboard_button()

        heading("h1", "text-3xl font-bold text-primary", "info.title")

        with ui.card().classes('w-full p-8'):
            heading("h2", "text-2xl font-semibold mb-4 text-primary", "info.metadata")
            ui.label(t("info.metadata_help")).classes('mb-6 text-gray-700')

            ui.input(label=t("info.name"),
                    value=project.project_name,
                    on_change=project.update_project_name).classes('w-full')

            ui.input(label=t("info.iso"),
                    value=project.project_language_code,
                    on_change=project.update_project_language_code).classes('w-full')

            ui.input(label=t("info.system"),
                    value=project.project_language_system_code,
                    on_change=project.update_project_language_system_code).classes('w-full')

            ui.input(label=t("info.display_name"),
                    value=project.project_display_name,
                    on_change=project.update_project_display_name).classes('w-full')

            ui.input(label=t("info.index_name"),
                    value=project.project_index_name,
                    on_change=project.update_project_index_name).classes('w-full')

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

        ui.button(t("info.save"),
                 on_click=save_and_create_csv
        ).props('size=lg color=primary').classes('w-full mt-8')
