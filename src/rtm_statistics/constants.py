"""String and numeric constants shared across the package."""

APP_NAME = "rtm_statistics"
DEFAULT_SETTINGS_FILE = "settings.ini"
AUTH_ONLY_FLAG = "--auth-only"

SECTION_RTM = "rtm"
SECTION_TRACKING = "tracking"
SECTION_OUTPUT = "output"
SECTION_LOGGING = "logging"

KEY_API_KEY = "api_key"
KEY_SHARED_SECRET = "shared_secret"
KEY_TOKEN = "token"
KEY_SMART_LIST = "smart_list"
KEY_COMPLETED_FILTER = "completed_filter"
KEY_DATABASE = "database"
KEY_LOG_LEVEL = "level"

DEFAULT_DATABASE = "data/statistics.sqlite"
DEFAULT_LOG_LEVEL = "INFO"

STATUS_INCOMPLETE = "status:incomplete"
STATUS_COMPLETED = "status:completed"
COMPLETED_TODAY_SUFFIX = "AND completed:today"

AUTH_PERMS = "read"
AUTH_POLL_SECONDS = 5
AUTH_MAX_ATTEMPTS = 12

# RTM API error code 98: "Login failed / Invalid auth token"
INVALID_TOKEN_CODE = 98

EXIT_OK = 0
EXIT_ERROR = 1
