# 🖥️ AnyDesk Monitor & Notifier

<img src="logo.png">

### This Python script monitors the connection status of the AnyDesk remote desktop application. It notifies a Rocket.Chat room when the AnyDesk service starts, restarts, or changes its address.

## 📋 Features

- 🔐 Authenticates with Rocket.Chat API
- 📡 Checks if AnyDesk is online using command-line
- 🔁 Automatically restarts the AnyDesk service if offline
- 🧠 Tracks and sends the current AnyDesk address (ID) and public IP
- 📢 Notifies a predefined Rocket.Chat room with status updates
- ⏱️ Runs in a continuous loop and reports on changes in real-time

## 🚀 How It Works

- Logs in to Rocket.Chat using provided credentials
- Sends a starting message with timestamp
- Periodically checks if AnyDesk is connected
- If connected and AnyDesk ID changes, sends the new ID and public IP
- If not connected, restarts AnyDesk service
- All messages are sent to a specific Rocket.Chat room


## 🧰 Requirements

- Python 3.7+
- requests library
- AnyDesk installed on the machine
- systemctl (Linux system service manager)
- Access to Rocket.Chat server with API enabled


