from pyrogram import Client, filters
import json
import os
import subprocess
import time
from functools import partial

api_id = "****"
api_hash = "***************************"
bot_token = "**************************"
user_id=1234567
Database_path='data.json'
download_dir = r"D:\Telegram Leech Bot\downloads"
thumbnail_path="D:\Telegram Desktop\BHVC.jpg"

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)


def download_file(message,download_url):
    """Function to handle the /download command."""
    url = download_url
    print(f"Starting download from URL: {url}")
    
    try:
        # Send initial message about starting the download
        progress_message = message.reply_text("Starting download...")
        last_edit_time = time.time()

        # Use aria2c to download the file from the URL
        process = subprocess.Popen(
            ["aria2c", "-x", "16", "-s", "16", "--continue", "--dir", download_dir, url],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # Merge stderr into stdout to avoid buffering issues
            universal_newlines=True,  # Ensures real-time output reading
        )

        # Read live output
        while True:
            output = process.stdout.readline()
            if output == "" and process.poll() is not None:
                break  # Exit loop when process is done
            
            if output:
                print(output.strip())  # Print for debugging

                # Extract progress percentage (this depends on aria2c output format)
                if "%" in output:
                    try:
                        progress_text = " ".join(output.strip().split()[1:])  # Extract everything after the first space
                        current_time = time.time()
                        if current_time - last_edit_time >= 10:  # Check if 10 seconds have passed
                            last_edit_time = current_time  # Update last edit time
                            progress_message.edit(progress_text)
                            
                    except Exception as e:
                        print(f"Error parsing progress: {e}")

                if "D:/Telegram Leech Bot/downloads/" in output:
                    download_path=output[output.find("D:/Telegram Leech Bot/downloads/"):]
                    download_path = download_path.rstrip('\n')

        process.wait()  # Ensure process fully finishes before continuing

        # After download completes, send the path of the downloaded file
        message.reply_text(f"Download complete! File saved at: {download_path}")
        return download_path

    except Exception as e:
        print(f"Error occurred while downloading: {e}")
        message.reply_text("An error occurred while downloading the file.")

def rename_file(file_path, new_name):
    try:
        if not os.path.exists(file_path):
            print("Error: File not found.")
            return

        directory = os.path.dirname(file_path)  # Get the directory of the file
        new_path = os.path.join(directory, new_name)  # Create new file path

        os.rename(file_path, new_path)
        print(f"File renamed successfully: {file_path} ➝ {new_path}")
    except PermissionError:
        print("Error: Permission denied.")
    except Exception as e:
        print(f"Error renaming file: {e}")

def upload_progress(current, total, message):
    """Function to track upload progress and send it to the user every 5 seconds."""
    percent = (current / total) * 100
    now = time.time()

    if not hasattr(upload_progress, "last_time") or now - upload_progress.last_time >= 5:
        progress_message = f"Uploaded: {current / (1024*1024):.2f} MB / {total / (1024*1024):.2f} MB ({percent:.2f}%)"
        print(progress_message)
        try:
            message.edit(progress_message)  # Update the message with progress
        except Exception as e:
            print(f"Error updating progress: {e}")
        upload_progress.last_time = now

def upload_file(message,output_file_path):
    file_path = output_file_path
    print(file_path)

    try:
        to_be_updated_msg=message.reply_text(f"📤 Uploading `{file_path}`...")

        # ✅ This is where the upload happens

        progress_with_message = partial(upload_progress, message=to_be_updated_msg)

        message.reply_document(file_path,thumb=thumbnail_path,progress=progress_with_message,caption=os.path.basename(file_path))

        message.reply_text("✅ Upload complete!")
        print("✅ Upload complete!")
    
    except Exception as e:
        message.reply_text(f"❌ Upload failed: {e}")

def split_file(message,file_path, part_size_mb):
    """Splits a file into multiple parts with progress updates every 5 seconds."""
    if not os.path.exists(file_path):
        print("❌ Error: File not found!")
        return

    part_size = part_size_mb * 1024 * 1024  # Convert MB to Bytes
    file_size = os.path.getsize(file_path)  # Get total file size
    part_number = 1
    bytes_processed = 0
    last_update_time = time.time()
    folder = os.path.dirname(file_path)  # Get folder where file exists

    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(part_size)
            if not chunk:
                break
            part_filename = os.path.join(folder, f"{os.path.basename(file_path)}.{part_number:03d}")
            with open(part_filename, "wb") as part_file:
                part_file.write(chunk)
            
            bytes_processed += len(chunk)
            part_number += 1

            percent_done = (bytes_processed / file_size) * 100
            print(f"Splitting Progress: {percent_done:.2f}% completed...")
            message.reply_text(f"Splitting Progress: {percent_done:.2f}% completed...")
            last_update_time = time.time()  # Reset the last update time

    print("\n✅ File split successfully!")
    part_number=part_number-1
    return part_number

