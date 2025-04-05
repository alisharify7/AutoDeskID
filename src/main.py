"""
🚀 AutoDeskID
Author: github.com/alisharify7
License: GPL-3.0 (2024)
Contact: alisharifyofficial@gmail.com
Repository: https://github.com/alisharify7/AutoDeskID

This script monitors the status of AnyDesk, checks its connection, and sends messages to a Rocket.Chat room.
If AnyDesk is disconnected, it attempts to restart the service and logs relevant information.
"""

import time
import subprocess
import datetime
import logging
import typing
import requests
import config

# Global variable to store AnyDesk address
address = ""


def get_my_public_ip_address() -> str:
    """Retrieve the public IP address of the current machine."""
    return requests.get("https://icanhazip.com/").text.strip()


def rocket_chat_login(username: str, password: str) -> typing.Tuple[str, str]:
    """Authenticate with Rocket.Chat and return the auth token and user ID."""
    url = f"{config.ROCKET_CHAT_URL}/api/v1/login"
    data = {"user": username, "password": password}

    response = requests.post(url, json=data)
    if response.status_code == 200 and response.json().get("status") == "success":
        auth_data = response.json()["data"]
        return auth_data["authToken"], auth_data["userId"]

    raise Exception("❌ Login to Rocket.Chat failed!")


def send_message_to_room(message: str):
    """Send a message to a predefined Rocket.Chat room."""
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
            logging.info(f"✅ Message sent successfully to {config.ROCKET_CHAT_ROOM_NAME}!")
        else:
            logging.warning(f"❌ Failed to send message! Error: {response.json()}")
    except Exception as e:
        logging.warning(f"❌ Error sending message: {e}")


def is_anydesk_connected() -> bool:
    """Check if AnyDesk is online and connected to the server."""
    try:
        output = subprocess.check_output("anydesk --get-status", shell=True, text=True).strip()
        return "online" in output.lower()
    except subprocess.CalledProcessError:
        return False


def reboot_anydesk_service() -> bool:
    """Restart, enable, and start the AnyDesk service using systemctl."""
    try:
        subprocess.check_output("systemctl restart anydesk && systemctl start anydesk && systemctl enable anydesk", shell=True, text=True)
        return True
    except subprocess.CalledProcessError:
        return False


def get_anydesk_address() -> str:
    """Retrieve the AnyDesk address (ID) of the current machine."""
    try:
        return subprocess.check_output("anydesk --get-id", shell=True, text=True).strip()
    except subprocess.CalledProcessError as e:
        return f"AnyDesk Address Not Found: {e}"


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    logging.info("🔍 Checking AnyDesk connection status...")

    send_message_to_room("*" * 50)
    send_message_to_room(f"{'*' * 25} Starting {'*' * 25}")
    send_message_to_room(f"\t\t{datetime.datetime.now()}\t\t")
    send_message_to_room("🔍 Checking AnyDesk state status...")

    while True:
        anydesk_connected_status = is_anydesk_connected()
        if anydesk_connected_status:
            anydesk_address = get_anydesk_address()
            if not anydesk_address.isdigit():
                send_message_to_room(
                    f"❌ Error: {anydesk_address}\n✅ Last known AnyDesk address: {address}\n✅ Public IP: {get_my_public_ip_address()}"
                )
                continue

            if address != anydesk_address:
                send_message_to_room(
                    f"✅ Device Public IP: {get_my_public_ip_address()}\n✅ AnyDesk is running\n✅ AnyDesk Address: {anydesk_address}"
                )
                send_message_to_room(f"{'*' * 25} Ending {'*' * 25}")
                send_message_to_room("*" * 50)
                address = anydesk_address

            logging.info(f"✅ AnyDesk is connected! Address: {address}")
            time.sleep(5)
        else:
            reboot_anydesk_service()
            logging.warning(
                f"❌ AnyDesk not connected. Retrying in 5 seconds. Last known address: {address}"
            )
            time.sleep(5)
