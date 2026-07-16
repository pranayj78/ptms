from pydantic_settings import BaseSettings


class PTMSSettings(BaseSettings):
    financial_year: str = "2025-26"

    assessment_year: str = "2026-27"

    default_currency: str = "INR"

    country_code = "IN"

    class Config:
        env_prefix = "PTMS_"
