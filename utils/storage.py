# utils/storage.py
from pathlib import Path
import uuid
import json
from datetime import datetime
from nicegui import app

# Base data directory - placed outside the project code (recommended for servers)
# On your Fedora server this will be ~/niv_louie_data
BASE_DATA_DIR = Path.home() / "niv_louie_data"
BASE_DATA_DIR.mkdir(parents=True, exist_ok=True)

# Directory for mapping sync codes to user_ids
SYNC_CODES_DIR = BASE_DATA_DIR / "sync_codes"
SYNC_CODES_DIR.mkdir(parents=True, exist_ok=True)


def get_current_web_user_id() -> str:
    """
    Get or create a unique user ID for the current browser session.
    Uses NiceGUI app.storage.user as primary method for true per-user isolation.
    """
    try:
        # Primary: Use NiceGUI session storage
        if hasattr(app, 'storage') and hasattr(app.storage, 'user') and app.storage.user is not None:
            user_id = app.storage.user.get("user_id")
            if user_id:
                return user_id

            # Create new user ID and store it in the session
            user_id = str(uuid.uuid4())
            app.storage.user["user_id"] = user_id
            print(f"LOG: Created new session user ID: {user_id}")
            return user_id

    except Exception as ex:
        if "storage_secret" not in str(ex).lower():
            print(f"LOG: Storage not ready yet: {ex}")

    # Fallback for very early calls before storage is initialized
    temp_id = f"temp_{uuid.uuid4().hex[:12]}"
    print(f"LOG: Using temporary user ID: {temp_id}")
    return temp_id


def generate_sync_code() -> str:
    """
    Generate a short, memorable sync code that can be used to link multiple devices
    to the same user_id.
    Returns an 8-character uppercase code (e.g. 'KX9P-2M7Q')
    """
    user_id = get_current_web_user_id()
    
    # Create a short code (8 characters)
    code = str(uuid.uuid4()).upper()[:8]
    # Make it more readable with a hyphen
    code = code[:4] + "-" + code[4:]
    
    # Save mapping: code -> user_id
    code_file = SYNC_CODES_DIR / f"{code}.json"
    data = {
        "user_id": user_id,
        "created_at": datetime.now().isoformat(),
        "expires_at": None  # Can add expiration later if needed
    }
    code_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
    
    print(f"LOG: Generated sync code {code} for user {user_id}")
    return code


def claim_sync_code(sync_code: str) -> bool:
    """
    Claim a sync code to link the current session to an existing user_id.
    Returns True if successful.
    """
    try:
        code_file = SYNC_CODES_DIR / f"{sync_code.upper()}.json"
        if not code_file.exists():
            print(f"LOG: Sync code {sync_code} not found")
            return False

        data = json.loads(code_file.read_text(encoding="utf-8"))
        target_user_id = data.get("user_id")

        if not target_user_id:
            return False

        # Apply the existing user_id to current session
        if hasattr(app, 'storage') and hasattr(app.storage, 'user') and app.storage.user is not None:
            app.storage.user["user_id"] = target_user_id
            print(f"LOG: Successfully claimed sync code {sync_code} for user {target_user_id}")
            return True

        return False
    except Exception as ex:
        print(f"LOG: Error claiming sync code {sync_code}: {ex}")
        return False


def get_private_user_dir() -> Path:
    """Get the private directory for the current user."""
    user_id = get_current_web_user_id()
    user_dir = BASE_DATA_DIR / "users" / user_id
    user_dir.mkdir(parents=True, exist_ok=True)
    return user_dir


# Directory helpers (these stay exactly the same so other files don't need changes)
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
    """Ensure all standard user subdirectories exist."""
    get_private_user_dir()
    get_user_projects_dir()
    get_user_documents_dir()
    get_user_braille_dir()
    get_user_tests_dir()
    get_user_nvda_dir()
    print(f"LOG: User directories ensured for {get_current_web_user_id()}")