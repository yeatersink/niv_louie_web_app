# pages/07_braille_document_builder.py

from nicegui import events, ui
import os
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
    init_user_storage()
    
    # DEBUG: Show exactly what projects are available in the list
    print(f"DEBUG: Available projects in list = {sorted(project.languages_list)}")

    with ui.column().classes('w-full max-w-3xl mx-auto p-8 gap-8 items-center'):
        
        # Centered header - no Go Back button as requested
        ui.html('<h1 class="text-3xl font-bold text-primary text-center">Braille Document Builder</h1>')

        # New descriptive text as requested
        ui.html('''
            <p class="text-center text-gray-700 max-w-2xl">
                Here you can choose one or several different projects to create a braille document.<br>
                This app currently supports <strong>.docx</strong>, <strong>.txt</strong>, and <strong>.pdf</strong> files for upload.<br>
                You will be able to download the resulting braille document in <strong>.docx</strong>, <strong>.txt</strong>, or <strong>.brf</strong> format.
            </p>
        ''').classes('mb-8')

        with ui.card().classes('w-full p-8'):
            ui.html('<h2 class="text-2xl font-semibold mb-6 text-primary">Upload Document</h2>')
            
            ui.upload(
                on_upload=document.handle_document_upload, 
                auto_upload=True,
                label='Select Document to Convert'
            ).props('color=accent').classes('w-full')

        with ui.card().classes('w-full p-8'):
            ui.html('<h2 class="text-2xl font-semibold mb-6 text-primary">Project Selection</h2>')
            
            ui.select(
                label="What projects do you want to use?", 
                options=sorted(project.languages_list), 
                multiple=True, 
                on_change=document.update_selected_projects
            ).classes('w-full')

            # Checkbox for English/general rules
            ui.checkbox(
                text="Apply general English / default braille rules", 
                value=document.apply_general_english,
                on_change=document.toggle_general_english
            ).classes('mt-4')

        # Main action button
        ui.button("Generate and Download Braille Document", 
                 on_click=document.convert_document
        ).props('size=lg color=accent').classes('w-full mt-6')

        # Document management section
        document_path = "documents"
        if os.path.exists(document_path):
            file_list = os.listdir(document_path)
            
            with ui.card().classes('w-full p-8'):
                ui.html('<h2 class="text-2xl font-semibold mb-6 text-primary">Existing Documents</h2>')
                
                ui.select(
                    label="What Document would you like to Select?", 
                    options=file_list, 
                    on_change=document.update_document_name
                ).classes('w-full')
                
                with ui.row().classes('gap-4 w-full'):
                    ui.button("Download Selected Document", 
                             on_click=lambda: ui.download(os.path.join(document_path, document.document_name)) 
                                              if document.document_name else None
                    ).props('color=accent').classes('flex-1')
                    
                    with ui.dialog() as dialog, ui.card().classes('p-8 w-full max-w-md'):
                        ui.html('<h3 class="text-2xl font-bold text-negative mb-6 text-center">Are you sure?</h3>')
                        ui.label('You are about to permanently delete this document.').classes('text-center mb-8')
                        
                        with ui.row().classes('gap-4 w-full justify-center'):
                            ui.button("Cancel", on_click=dialog.close).props('flat color=primary size=lg')
                            def confirm_delete():
                                document.remove_document()
                                dialog.close()
                            ui.button("Yes, Delete", on_click=confirm_delete).props('color=negative size=lg')
                    
                    ui.button("Remove Document", 
                             on_click=dialog.open
                    ).props('color=negative').classes('flex-1')

        # Home button
        ui.button("Return to Home", 
                 on_click=lambda: ui.navigate.to("/")
        ).props('flat color=primary size=lg').classes('w-full mt-8')