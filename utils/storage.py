# utils/storage.py
from pathlib import Path
import uuid
import json
from datetime import datetime
from nicegui import app

# Base data directory on the server
BASE_DATA_DIR = Path.home() / "niv_louie_data"
BASE_DATA_DIR.mkdir(parents=True, exist_ok=True)

# Directory for sync codes
SYNC_CODES_DIR = BASE_DATA_DIR / "sync_codes"
SYNC_CODES_DIR.mkdir(parents=True, exist_ok=True)


def get_current_web_user_id(create_if_missing: bool = False) -> str | None:
    """
    Get the current user's ID.
    
    Args:
        create_if_missing: If True, create a new user ID when none exists.
                          If False, return None if no user is logged in.
    """
    try:
        if hasattr(app, 'storage') and hasattr(app.storage, 'user') and app.storage.user is not None:
            user_id = app.storage.user.get("user_id")
            if user_id:
                return str(user_id)

            # Only create a new ID if explicitly allowed
            if create_if_missing:
                user_id = str(uuid.uuid4())
                app.storage.user["user_id"] = user_id
                print(f"LOG: Created new user ID: {user_id}")
                return user_id
            else:
                return None

    except Exception as ex:
        # Suppress common startup warnings
        if "storage_secret" not in str(ex).lower():
            print(f"LOG: Storage not ready: {ex}")

    return None


def generate_sync_code() -> str:
    """Generate a readable sync code for linking devices"""
    user_id = get_current_web_user_id(create_if_missing=True)
    if not user_id:
        raise ValueError("Cannot generate sync code: No user logged in")

    adjectives = ["BLUE", "GREEN", "GOLD", "SILVER", "WISE", "CALM", "BRIGHT", "NOBLE"]
    nouns = ["APPLE", "RIVER", "MOUNTAIN", "STAR", "BIRD", "STONE", "OCEAN", "FOREST"]
    
    adj = adjectives[uuid.uuid4().int % len(adjectives)]
    noun = nouns[uuid.uuid4().int % len(nouns)]
    number = str(uuid.uuid4().int % 100).zfill(2)
    
    code = f"{adj}-{noun}-{number}"
    
    code_file = SYNC_CODES_DIR / f"{code}.json"
    data = {
        "user_id": user_id,
        "created_at": datetime.now().isoformat(),
        "expires_at": None
    }
    
    code_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
    
    print(f"LOG: Generated sync code {code} for user {user_id}")
    return code


def claim_sync_code(sync_code: str) -> bool:
    """Claim a sync code to link current session to existing user"""
    try:
        clean_code = sync_code.strip().upper()
        code_file = SYNC_CODES_DIR / f"{clean_code}.json"
        
        if not code_file.exists():
            return False

        data = json.loads(code_file.read_text(encoding="utf-8"))
        target_user_id = data.get("user_id")

        if not target_user_id:
            return False

        if hasattr(app, 'storage') and hasattr(app.storage, 'user') and app.storage.user is not None:
            app.storage.user["user_id"] = target_user_id
            print(f"LOG: Claimed sync code {clean_code} → user {target_user_id}")
            return True

        return False
    except Exception as ex:
        print(f"LOG: Error claiming sync code: {ex}")
        return False


def get_private_user_dir() -> Path:
    """Get the private directory for the current user. Creates it if user exists."""
    user_id = get_current_web_user_id()
    if not user_id:
        raise ValueError("Cannot get user directory: No user is logged in")
    
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
    """Ensure all user subdirectories exist. Only works if user is logged in."""
    try:
        get_private_user_dir()
        get_user_projects_dir()
        get_user_documents_dir()
        get_user_braille_dir()
        get_user_tests_dir()
        get_user_nvda_dir()
        print(f"LOG: User directories ensured for {get_current_web_user_id()}")
    except Exception as e:
        print(f"LOG: Could not ensure directories (no user logged in?): {e}")


def create_new_user_session(nickname: str) -> str:
    """Explicitly create a new user session with ID and directories."""
    if not nickname or not nickname.strip():
        raise ValueError("Nickname is required")
    
    user_id = get_current_web_user_id(create_if_missing=True)
    if hasattr(app, 'storage') and hasattr(app.storage, 'user'):
        app.storage.user["nickname"] = nickname.strip()
    
    ensure_user_directories()
    print(f"LOG: New user session created - ID: {user_id}, Nickname: {nickname}")
    return user_id