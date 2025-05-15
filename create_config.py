#!/usr/bin/env python3
import argparse


def create_config(bot_token, imgur_token, white_list_chats="", white_list_users=""):
    config_content = f"""# Telegram Bot
BOT_TOKEN={bot_token}

# Imgur API
API_TOKEN={imgur_token}

# WhiteList Telegram
WHITE_LIST_CHATS={white_list_chats}
WHITE_LIST_USERS={white_list_users}
"""

    with open("config.env", "w") as f:
        f.write(config_content)

    print("Файл config.env успешно создан!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Создание config.env для бота')
    parser.add_argument('api_bot', help='Telegram Bot Token')
    parser.add_argument('api_imgur', help='Imgur API Token')
    parser.add_argument('--chats', help='WHITE_LIST_CHATS (через запятую)', default="")
    parser.add_argument('--users', help='WHITE_LIST_USERS (через запятую)', default="")

    args = parser.parse_args()

    create_config(
        bot_token=args.api_bot,
        imgur_token=args.api_imgur,
        white_list_chats=args.chats,
        white_list_users=args.users
    )