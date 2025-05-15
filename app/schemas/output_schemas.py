from typing import List

from app.schemas.custom_base_model import CustomBaseModel


class PasswordOutput(CustomBaseModel):
    message: str
    data: List[dict]
