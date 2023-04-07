
import os
from typing import Optional
import yaml
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

from core.abstract_component import AbstractComponent


class SaveOutputsInputDict(BaseModel):
    PodcastTranscript: str
    PodcastSummary: str
    PodcastSummaryAudio: bytes


class TranscriptSummaryAudioResponse(BaseModel):
    transcript_file_path: str
    summary_file_path: str
    summary_audio_file_path: str


class SaveOutputs(AbstractComponent):
    def __init__(self) -> None:
        super().__init__()
        with open(self.component_configuration_path(), "r", encoding="utf-8") as file:
            yaml_data = yaml.safe_load(file)
        self.output_directory: str = yaml_data["parameters"]["output_directory"]
        self.transcript_filename: str = yaml_data["parameters"]["transcript_filename"]
        self.summary_filename: str = yaml_data["parameters"]["summary_filename"]
        self.summary_audio_filename: str = yaml_data["parameters"]["summary_audio_filename"]

    def transform(
        self, args: SaveOutputsInputDict
    ) -> TranscriptSummaryAudioResponse:
        os.makedirs(self.output_directory, exist_ok=True)

        transcript_file_path = os.path.join(self.output_directory, self.transcript_filename)
        with open(transcript_file_path, "w") as f:
            f.write(args.PodcastTranscript)

        summary_file_path = os.path.join(self.output_directory, self.summary_filename)
        with open(summary_file_path, "w") as f:
            f.write(args.PodcastSummary)

        summary_audio_file_path = os.path.join(self.output_directory, self.summary_audio_filename)
        with open(summary_audio_file_path, "wb") as f:
            f.write(args.PodcastSummaryAudio)

        output = TranscriptSummaryAudioResponse(
            transcript_file_path=transcript_file_path,
            summary_file_path=summary_file_path,
            summary_audio_file_path=summary_audio_file_path,
        )
        return output


load_dotenv()
save_outputs_app = FastAPI()


@save_outputs_app.post("/transform/")
async def transform(
    args: SaveOutputsInputDict,
) -> TranscriptSummaryAudioResponse:
    save_outputs = SaveOutputs()
    return save_outputs.transform(args)
