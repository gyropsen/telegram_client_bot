from src.utils import *
from src.logger import setup_logging

from telethon.errors.rpcerrorlist import PhoneNumberBannedError
from simple_term_menu import TerminalMenu
from pathlib import Path
import time

phone_numbers_path = str(Path(Path(__file__).parent, "data", "phone_numbers.json"))
accounts_data_json = str(Path(Path(__file__).parent, "data", "accounts_data.json"))
accounts_data_xlsx = str(Path(Path(__file__).parent, "data", "accounts_data.xlsx"))

logger = setup_logging()


def main():
    username_channel = get_username_channel()
    class_account = get_class_account()
    accounts: list = []

    main_menu_title = "  Main Menu.\n  Press Q or Esc to quit. \n"
    main_menu_items = ["Manage accounts", "Manage account", "Add accounts", "Quit"]
    main_menu_cursor = "> "
    main_menu_cursor_style = ("fg_red", "bold")
    main_menu_style = ("bg_red", "fg_yellow")
    main_menu_exit = False

    main_menu = TerminalMenu(
        menu_entries=main_menu_items,
        title=main_menu_title,
        menu_cursor=main_menu_cursor,
        menu_cursor_style=main_menu_cursor_style,
        menu_highlight_style=main_menu_style,
        cycle_cursor=True,
        clear_screen=True,
    )

    manage_accounts_menu_title = "  Manage accounts Menu.\n  Press Q or Esc to back to main menu. \n"
    manage_accounts_menu_items = ["Subscribe to the channel", "Unsubscribe from the channel", "Back to Main Menu"]
    manage_accounts_menu_back = False
    manage_accounts_menu = TerminalMenu(
        manage_accounts_menu_items,
        title=manage_accounts_menu_title,
        menu_cursor=main_menu_cursor,
        menu_cursor_style=main_menu_cursor_style,
        menu_highlight_style=main_menu_style,
        cycle_cursor=True,
        clear_screen=True,
    )

    manage_account_menu_title = "  Manage account Menu.\n  Press Q or Esc to back to main menu. \n"
    manage_account_menu_items = ["Subscribe to the channel", "Unsubscribe from the channel", "Back to Main Menu"]
    manage_account_menu_back = False
    manage_account_menu = TerminalMenu(
        manage_account_menu_items,
        title=manage_account_menu_title,
        menu_cursor=main_menu_cursor,
        menu_cursor_style=main_menu_cursor_style,
        menu_highlight_style=main_menu_style,
        cycle_cursor=True,
        clear_screen=True,
    )

    while not main_menu_exit:

        main_sel = main_menu.show()

        if main_sel == 0:

            available_numbers: list[str, str] | list = get_numbers(phone_numbers_path)
            accounts: list = [class_account(number) for number in available_numbers]

            for account in accounts:
                try:
                    readiness_check(account)
                except PhoneNumberBannedError as ban_error:
                    logger.error(ban_error)
                    print(ban_error)
                except Exception as error:
                    logger.error(error)
                    print(error)
            time.sleep(5)

            while not manage_accounts_menu_back:
                edit_sel = manage_accounts_menu.show()
                if edit_sel == 0:
                    print("Subscribe to the channel")

                    for account in accounts:
                        subscribe(account, username_channel, subs=True)

                    print(f"All accounts subscribe to the channel {username_channel}")
                    time.sleep(3)

                elif edit_sel == 1:
                    print("Unsubscribe from the channel")

                    for account in accounts:
                        subscribe(account, username_channel, subs=False)

                    print(f"All accounts unsubscribed from the channel {username_channel}")
                    time.sleep(3)

                elif edit_sel == 2 or edit_sel is None:
                    manage_accounts_menu_back = True
                    print("Back Selected")
            manage_accounts_menu_back = False

        elif main_sel == 1:
            manage_phone: str = input("Enter the account number you want to manage: ")
            available_numbers: list = get_numbers(phone_numbers_path)

            if manage_phone in available_numbers:
                print("Account number is available")
                account = class_account(manage_phone)
                readiness_check(account)
                time.sleep(5)

                while not manage_account_menu_back:
                    edit_sel = manage_account_menu.show()

                    if edit_sel == 0:
                        subscribe(account, username_channel, subs=True)

                    elif edit_sel == 1:
                        subscribe(account, username_channel, subs=False)

                    elif edit_sel == 2 or edit_sel is None:
                        manage_account_menu_back = True
                        print("Back Selected")

                manage_account_menu_back = False

            else:
                manage_account_menu_back = True
                print("Account number is not available.\nBack to main menu")
            time.sleep(3)

        elif main_sel == 2:
            add_numbers(phone_numbers_path)
            time.sleep(3)

        elif main_sel == 3 or main_sel is None:
            data: list[dict] = [account.__dict__ for account in accounts]
            write_json(accounts_data_json, data)
            write_xlsx(accounts_data_xlsx, data)
            main_menu_exit = True
            print("Quit Selected")


if __name__ == '__main__':
    main()
