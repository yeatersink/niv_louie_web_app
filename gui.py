# gui.py - Main entry point for Niv Louie (Web Version)

from nicegui import ui, app
import os

# Import all pages so NiceGUI registers the @ui.page decorators
from pages.home import home
from pages.login import login
from pages.existing_project import existing_project
from pages.create_project import create_project
from pages.project_information import project_information
from pages.edit_project_information import edit_project_information
from pages.braille_document_builder import braille_document_builder
from pages.nvda_extention_builder import nvda_extention_builder
from pages.create_extention import create_extention
from pages.edit_extention import edit_extention
from pages.liblouis_table_builder import liblouis_table_builder
from pages.liblouis_test_builder import liblouis_test_builder
from pages.collaborate import collaborate

from utils.storage import ensure_user_directories


# ====================== STARTUP INITIALIZATION ======================
def startup():
    """Run once when the server starts"""
    try:
        ensure_user_directories()
        print("LOG: Niv Louie Web - Global user directories ensured at startup")
        
        # Color scheme
        ui.colors(
            primary='#0B2A4D',      # Dark Navy Blue
            secondary='#20B2AA',    # Teal
            accent='#20B2AA',       # Teal
            positive='#28A745',
            negative='#DC3545'
        )
        
        # Strong global CSS - especially for Teal accent
        ui.add_head_html('''
            <style>
                :root, html, body, .q-body, .nicegui-content {
                    --q-primary: #0B2A4D !important;
                    --q-accent: #20B2AA !important;
                    --q-secondary: #20B2AA !important;
                }
                
                /* Header / banner */
                .q-header, .q-toolbar, .q-toolbar__title {
                    background-color: #0B2A4D !important;
                    color: white !important;
                }
                
                /* Headings */
                h1, h2, h3, .text-h1, .text-h2, .text-h3 {
                    color: #0B2A4D !important;
                }
                
                /* Primary buttons - Navy */
                .q-btn--primary {
                    background-color: #0B2A4D !important;
                    color: white !important;
                }
                
                /* Teal Accent / Secondary buttons - FORCE TEAL */
                .q-btn--accent,
                .q-btn--secondary,
                .bg-accent,
                .bg-secondary,
                button[color="accent"],
                button[color="secondary"] {
                    background-color: #20B2AA !important;
                    color: white !important;
                    font-weight: 600 !important;
                }
                
                /* Royal blue click feedback on primary */
                .q-btn--primary:active,
                .q-btn--primary:focus,
                .q-btn--primary.q-btn--active {
                    background-color: #4169E1 !important;
                }
                
                /* Cards */
                .q-card {
                    border-radius: 12px !important;
                    box-shadow: 0 4px 15px rgba(11, 42, 77, 0.15) !important;
                }
                
                /* Responsive */
                @media (max-width: 768px) {
                    .q-page { padding: 1rem !important; }
                    h1 { font-size: 1.8rem !important; }
                    .q-btn { width: 100% !important; margin-bottom: 0.75rem !important; }
                }
            </style>
        ''', shared=True)
        
    except Exception as e:
        print(f"WARNING: Could not set styles: {e}")


# Register startup function
app.on_startup(startup)


# ====================== WEB SERVER SETUP ======================
if __name__ == "__main__":
    # Detect if we're running in Docker
    is_docker = os.getenv("DOCKER") or os.getenv("RUNNING_IN_DOCKER")
    
    ui.run(
        host="0.0.0.0" if is_docker else "127.0.0.1",
        port=8080,
        title="Niv Louie - Making the World Accessible, One Braille Table at a Time",
        reload=False,
        show=not is_docker,           # Show window only on Windows, hide in Docker
        storage_secret="niv_louie_secret_key_2026",
        favicon="🌐",
        dark=False,
        viewport="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no"
    )