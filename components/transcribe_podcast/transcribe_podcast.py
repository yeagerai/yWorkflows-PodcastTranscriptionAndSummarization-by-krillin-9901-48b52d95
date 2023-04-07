
import os
from typing import Any, Dict

import yaml
from dotenv import load_dotenv
from fastapi import FastAPI, File
from pydantic import BaseModel
import requests

from core.abstract_component import AbstractComponent


class TranscribePodcastInputDict(BaseModel):
    PodcastAudioFile: Any


class TranscribePodcastOutputDict(BaseModel):
    PodcastTranscript: str


class TranscribePodcast(AbstractComponent):
    def __init__(self) -> None:
        super().__init__()
        with open(self.component_configuration_path(), "r", encoding="utf-8") as file:
            yaml_data = yaml.safe_load(file)
        self.api_key: str = os.environ.get(yaml_data["parameters"]["api_key"])
        self.language_code: str = yaml_data["parameters"]["language_code"]

    def transform(
        self, args: TranscribePodcastInputDict
    ) -> TranscribePodcastOutputDict:
        print(f"Executing the transform of the {type(self).__name__} component...")

        # Initialize the Whisper ASR API with the provided API key
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "audio/wav",
            "language": self.language_code,
        }

        # Send the audio file to the Whisper ASR API for transcription
        response = requests.post(
            "https://api.whisper.asr.example.com/v1/asr",
            headers=headers,
            data=args.PodcastAudioFile,
        )

        # Receive the transcription result from the API
        response_json = response.json()
        transcript = response_json["transcript"]

        # Return the transcribed text as PodcastTranscript
        return TranscribePodcastOutputDict(PodcastTranscript=transcript)


load_dotenv()
transcribe_podcast_app = FastAPI()


@transcribe_podcast_app.post("/transform/")
async def transform(
    args: Dict[str, Any],
) -> TranscribePodcastOutputDict:
    audio_file = args["PodcastAudioFile"].file.read()
    transcribe_podcast = TranscribePodcast()
    return transcribe_podcast.transform(TranscribePodcastInputDict(PodcastAudioFile=audio_file))

