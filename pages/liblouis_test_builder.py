# pages/12_liblouis_test_builder.py

from nicegui import events, ui
from utils.i18n import heading, language_switcher, prepare_page, t
from utils.storage import ensure_user_directories
from utils.braille import create_braille_tests
from utils.project import project


def init_user_storage():
    try:
        ensure_user_directories()
        project.set_user_storage()   
        print("LOG: User storage + project languages reloaded from liblouis_test_builder page")
    except Exception as e:
        print(f"LOG: Could not init user storage: {e}")


@ui.page("/liblouis_test_builder")
def liblouis_test_builder():
    prepare_page("test.title")
    init_user_storage()
    selected_projects = []

    with ui.column().classes('w-full max-w-3xl mx-auto p-8 gap-8 items-center'):
        
        # Centered header - no Go Back button
        with ui.row().classes('w-full justify-end'):
            language_switcher()
        heading("h1", "text-3xl font-bold text-primary text-center", "test.title")
        ui.markdown(t("test.intro")).classes('text-center text-gray-700 max-w-2xl mb-10')

        with ui.card().classes('w-full p-8'):
            heading("h2", "text-2xl font-semibold mb-6 text-primary", "common.project_selection")
            
            def update_selected_project_list(e: events.ValueChangeEventArguments):
                nonlocal selected_projects
                selected_projects = e.value if e.value else []
                
                if selected_projects:
                    project.set_project_name(selected_projects[0])
                    project.set_all_fields()
                    print(f"DEBUG: Selected project '{selected_projects[0]}' | Language code set to '{project.project_language_code}'")
                    ui.notify(t("notify.selected_project", name=selected_projects[0], code=project.project_language_code))

            ui.select(
                label=t("test.which_projects"), 
                options=sorted(project.languages_list), 
                multiple=True, 
                with_input=True, 
                on_change=update_selected_project_list
            ).classes('w-full')

        with ui.card().classes('w-full p-8'):
            heading("h2", "text-2xl font-semibold mb-6 text-primary", "test.upload")
            
            ui.upload(
                label=t("test.which_document"), 
                on_upload=project.handle_test_upload, 
                auto_upload=True
            ).props('color=accent').classes('w-full')

        ui.button(
            t("test.generate"),
            on_click=lambda: create_braille_tests(selected_projects, include_metadata=True)
        ).props('size=lg color=accent').classes('w-full mt-6')

        ui.button(
            t("test.generate_plain"),
            on_click=lambda: create_braille_tests(selected_projects, include_metadata=False)
        ).props('size=lg color=accent').classes('w-full')

        ui.label(t("test.note")).classes('text-center text-gray-700')

        ui.button(t("common.return_dashboard"),
                 on_click=lambda: ui.navigate.to("/dashboard")
        ).props('flat color=primary size=lg').classes('w-full mt-8')