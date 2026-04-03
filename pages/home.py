# pages/home.py - Public Home Page

from nicegui import ui, app


def logout():
    try:
        if hasattr(app.storage, 'user') and app.storage.user is not None:
            app.storage.user.clear()
        ui.notify("You have been logged out successfully", type="positive")
        ui.navigate.to('/')
    except Exception as e:
        ui.notify("Logged out successfully", type="positive")
        ui.navigate.to('/')


def go_to_dashboard_or_login():
    """Smart button: Dashboard if logged in, Login if not"""
    try:
        user_id = app.storage.user.get("user_id") if hasattr(app.storage, 'user') and app.storage.user is not None else None
        if user_id:
            ui.navigate.to('/dashboard')
        else:
            ui.navigate.to('/login')
    except Exception:
        ui.navigate.to('/login')


def go_to_protected_page(page_path: str):
    """Smart navigation for protected pages: Go to page if logged in, otherwise go to login with notification"""
    try:
        user_id = app.storage.user.get("user_id") if hasattr(app.storage, 'user') and app.storage.user is not None else None
        if user_id:
            ui.navigate.to(page_path)
        else:
            ui.notify("Please log in first to access this feature", type="warning")
            ui.navigate.to('/login')
    except Exception:
        ui.notify("Please log in first to access this feature", type="warning")
        ui.navigate.to('/login')


