import os
from dotenv import load_dotenv
import json
import base64
from google.cloud import secretmanager
from google.oauth2 import service_account
import polars as pl
from app.common.variables import PROJECT_ID, SECRET_ID


def get_credentials_sm():
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{PROJECT_ID}/secrets/{SECRET_ID}"
    response = client.access_secret_version(request={"name": name})
    payload = response.payload.data.decode("UTF-8")
    print(payload)
    return payload

def get_credentials(env:str = "local"):
    if env == "local":
        load_dotenv()
        json_creds = json.loads(base64.b64decode(os.getenv("GCP_CREDENTIALS")), strict = False)
        creds = service_account.Credentials.from_service_account_info(json_creds)
    return creds


# if __name__ == "__main__":
#     get_credentials()
