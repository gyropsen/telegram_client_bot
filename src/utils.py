import csv
import json
import logging
import os
import time

from telethon.errors.rpcerrorlist import PhoneNumberBannedError

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


def read_json(path: str) -> list | dict:
    with open(path, "r") as file:
        data = json.load(file)
    return data


def write_json(path: str, data) -> None:
    with open(path, "w") as file:
        json.dump(data, file)


def get_numbers(path: str) -> list:
    if os.path.isfile(path):
        return read_json(path)
    else:
        write_json(path, [])
        return []


def add_numbers(path):
    input_phones = input("Enter phone numbers separated by commas " "<79001234567, 627871234567, 911156231278>: ")

    available_numbers = get_numbers(path)

    numbers_phone = input_phones.strip().split(", ")
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


def get_username_channel():
    while True:
        channel = input("Enter the link to the format channel <https://t.me/wewantyoutodothejob>: ")
        if channel[:13] != "https://t.me/":
            print("Incorrect URL, please enter again")
            time.sleep(2)
        else:
            print("Correct URL")
            time.sleep(2)
            return channel


def subscribe_telethon(account, username_channel, subscribe: bool) -> None:
    if subscribe:
        action = account.subscribe
    else:
        action = account.unsubscribe
    try:
        with account.get_client_telethon() as client:
            client.loop.run_until_complete(action(username_channel, client))
    except PhoneNumberBannedError as ban_error:
        logger.error(ban_error)
        print(ban_error)
    except Exception as error:
        logger.error(error)
        print(error)


def readiness_check_telethon(account):
    client = account.get_client()
    with client:
        client.loop.run_until_complete(account.get_status_premium(client))

    account.check_session()

    print(f"Account {account.number} has a session: {account.session}")
    print(f"Account {account.number} has a premium: {account.premium}")
    time.sleep(1)
