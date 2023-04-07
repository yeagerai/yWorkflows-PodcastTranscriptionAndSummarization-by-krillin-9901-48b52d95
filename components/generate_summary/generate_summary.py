
import os

import openai
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

from core.abstract_component import AbstractComponent


class GenerateSummaryInputDict(BaseModel):
    PodcastTranscript: str


class GenerateSummaryOutputDict(BaseModel):
    PodcastSummary: str


class GenerateSummary(AbstractComponent):
    def __init__(self) -> None:
        super().__init__()
        self.openai_api_key: Optional[str] = os.environ.get("OPENAI_API_KEY")

    def transform(
        self, args: GenerateSummaryInputDict
    ) -> GenerateSummaryOutputDict:
        openai.api_key = self.openai_api_key
        print(f"Executing the transform of the {type(self).__name__} component...")

        prompt = f"Please summarize the following podcast transcript:\n\n{args.PodcastTranscript}"

        completion = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.5
        )

        response = completion.choices[0].text.strip()

        out = GenerateSummaryOutputDict(
            PodcastSummary=response
        )
        
        return out


load_dotenv()
generate_summary_app = FastAPI()


@generate_summary_app.post("/transform/")
async def transform(
    args: GenerateSummaryInputDict,
) -> GenerateSummaryOutputDict:
    generate_summary = GenerateSummary()
    return generate_summary.transform(args)
