# pages/home.py - Public Home Page

from pathlib import Path
from nicegui import ui, app
from utils.i18n import heading, language_switcher, prepare_page, site_footer, t


def logout():
    try:
        if hasattr(app.storage, 'user') and app.storage.user is not None:
            app.storage.user.clear()
        ui.notify(t("home.logout_success"), type="positive")
        ui.navigate.to('/')
    except Exception as e:
        ui.notify(t("home.logout_done"), type="positive")
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


def _log_if_example_missing(filename):
    root = Path(__file__).resolve().parent.parent
    search_paths = [
        root / "static" / filename,
        root / "static" / "files" / filename,
        root / filename,
    ]
    for path in search_paths:
        if path.is_file():
            return
    print(f"LOG: Example file missing: {filename}")


@ui.page("/")
def home():
    # NO ensure_user_directories() here - this is a public page
    prepare_page("home.title")

    _log_if_example_missing("example of Csv.csv")
    _log_if_example_missing("example of test.csv")

    # Strong layout setup to push footer to the bottom
    ui.query('.nicegui-content').classes('w-full')
    ui.query('.q-page').classes('flex flex-col min-h-screen')

    with ui.header().classes('items-center justify-between bg-primary text-white p-4 shadow'):
        with ui.row().classes('items-center gap-6 w-full max-w-6xl mx-auto'):
            ui.label(t("common.brand")).classes('text-3xl font-bold tracking-tight')
            ui.space()
            language_switcher()
            
            # Smart Dashboard button
            ui.button(t("common.dashboard"), 
                     on_click=go_to_dashboard_or_login).props('flat color=accent')
            
            # Original Log In button
            ui.button(t("common.log_in"), 
                     on_click=lambda: ui.navigate.to('/login')).props('flat color=accent')
            
            ui.button(t("common.collaborate"), 
                     on_click=lambda: ui.navigate.to('/collaborate')).props('flat color=white')

    # Main content area
    with ui.column().classes('flex-1 w-full max-w-4xl mx-auto p-8 gap-16 items-center'):
        # Larger project image / visual representation area (linked to documentation)
        with ui.row().classes('w-full justify-center mb-8'):
            with ui.link(target='/documentation').classes('block w-full max-w-lg md:max-w-2xl'):
                ui.image('/static/images/nivlouie.jpeg').classes('w-full h-auto rounded-2xl shadow-xl object-contain')
        
        # Description for the image
        with ui.row().classes('w-full justify-center mb-12'):
            ui.label(t("common.image_caption")).classes('text-center text-gray-600 max-w-2xl text-lg')    

        heading("h1", "text-4xl font-bold text-center text-primary", "home.welcome")

        ui.markdown(t("home.intro"), sanitize=False).classes('text-base leading-relaxed text-center max-w-3xl text-primary')

        with ui.card().classes('p-8 w-full max-w-3xl'):
            heading("h2", "text-2xl font-semibold mb-4 text-center text-primary", "home.what_title")
            ui.markdown(t("home.what_body")).classes('text-base leading-relaxed')

        with ui.card().classes('p-8 w-full max-w-3xl border border-negative'):
            heading("h2", "text-2xl font-semibold mb-6 text-negative text-center", "home.disclaimer_title")
            ui.markdown(t("home.disclaimer_body")).classes('text-base leading-relaxed text-center')

        with ui.card().classes('p-8 w-full max-w-3xl'):
            heading("h2", "text-2xl font-semibold mb-8 text-center text-primary", "home.how_title")

            with ui.card().classes('p-6 mb-6'):
                heading("h3", "text-xl font-semibold mb-3 text-primary", "home.step1_title")
                ui.markdown(t("home.step1_body"))
                ui.markdown(t("home.step1_download_note"))
                ui.link(t("home.step1_download"), "/static/example of Csv.csv").props('download="example of Csv.csv"').classes('text-accent hover:underline font-medium')

            with ui.card().classes('p-6 mb-6'):
                heading("h3", "text-xl font-semibold mb-3 text-primary", "home.step2_title")
                ui.markdown(t("home.step2_body"))

            with ui.card().classes('p-6 mb-6'):
                heading("h3", "text-xl font-semibold mb-3 text-primary", "home.step3_title")
                ui.markdown(t("home.step3_body"))
                ui.markdown(t("home.step3_download_note"))
                ui.link(t("home.step3_download"), "/static/example of test.csv").props('download="example of test.csv"').classes('text-accent hover:underline font-medium')

            with ui.card().classes('p-6 mb-6'):
                heading("h3", "text-xl font-semibold mb-3 text-primary", "home.step4_title")
                ui.markdown(t("home.step4_body"))

            with ui.card().classes('p-6'):
                heading("h3", "text-xl font-semibold mb-3 text-primary", "home.step5_title")
                ui.markdown(t("home.step5_body"))

        # New Get Started section - consistent styling
        with ui.card().classes('p-8 w-full max-w-3xl'):
            heading("h2", "text-2xl font-semibold mb-6 text-center text-primary", "home.get_started_title")
            ui.markdown(t("home.get_started_body")).classes('text-base leading-relaxed')
            
            ui.button(t("home.get_started_button"), 
                     on_click=lambda: ui.navigate.to('/login')).props('size=lg color=accent').classes('w-full mt-6')

    site_footer("https://www.youtube.com/@NivLouieInfo")
