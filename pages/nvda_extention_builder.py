# pages/08_nvda_extention_builder.py

from nicegui import ui
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
        ui.notify("Select an add-on first", type="negative")
        return False
    return True


def download_existing_addon():
    name = extention.extention_name
    if not name:
        ui.notify("Select an add-on first", type="negative")
        return
    path = get_user_nvda_dir() / f"{name}.nvda-addon"
    print(f"DEBUG: download path={path} exists={path.exists()}")
    if path.exists():
        ui.download.content(path.read_bytes(), filename=path.name)
        ui.notify(f"Downloading {path.name}")
        return
    else:
        ui.notify("No add-on file yet. Use Create NVDA add-on first.", type="warning")
        return


def go_edit_addon():
    if not require_selected_addon():
        return
    ui.navigate.to("/edit_extention")


@ui.page("/nvda_extention_builder")
def nvda_extention_builder():
    init_user_storage()

    with ui.column().classes('w-full max-w-3xl mx-auto p-8 gap-8'):
        with ui.row().classes('w-full items-center justify-between'):
            ui.html('<h1 class="text-3xl font-bold text-primary">NVDA Add-on Builder</h1>')
            ui.button(
                "Go to Dashboard",
                on_click=lambda: ui.navigate.to("/dashboard"),
            ).props('flat color=primary size=lg')

        with ui.card().classes('w-full p-8'):
            ui.html('<h2 class="text-2xl font-semibold mb-4 text-primary">Create</h2>')
            ui.html('''
                <p class="text-gray-700 mb-6">
                    Create a new NVDA add-on from your saved projects.
                </p>
            ''')
            ui.button(
                "Create NVDA add-on",
                on_click=lambda: ui.navigate.to("/create_extention"),
            ).props('size=lg color=accent').classes('w-full')

        with ui.card().classes('w-full p-8'):
            ui.html('<h2 class="text-2xl font-semibold mb-4 text-primary">Saved add-ons</h2>')

            addon_select = ui.select(
                label="Choose an add-on",
                options=sorted(extention.extentions_list),
                on_change=extention.update_extention_name,
            ).classes('w-full mb-6')

            ui.button(
                "Edit selected add-on",
                on_click=go_edit_addon,
            ).props('flat color=primary size=lg').classes('w-full')

            ui.button(
                "Download Addon",
                on_click=download_existing_addon,
            ).props('size=lg color=accent').classes('w-full mt-4')

            with ui.dialog() as dialog, ui.card().classes('p-8 w-full max-w-md'):
                ui.html('<h2 class="text-2xl font-bold text-negative mb-6 text-center">Delete add-on</h2>')
                ui.label("Are you sure you want to permanently remove this add-on?").classes('text-center mb-8')

                with ui.row().classes('gap-4 w-full justify-center'):
                    ui.button("Cancel", on_click=dialog.close).props('flat color=primary size=lg')

                    def confirm_delete():
                        if not require_selected_addon():
                            dialog.close()
                            return
                        extention.remove_extention()
                        addon_select.options = sorted(extention.extentions_list)
                        addon_select.value = None
                        dialog.close()

                    ui.button("Yes, Delete", on_click=confirm_delete).props('color=negative size=lg')

            def open_remove_dialog():
                if not require_selected_addon():
                    return
                dialog.open()

            ui.button(
                "Remove selected add-on",
                on_click=open_remove_dialog,
            ).props('flat color=negative size=lg').classes('w-full mt-4')
