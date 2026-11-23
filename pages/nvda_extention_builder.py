# pages/08_nvda_extention_builder.py

from nicegui import ui
from utils.i18n import heading, language_switcher, prepare_page, t
from utils.storage import ensure_user_directories, get_user_nvda_dir
from utils.project_extention import extention


def init_user_storage():
    try:
        ensure_user_directories()
        extention.set_user_storage(get_user_nvda_dir())
        print("LOG: User storage + extensions reloaded from nvda_extention_builder page")
    except Exception as e:
        print(f"LOG: Could not init user storage: {e}")


def require_selected_addon():
    if not extention.extention_name:
        ui.notify(t("notify.select_addon"), type="negative")
        return False
    return True


def download_existing_addon():
    name = extention.extention_name
    if not name:
        ui.notify(t("notify.select_addon"), type="negative")
        return
    path = get_user_nvda_dir() / f"{name}.nvda-addon"
    print(f"DEBUG: download path={path} exists={path.exists()}")
    if path.exists():
        ui.download.content(path.read_bytes(), filename=path.name)
        ui.notify(t("notify.downloading", name=path.name))
        return
    else:
        ui.notify(t("notify.no_addon_file"), type="warning")
        return


def go_edit_addon():
    if not require_selected_addon():
        return
    ui.navigate.to("/edit_extention")


@ui.page("/nvda_extention_builder")
def nvda_extention_builder():
    prepare_page("nvda.title")
    init_user_storage()

    with ui.column().classes('w-full max-w-3xl mx-auto p-8 gap-8'):
        with ui.row().classes('w-full items-center justify-between'):
            heading("h1", "text-3xl font-bold text-primary", "nvda.title")
            language_switcher()
            ui.button(
                t("common.go_dashboard"),
                on_click=lambda: ui.navigate.to("/dashboard"),
            ).props('flat color=primary size=lg')

        with ui.card().classes('w-full p-8'):
            heading("h2", "text-2xl font-semibold mb-4 text-primary", "nvda.create")
            ui.label(t("nvda.create_help")).classes("text-gray-700 mb-6")
            ui.button(
                t("nvda.create_button"),
                on_click=lambda: ui.navigate.to("/create_extention"),
            ).props('size=lg color=accent').classes('w-full')

        with ui.card().classes('w-full p-8'):
            heading("h2", "text-2xl font-semibold mb-4 text-primary", "nvda.saved")

            addon_select = ui.select(
                label=t("nvda.choose"),
                options=sorted(extention.extentions_list),
                on_change=extention.update_extention_name,
            ).classes('w-full mb-6')

            ui.button(
                t("nvda.edit"),
                on_click=go_edit_addon,
            ).props('flat color=primary size=lg').classes('w-full')

            ui.button(
                t("nvda.download"),
                on_click=download_existing_addon,
            ).props('size=lg color=accent').classes('w-full mt-4')

            with ui.dialog() as dialog, ui.card().classes('p-8 w-full max-w-md'):
                heading("h2", "text-2xl font-bold text-negative mb-6 text-center", "nvda.delete_title")
                ui.label(t("nvda.delete_body")).classes('text-center mb-8')

                with ui.row().classes('gap-4 w-full justify-center'):
                    ui.button(t("common.cancel"), on_click=dialog.close).props('flat color=primary size=lg')

                    def confirm_delete():
                        if not require_selected_addon():
                            dialog.close()
                            return
                        extention.remove_extention()
                        addon_select.options = sorted(extention.extentions_list)
                        addon_select.value = None
                        dialog.close()

                    ui.button(t("common.yes_delete"), on_click=confirm_delete).props('color=negative size=lg')

            def open_remove_dialog():
                if not require_selected_addon():
                    return
                dialog.open()

            ui.button(
                t("nvda.remove"),
                on_click=open_remove_dialog,
            ).props('flat color=negative size=lg').classes('w-full mt-4')
