from pydantic_settings import BaseSettings
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """
    Application settings class
    """

    # CALENDARIFIC API
    BASE_URL: str
    CALENDARIFIC_API_KEY: str

    class Config:
        env_file = "../../.env"
        from_attributes = True
