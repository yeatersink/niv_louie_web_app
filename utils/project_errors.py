# utils/project_errors.py

from nicegui import ui


class ProjectCsvError(Exception):
    """A CSV or column-mapping problem that should be shown in a dialog, not a 500 page."""

    def __init__(self, title, message, how_to_fix):
        super().__init__(message)
        self.title = title
        self.message = message
        self.how_to_fix = how_to_fix


def format_header_list(columns):
    if columns is None:
        return "(none)"
    names = list(columns)
    if not names:
        return "(none)"
    return ", ".join(f'"{c}"' for c in names)


def show_project_error(title, message, how_to_fix):
    with ui.dialog() as dialog, ui.card().classes("p-8 w-full max-w-md"):
        ui.label(title).classes("text-2xl font-bold text-negative mb-4")
        ui.label(message).classes("mb-4 text-gray-800")
        ui.label(how_to_fix).classes("mb-6 text-gray-700")

        def refresh_project_manager():
            dialog.close()
            ui.navigate.to("/create_project")

        ui.button(
            "Refresh project manager",
            on_click=refresh_project_manager,
        ).props("color=accent size=lg").classes("w-full")
    dialog.open()
