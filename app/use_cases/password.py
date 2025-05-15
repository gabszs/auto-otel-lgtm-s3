# script to generate a Random Password
import asyncio
from random import shuffle
from secrets import choice
from string import ascii_letters
from string import digits
from string import punctuation
from typing import List

from app.core.telemetry import instrument


@instrument
class PasswordGenerator:
    """
    Class for generating random passwords and PIN codes.

    Methods:
    async_pin(pin_lenght: int) -> int:
        Generates a random PIN code with the given length.

    async_password(password_length: int, has_ponctuation: bool = False) -> str:
        Generates a random password with the given length and optionally with punctuations.
    """

    async def async_pin(self, pin_lenght: int) -> int:
        """
        Generates a random PIN code with the given length.

        Args:
        pin_lenght (int): The length of the generated PIN code.

        Returns:
        int: The generated PIN code.
        """
        pin_range = "1234567890"
        pin_choice = "".join(choice(pin_range) for _ in range(int(pin_lenght)))
        return pin_choice

    async def async_password(
        self, password_length: int, has_ponctuation: bool = False
    ) -> str:
        """
        Generates a random password with the given length and optionally with punctuations.

        Args:
        password_length (int): The length of the generated password.
        has_ponctuation (bool, optional): Whether or not to include punctuations in the password. Defaults to False.

        Returns:
        str: The generated password.
        """
        minimum_string = (
            choice(ascii_letters) + choice(digits) + choice(digits + ascii_letters)
        )
        letters = ascii_letters + digits

        if has_ponctuation:
            minimum_string = list(minimum_string)
            del minimum_string[0]
            minimum_string = "".join(minimum_string)

            minimum_string += choice(punctuation)
            letters += punctuation

        if password_length == 3:
            password = "".join(choice(minimum_string) for _ in len(minimum_string))
            return PasswordGenerator.lower_upper_func(password)

        else:
            password_choice = (
                "".join(choice(letters) for _ in range(password_length - 3))
                + minimum_string
            )
            password_list = list(password_choice)
            shuffle(password_list)
            password = "".join(password_list)
            return PasswordGenerator.lower_upper_func(password)

    async def async_complex_password(
        self,
        char_inject: List[str],
        string_inject: List[str],
        suffle_string_inject: bool = False,
        adicional_lenght: int = 0,
        has_ponctuation: bool = False,
    ) -> str:
        password = await self.async_password(
            password_length=adicional_lenght, has_ponctuation=has_ponctuation
        )

        if suffle_string_inject:
            for count, string in enumerate(string_inject):
                string = list(string)
                shuffle(string)
                string_inject[count] = "".join(string)

        password = list(password)
        [password.append(item) for item in string_inject]
        [password.append(item) for item in char_inject]
        shuffle(password)

        password = "".join(password)

        return password

    @classmethod
    def lower_upper_func(cls, password: str) -> str:
        if password.upper() == password:
            password = list(password)
            randchoice = choice(list(range(len(password))))
            num = password[randchoice]

            while not num.isalpha():
                randchoice = choice(list(range(len(password))))
                num = password[randchoice]

            password[randchoice] = password[randchoice].lower()
            return "".join(password)

        elif password.lower() == password:
            password = list(password)
            randchoice = choice(list(range(len(password))))
            num = password[randchoice]

            while not num.isalpha():
                randchoice = choice(list(range(len(password))))
                num = password[randchoice]

            password[randchoice] = password[randchoice].upper()
            return "".join(password)

        else:
            return password


if __name__ == "__main__":
    pg = PasswordGenerator()

    async def test():
        password = await pg.async_complex_password(
            char_inject=["a", "b", "/0"],
            adicional_lenght=10,
            has_ponctuation=True,
            string_inject=["Gab", "tao", "2018"],
            suffle_string_inject=False,
        )
        return password

    async def main():
        password = await test()
        print(password)

    asyncio.run(main())

    # print(password(10, ponctuation=False))
