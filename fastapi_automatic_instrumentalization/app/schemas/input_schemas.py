import re
from typing import List
from typing import Optional

from app.schemas.custom_base_model import CustomBaseModel
from fastapi import Query
from pydantic import BaseModel
from pydantic import field_validator


class PinPasswordOptions(BaseModel):
    password_length: Optional[int] = 12
    quantity: Optional[int] = 1


class PasswordOptions(PinPasswordOptions):
    password_length: Optional[int] = 12
    quantity: Optional[int] = 1
    has_ponctuation: Optional[bool] = True


class PasswordBody(CustomBaseModel):
    adicional_lenght: int = Query(gt=0, le=100)
    quantity: int = Query(gt=0, le=100)
    ponctuation: bool = False
    suffle_string_inject: bool = False
    char_inject: Optional[List[str]]
    string_inject: Optional[List[str]]

    @field_validator("char_inject")
    def validate_char_inject(cls, char_list):
        if any(len(char) != 1 for char in char_list):
            raise ValueError(
                "Invalid Char Regex, The items in the list need to be only one ascii carachter"
            )
        return char_list

    @field_validator("string_inject")
    def validate_string_inject(cls, string_list):
        if not any(re.match(".{2,}", string) for string in string_list):
            raise ValueError(
                "Invalide String Regex, the items in the list need be more than one ascii charater"
            )
        return string_list


if __name__ == "__main__":
    pb = PasswordBody(
        suffle_string_inject=False,
        char_inject=["s", "b", "_", "2"],
        string_inject=["gabriel23%#@", "dudus1@"],
    )

    print(pb.dict())
