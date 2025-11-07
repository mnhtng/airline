from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator


class Settings(BaseSettings):
    DATABASE_URL: str
    API_PREFIX: str = "/api/v1"
    DEBUG: bool = False
    ALLOWED_ORIGINS: str = ""
    OPENAI_API_KEY: str

    # Validate and split the ALLOWED_ORIGINS before storing
    @field_validator("ALLOWED_ORIGINS")
    def parse_allowed_origins(cls, v: str) -> List[str]:
        return v.split(",") if v else []

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()


# Used for linux(ubuntu) server

# from typing import List
# from pathlib import Path
# from pydantic_settings import BaseSettings
# from pydantic import field_validator


# class Settings(BaseSettings):
#     DATABASE_URL: str
#     API_PREFIX: str = "/api/v1"
#     DEBUG: bool = False
#     ALLOWED_ORIGINS: str = ""
#     OPENAI_API_KEY: str = ""  # Optional, default to empty string

#     # Validate and split the ALLOWED_ORIGINS before storing
#     @field_validator("ALLOWED_ORIGINS")
#     def parse_allowed_origins(cls, v: str) -> List[str]:
#         return v.split(",") if v else []

#     class Config:
#         # Look for .env in backend/ directory
#         env_file = str(Path(__file__).parent.parent / ".env")
#         env_file_encoding = "utf-8"
#         case_sensitive = True


# settings = Settings()
