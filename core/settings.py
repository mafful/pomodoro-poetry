from pydantic_settings import BaseSettings
from pydantic import ValidationError
from loguru import logger


class Settings(BaseSettings):
    """
    Настройки проекта для запуска приложения.

    Параметры задаются через переменные окружения, указанные в `.env`.

    Attributes
    ----------
    app_title : str
        Название приложения.
    app_description : str
        Описание приложения.
    database_url : str
        URL подключения к базе данных.

    """

    app_title: str
    app_description: str
    database_url: str

    class Config:
        env_file = ".env"
        extra = "allow"


try:
    logger.info("Создание экземпляра настроек проекта.")
    settings = Settings()
    logger.info("Настройки успешно загружены.")

except ValidationError as e:
    logger.error(f"Ошибка валидации настроек: {e}.", exc_info=True)

except Exception as e:
    logger.error(f"Не удалось загрузить настройки: {e}.", exc_info=True)
