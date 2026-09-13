# pages/dashboard.py - Logged-in Dashboard

from html import escape
from nicegui import ui, app
from utils.storage import ensure_user_directories, get_current_web_user_id
from utils.project import project


def init_user_storage():
    try:
        # Only try to ensure directories if we have a real user_id
        user_id = get_current_web_user_id()
        if user_id and not user_id.startswith("temp_"):
            ensure_user_directories()
            nickname = app.storage.user.get("nickname", "User")
            print(f"LOG: Dashboard loaded - Logged in as: {nickname} (ID: {user_id})")
        else:
            print(f"LOG: Dashboard accessed without full login (ID: {user_id})")
    except Exception as e:
        print(f"LOG: Could not init user storage on dashboard: {e}")


def logout():
    try:
        if hasattr(app.storage, 'user') and app.storage.user is not None:
            app.storage.user.clear()
        ui.notify("You have been logged out successfully", type="positive")
        ui.navigate.to('/')
    except Exception as e:
        print(f"LOG: Logout error on dashboard: {e}")
        ui.notify("Logged out successfully", type="positive")
        ui.navigate.to('/')


def load_user_project_names():
    ensure_user_directories()
    project.set_user_storage()
    project.reload_languages()
    return [name for name in project.languages_list if name]


@ui.page("/dashboard")
def dashboard():
    init_user_storage()
    
    user_id = get_current_web_user_id()
    nickname = app.storage.user.get("nickname", "User")
    project_list_container = None

    def show_my_projects():
        names = load_user_project_names()
        project_list_container.clear()
        with project_list_container:
            ui.html('<h2 class="text-2xl font-semibold mb-3 text-primary">Your projects</h2>')
            if not names:
                ui.label(
                    "You have no saved projects yet. Use Project Manager to create one."
                ).classes('text-gray-700')
            else:
                items = "".join(f"<li>{escape(str(name))}</li>" for name in names)
                ui.html(
                    f'<ul style="list-style: disc; padding-left: 1.5rem;">{items}</ul>'
                )

    # Layout fixes - same as home page
    ui.query('.nicegui-content').classes('w-full')
    ui.query('.q-page').classes('flex flex-col min-h-screen')

    with ui.header().classes('items-center justify-between bg-primary text-white p-4 shadow'):
        with ui.row().classes('items-center gap-6 w-full max-w-6xl mx-auto'):
            ui.label('Niv Louie').classes('text-3xl font-bold tracking-tight')
            ui.space()
            
            # New Home button - matching the style and position of the Dashboard button on home page
            ui.button('Home', 
                     on_click=lambda: ui.navigate.to('/')).props('flat color=accent')
            
            ui.button('Log Out', on_click=logout).props('flat color=white')
            ui.button('Collaborate', 
                     on_click=lambda: ui.navigate.to('/collaborate')).props('flat color=white')

    # Main content - flex-1 pushes footer down
    with ui.column().classes('flex-1 w-full max-w-4xl mx-auto p-8 gap-12 items-center'):

        # Larger project image / visual representation area (linked to documentation)
        with ui.row().classes('w-full justify-center mb-8'):
            with ui.link(target='/documentation').classes('block w-full max-w-lg md:max-w-2xl'):
                ui.image('/static/images/nivlouie.jpeg').classes('w-full h-auto rounded-2xl shadow-xl object-contain')
                        
        # Description for the image
        with ui.row().classes('w-full justify-center mb-12'):
            ui.label('Image of braille representing various images, indicating accessibility to all things through braille and technology').classes('text-center text-gray-600 max-w-2xl text-lg')

        ui.html(f'<h1 class="text-4xl font-bold text-center text-primary">Welcome back, {escape(str(nickname))}</h1>')

        # Logged-in status
        with ui.card().classes('p-6 w-full max-w-3xl'):
            with ui.row().classes('items-center justify-between w-full'):
                ui.html(f'<h2 class="text-2xl font-semibold text-primary">Logged in as: {escape(str(nickname))}</h2>')
                ui.button('Log Out', on_click=logout).props('flat color=negative')

            ui.button('Show my projects',
                      on_click=show_my_projects
            ).props('size=lg color=accent').classes('w-full mt-6')

        with ui.column().classes('w-full max-w-3xl') as project_list_container:
            pass
        show_my_projects()

        # Tool cards
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
            ui.html('<h2 class="text-2xl font-semibold mb-3 text-primary">Liblouis Table Builder</h2>')
            ui.markdown('Choose a project and Niv Louie will automatically generate a Braille table for Liblouis. This table can be submitted to the Liblouis team for inclusion in future releases. Please consult your local Braille authority before publishing tables for standardized scripts.')
            ui.button('Go to Liblouis Table Builder', 
                      on_click=lambda: ui.navigate.to('/liblouis_table_builder')).props('size=lg color=accent').classes('w-full')

        with ui.card().classes('p-6 w-full max-w-3xl text-center'):
            ui.html('<h2 class="text-2xl font-semibold mb-3 text-primary">Liblouis Test Builder</h2>')
            ui.markdown('This tool helps you create test files to verify your project produces correct Braille output. Upload a test document, select your project, and Niv Louie will generate a `.yaml` test file and automatically download it.')
            ui.button('Go to Liblouis Test Builder', 
                      on_click=lambda: ui.navigate.to('/liblouis_test_builder')).props('size=lg color=accent').classes('w-full')


    # Footer
    with ui.column().classes('w-full bg-gray-100 py-36 mt-24 border-t'):
        with ui.column().classes('w-full max-w-4xl mx-auto gap-10 items-center text-center'):

            ui.html('<h2 class="text-2xl font-semibold mb-6 text-primary">Acknowledgements</h2>')
            ui.markdown('''
Niv Louie has come together in a monumental way thanks to the generous assistance, 
valuable feedback, and tremendous support from multiple leading institutions and organizations.

Niv Louie is Ariel University and the Digital Pasts Lab’s contribution to education and accessibility, 
developed as part of a research scholarship for a blind PhD candidate.
            ''').classes('text-base leading-relaxed text-primary text-center mb-10')

            ui.html('<h3 class="text-xl font-semibold mb-6 text-primary">Our Partners & Supporters</h3>')
            with ui.grid(columns=2).classes('w-full gap-6 text-center'):
                ui.link('Ariel University', 'https://www.ariel.ac.il/wp/en/').props('target=_blank').classes('text-accent hover:underline font-medium')
                ui.link('Digital Pasts Lab – Ariel University', 'https://digitalpasts.github.io/').props('target=_blank').classes('text-accent hover:underline font-medium')
                ui.link('Heidelberg University', 'https://www.uni-heidelberg.de/en').props('target=_blank').classes('text-accent hover:underline font-medium')
                ui.link('National Federation of the Blind', 'https://nfb.org/').props('target=_blank').classes('text-accent hover:underline font-medium')
                ui.link('Royal National Institute of Blind People (RNIB)', 'https://www.rnib.org.uk/').props('target=_blank').classes('text-accent hover:underline font-medium')
                ui.link('Envisionly Tech', 'https://envisionly.tech/').props('target=_blank').classes('text-accent hover:underline font-medium')
                ui.link('Liblouis', 'https://liblouis.io/').props('target=_blank').classes('text-accent hover:underline font-medium')
                ui.link('NVDA – NV Access', 'https://www.nvaccess.org/').props('target=_blank').classes('text-accent hover:underline font-medium')

            with ui.row().classes('gap-16 mt-8'):
                with ui.column().classes('items-center'):
                    ui.html('<h3 class="text-xl font-semibold mb-3 text-primary">Documentation</h3>')
                    ui.link('User Guide & Technical Documentation', '/documentation').classes('text-accent hover:underline font-medium')

                with ui.column().classes('items-center'):
                    ui.html('<h3 class="text-xl font-semibold mb-3 text-primary">Video Instructions</h3>')
                    ui.link('Tutorial videos and how-to guides', 'https://www.youtube.com/channel/UCGSfwD06fubtGXRkR7kn_Jg').props('target=_blank').classes('text-accent hover:underline font-medium')

            ui.separator().classes('my-10 w-full')

            ui.html('<h3 class="text-xl font-semibold mb-4 text-primary">Contact Us</h3>')
            ui.label('Have questions or want to collaborate?').classes('text-gray-600 mb-2')
            ui.link('info@nivlouie.com', 'mailto:info@nivlouie.com').classes('text-accent hover:underline text-lg')
            
            ui.label('© 2026 Niv Louie - Free and Open Source (GPL-3.0)').classes('text-xs text-gray-500 mt-8')
