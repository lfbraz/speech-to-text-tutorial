# Speech to Text using Azure Cognitive Services **(Speech API)**
This implementation is for learning purposes. The class speech.py could be used to obtain the transcription from an audio file. This code was adapted from [How to use the Speech Services Batch Transcription API from Python](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples/batch/python#how-to-use-the-speech-services-batch-transcription-api-from-python).

Could be used in scenarios like call center sentiment analysis, fraud detection, and much more.

Use your creativity to expand the use ~~to have fun~~ to fix a lot of real world problems and feel free to clone this repo and adapt this code for your requirements :)

## [Activate environment](https://pipenv.readthedocs.io/en/latest/)
`pipenv shell`

## Flake8 config
Use the bellow code to adjust the max line length limit
flake8 --max-line-length=140

If you use VSCode you can add this config to settings.json adding the code:

```
"python.linting.flake8Args": [
        "--max-line-length=140",
    ]
```

## Prerequisites
```
sudo apt-get update
sudo apt-get install libssl1.0.0 libasound2
```

You also need to follow the requirement from [How to use the Speech Services Batch Transcription API from Python](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples/batch/python#how-to-use-the-speech-services-batch-transcription-api-from-python) to be able to use the API.

## Set environment variables
### You can find API Key in Quick start section of your API on Azure Portal
`export SPEECH_KEY=<KEY_1>`
### You can find API endpoint in Quick start section of your API on Azure Portal
`export REGION=<REGION>`


## How to run
Run `run.py` and change the variable `BLOB_URI_INPUT` with the URL SAS generated in your Storage Account

**name**: Just a name for the transcript execution

**description**: Just a description

**locale**: Is the code of the language that the API need to use during the transcription process. To get the language's code go to this [url](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support)

**properties**: Is a dict with the [configurations options](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/batch-transcription#configuration-properties)

**output_file**: Is the filename with json content

## Clean up resources
To clean up resources you can delete the Resource Group or the API using Azure Portal.
