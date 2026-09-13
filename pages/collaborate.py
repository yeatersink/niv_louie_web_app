# pages/13_collaborate.py

from nicegui import ui, app


@ui.page("/collaborate")
def collaborate():
    # Check if user is logged in
    user_id = app.storage.user.get("user_id") if hasattr(app.storage, 'user') and app.storage.user is not None else None

    if not user_id:
        with ui.column().classes('w-full max-w-md mx-auto p-8 text-center'):
            ui.icon('login', size='5xl', color='primary').classes('mx-auto mb-6')
            ui.html('<h1 class="text-3xl font-bold text-primary mb-4">Please Log In First</h1>')
            ui.label('You must log in to see your User ID.').classes('text-lg mb-8')
            ui.button('Go to Login',
                     on_click=lambda: ui.navigate.to('/login')).props('size=lg color=accent')
            ui.button('Home',
                     on_click=lambda: ui.navigate.to('/')).props('flat color=primary size=lg').classes('w-full mt-4')
        return

    # Global layout styling - consistent with other pages
    ui.query('.nicegui-content').classes('w-full')
    ui.query('.q-page').classes('flex flex-col min-h-screen')

    with ui.column().classes('flex-1 w-full max-w-4xl mx-auto p-8 gap-10'):

        # Header with back button
        with ui.row().classes('w-full items-center justify-between'):
            ui.button("← Go Back",
                     on_click=ui.navigate.back).props('flat color=primary size=lg')

            ui.html('<h1 class="text-3xl font-bold text-primary">Collaborate with Others</h1>')

        ui.markdown("""
You can open the same Niv Louie account on another device by signing in with this User ID.
        """).classes('text-base leading-relaxed')

        # ==================== Real-time Editing ====================
        with ui.card().classes('w-full p-8 border border-warning'):
            ui.html('<h2 class="text-2xl font-semibold mb-6 text-primary">Real-time Editing & Collaboration</h2>')

            ui.markdown("""
Real-time editing and collaboration works best in an environment that has this functionality mastered already. 

For this reason, **Niv Louie recommends**:

- **VS Code Live Share** for real-time Python code and script collaboration  
- **Microsoft 365** for real-time editing on Excel spreadsheets

Excel will allow saving as `.csv`, and **Niv Louie also supports Excel spreadsheets**.
            """).classes('text-base leading-relaxed')

        # ==================== Your User ID ====================
        with ui.card().classes('w-full p-8'):
            ui.html('<h2 class="text-2xl font-semibold mb-6 text-primary">Your User ID</h2>')
            ui.label("Use this User ID to sign in directly on any device:").classes('font-medium mb-3')

            ui.input(
                value=user_id,
                label="Your User ID"
            ).props('readonly').classes('w-full font-mono')

            ui.label("This User ID is how you sign in on another device.").classes('text-sm text-gray-600 mt-4')

        ui.button("Go to Dashboard",
                 on_click=lambda: ui.navigate.to("/dashboard")
        ).props('flat color=primary size=lg').classes('w-full mt-8')

        ui.label("More advanced collaboration features (fine-grained permissions, notifications) are planned for future updates.").classes('text-sm text-gray-500 mt-12 text-center')

    # Footer
    with ui.column().classes('w-full bg-gray-100 py-12 border-t mt-auto'):
        ui.label('© 2026 Niv Louie - Free and Open Source (GPL-3.0)').classes('text-xs text-gray-500 text-center mx-auto')