def upload(message,output_file_path):
    file_size = os.path.getsize(output_file_path)

    file_size_mb = file_size / (1024 * 1024)

    if file_size_mb < 2000:
        upload_file(message,output_file_path)
    else:
        message.reply_text("splitting the file")
        no_of_parts=split_file(message,output_file_path,2000)
        folder=os.path.dirname(output_file_path)
        for i in range(1,no_of_parts+1):
            part_file_path = os.path.join(folder, f"{os.path.basename(output_file_path)}.{i:03d}")
            message.reply_text(f'uploading {i}/{no_of_parts} file...')
            upload_file(message,part_file_path)
        message.reply_text("✅ All parts uploaded successfully")
        message.reply_text(f'File size :- {file_size_mb/1024}GB')

@app.on_message(filters.command("leech_url") & filters.regex(r"^/leech_url\s+(http[s]?://[^\s]+)\s+(.+)$"))
def leech_url_handler(client, message):
    if not message.from_user.id==user_id:
        message.reply_text('You are not authorised to access this bot.')
        return
    """Handles the /leech_url command with a URL and a string."""
    try:
        # Extract URL and string from message text
        parts = message.text.split(" ", 2)  # Split into 3 parts: [command, URL, string]

        if len(parts) < 3:
            message.reply_text("Invalid format! Use: `/leech_url <url> <string>`")
            return

        url = parts[1]  # Extract URL
        new_name = parts[2]  # Extract string

        download_path=download_file(message,url)

        folder_path = os.path.dirname(download_path)

        output_file_path = os.path.join(folder_path, new_name)

        message.reply_text('Renaming...')
        rename_file(download_path,output_file_path)
        message.reply_text('Renamed')

        upload(message,output_file_path)
    
    except Exception as e:
        message.reply_text(f"Error: {e}")

def save_document(client, message):
    user_id=message.from_user.id
    file_id=message.document.file_id
    file_name=message.document.file_name
    file_size=message.document.file_size

    file_size=file_size/(1024*1024)

    with open(Database_path, 'r') as f:
        data = json.load(f)

    Total_files=int(data['Total_files'])
    Total_files=Total_files+1
    data['size']+=file_size

    data['Total_files']=str(Total_files)
    data['file_ids'].update({str(Total_files):file_id})

    with open(Database_path,'w') as f:
        json.dump(data,f,indent=2)
    
    return Total_files

def send_document(client, message, id):
    with open(Database_path,'r') as f:
        data=json.load(f)

    file_id=data['file_ids'][id]

    message.reply_document(file_id)

# @app.on_message(filters.command("start"))
@app.on_message()
def start(client, message):

    # with open(Database_path,'r') as f:
    #     data=json.load(f)

    # if message.from_user.id not in data["users"]:
    #     userid=message.from_user.id
    #     username=message.from_user.username

    #     data["users"][user_id] = {
    #         "name": username,
    #         "usage": 0,
    #         "files": {}
    #     }

    #     with open(Database_path,'w') as f:
    #         json.dump(data,f,indent=2)

    # print(message)


    if message.document:
        id=save_document(client, message)
        message.reply_text(f'Your file id is : {id}')
    else:
        text=message.text.split()
        
        command=text[0]

        if command=='/start':
            message.reply_text(f'''Welcome to BHVC ultimate storage bot.
Use /help for assistance.''')
            
        elif command=='/help':
            message.reply_text(f'''Send any document and i will save it with a unique id.
Use /get to get your file with id.
Syntax is /get id
Use /size to know the total storage used.''')
            
        elif command=='/size':
            with open(Database_path,'r') as f:
                data=json.load(f)

            size=data['size']
            size=round(size/1024,2)
            message.reply_text(f'Your total size is : {size}GB')
            
        elif command=='/get':
            req_id=text[1]

            send_document(client, message, req_id)



    

app.run()
