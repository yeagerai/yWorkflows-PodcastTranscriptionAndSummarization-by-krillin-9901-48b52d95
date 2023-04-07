
# TranscribePodcast

This component transcribes the podcast audio file using the Whisper ASR API. It takes an audio file as input and generates a text transcript of the podcast as output.

## Initial generation prompt
description: 'This component transcribes the podcast audio file using the Whisper
  ASR API. Inputs: PodcastAudioFile (from FetchPodcast). Outputs: PodcastTranscript
  (the generated text transcript of the podcast).'
name: TranscribePodcast


## Transformer breakdown
- Load the PodcastAudioFile from the input.
- Initialize the Whisper ASR API with the provided API key.
- Send the audio file to the Whisper ASR API for transcription.
- Receive the transcription result from the API.
- Return the transcribed text as PodcastTranscript.

## Parameters
[{'name': 'api_key', 'default_value': 'YOUR_API_KEY', 'description': 'The API key to authenticate with the Whisper ASR API.', 'type': 'str'}, {'name': 'language_code', 'default_value': 'en-US', 'description': 'The language code of the podcast audio.', 'type': 'str'}]

        