@ui.page("/")
def home():
    # NO ensure_user_directories() here - this is a public page

    # Strong layout setup to push footer to the bottom
    ui.query('.nicegui-content').classes('w-full')
    ui.query('.q-page').classes('flex flex-col min-h-screen')

    with ui.header().classes('items-center justify-between bg-primary text-white p-4 shadow'):
        with ui.row().classes('items-center gap-6 w-full max-w-6xl mx-auto'):
            ui.label('Niv Louie').classes('text-3xl font-bold tracking-tight')
            ui.space()
            
            # Smart Dashboard button
            ui.button('Dashboard', 
                     on_click=go_to_dashboard_or_login).props('flat color=accent')
            
            # Original Log In button
            ui.button('Log In', 
                     on_click=lambda: ui.navigate.to('/login')).props('flat color=accent')
            
            ui.button('Collaborate', 
                     on_click=lambda: ui.navigate.to('/collaborate')).props('flat color=white')

    # Main content area
    with ui.column().classes('flex-1 w-full max-w-4xl mx-auto p-8 gap-16 items-center'):

        # Larger project image / visual representation area (linked to documentation)
        with ui.row().classes('w-full justify-center mb-8'):
            with ui.link(target='/documentation').classes('block'):
                ui.image('/images/nivlouie.jpg').classes('max-w-3xl w-full rounded-2xl shadow-xl')

        # Description for the image
        with ui.row().classes('w-full justify-center mb-12'):
            ui.label('Image of braille representing various images, indicating accessibility to all things through braille and technology').classes('text-center text-gray-600 max-w-2xl text-lg')

        ui.html('<h1 class="text-4xl font-bold text-center text-primary">Welcome to Niv Louie</h1>')

        with ui.card().classes('p-8 w-full max-w-3xl'):
            ui.html('<h2 class="text-2xl font-semibold mb-4 text-center text-primary">What Niv Louie Can Do</h2>')
            ui.markdown('''
Niv Louie allows anyone to upload simple CSV files containing Unicode symbols, character names, and desired Braille representations, then instantly generates:

1. Lib Louis Braille tables for high-quality Braille translation  
2. Custom Braille for development of new Braille scripts and systems for any language or writing system, even those without existing Braille support  
3. Braille documents that can be printed or embossed from the custom tables built with Niv Louie  
4. NVDA extensions that give screen readers immediate spoken and Braille access to any Unicode character or symbol in digital content, including math, music, scientific symbols, emojis, and more.
            ''').classes('text-base leading-relaxed')

        with ui.card().classes('p-8 w-full max-w-3xl border border-negative'):
            ui.html('<h2 class="text-2xl font-semibold mb-6 text-negative text-center">DISCLAIMER</h2>')
            ui.markdown('''
Niv Louie is not intended to serve as a replacement for established Braille translation software systems. 

This tool is designed to facilitate access to specialized Unicode characters for blind students and users. 
Its primary purpose is to support educational accessibility.

Users are strongly encouraged to consult with their respective Braille authority prior to developing or disseminating any new Braille system.
            ''').classes('text-base leading-relaxed text-center')

        with ui.card().classes('p-8 w-full max-w-3xl'):
            ui.html('<h2 class="text-2xl font-semibold mb-8 text-center text-primary">How Niv Louie Works</h2>')

            with ui.card().classes('p-6 mb-6'):
                ui.html('<h3 class="text-xl font-semibold mb-3 text-primary">1. Project Manager</h3>')
                ui.markdown('This is where you create and manage your projects. Upload a CSV file, map the columns, and save your project for use across the app.')
                ui.button('Go to Project Manager', 
                          on_click=lambda: go_to_protected_page('/existing_project')).props('size=lg color=accent').classes('w-full')

            with ui.card().classes('p-6 mb-6'):
                ui.html('<h3 class="text-xl font-semibold mb-3 text-primary">2. Lib Louis Table Builder</h3>')
                ui.markdown('Choose a project and Niv Louie will automatically generate a Braille table for Liblouis.')
                ui.button('Go to Lib Louis Table Builder', 
                          on_click=lambda: go_to_protected_page('/liblouis_table_builder')).props('size=lg color=accent').classes('w-full')

            with ui.card().classes('p-6 mb-6'):
                ui.html('<h3 class="text-xl font-semibold mb-3 text-primary">3. Lib Louis Test Builder</h3>')
                ui.markdown('This tool helps you create test files to verify your project produces correct Braille output.')
                ui.button('Go to Lib Louis Test Builder', 
                          on_click=lambda: go_to_protected_page('/liblouis_test_builder')).props('size=lg color=accent').classes('w-full')

            with ui.card().classes('p-6 mb-6'):
                ui.html('<h3 class="text-xl font-semibold mb-3 text-primary">4. NVDA Add-on Builder</h3>')
                ui.markdown('Use your projects to automatically generate an NVDA extension.')
                ui.button('Go to NVDA Extension Builder', 
                          on_click=lambda: go_to_protected_page('/nvda_extention_builder')).props('size=lg color=accent').classes('w-full')

            with ui.card().classes('p-6'):
                ui.html('<h3 class="text-xl font-semibold mb-3 text-primary">5. Custom Braille Document Builder</h3>')
                ui.markdown('This tool lets you convert printed documents into Braille using the projects you created.')
                ui.button('Go to Braille Document Builder', 
                          on_click=lambda: go_to_protected_page('/braille_document_builder')).props('size=lg color=accent').classes('w-full')

        # New Get Started section - consistent styling
        with ui.card().classes('p-8 w-full max-w-3xl'):
            ui.html('<h2 class="text-2xl font-semibold mb-6 text-center text-primary">Get Started</h2>')
            ui.markdown('''
Many screen reader and Braille translation software companies take a long time to develop Braille tables, and much of it requires skilled developers. 

Niv Louie attempts to bridge this gap by creating an easy way for anyone to make their Unicode documents accessible by both speech and Braille, utilizing free and open source tools which are available to everyone. 

If you can build a spreadsheet, you can make your Unicode accessible by both speech and Braille in just a few clicks after the initial spreadsheet is created. This allows users, teachers, and students to develop in an easy and manageable way — everything from custom Braille symbols for home or school projects, to a complete Braille system for languages, writing systems, and Unicode symbols which were previously believed to be inaccessible. 

Now, if you can put that Unicode symbol in a spreadsheet, you can make accessibility possible — for yourself, and even share it with the world.
            ''').classes('text-base leading-relaxed')
            
            ui.button('Log In to Get Started', 
                     on_click=lambda: ui.navigate.to('/login')).props('size=lg color=accent').classes('w-full mt-6')

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