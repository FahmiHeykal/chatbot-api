from pydantic import BaseSettings
from typing import List, Union
import ast

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    OPENAI_API_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str
    CORS_ORIGINS: Union[str, List[str]]

    class Config:
        env_file = ".env"

    @property
    def cors_origin_list(self) -> List[str]:
        if isinstance(self.CORS_ORIGINS, str):
            return ast.literal_eval(self.CORS_ORIGINS)
        return self.CORS_ORIGINS

settings = Settings()
