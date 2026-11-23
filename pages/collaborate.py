# pages/13_collaborate.py

from nicegui import ui, app
from utils.i18n import back_button, copyright_footer, dashboard_button, heading, language_switcher, prepare_page, t


@ui.page("/collaborate")
def collaborate():
    prepare_page("collaborate.title")
    # Check if user is logged in
    user_id = app.storage.user.get("user_id") if hasattr(app.storage, 'user') and app.storage.user is not None else None

    if not user_id:
        with ui.column().classes('w-full max-w-md mx-auto p-8 text-center'):
            language_switcher()
            ui.icon('login', size='5xl', color='primary').classes('mx-auto mb-6')
            heading("h1", "text-3xl font-bold text-primary mb-4", "collaborate.login_first")
            ui.label(t("collaborate.login_help")).classes('text-lg mb-8')
            ui.button(t("collaborate.go_login"),
                     on_click=lambda: ui.navigate.to('/login')).props('size=lg color=accent')
            ui.button(t("common.home"),
                     on_click=lambda: ui.navigate.to('/')).props('flat color=primary size=lg').classes('w-full mt-4')
        return

    # Global layout styling - consistent with other pages
    ui.query('.nicegui-content').classes('w-full')
    ui.query('.q-page').classes('flex flex-col min-h-screen')

    with ui.column().classes('flex-1 w-full max-w-4xl mx-auto p-8 gap-10'):

        # Header with back button
        with ui.row().classes('w-full items-center justify-between'):
            back_button()
            language_switcher()

            heading("h1", "text-3xl font-bold text-primary", "collaborate.title")

        ui.markdown(t("collaborate.intro")).classes('text-base leading-relaxed')

        # ==================== Real-time Editing ====================
        with ui.card().classes('w-full p-8 border border-warning'):
            heading("h2", "text-2xl font-semibold mb-6 text-primary", "collaborate.realtime_title")

            ui.markdown(t("collaborate.realtime_body")).classes('text-base leading-relaxed')

        # ==================== Your User ID ====================
        with ui.card().classes('w-full p-8'):
            heading("h2", "text-2xl font-semibold mb-6 text-primary", "collaborate.user_id_title")
            ui.label(t("collaborate.user_id_help")).classes('font-medium mb-3')

            ui.input(
                value=user_id,
                label=t("login.user_id")
            ).props('readonly').classes('w-full font-mono')

            ui.label(t("collaborate.user_id_note")).classes('text-sm text-gray-600 mt-4')

        dashboard_button()

        ui.label(t("collaborate.future")).classes('text-sm text-gray-500 mt-12 text-center')

    copyright_footer()
