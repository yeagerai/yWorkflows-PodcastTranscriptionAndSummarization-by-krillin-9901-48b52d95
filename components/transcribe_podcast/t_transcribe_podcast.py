
# test_transcribe_podcast.py

import os
import pytest
from pydantic import ValidationError
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from core.transcribe_podcast import (
    TranscribePodcast,
    TranscribePodcastInputDict,
    TranscribePodcastOutputDict,
)

# Import the FastAPI app from the source code file
from core.transcribe_podcast import transcribe_podcast_app

# Create a TestClient to properly test the FastAPI app
client = TestClient(transcribe_podcast_app)


@pytest.mark.parametrize(
    "input_dict, expected_output",
    [
        (
            {"PodcastAudioFile": b"Mocked audio file content"},
            {"PodcastTranscript": "This is a mocked transcript"},
        ),
        (
            {"PodcastAudioFile": b"Another mocked audio file content"},
            {"PodcastTranscript": "This is another mocked transcript"},
        ),
    ],
)
def test_transcribe_podcast_transform(input_dict, expected_output):
    with patch("requests.post") as mocked_post:
        # Set up the mocked response from the Whisper ASR API
        mocked_response = MagicMock()
        mocked_response.json.return_value = expected_output
        mocked_post.return_value = mocked_response

        # Create a TranscribePodcast instance and call the transform method
        transcribe_podcast = TranscribePodcast()
        input_data = TranscribePodcastInputDict(**input_dict)
        output = transcribe_podcast.transform(input_data)

        # Assert that the output matches the expected_output
        assert output.dict() == expected_output

        # Check that the Whisper ASR API is called with the correct headers and data
        headers = {
            "Authorization": f"Bearer {os.environ.get('API_KEY')}",
            "Content-Type": "audio/wav",
            "language": "en-US",
        }
        mocked_post.assert_called_with(
            "https://api.whisper.asr.example.com/v1/asr",
            headers=headers,
            data=input_dict["PodcastAudioFile"],
        )


def test_invalid_podcast_audio_file():
    # Test a scenario where the PodcastAudioFile is not provided or is None
    with pytest.raises(ValidationError):
        TranscribePodcastInputDict(PodcastAudioFile=None)


def test_fastapi_transform_endpoint():
    with patch("requests.post") as mocked_post:
        # Set up the mocked response from the Whisper ASR API
        mocked_response = MagicMock()
        mocked_response.json.return_value = {
            "PodcastTranscript": "This is a mocked transcript"
        }
        mocked_post.return_value = mocked_response

        # Call the FastAPI transform endpoint with mocked input data
        response = client.post(
            "/transform/",
            json={"PodcastAudioFile": "Mocked audio file content"},
        )

        assert response.status_code == 200
        assert response.json() == {"PodcastTranscript": "This is a mocked transcript"}

        # Check that the Whisper ASR API is called with the correct headers and data
        headers = {
            "Authorization": f"Bearer {os.environ.get('API_KEY')}",
            "Content-Type": "audio/wav",
            "language": "en-US",
        }
        mocked_post.assert_called_with(
            "https://api.whisper.asr.example.com/v1/asr",
            headers=headers,
            data="Mocked audio file content",
        )
