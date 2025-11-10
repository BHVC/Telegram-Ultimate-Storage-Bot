🧠 BHVC Ultimate Storage Telegram Bot

A powerful Telegram Drive + URL Leech Bot built using Python and Pyrogram, that lets you:

Download files from direct URLs (using aria2c)

Automatically split large files before uploading

Upload files to Telegram with live progress

Store uploaded files in a local JSON database

Retrieve files anytime using unique file IDs

Track total storage size usage

🚀 Features

✅ URL Leeching — Download files directly from any HTTP/HTTPS link
✅ File Renaming — Automatically rename files before uploading
✅ Auto Splitting — Large files (>2 GB) are split into multiple parts
✅ Upload Progress — Real-time progress updates while uploading
✅ Persistent Storage — File metadata is stored in data.json
✅ Retrieve by ID — Get your stored files instantly using /get <id>
✅ Size Tracking — View total storage used with /size
✅ Admin-only Leech Access — Restrict /leech_url command to authorized users

🧩 Project Structure
Telegram-Leech-Bot/
│
├── main.py               # Main bot script (Pyrogram)
├── data.json             # JSON database to store file info
├── downloads/            # Folder where files are downloaded
└── README.md             # This file

⚙️ Requirements

Python 3.10+

Telegram API credentials

Installed aria2
 command-line downloader

🛠️ Installation
1️⃣ Clone the repository
git clone https://github.com/BHVC/Telegram-Ultimate-Storage-Bot
cd telegram-drive-bot

2️⃣ Install dependencies
pip install pyrogram tgcrypto

3️⃣ Install aria2

Windows:
Download from aria2 releases
 and add it to PATH.

Linux/macOS:

sudo apt install aria2

4️⃣ Create data.json

Before starting the bot, create an empty data.json file:

{
  "Total_files": "0",
  "size": 0,
  "file_ids": {}
}

5️⃣ Set your credentials in main.py

Edit the top of the file:

api_id = "YOUR_API_ID"
api_hash = "YOUR_API_HASH"
bot_token = "YOUR_BOT_TOKEN"
user_id = 123456789     # your Telegram user ID
download_dir = "D:\\Telegram Leech Bot\\downloads"
thumbnail_path = "D:\\Telegram Desktop\\thumbnail.jpg"

▶️ Running the Bot
python main.py


Once it starts, you should see:

Pyrogram: started...


Now open Telegram and chat with your bot!

💬 Available Commands
Command	Description
/start	Welcome message
/help	Show usage instructions
/size	Show total storage used
/get <id>	Retrieve a file by its unique ID
/leech_url <url> <filename>	(Admin only) Download a file from a URL, rename it, and upload it
📦 File Storage Logic

All uploaded documents are recorded in data.json with:

A unique incremental ID

File name and size

File ID (for quick Telegram retrieval)

Example:

{
  "Total_files": "3",
  "size": 45.76,
  "file_ids": {
    "1": "BQACAgUAAx0...",
    "2": "BQACAgUAAx1...",
    "3": "BQACAgUAAx2..."
  }
}

🧰 Functions Overview
Function	Description
download_file()	Downloads a file using aria2c with live progress updates
rename_file()	Renames downloaded files
upload_file()	Uploads a file to Telegram with progress tracking
split_file()	Splits large files (>2 GB) into 2 GB parts
upload()	Handles split logic + upload
save_document()	Saves Telegram document info to JSON
send_document()	Sends stored file by ID
leech_url_handler()	Handles /leech_url command
start()	Handles messages and user commands


🧾 Example Usage

1️⃣ Send a document
→ Bot replies with a file ID:

Your file id is: 3


2️⃣ Retrieve the same file later

/get 3


3️⃣ Check total used space

/size


4️⃣ Admin command to leech and upload

/leech_url https://example.com/file.zip myfile.zip

💡 To-Do / Future Improvements

✅ Multi-user storage tracking

✅ Command to list all files

🕒 Optional auto-cleanup system

🧠 Integration with MongoDB for scalable storage

💾 Async upload/download optimization

🧑‍💻 Author

👤 BHVC (Harsha Vardhan Chowdary Borra)
Telegram Automation Enthusiast | Python Developer
