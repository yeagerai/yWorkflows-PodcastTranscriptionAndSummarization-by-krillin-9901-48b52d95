
# Import necessary libraries
import pytest
from pydantic import ValidationError

# Import the GenerateAudio component
from your_package_path import GenerateAudio, GenerateAudioInputDict, GenerateAudioOutputDict

# Define test cases with mocked input and expected output data
test_data = [
    (
        GenerateAudioInputDict(PodcastSummary="Test podcast summary"),
        GenerateAudioOutputDict(PodcastSummaryAudio=b"mocked_audio_data"),
    ),
    (
        GenerateAudioInputDict(PodcastSummary="Another test podcast summary"),
        GenerateAudioOutputDict(PodcastSummaryAudio=b"mocked_audio_data_2"),
    ),
]

# Define test cases to handle error scenarios
error_test_data = [
    (
        {"PodcastSummary": 123},  # invalid input data type
        ValidationError,
    ),
    (
        {"NotAPodcastSummary": "Invalid key"},  # invalid input key
        ValidationError,
    ),
]


@pytest.mark.parametrize("test_input, expected_output", test_data)
def test_generate_audio_transform_valid(test_input, expected_output, mocker):
    # Mock the external API request
    mocker.patch("requests.post")
    requests.post.return_value = mocker.MagicMock(status_code=200, content=expected_output.PodcastSummaryAudio)

    # Instantiate the GenerateAudio component
    generate_audio = GenerateAudio()

    # Call the component's transform() method with the mocked input
    output = generate_audio.transform(test_input)

    # Assert that the output matches the expected output
    assert output == expected_output


@pytest.mark.parametrize("test_input, expected_exception", error_test_data)
def test_generate_audio_transform_invalid(test_input, expected_exception, mocker):
    # Instantiate the GenerateAudio component
    generate_audio = GenerateAudio()

    # Call the component's transform() method with the invalid input data and assert the expected exception
    with pytest.raises(expected_exception):
        generate_audio.transform(test_input)
