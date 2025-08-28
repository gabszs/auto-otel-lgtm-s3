from asyncio import gather
from typing import Annotated

from app.core.dependencies import logger
from app.schemas.input_schemas import PasswordBody
from app.schemas.input_schemas import PasswordOptions
from app.schemas.input_schemas import PinPasswordOptions
from app.schemas.output_schemas import PasswordOutput
from app.use_cases.password import PasswordGenerator
from fastapi import APIRouter
from fastapi import Depends

_password_generator = Annotated[PasswordGenerator, Depends(PasswordGenerator)]
router = APIRouter(tags=["Password-Generator"])


@router.get("/", response_model=PasswordOutput)
async def get_password(
    pg: _password_generator, password_options: PasswordOptions = Depends()
):
    corroutines = list()
    for number in range(password_options.quantity):
        coro = pg.async_password(
            password_length=password_options.password_length,
            has_ponctuation=password_options.has_ponctuation,
        )
        corroutines.append(coro)

    gather_result = await gather(*corroutines)
    logger.info(
        "senhas geradas com sucesso",
        extra={
            f"{count + 1}º pin": gather_result[count]
            for count in range(len(gather_result))
        },
    )
    return PasswordOutput(
        message="Success",
        data=[
            {f"{count + 1}º pin": gather_result[count]}
            for count in range(password_options.quantity)
        ],
    )


@router.get("/pin", response_model=PasswordOutput)
async def pin_code(
    pg: _password_generator, password_options: PinPasswordOptions = Depends()
):
    pg = PasswordGenerator()
    corroutines = list()

    for number in range(password_options.quantity):
        coro = pg.async_pin(pin_lenght=password_options.password_length)
        corroutines.append(coro)

    gather_result = await gather(*corroutines)
    logger.info(
        "senhas geradas com sucesso",
        extra={
            f"{count + 1}º pin": gather_result[count]
            for count in range(len(gather_result))
        },
    )
    return PasswordOutput(
        message="Success",
        data=[
            {f"{count + 1}º pin": gather_result[count]}
            for count in range(password_options.quantity)
        ],
    )


@router.post("/complex_password", response_model=PasswordOutput)
async def complex_password(password_options: PasswordBody, pg: _password_generator):
    corroutines = list()

    for number in range(password_options.quantity):
        coro = pg.async_complex_password(
            char_inject=password_options.char_inject,
            string_inject=password_options.string_inject,
            suffle_string_inject=password_options.suffle_string_inject,
            adicional_lenght=password_options.adicional_lenght,
            has_ponctuation=password_options.ponctuation,
        )
        corroutines.append(coro)

    gather_result = await gather(*corroutines)
    logger.info(
        "senhas geradas com sucesso",
        extra={
            f"{count + 1}º pin": gather_result[count]
            for count in range(len(gather_result))
        },
    )
    return PasswordOutput(
        message="Success",
        data=[
            {f"{count + 1}º pin": gather_result[count]}
            for count in range(password_options.quantity)
        ],
    )
