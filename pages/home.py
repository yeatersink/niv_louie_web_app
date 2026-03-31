# pages/01_home.py

from nicegui import ui, app
from utils.storage import ensure_user_directories
from utils.storage import (
    get_user_projects_dir,
    get_user_documents_dir,
    get_user_nvda_dir,
    get_user_tests_dir
)
from utils.project import project
from pathlib import Path


def get_current_user_info():
    try:
        user_id = app.storage.user.get("user_id")
        nickname = app.storage.user.get("nickname", "User")
        return user_id, nickname
    except Exception as e:
        print(f"LOG: Error getting user info: {e}")
        return None, "User"


def init_user_storage():
    try:
        ensure_user_directories()
        project.set_user_storage()
        user_id, nickname = get_current_user_info()
        print(f"LOG: User storage + project reloaded. Logged in as: {nickname}")
    except Exception as e:
        print(f"LOG: Could not init user storage: {e}")


def logout():
    try:
        app.storage.user.clear()
        ui.notify("You have been logged out", type="positive")
        ui.navigate.to("/")
    except Exception as e:
        ui.notify(f"Logout error: {e}", type="negative")


# ====================== HELPER FUNCTIONS ======================

def delete_file(file_path: Path):
    try:
        if file_path.exists():
            file_path.unlink()
            ui.notify(f'Deleted: {file_path.name}', type='positive')
        else:
            ui.notify('File no longer exists', type='warning')
    except Exception as e:
        ui.notify(f'Could not delete file: {e}', type='negative')


def share_file(file_path: Path):
    with ui.dialog() as dialog, ui.card().classes('w-full max-w-md p-6'):
        ui.html(f'<h3 class="text-xl font-bold mb-4 text-primary">Share: {file_path.name}</h3>')
        
        ui.button('Copy File Path', 
                  icon='content_copy',
                  on_click=lambda: ui.notify('File path copied (coming soon)')).classes('w-full mb-3')
        
        ui.button('Email This File', 
                  icon='email',
                  on_click=lambda: ui.notify('Email sharing coming soon')).classes('w-full')

        ui.button('Close', on_click=dialog.close).props('flat color=primary').classes('mt-4 w-full')

    dialog.open()


# ====================== SHOW MY FILES DIALOG ======================
def show_my_files():
    document_folder = get_user_documents_dir()
    projects_folder = get_user_projects_dir()
    nvda_folder = get_user_nvda_dir()
    tests_folder = get_user_tests_dir()

    with ui.dialog().props('maximized') as dialog, ui.card().classes('w-full h-full flex flex-col p-6'):
        
        ui.html('<h2 class="text-2xl font-bold text-center mb-6 text-primary">My Files</h2>')

        with ui.column().classes('w-full gap-6 flex-grow overflow-auto'):

            def create_folder_section(title: str, folder_path: Path, extensions: list = None):
                with ui.expansion(title, icon='folder').classes('w-full'):
                    if not folder_path.exists():
                        ui.label('Folder not found yet.').classes('italic text-gray-500 py-4')
                        return

                    files = []
                    if extensions:
                        for ext in extensions:
                            files.extend(folder_path.rglob(f"*{ext}"))
                    else:
                        files.extend(folder_path.rglob("*"))

                    files = sorted(set(files), key=lambda p: p.name.lower())

                    if not files:
                        ui.label('No files in this folder yet.').classes('italic text-gray-500 py-4')
                        return

                    with ui.column().classes('w-full gap-3 pl-4'):
                        for file_path in files:
                            with ui.row().classes('items-center justify-between w-full p-3 border rounded-lg'):
                                ui.label(file_path.name).classes('flex-grow truncate')

                                with ui.row().classes('gap-2'):
                                    ui.button(icon='download', 
                                              on_click=lambda fp=file_path: ui.download(fp)).props('flat color=primary size=sm')
                                    
                                    ui.button(icon='delete', 
                                              on_click=lambda fp=file_path: delete_file(fp)).props('flat color=negative size=sm')
                                    
                                    ui.button(icon='share', 
                                              on_click=lambda fp=file_path: share_file(fp)).props('flat color=accent size=sm')

            create_folder_section("1. Source CSV Files", projects_folder, ['.csv'])
            create_folder_section("2. Braille Documents", document_folder, ['.txt', '.brf', '.docx', '_braille'])
            create_folder_section("3. Liblouis Tables", projects_folder, ['.tbl', '.ctb', '.cti', '.utb', '.dis'])
            create_folder_section("4. Test Files", tests_folder, ['.yml', '.yaml'])
            create_folder_section("5. NVDA Add-ons", nvda_folder, ['.nvda-addon'])

        with ui.row().classes('w-full justify-end gap-4 p-6 border-t mt-auto'):
            ui.button('Close', on_click=dialog.close).props('flat size=lg color=accent')

    dialog.open()


