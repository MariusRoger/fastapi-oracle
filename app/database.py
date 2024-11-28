from app_settings import get_settings

settings = get_settings()

username = settings.ORACLE_DB_USERNAME
password = settings.ORACLE_DB_PASSWORD
dsn = settings.ORACLE_DB_DSN
