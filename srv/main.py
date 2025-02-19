"""
 * 🚀 AutoDeskID
 * author: github.com/alisharify7
 * Copyright 2024.  GPL-3.0 license
 * email: alisharifyofficial@gmail.com
 * https://github.com/alisharify7/AutoDeskID
"""

import time
import subprocess
import datetime
import logging
import typing

import requests
import config

global address
address = ""


def get_my_public_ip_address():
    """getting current user public ip address from <https://icanhazip.com/>"""
    return requests.get("https://icanhazip.com/").text.strip()

def rocket_chat_login(username: str, password: str) -> typing.Union[Exception, tuple]:
    """login to rocket chat,"""
    url = f"{config.ROCKET_CHAT_URL}/api/v1/login"
    data = {"user": username, "password": password}

    response = requests.post(url, json=data)
    if response.status_code == 200 and response.json().get("status") == "success":
        auth_data = response.json()["data"]
        return auth_data["authToken"], auth_data["userId"]
    else:
        raise Exception("❌ Login failed!")


def send_message_to_room(message):
    """send message to rocket chat room"""
    try:
        auth_token, user_id = rocket_chat_login(config.ROCKET_CHAT_USERNAME, config.ROCKET_CHAT_PASSWORD)

        url_get_room = f"{config.ROCKET_CHAT_URL}/api/v1/rooms.info?roomName={config.ROCKET_CHAT_ROOM_NAME}"
        headers = {"X-Auth-Token": auth_token, "X-User-Id": user_id}

        response = requests.get(url_get_room, headers=headers)
        if response.status_code == 200:
            room_id = response.json().get("room", {}).get("_id")
        else:
            raise Exception("❌ Room not found!")

        url_send_message = f"{config.ROCKET_CHAT_URL}/api/v1/chat.postMessage"
        payload = {"roomId": room_id, "text": message}
        response = requests.post(url_send_message, json=payload, headers=headers)

        if response.status_code == 200:
            logging.warning(f"✅ Message sent successfully to {config.ROCKET_CHAT_ROOM_NAME}!")
        else:
            logging.warning(f"❌ Failed to send message to  {config.ROCKET_CHAT_ROOM_NAME}!\nerror:{response.json()}")

    except Exception as e:
        logging.warning(e)


def is_anydesk_connected():
    """check Anydesk in online and connected to server"""
    try:
        output = subprocess.check_output(
            "anydesk --get-status", shell=True, text=True
        ).strip()
        return "online" in output.lower()
    except subprocess.CalledProcessError:
        return False


def reboot_anydesk_service():
    """restart/enable/start anydesk service using systemctl"""
    try:
        output = subprocess.check_output(
            "systemctl restart anydesk && systemctl start anydesk && systemctl enable anydesk", shell=True, text=True
        ).strip()
        return True
    except subprocess.CalledProcessError:
        return False


def get_anydesk_address():
    """get anydesk address id"""
    try:
        output = subprocess.check_output(
            "anydesk --get-id", shell=True, text=True
        ).strip()
        return output
    except subprocess.CalledProcessError as e:
        return f"AnyDesk Address Not Found, {e.output} {e.stdout} {e.stderr}"


if __name__ == "__main__":
    logging.warning("🔍 Checking AnyDesk connection status...")
    send_message_to_room(f"*" * 50)
    send_message_to_room(f"*" * 25 + f" starting " + "*" * 25)
    send_message_to_room(f"\t\t{datetime.datetime.now()}\t\t")

    send_message_to_room(f"🔍 Checking AnyDesk state status...")


    while True:
        if (anydesk_connected_status := is_anydesk_connected()):
            anydesk_address = str(get_anydesk_address())
            if not anydesk_address.isdigit():
                send_message_to_room(
                    f"❌ error: {anydesk_address}\n✅ last anydesk address: {address}\n✅ public ip address: {get_my_public_ip_address()}")
                continue
            if address != anydesk_address:
                send_message_to_room(
                    f"✅ device public ip address : {get_my_public_ip_address()}\n✅ anydesk is up and running\n✅ anydesk address: {anydesk_address}")
                send_message_to_room(f"*" * 25 + f" ending " + "*" * 25)
                send_message_to_room(f"*" * 50)


            address = anydesk_address
            logging.warning(f"✅ AnyDesk is connected! Address: {address}")
            time.sleep(5)

        else:
            reboot_anydesk_service()
            logging.warning(
                "❌ AnyDesk is not connected yet... Retrying in 5 seconds." + f" status: {anydesk_connected_status}, last anydesk address: {address}")
            logging.warning("⏳ AnyDesk is not connected yet... Retrying in 5 seconds.")
            time.sleep(5)

