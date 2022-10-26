from math import floor
import os
from main import queue
import cv2
import random
from string import ascii_letters, ascii_uppercase, digits
from pyrogram.types import Message, MessageEntity


def get_duration(file):
    data = cv2.VideoCapture(file)

    frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = int(data.get(cv2.CAP_PROP_FPS))
    return int(frames / fps)


def get_screenshot(file):
    cap = cv2.VideoCapture(file)
    name = "./" + \
        "".join(random.choices(ascii_uppercase + digits, k=10)) + ".jpg"

    total_frames = round(cap.get(cv2.CAP_PROP_FRAME_COUNT))-1
    frame_num = random.randint(0, total_frames)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num-1)
    res, frame = cap.read()

    cv2.imwrite(name, frame)
    cap.release()
    # cv2.destroyAllWindows()
    return name


def get_filesize(file):
    x = os.path.getsize(file)
    x = round(x/(1024*1024))
    x = f"{str(round(x / 1024, 2))} GB" if x > 1024 else f"{str(x)} MB"
    return x


def get_epnum(name):
    x = name.split(" - ")[-1].strip()
    x = x.split(" ")[0]
    x = x.strip()
    return x


def format_time(time):
    min = floor(time/60)
    sec = round(time-(min*60))

    time = f"{str(min)}:{str(sec)}"
    return time


def format_text(text):
    ftext = "".join(
        x if x in ascii_letters or x == " " or x in digits else " "
        for x in text
    )

    while "  " in ftext:
        ftext = ftext.replace("  ", " ")
    return ftext


def episode_linker(f, en, text, link):
    ent = en
    off = len(f) + 2
    length = len(text)
    new = MessageEntity(type="text_link", offset=off, length=length, url=link)
    ent.append(new)
    return ent


def tags_generator(title):
    x = "#" + title.replace(" ", "_")

    while x[-1] == "_":
        x = x[:-1]
    return x


async def status_text(text):
    stat = """
⭐️ **Status :** {}

⏳ **Queue :** 

{}
"""

    queue_text = "".join(
        "📌 "
        + i["title"].replace(".mkv", "").replace(".mp4", "").strip()
        + "\n"
        for i in queue
    )

    if not queue_text:
        queue_text = "❌ Empty"

    return stat.format(
        text,
        queue_text
    )


def download_progress(filename, current, total, total_size, downloaded):
    text = """Name: {}
Downloading: {}%
⟨⟨{}⟩⟩
{} of {}
Speed: {}
ETA: {}
    """

    percent = floor((current/total)*100)

    fill = "▪️"
    blank = "▫️"
    bar = fill*floor(percent/10)
    bar += blank*(int(((20-len(bar))/2)))

    size_downloaded = (percent/100)*total_size
    a = size_downloaded
    b = total_size
    size_downloaded = round(size_downloaded/(1024*1024), 2)  # in MB
    total_size = round(total_size/(1024*1024), 2)  # in MB

    if size_downloaded < 1024:
        dtext1 = f'{str(size_downloaded)} MB'
    else:
        x = round(size_downloaded/1024, 2)  # in GB
        dtext1 = f'{str(x)} GB'

    if total_size < 1024:
        dtext2 = f'{str(total_size)} MB'
    else:
        total_size = round(total_size/1024, 2)  # in GB
        dtext2 = f'{str(total_size)} GB'

    speed = round((a-downloaded)/(10*1024), 2)
    if speed < 1024:
        stext = f'{str(speed)} Kbps'
    else:
        x = round(speed/1024, 2)
        stext = f'{str(x)} Mbps'

    remaining = (b - a)/1024  # in kb
    time_remaining = floor(remaining/speed)  # in seconds

    if time_remaining < 60:
        ttext = f'{str(time_remaining)} seconds'
    elif time_remaining < 3600:
        x = floor(time_remaining/60)
        y = time_remaining-(x*60)
        ttext = f'{str(x)} minute {str(y)} seconds'
    else:
        x = floor(time_remaining/3600)
        y = time_remaining-(x*3600)
        ttext = f'{str(x)} hour {str(y)} minutes'

    text = text.format(
        filename,
        percent,
        bar,
        dtext1,
        dtext2,
        stext,
        ttext
    )
    return text, size_downloaded*1024*1024

def get_progress_text(name, status, completed, speed, total):
    text = """Name: {}
{}: {}%
⟨⟨{}⟩⟩
{} of {}
Speed: {}
ETA: {}
    """

    total = str(total)
    completed = round(completed*100, 2)
    size, forma = total.split(' ')
    if forma == "MiB":
        size = int(round(float(size)))
    elif forma == "GiB":
        size = int(round(float(size)*1024, 2))
    percent = completed
    speed = round(float(speed)/1024)  # kbps
    if speed == 0:
        speed = 0.1
    ETA = round((size - ((percent/100)*size))/(speed/1024))
    if ETA > 60:
        x = floor(ETA/60)
        y = ETA-(x*60)
        if x > 60:
            z = floor(x/60)
            x = x-(z*60)
            ETA = f"{str(z)} Hour {str(x)} Minute"
        else:
            ETA = f"{str(x)} Minute {str(y)} Second"
    else:
        ETA = f"{str(ETA)} Second"
    if speed > 1024:
        speed = f"{str(round(speed / 1024))} MB"
    else:
        speed = f"{str(speed)} KB"
    completed = round((percent/100)*size)
    if completed > 1024:
        completed = f"{str(round(completed / 1024, 2))} GB"
    else:
        completed = str(completed) + " MB"
    size = str(round(size/1024, 2)) + " GB" if size > 1024 else str(size) + " MB"
    fill = "▪️"
    blank = "▫️"
    bar = ""
    bar += round(percent/10)*fill
    bar += round(((20 - len(bar))/2))*blank
    speed += "/sec"
    text = text.format(
        name,
        status,
        percent,
        bar,
        completed,
        size,
        speed,
        ETA
    )
    return text
