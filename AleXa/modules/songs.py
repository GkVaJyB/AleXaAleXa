import os

import aiohttp
from pyrogram import filters
from pytube import YouTube
import requests
from youtubesearchpython import VideosSearch

from AleXa import LOGGER, pbot
from AleXa.utils.uut import get_arg


def yt_search(song):
    videosSearch = VideosSearch(song, limit=1)
    result = videosSearch.result()
    if not result:
        return False
    else:
        video_id = result["result"][0]["id"]
        url = f"https://youtu.be/{video_id}"
        return url


class AioHttp:
    @staticmethod
    async def get_json(link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.json()

    @staticmethod
    async def get_text(link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.text()

    @staticmethod
    async def get_raw(link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.read()


@pbot.on_message(filters.command("song"))
async def song(client, message):
    message.chat.id
    user_id = message.from_user["id"]
    args = get_arg(message) + " " + "song"
    if args.startswith(" "):
        await message.reply("Enter a song name. Check /help")
        return ""
    status = await message.reply("**Downloading Song** 😊")
    video_link = yt_search(args)
    if not video_link:
        await status.edit("**Song not found.** 🤔")
        return ""
    yt = YouTube(video_link)
    audio = yt.streams.filter(only_audio=True).first()
    try:
    response = download(f'https://img.youtube.com/vi/{video_id}/0.jpg')
    DIRCOVER =  message.message_id + ".jpg"
    file = open(DIRCOVER, "wb")
    file.write(response.content)
    file.close()
        thumb_name = f'{message.message_id}.jpg'
        download = audio.download(filename=f"{str(yt.title)}")
    except Exception as ex:
        await status.edit("Failed to download song")
        LOGGER.error(ex)
        return ""
    os.rename(download, f"{str(yt.title)}.mp3")
    await pbot.send_chat_action(message.chat.id, "upload_audio")
    await pbot.send_audio(
        chat_id=message.chat.id,
        audio=f"{str(yt.title)}.mp3",
        duration=int(yt.length),
        title=str(yt.title),
        performer=str(yt.author),
        thumb=thumb_name,
        reply_to_message_id=message.message_id,
       )
    await status.delete()
    os.remove(f"{str(yt.title)}.mp3")


__help__ = """
 *You can either enter just the song name or both the artist and song
  name. *
  /song <songname artist(optional)>*:* uploads the song in it's best quality available
  /video <songname artist(optional)>*:* uploads the video song in it's best quality available
  /lyrics <song>*:* returns the lyrics of that song.
"""

__mod_name__ = "Music"