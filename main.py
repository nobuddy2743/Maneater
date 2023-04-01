from pyrogram import Client, filters
from techzapi.api import TechZApi
import time

# TechZApi API Key
TECHZAPI_API_KEY = "SNMYTI"

# Telegram Bot Credentials
API_ID = YOUR_API_ID_HERE
API_HASH = 'YOUR_API_HASH_HERE'
BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE'

app = Client(
    "TechZBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

scrapper = TechZApi.MkvCinemas(TECHZAPI_API_KEY)

@ app.on_message(filters.private)
def start_message(client, message):
    client.send_message(
        message.chat.id,
        "Enter url of any movie or series: "
    )

    @ app.on_message(filters.private)
    def receive_url(client, message):
        url = message.text.strip()
        max = 3  # Max no. of links to scrap

        client.send_message(
            message.chat.id,
            "Adding task to queue..."
        )

        data = scrapper.add_task(url, max)
        queue = data["queue"]
        hash = data["hash"]

        client.send_message(
            message.chat.id,
            f"Added task to queue, Queue Position : {queue}"
        )

        while True:
            time.sleep(15)
            status_message = "Checking queue".center(50, "=")
            client.send_message(message.chat.id, status_message)

            data = scrapper.get_task(hash)

            if data["status"] == "pending":
                status = f'Status: Pending || Queue Position : {data["queue"]}'.center(50)
                client.send_message(message.chat.id, status)
                continue

            if data["status"] == "processing":
                status = f'Status : Processing || Links Scrapped : {data["scrapped"]}'.center(50)
                client.send_message(message.chat.id, status)
                continue

            if data["status"] == "completed":
                client.send_message(
                    message.chat.id,
                    "Task completed...\nLinks: {}".format(data["results"])
                )
                break

            if data["status"] == "failed":
                client.send_message(message.chat.id, "Task failed...")
                break

app.run()
