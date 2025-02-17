from google.cloud import storage
from dotenv import load_dotenv
from app.common.utils import get_credentials
from app.common.variables import PROJECT_ID, BUCKET_NAME

class GCSConnection():

    def __init__(self):
        load_dotenv()
        self._creds = get_credentials()
        self.client = storage.Client(project=PROJECT_ID, credentials=self._creds)
        self.bucket = self.client.bucket(BUCKET_NAME)
    
    def upload_file(self, source_file, destination):
        blob = self.bucket.blob(destination)

        try:
            blob.upload_from_filename(source_file)

            print(
                f"File {source_file} uploaded to {destination}"
            )
            return True
        except Exception as e:
            print(e)
            return False
        