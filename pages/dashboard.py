# pages/dashboard.py - Logged-in Dashboard

from html import escape
from nicegui import ui, app
from utils.i18n import heading, language_switcher, prepare_page, site_footer, t
from utils.storage import ensure_user_directories, get_current_web_user_id
from utils.project import project


def init_user_storage():
    try:
        # Only try to ensure directories if we have a real user_id
        user_id = get_current_web_user_id()
        if user_id and not user_id.startswith("temp_"):
            ensure_user_directories()
            nickname = app.storage.user.get("nickname", t("common.user_fallback"))
            print(f"LOG: Dashboard loaded - Logged in as: {nickname} (ID: {user_id})")
        else:
            print(f"LOG: Dashboard accessed without full login (ID: {user_id})")
    except Exception as e:
        print(f"LOG: Could not init user storage on dashboard: {e}")


def logout():
    try:
        if hasattr(app.storage, 'user') and app.storage.user is not None:
            app.storage.user.clear()
        ui.notify(t("home.logout_success"), type="positive")
        ui.navigate.to('/')
    except Exception as e:
        print(f"LOG: Logout error on dashboard: {e}")
        ui.notify(t("home.logout_done"), type="positive")
        ui.navigate.to('/')


def load_user_project_names():
    ensure_user_directories()
    project.set_user_storage()
    project.reload_languages()
    return [name for name in project.languages_list if name]


@ui.page("/dashboard")
def dashboard():
    prepare_page("dashboard.title")
    init_user_storage()
    
    user_id = get_current_web_user_id()
    nickname = app.storage.user.get("nickname", t("common.user_fallback"))
    project_list_container = None

    def show_my_projects():
        names = load_user_project_names()
        project_list_container.clear()
        with project_list_container:
            heading("h2", "text-2xl font-semibold mb-3 text-primary", "dashboard.your_projects")
            if not names:
                ui.label(t("dashboard.no_projects")).classes('text-gray-700')
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
            ui.label(t("common.brand")).classes('text-3xl font-bold tracking-tight')
            ui.space()
            language_switcher()
            
            # New Home button - matching the style and position of the Dashboard button on home page
            ui.button(t("common.home"), 
                     on_click=lambda: ui.navigate.to('/')).props('flat color=accent')
            
            ui.button(t("common.log_out"), on_click=logout).props('flat color=white')
            ui.button(t("common.collaborate"), 
                     on_click=lambda: ui.navigate.to('/collaborate')).props('flat color=white')

    # Main content - flex-1 pushes footer down
    with ui.column().classes('flex-1 w-full max-w-4xl mx-auto p-8 gap-12 items-center'):

        # Larger project image / visual representation area (linked to documentation)
        with ui.row().classes('w-full justify-center mb-8'):
            with ui.link(target='/documentation').classes('block w-full max-w-lg md:max-w-2xl'):
                ui.image('/static/images/nivlouie.jpeg').classes('w-full h-auto rounded-2xl shadow-xl object-contain')
                        
        # Description for the image
        with ui.row().classes('w-full justify-center mb-12'):
            ui.label(t("common.image_caption")).classes('text-center text-gray-600 max-w-2xl text-lg')

        heading("h1", "text-4xl font-bold text-center text-primary", "dashboard.welcome", nickname=escape(str(nickname)))

        # Logged-in status
        with ui.card().classes('p-6 w-full max-w-3xl'):
            with ui.row().classes('items-center justify-between w-full'):
                heading("h2", "text-2xl font-semibold text-primary", "dashboard.logged_in", nickname=escape(str(nickname)))
                ui.button(t("common.log_out"), on_click=logout).props('flat color=negative')

            ui.button(t("dashboard.show_projects"),
                      on_click=show_my_projects
            ).props('size=lg color=accent').classes('w-full mt-6')

        with ui.column().classes('w-full max-w-3xl') as project_list_container:
            pass
        show_my_projects()

        # Tool cards
        with ui.card().classes('p-6 w-full max-w-3xl text-center'):
            heading("h2", "text-2xl font-semibold mb-3 text-primary", "dashboard.project_manager")
            ui.markdown(t("home.step1_body"))
            ui.button(t("dashboard.go_project_manager"), 
                      on_click=lambda: ui.navigate.to('/existing_project')).props('size=lg color=accent').classes('w-full')

        with ui.card().classes('p-6 w-full max-w-3xl text-center'):
            heading("h2", "text-2xl font-semibold mb-3 text-primary", "dashboard.braille_doc")
            ui.markdown(t("dashboard.braille_doc_body"))
            ui.button(t("dashboard.go_braille"), 
                      on_click=lambda: ui.navigate.to('/braille_document_builder')).props('size=lg color=accent').classes('w-full')

        with ui.card().classes('p-6 w-full max-w-3xl text-center'):
            heading("h2", "text-2xl font-semibold mb-3 text-primary", "dashboard.nvda")
            ui.markdown(t("dashboard.nvda_body"))
            ui.button(t("dashboard.go_nvda"), 
                      on_click=lambda: ui.navigate.to('/nvda_extention_builder')).props('size=lg color=accent').classes('w-full')

        with ui.card().classes('p-6 w-full max-w-3xl text-center'):
            heading("h2", "text-2xl font-semibold mb-3 text-primary", "dashboard.liblouis")
            ui.markdown(t("dashboard.liblouis_body"))
            ui.button(t("dashboard.go_liblouis"), 
                      on_click=lambda: ui.navigate.to('/liblouis_table_builder')).props('size=lg color=accent').classes('w-full')

        with ui.card().classes('p-6 w-full max-w-3xl text-center'):
            heading("h2", "text-2xl font-semibold mb-3 text-primary", "dashboard.test")
            ui.markdown(t("dashboard.test_body"))
            ui.button(t("dashboard.go_test"), 
                      on_click=lambda: ui.navigate.to('/liblouis_test_builder')).props('size=lg color=accent').classes('w-full')


    site_footer("https://www.youtube.com/channel/UCGSfwD06fubtGXRkR7kn_Jg")
