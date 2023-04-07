
import os
import pytest
from dotenv import load_dotenv
from pydantic import BaseModel
from core.abstract_component import AbstractComponent

from your_path_to_generate_summary import GenerateSummary, GenerateSummaryInputDict, GenerateSummaryOutputDict

# Mocked input and expected output data
test_data = [
    (
        GenerateSummaryInputDict(PodcastTranscript="Transcript 1"),
        GenerateSummaryOutputDict(PodcastSummary="Summary 1")
    ),
    (
        GenerateSummaryInputDict(PodcastTranscript="Transcript 2"),
        GenerateSummaryOutputDict(PodcastSummary="Summary 2")
    ),
    (
        GenerateSummaryInputDict(PodcastTranscript="Transcript 3"),
        GenerateSummaryOutputDict(PodcastSummary="Summary 3")
    )
]

# Mocked error handling and edge case scenarios
edge_cases = [
    (GenerateSummaryInputDict(PodcastTranscript=""),GenerateSummaryOutputDict(PodcastSummary=""))
]

@pytest.mark.parametrize('input_data, expected_output', test_data)
def test_transform(input_data: GenerateSummaryInputDict, expected_output: GenerateSummaryOutputDict):

    load_dotenv()
    generate_summary = GenerateSummary()

    # Mock the API calls
    API_KEY = os.getenv("OPENAI_API_KEY")
    generate_summary.openai_api_key = API_KEY

    result = generate_summary.transform(input_data)

    assert result == expected_output

@pytest.mark.parametrize('input_data, expected_output', edge_cases)
def test_edge_cases(input_data: GenerateSummaryInputDict, expected_output: GenerateSummaryOutputDict):

    load_dotenv()
    generate_summary = GenerateSummary()

    # Mock the API calls
    API_KEY = os.getenv("OPENAI_API_KEY")
    generate_summary.openai_api_key = API_KEY

    result = generate_summary.transform(input_data)

    assert result == expected_output
