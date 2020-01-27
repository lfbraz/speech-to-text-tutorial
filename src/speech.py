# coding: utf-8

import config.settings as conf
import swagger_client as cris_client
import logging
import sys
from typing import List
import requests
import time
import json


class Speech():
    def __init__(self):
        self.speech_key = conf.KEY
        self.service_region = conf.REGION
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format="%(message)s")

    def transcribe(self, blob_uri, name='', description='', locale='en-US', properties={}, output_file=None):
        logging.info("Starting transcription client...")

        # configure API key authorization: subscription_key
        configuration = cris_client.Configuration()
        configuration.api_key['Ocp-Apim-Subscription-Key'] = self.speech_key
        configuration.host = "https://{}.cris.ai".format(self.service_region)

        # create the client object and authenticate
        client = cris_client.ApiClient(configuration)

        # create an instance of the transcription api class
        transcription_api = cris_client.CustomSpeechTranscriptionsApi(api_client=client)

        # get all transcriptions for the subscription
        transcriptions: List[cris_client.Transcription] = transcription_api.get_transcriptions()

        logging.info("Deleting all existing completed transcriptions.")

        # delete all pre-existing completed transcriptions
        # if transcriptions are still running or not started, they will not be deleted
        for transcription in transcriptions:
            try:
                transcription_api.delete_transcription(transcription.id)
            except Exception as e:
                print(e)

        # Specify transcription properties by passing a dict to the properties parameter. See
        # https://docs.microsoft.com/azure/cognitive-services/speech-service/batch-transcription#configuration-properties
        # for supported parameters.
        # properties = {
            # 'PunctuationMode': 'DictatedAndAutomatic',
            # 'ProfanityFilterMode': 'Masked',
            # 'AddWordLevelTimestamps': 'False',
            # 'AddDiarization': 'False',
            # 'AddSentiment': False,
            # 'TranscriptionResultsContainerUrl': "<results container>"
        # }

        # Use base models for transcription. Comment this block if you are using a custom model.
        transcription_definition = cris_client.TranscriptionDefinition(
            name=name, description=description, locale=locale, recordings_url=blob_uri,
            properties=properties
        )

        data, status, headers = transcription_api.create_transcription_with_http_info(transcription_definition)

        # extract transcription location from the headers
        transcription_location: str = headers["location"]

        # get the transcription Id from the location URI
        created_transcription: str = transcription_location.split('/')[-1]

        logging.info("Created new transcription with id {}".format(created_transcription))

        logging.info("Checking status.")

        completed = False

        while not completed:
            running, not_started = 0, 0

            # get all transcriptions for the user
            transcriptions: List[cris_client.Transcription] = transcription_api.get_transcriptions()

            # for each transcription in the list we check the status
            for transcription in transcriptions:
                if transcription.status in ("Failed", "Succeeded"):
                    # we check to see if it was the transcription we created from this client
                    if created_transcription != transcription.id:
                        continue

                    completed = True

                    if transcription.status == "Succeeded":
                        results_uri = transcription.results_urls["channel_0"]
                        results = requests.get(results_uri)
                        logging.info("Transcription succeeded. Results: ")

                        logging.info("######### TRANSCRIPTION BEGIN ########## ")
                        logging.info(results.content.decode("utf-8"))

                        if(output_file):
                            json_file = open(output_file, 'w')
                            json_file.write(json.loads(json.dumps(results.content.decode("utf-8"), ensure_ascii=False)))

                        logging.info("######### TRANSCRIPTION END ########## ")
                    else:
                        logging.info("Transcription failed :{}.".format(transcription.status_message))
                        break
                elif transcription.status == "Running":
                    running += 1
                elif transcription.status == "NotStarted":
                    not_started += 1

            logging.info("Transcriptions status: "
                         "completed (this transcription): {}, {} running, {} not started yet".format(
                            completed, running, not_started))

            # wait for 5 seconds
            time.sleep(5)
