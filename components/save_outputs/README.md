
# SaveOutputs

This component saves the transcript.txt, summary.txt, and summary.mp3 files to disk. It takes the PodcastTranscript (from TranscribePodcast), PodcastSummary (from GenerateSummary), and PodcastSummaryAudio (from GenerateAudio) as inputs, processes them, and provides the paths to the generated output files in the form of a TranscriptSummaryAudioResponse object as the output.

## Initial generation prompt
description: 'This component saves the transcript.txt, summary.txt, and summary.mp3
  files to disk. Inputs: PodcastTranscript (from TranscribePodcast), PodcastSummary
  (from GenerateSummary), and PodcastSummaryAudio (from GenerateAudio). Outputs: TranscriptSummaryAudioResponse
  (containing paths to the generated output files).'
name: SaveOutputs


## Transformer breakdown
- Create output directory if it does not exist
- Verify and clean input data
- Save transcript text to file
- Save summary text to file
- Save summary audio to file
- Create TranscriptSummaryAudioResponse object with file paths as attributes
- Output TranscriptSummaryAudioResponse object

## Parameters
[{'name': 'output_directory', 'default_value': 'outputs', 'description': 'Directory path to save the output files.', 'type': 'str'}, {'name': 'transcript_filename', 'default_value': 'transcript.txt', 'description': 'Filename for saving the transcript.', 'type': 'str'}, {'name': 'summary_filename', 'default_value': 'summary.txt', 'description': 'Filename for saving the summary.', 'type': 'str'}, {'name': 'summary_audio_filename', 'default_value': 'summary.mp3', 'description': 'Filename for saving the audio summary.', 'type': 'str'}]

        