# ====================== HOME PAGE ======================
@ui.page("/")
def home():
    init_user_storage()
    
    user_id, nickname = get_current_user_info()
    is_logged_in = bool(user_id)

    with ui.header().classes('items-center justify-between bg-primary text-white p-4 shadow'):
        with ui.row().classes('items-center gap-6 w-full max-w-6xl mx-auto'):
            ui.label('Niv Louie').classes('text-3xl font-bold tracking-tight')
            ui.space()
            if is_logged_in:
                ui.button('Log Out', on_click=logout).props('flat color=white')
            else:
                ui.button('Log In', 
                         on_click=lambda: ui.navigate.to('/login')).props('flat color=accent')
            ui.button('Collaborate', 
                     on_click=lambda: ui.navigate.to('/collaborate')).props('flat color=white')

    with ui.column().classes('w-full max-w-4xl mx-auto p-8 gap-12 items-center'):
        ui.html('<h1 class="text-4xl font-bold text-center text-primary">Welcome to Niv Louie</h1>')

        # Logged-in User Section
        if is_logged_in:
            with ui.card().classes('p-6 w-full max-w-3xl'):
                with ui.row().classes('items-center justify-between w-full'):
                    ui.html(f'<h2 class="text-2xl font-semibold text-primary">Logged in as: {nickname}</h2>')
                    ui.button('Log Out', on_click=logout).props('flat color=negative')

                ui.button('📁 Show My Files', 
                          on_click=show_my_files, 
                          icon='folder_special').props('size=lg color=accent').classes('w-full mt-6')

        with ui.card().classes('p-6 w-full max-w-3xl'):
            ui.html('<h2 class="text-2xl font-semibold mb-4 text-center text-primary">Current Session</h2>')
            ui.label('All your projects, documents, tables, and extensions are saved privately for your user account.').classes('text-center')

        with ui.card().classes('p-8 w-full max-w-3xl'):
            ui.html('<h2 class="text-2xl font-semibold mb-4 text-center text-primary">What Niv Louie Can Do</h2>')
            ui.markdown('''
Niv Louie allows anyone to upload simple CSV files containing Unicode symbols, character names, and desired Braille representations, then instantly generates:

1. **Lib Louis Braille tables** for high-quality Braille translation  
2. **Custom Braille** for development of new Braille scripts and systems for any language or writing system, even those without existing Braille support  
3. **Braille documents** that can be printed or embossed from the custom tables built with Niv Louie  
4. **NVDA extensions** that give screen readers immediate spoken and Braille access to any Unicode character or symbol in digital content, including math, music, scientific symbols, emojis, and more.
            ''').classes('text-base leading-relaxed')

        # Action cards with teal accent buttons
        with ui.card().classes('p-6 w-full max-w-3xl text-center'):
            ui.html('<h2 class="text-2xl font-semibold mb-3 text-primary">Project Manager</h2>')
            ui.markdown('This is where you create and manage your projects. Upload a CSV file, map the columns, and save your project for use across the app.')
            ui.button('Go to Project Manager', 
                      on_click=lambda: ui.navigate.to('/existing_project')).props('size=lg color=accent').classes('w-full')

        with ui.card().classes('p-6 w-full max-w-3xl text-center'):
            ui.html('<h2 class="text-2xl font-semibold mb-3 text-primary">Braille Document Builder</h2>')
            ui.markdown('This tool lets you convert printed documents into Braille using the projects you created. Upload a .docx or .txt file, choose your project(s), and Niv Louie will generate a Braille document and automatically download it.')
            ui.button('Go to Braille Document Builder', 
                      on_click=lambda: ui.navigate.to('/braille_document_builder')).props('size=lg color=accent').classes('w-full')

        with ui.card().classes('p-6 w-full max-w-3xl text-center'):
            ui.html('<h2 class="text-2xl font-semibold mb-3 text-primary">NVDA Extension Builder</h2>')
            ui.markdown('Use your projects to automatically generate an NVDA extension. Select your project(s), click "Create Extension", and Niv Louie will generate an `.nvda-addon` file and send it to your downloads folder.')
            ui.button('Go to NVDA Extension Builder', 
                      on_click=lambda: ui.navigate.to('/nvda_extention_builder')).props('size=lg color=accent').classes('w-full')

        with ui.card().classes('p-6 w-full max-w-3xl text-center'):
            ui.html('<h2 class="text-2xl font-semibold mb-3 text-primary">Lib Louis Table Builder</h2>')
            ui.markdown('Choose a project and Niv Louie will automatically generate a Braille table for Liblouis. This table can be submitted to the Liblouis team for inclusion in future releases. Please consult your local Braille authority before publishing tables for standardized scripts.')
            ui.button('Go to Lib Louis Table Builder', 
                      on_click=lambda: ui.navigate.to('/liblouis_table_builder')).props('size=lg color=accent').classes('w-full')

        with ui.card().classes('p-6 w-full max-w-3xl text-center'):
            ui.html('<h2 class="text-2xl font-semibold mb-3 text-primary">Lib Louis Test Builder</h2>')
            ui.markdown('This tool helps you create test files to verify your project produces correct Braille output. Upload a test document, select your project, and Niv Louie will generate a `.yaml` test file and automatically download it.')
            ui.button('Go to Lib Louis Test Builder', 
                      on_click=lambda: ui.navigate.to('/liblouis_test_builder')).props('size=lg color=accent').classes('w-full')

        # ==================== ACKNOWLEDGEMENTS SECTION ====================
        with ui.card().classes('w-full max-w-4xl p-8'):
            ui.html('<h2 class="text-2xl font-semibold mb-6 text-primary text-center">Acknowledgements</h2>')
            
            ui.markdown('''
                Niv Louie has come together in a monumental way thanks to the generous assistance, 
                valuable feedback, and tremendous support from multiple leading institutions and organizations.
                
                **Niv Louie** is Ariel University and the Digital Pasts Lab’s contribution to education and accessibility, 
                developed as part of a research scholarship for a blind PhD candidate.
                
                Special thanks go to the entire team who offered their insight, expertise, and unwavering help 
                throughout the development of this project.
            ''').classes('text-base leading-relaxed text-center mb-10')

            ui.html('<h3 class="text-xl font-semibold mb-6 text-primary text-center">Our Partners &amp; Supporters</h3>')

            with ui.grid(columns=2).classes('w-full gap-6 text-center'):
                ui.link('Ariel University', 'https://www.ariel.ac.il/wp/en/').props('target=_blank').classes('text-accent hover:underline font-medium')
                ui.link('Digital Pasts Lab – Ariel University', 'https://digitalpasts.github.io/').props('target=_blank').classes('text-accent hover:underline font-medium')
                ui.link('Heidelberg University', 'https://www.uni-heidelberg.de/en').props('target=_blank').classes('text-accent hover:underline font-medium')
                ui.link('National Federation of the Blind', 'https://nfb.org/').props('target=_blank').classes('text-accent hover:underline font-medium')
                ui.link('Royal National Institute of Blind People (RNIB)', 'https://www.rnib.org.uk/').props('target=_blank').classes('text-accent hover:underline font-medium')
                ui.link('Envisionly Tech', 'https://envisionly.tech/').props('target=_blank').classes('text-accent hover:underline font-medium')
                ui.link('Liblouis', 'https://liblouis.io/').props('target=_blank').classes('text-accent hover:underline font-medium')
                ui.link('NVDA – NV Access', 'https://www.nvaccess.org/').props('target=_blank').classes('text-accent hover:underline font-medium')

    with ui.footer().classes('bg-gray-100 py-8 mt-12'):
        with ui.column().classes('w-full max-w-4xl mx-auto gap-6 items-center'):
            ui.label("Making the World Accessible, One Braille Table at a Time").classes('text-sm text-gray-500')