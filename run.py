from src.speech import Speech

BLOB_URI_INPUT = 'SAS_URL_BLOB_STORAGE'

speech = Speech()
speech = Speech()

speech.transcribe(blob_uri=BLOB_URI_INPUT,
                  name='Test Speech to Text',
                  description='This is a test of the Speech to Text API using Swagger',
                  locale='en-US',
                  properties={'AddDiarization': 'True'},
                  output_file='transcript.json'
                  )
