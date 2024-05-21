import csv
import json
import logging
import os
import time

from src.classes.account_pyrogram import TGAccountPyrogram
from src.classes.account_telethon import TGAccountTelethon

logger = logging.getLogger(__name__)


def write_xlsx(path: str, data: list[dict]) -> None:
    """
    Запись в csv файл
    :param data: список словарей с данными
    :param path: путь к файлу
    :return: None
    """
    with open(path, "w", newline="") as file:
        fieldnames = ["number", "session", "premium"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow({"number": "number", "session": "session", "premium": "premium"})
        for row in data:
            writer.writerow(row)


def read_json(path: str) -> list[str, str]:
    """
    Прочитать файл.json
    :param path: путь до файла
    :return: данные в файле.json
    """
    with open(path, "r") as file:
        data = json.load(file)
    return data


def write_json(path: str, data) -> None:
    """
    Записать данные в файл.json
    :param path: путь до файла
    :param data: данные для записи
    :return: None
    """
    with open(path, "w") as file:
        json.dump(data, file)


def get_numbers(path: str) -> list[str, str] | list:
    """
    Получить номера телефонов, если их нет, записать и вернуть пустой список
    :param path: путь до файла
    :return: list[str, str] | list
    """
    if os.path.isfile(path):
        return read_json(path)
    else:
        write_json(path, [])
        return []


def add_numbers(path: str) -> None:
    """
    Добавить номер в базу данных управляемых номеров
    :param path: путь до файла
    :return: None
    """
    input_phones = input("Enter phone numbers separated by commas " "<79001234567 627871234567 911156231278>: ")

    available_numbers = get_numbers(path)

    numbers_phone = input_phones.strip().split(" ")
    for number in numbers_phone:
        if not number.isdigit() or len(number) < 10:
            print(f"{number} is not corrected, pass")
            continue
        elif number in available_numbers:
            print(f"{number} is in the list of available numbers, pass")
            continue
        available_numbers.append(number)

    write_json(path, available_numbers)
    print(f"Such numbers will be recorded: {available_numbers}")


def get_username_channel() -> str:
    """
    Получение от пользователя ссылки на тг-канал, и проверка его на соответствие
    :return: ссылка на тг-канал str
    """
    while True:
        channel: str = input("Enter the link to the format channel <https://t.me/wewantyoutodothejob>: ")
        if channel[:13] != "https://t.me/":
            print("Incorrect URL, please enter again")
            time.sleep(2)
        else:
            print("Correct URL")
            time.sleep(2)
            return channel


def get_class_account():
    """
    Получить от пользователя класс, с которым будем работать
    :return: None
    """
    while True:
        account = input(
            """Enter the library to work with:
            1. Pyrogram
            2. Telethon"""
        )
        if account == "1":
            print("Library Pyrogram selected")
            time.sleep(2)
            return TGAccountPyrogram

        elif account == "2":
            print("Library Telethon selected")
            time.sleep(2)
            return TGAccountTelethon

        else:
            print("Incorrect library selected")
            time.sleep(2)


def readiness_check(account: TGAccountTelethon | TGAccountPyrogram) -> None:
    """
    Проверить готовность аккаунта к работе
    :param account: экземпляр класса для работы с одной из библиотек
    :return: None
    """
    client = account.get_client()
    with client:
        account.run(client, account.get_status_premium)

    account.check_session()

    print(f"Account {account.number} has a session: {account.session}")
    print(f"Account {account.number} has a premium: {account.premium}")
    time.sleep(1)


def subscribe(account: TGAccountTelethon | TGAccountPyrogram, username_channel: str, subs: bool) -> None:
    """
    Подписывается или отписывается от канала в зависимости от subs
    :param account: экземпляр класса для работы с одной из библиотек
    :param username_channel: Ссылка или имя канала для подписки
    :param subs: True - подписаться, False - отписаться
    :return:
    """
    if subs:
        action = account.subscribe
    else:
        action = account.unsubscribe
    try:
        with account.get_client() as client:
            account.run(client, action, username_channel)
    except Exception as error:
        logger.error(error)
        print(error)
