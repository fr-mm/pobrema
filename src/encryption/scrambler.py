import os
from pathlib import Path

from src.encryption.errors import FileWithoutExtensionError, FileHasExtensionError, TargetFileAlreadyExistsError
from src.encryption.char_swapper import CharSwapper
from src.enums import FileSystemEnum as En


class Scrambler:
    __file: str
    __char_swapper: CharSwapper

    def __init__(self, file: str) -> None:
        self.__file = file
        if not Path(file).exists():
            raise FileNotFoundError(file)

    def encrypt(self) -> None:
        new_name = self.__get_encrypted_file_name()
        if self.__file_has_extension() and not self.__target_file_already_exists(new_name):
            self.__set_to_encrypt()
            self.__transform_file(new_name)

    def decrypt(self) -> None:
        new_name = self.__get_decrypted_file_name()
        if self.__file_has_no_extension() and not self.__target_file_already_exists(new_name):
            self.__set_to_decrypt()
            self.__transform_file(new_name)

    @property
    def is_encrypted(self) -> bool:
        return '.' not in self.__file

    def __transform_file(self, new_name: str) -> None:
        self.__translate()
        self.__rename(new_name)
        self.__file = new_name

    def __set_to_encrypt(self) -> None:
        self.__char_swapper = CharSwapper.to_encrypt()

    def __set_to_decrypt(self) -> None:
        self.__char_swapper = CharSwapper.to_decrypt()

    def __translate(self) -> None:
        with open(self.__file, 'r') as file:
            original_content = file.read()

        new_content = self.__translate_content(original_content)

        with open(self.__file, 'w') as file:
            file.write(new_content)

    def __translate_content(self, content: str) -> str:
        return ''.join([self.__char_swapper.swap(char) for char in content])

    def __rename(self, new_name: str) -> None:
        os.rename(self.__file, new_name)

    def __get_encrypted_file_name(self) -> str:
        return self.__file.split('.')[0]

    def __get_decrypted_file_name(self) -> str:
        return f'{self.__file}.{En.FILE_EXTENSION}'

    def __file_has_extension(self) -> bool:
        extension = self.__file.split('.')[-1]
        extension_unrecognized = extension != En.FILE_EXTENSION
        if extension_unrecognized:
            raise FileWithoutExtensionError(self.__file)
        return not extension_unrecognized

    def __file_has_no_extension(self) -> bool:
        file_has_no_extension = self.is_encrypted
        if not file_has_no_extension:
            raise FileHasExtensionError(self.__file)
        return file_has_no_extension

    def __target_file_already_exists(self, target_file: str) -> bool:
        target_file_already_exists = Path(target_file).is_file()
        if target_file_already_exists:
            raise TargetFileAlreadyExistsError(self.__file, target_file)
        return target_file_already_exists
