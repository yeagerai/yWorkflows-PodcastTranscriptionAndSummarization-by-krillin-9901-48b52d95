
# PodcastTranscriptionAndSummarization

This Yeager Workflow transcribes podcasts using the Whisper ASR API and the Listen Notes API. It takes the podcast URL as input and outputs a transcript.txt file. It uses the OpenAI ChatGPT API to produce a summary of the transcript, which is saved as a summary.txt file. Finally, the workflow utilizes the Eleven Labs API to convert the summary.txt to an audio file in mp3 format.
## Initial generation prompt
a workflow that transcribes podcasts using the whisper API and listen notes API. output is a transcript.txt file. use the chatGPT api to summarize the transcript.txt file to generate a summary.txt file. finally, use the eleven labs API to produce an mp3 file based on the summary.txt

## Authors: 
- yWorkflows
- krillin#9901
        