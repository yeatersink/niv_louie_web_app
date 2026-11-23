# pages/07_braille_document_builder.py

from nicegui import events, ui
import os
from utils.i18n import heading, language_switcher, prepare_page, t
from utils.storage import ensure_user_directories
from utils.braille_document_manager import document
from utils.project import project


def init_user_storage():
    try:
        ensure_user_directories()
        project.set_user_storage()   # This reloads project.languages_list for the select
        print("LOG: User storage + project languages reloaded from braille_document_builder page")
    except Exception as e:
        print(f"LOG: Could not init user storage: {e}")


@ui.page("/braille_document_builder")
def braille_document_builder():
    prepare_page("braille.title")
    init_user_storage()
    
    # DEBUG: Show exactly what projects are available in the list
    print(f"DEBUG: Available projects in list = {sorted(project.languages_list)}")

    with ui.column().classes('w-full max-w-3xl mx-auto p-8 gap-8 items-center'):
        
        # Centered header - no Go Back button as requested
        with ui.row().classes('w-full justify-end'):
            language_switcher()
        heading("h1", "text-3xl font-bold text-primary text-center", "braille.title")
        ui.markdown(t("braille.intro")).classes('text-center text-gray-700 max-w-2xl mb-8')

        with ui.card().classes('w-full p-8'):
            heading("h2", "text-2xl font-semibold mb-6 text-primary", "braille.upload")
            
            ui.upload(
                on_upload=document.handle_document_upload, 
                auto_upload=True,
                label=t("braille.select_document")
            ).props('color=accent').classes('w-full')

        with ui.card().classes('w-full p-8'):
            heading("h2", "text-2xl font-semibold mb-6 text-primary", "common.project_selection")
            
            ui.select(
                label=t("braille.which_projects"), 
                options=sorted(project.languages_list), 
                multiple=True, 
                on_change=document.update_selected_projects
            ).classes('w-full')

            # Checkbox for English/general rules
            ui.checkbox(
                text=t("braille.english_rules"), 
                value=document.apply_general_english,
                on_change=document.toggle_general_english
            ).classes('mt-4')

        # Main action button
        ui.button(t("braille.generate"), 
                 on_click=document.convert_document
        ).props('size=lg color=accent').classes('w-full mt-6')

        # Document management section
        document_path = "documents"
        if os.path.exists(document_path):
            file_list = os.listdir(document_path)
            
            with ui.card().classes('w-full p-8'):
                heading("h2", "text-2xl font-semibold mb-6 text-primary", "braille.existing")
                
                ui.select(
                    label=t("braille.which_document"), 
                    options=file_list, 
                    on_change=document.update_document_name
                ).classes('w-full')
                
                with ui.row().classes('gap-4 w-full'):
                    ui.button(t("braille.download_selected"), 
                             on_click=lambda: ui.download(os.path.join(document_path, document.document_name)) 
                                              if document.document_name else None
                    ).props('color=accent').classes('flex-1')
                    
                    with ui.dialog() as dialog, ui.card().classes('p-8 w-full max-w-md'):
                        heading("h3", "text-2xl font-bold text-negative mb-6 text-center", "projects.confirm_title")
                        ui.label(t("braille.delete_body")).classes('text-center mb-8')
                        
                        with ui.row().classes('gap-4 w-full justify-center'):
                            ui.button(t("common.cancel"), on_click=dialog.close).props('flat color=primary size=lg')
                            def confirm_delete():
                                document.remove_document()
                                dialog.close()
                            ui.button(t("common.yes_delete"), on_click=confirm_delete).props('color=negative size=lg')
                    
                    ui.button(t("braille.remove"), 
                             on_click=dialog.open
                    ).props('color=negative').classes('flex-1')

        # Home button
        ui.button(t("common.return_home"), 
                 on_click=lambda: ui.navigate.to("/")
        ).props('flat color=primary size=lg').classes('w-full mt-8')