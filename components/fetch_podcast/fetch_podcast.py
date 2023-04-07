
import os
import requests
from typing import Optional
import yaml
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

from core.abstract_component import AbstractComponent


class PodcastUrlInputDict(BaseModel):
    podcast_url: str


class PodcastAudioFileOutputDict(BaseModel):
    podcast_audio_file: bytes


class FetchPodcast(AbstractComponent):
    def __init__(self) -> None:
        super().__init__()

    def transform(
        self, args: PodcastUrlInputDict
    ) -> PodcastAudioFileOutputDict:
        listen_notes_api_url = "https://listen-api.listennotes.com/api/v2/get_podcast"
        headers = {"X-ListenAPI-Key": os.environ.get("LISTEN_NOTES_API_KEY")}

        response = requests.get(
            listen_notes_api_url, headers=headers, params={"url": args.podcast_url}
        )
        response.raise_for_status()

        podcast_data = response.json()
        audio_file_url = podcast_data["audio"]

        audio_file_response = requests.get(audio_file_url)
        audio_file_response.raise_for_status()

        podcast_audio_file = audio_file_response.content

        return PodcastAudioFileOutputDict(podcast_audio_file=podcast_audio_file)


load_dotenv()
fetch_podcast_app = FastAPI()


@fetch_podcast_app.post("/transform/")
async def transform(
    args: PodcastUrlInputDict,
) -> PodcastAudioFileOutputDict:
    fetch_podcast = FetchPodcast()
    return fetch_podcast.transform(args)
