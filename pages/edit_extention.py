# pages/10_edit_extention.py

from nicegui import ui
from utils.i18n import back_button, dashboard_button, heading, language_switcher, prepare_page, t
from utils.storage import ensure_user_directories, get_user_nvda_dir
from utils.project_extention import extention
from utils.project import project
from utils.nvda import create_nvda_extention


def init_user_storage():
    try:
        ensure_user_directories()
        project.set_user_storage()
        extention.set_user_storage(get_user_nvda_dir())
        print("LOG: User storage + project + extensions reloaded from edit_extention page")
    except Exception as e:
        print(f"LOG: Could not init user storage: {e}")


@ui.page("/edit_extention")
def edit_extention():
    prepare_page("addon.edit_title")
    init_user_storage()
    extention.set_fields()
    old_extention_name = extention.extention_name

    with ui.column().classes('w-full max-w-3xl mx-auto p-8 gap-8'):

        with ui.row().classes('w-full items-center justify-between'):
            back_button()
            language_switcher()
            dashboard_button()

        heading("h1", "text-3xl font-bold text-primary", "addon.edit_title")

        with ui.card().classes('w-full p-8'):
            heading("h2", "text-2xl font-semibold mb-6 text-primary", "addon.details")

            ui.input(label=t("addon.name"),
                     on_change=extention.update_extention_name,
                     value=extention.extention_name).classes('w-full')

            ui.input(label=t("addon.summary"),
                     on_change=extention.update_extention_summary,
                     value=extention.extention_summary).classes('w-full')

            ui.input(label=t("addon.description"),
                     on_change=extention.update_extention_description,
                     value=extention.extention_description).classes('w-full')

            ui.input(label=t("addon.authors"),
                     on_change=extention.update_extention_author,
                     value=extention.extention_author).classes('w-full')

            ui.input(label=t("addon.version"),
                     on_change=extention.update_extention_version,
                     value=extention.extention_version).classes('w-full')

            ui.input(label=t("addon.minimum"),
                     on_change=extention.update_extention_minimum_version,
                     value=extention.extention_minimum_version).classes('w-full')

            ui.input(label=t("addon.tested"),
                     on_change=extention.update_extention_last_tested_version,
                     value=extention.extention_last_tested_version).classes('w-full')

            ui.input(label=t("addon.locale"),
                     on_change=extention.update_extention_locale,
                     value=extention.extention_locale).classes('w-full')

        with ui.card().classes('w-full p-8'):
            heading("h2", "text-2xl font-semibold mb-6 text-primary", "common.project_selection")

            ui.select(options=sorted(project.languages_list),
                      label=t("addon.include_projects"),
                      multiple=True,
                      on_change=extention.update_extention_included_projects,
                      value=extention.extention_included_projects).classes('w-full')

        def save_and_generate():
            extention.save_changes(old_extention_name)

            if not extention.extention_name:
                ui.notify(t("notify.select_addon"), type="negative")
                return

            built = create_nvda_extention()
            if not built:
                return

            ui.navigate.to('/nvda_extention_builder')
            ui.notify(t("notify.addon_updated"), type="positive")

        ui.button(t("addon.save_generate"),
                  on_click=save_and_generate
        ).props('size=lg color=accent').classes('w-full mt-8')

        ui.button(t("common.cancel"),
                  on_click=lambda: ui.navigate.to('/nvda_extention_builder')
        ).props('flat color=primary').classes('mt-4')
