
import typing
from typing import Optional
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

from core.workflows.abstract_workflow import AbstractWorkflow


class PodcastUrl(BaseModel):
    podcast_url: str

class TranscriptSummaryAudioResponse(BaseModel):
    transcript_path: str
    summary_path: str
    summary_audio_path: str


class PodcastTranscriptionAndSummarization(AbstractWorkflow):
    def __init__(self) -> None:
        super().__init__()

    async def transform(
        self, args: PodcastUrl, callbacks: typing.Any
    ) -> TranscriptSummaryAudioResponse:
        results_dict = await super().transform(args=args, callbacks=callbacks)
        transcript_path = results_dict["transcript"].transcript_path
        summary_path = results_dict["summary"].summary_path
        summary_audio_path = results_dict["summary_audio"].summary_audio_path
        out = TranscriptSummaryAudioResponse(
            transcript_path=transcript_path,
            summary_path=summary_path,
            summary_audio_path=summary_audio_path,
        )
        return out

load_dotenv()
podcast_transcription_and_summarization_app = FastAPI()


@podcast_transcription_and_summarization_app.post("/transform/")
async def transform(
    args: PodcastUrl,
) -> TranscriptSummaryAudioResponse:
    podcast_transcription_and_summarization = PodcastTranscriptionAndSummarization()
    return await podcast_transcription_and_summarization.transform(args, callbacks=None)
