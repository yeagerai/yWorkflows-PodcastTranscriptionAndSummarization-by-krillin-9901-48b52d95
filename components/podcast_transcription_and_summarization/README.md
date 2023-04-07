
# PodcastTranscriptionAndSummarization

The Workflow requires a PodcastUrl as input (a subclass of pydantic.BaseModel with an attribute containing the podcast url as a string). The output is a TranscriptSummaryAudioResponse subclass of pydantic.BaseModel containing the path to the generated transcript.txt, summary.txt, and summary.mp3 files.

## Initial generation prompt
description: "IOs - The Workflow requires a PodcastUrl as input (a subclass of pydantic.BaseModel\
  \ with\n  an attribute containing the podcast url as a string). The output is a\
  \ TranscriptSummaryAudioResponse\n  subclass of pydantic.BaseModel containing the\
  \ path to the generated transcript.txt,\n  summary.txt, and summary.mp3 files.\n\
  ...\n"
name: PodcastTranscriptionAndSummarization


## Transformer breakdown
- Execute the transform of the AbstractWorkflow
- Prepare the Output BaseModel

## Parameters
[]

        