
import os

import yaml
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
import requests

from core.abstract_component import AbstractComponent


class GenerateAudioInputDict(BaseModel):
    PodcastSummary: str


class GenerateAudioOutputDict(BaseModel):
    PodcastSummaryAudio: bytes


class GenerateAudio(AbstractComponent):
    def __init__(self) -> None:
        super().__init__()

    def transform(
        self, args: GenerateAudioInputDict
    ) -> GenerateAudioOutputDict:
        print(f"Executing the transform of the {type(self).__name__} component...")

        # Connect to the Eleven Labs API
        eleven_labs_url = "https://api.eleven-labs.com/generate-audio"
        data = {"text": args.PodcastSummary}
        headers = {"Content-Type": "application/json"}

        # Make a request to Eleven Labs API sending the PodcastSummary as input
        response = requests.post(eleven_labs_url, json=data, headers=headers)

        if response.status_code == 200:
            # Receive the mp3 audio file data from the Eleven Labs API
            audio_data = response.content

            # Return the mp3 audio data as PodcastSummaryAudio output
            return GenerateAudioOutputDict(PodcastSummaryAudio=audio_data)
        else:
            raise ValueError("Error while generating audio. Please check the input and try again.")


load_dotenv()
generate_audio_app = FastAPI()


@generate_audio_app.post("/transform/")
async def transform(
    args: GenerateAudioInputDict,
) -> GenerateAudioOutputDict:
    generate_audio = GenerateAudio()
    return generate_audio.transform(args)

