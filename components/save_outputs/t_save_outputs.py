
import os
import shutil
from pathlib import Path
from typing import List, Tuple

import pytest
from pydantic import ValidationError

from src.main import SaveOutputs, SaveOutputsInputDict, TranscriptSummaryAudioResponse


# Define test cases with mocked input and expected output data
@pytest.mark.parametrize(
    "input_data, output_data",
    [
        (
            SaveOutputsInputDict(
                PodcastTranscript="Sample transcript",
                PodcastSummary="Sample summary",
                PodcastSummaryAudio=b"Sample summary audio",
            ),
            TranscriptSummaryAudioResponse(
                transcript_file_path="output/transcript.txt",
                summary_file_path="output/summary.txt",
                summary_audio_file_path="output/summary_audio.mp3",
            ),
        ),
        (
            SaveOutputsInputDict(
                PodcastTranscript="",
                PodcastSummary="",
                PodcastSummaryAudio=b"",
            ),
            TranscriptSummaryAudioResponse(
                transcript_file_path="output/transcript.txt",
                summary_file_path="output/summary.txt",
                summary_audio_file_path="output/summary_audio.mp3",
            ),
        ),
    ],
)
def test_transform(input_data: SaveOutputsInputDict, output_data: TranscriptSummaryAudioResponse) -> None:
    # If output directory exists, delete it
    if os.path.exists("output"):
        shutil.rmtree("output")

    # Instantiate the SaveOutputs component and call the transform method
    save_outputs = SaveOutputs()
    result = save_outputs.transform(input_data)

    # Assert that the output matches the expected output
    assert result == output_data

    # Assert that the files are actually created in the output directory
    assert Path(output_data.transcript_file_path).is_file()
    assert Path(output_data.summary_file_path).is_file()
    assert Path(output_data.summary_audio_file_path).is_file()

    # Delete the created output directory
    shutil.rmtree("output")


# Error handling and edge case scenarios
def test_transform_invalid_input() -> None:
    # Test with missing PodcastTranscript field
    with pytest.raises(ValidationError):
        SaveOutputsInputDict(PodcastSummary="Sample summary", PodcastSummaryAudio=b"Sample summary audio")

    # Test with missing PodcastSummary field
    with pytest.raises(ValidationError):
        SaveOutputsInputDict(PodcastTranscript="Sample transcript", PodcastSummaryAudio=b"Sample summary audio")

    # Test with missing PodcastSummaryAudio field
    with pytest.raises(ValidationError):
        SaveOutputsInputDict(PodcastTranscript="Sample transcript", PodcastSummary="Sample summary")

    # Test with no input fields
    with pytest.raises(ValidationError):
        SaveOutputsInputDict()

