# utils/storage.py
from pathlib import Path
import uuid
from nicegui import app

# Base directory for all Niv Louie data
BASE_DATA_DIR = Path(__file__).parent.parent / "niv_louie_data"
BASE_DATA_DIR.mkdir(parents=True, exist_ok=True)

# Persistent fallback user ID file (this is the single source of truth)
USER_ID_FILE = BASE_DATA_DIR / "user_id.txt"


def get_user_id() -> str:
    """Always prefer the persistent file on disk."""
    try:
        if USER_ID_FILE.exists():
            user_id = USER_ID_FILE.read_text(encoding="utf-8").strip()
            if user_id:
                return user_id

        user_id = str(uuid.uuid4())
        USER_ID_FILE.write_text(user_id, encoding="utf-8")
        print(f"LOG: Created new persistent user ID: {user_id}")
        return user_id
    except Exception as ex:
        print(f"LOG: Error in get_user_id: {ex}")
        return "default_user"


def get_current_web_user_id() -> str:
    """Get user ID for current session, falling back to disk."""
    try:
        if (hasattr(app, 'storage') and 
            hasattr(app.storage, 'user') and 
            app.storage.user is not None):
            user_id = app.storage.user.get("user_id")
            if user_id:
                return user_id

            # Create and store in session
            user_id = get_user_id()
            app.storage.user["user_id"] = user_id
            print(f"LOG: Stored user ID in session storage: {user_id}")
            return user_id
    except Exception as ex:
        if "storage_secret" not in str(ex).lower():
            print(f"LOG: Storage not ready yet: {ex}")

    # Fallback to persistent disk ID
    return get_user_id()


def get_private_user_dir() -> Path:
    user_id = get_current_web_user_id()
    user_dir = BASE_DATA_DIR / "users" / user_id
    user_dir.mkdir(parents=True, exist_ok=True)
    return user_dir


# Directory helpers
def get_user_projects_dir() -> Path:
    return get_private_user_dir() / "projects"

def get_user_documents_dir() -> Path:
    return get_private_user_dir() / "documents"

def get_user_braille_dir() -> Path:
    return get_private_user_dir() / "braille"

def get_user_tests_dir() -> Path:
    return get_private_user_dir() / "braille_tests"

def get_user_nvda_dir() -> Path:
    return get_private_user_dir() / "nvda_extensions"


def ensure_user_directories():
    """Ensure all user folders exist."""
    get_private_user_dir()
    get_user_projects_dir()
    get_user_documents_dir()
    get_user_braille_dir()
    get_user_tests_dir()
    get_user_nvda_dir()
    print(f"LOG: All user directories ensured for {get_current_web_user_id()}")