
from googleapiclient.discovery import build
from http.server import BaseHTTPRequestHandler
from google.oauth2 import service_account

import urllib3
import json
import os
 
def get_data_lambda():
    http = urllib3.PoolManager()
    url = "https://cloud.iexapis.com/stable/stock/tsla/previous?token=" + os.environ.get("API_KEY")
    resp = http.request("GET", url)
    values = json.loads(resp.data)
    return values
 
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SAMPLE_SPREADSHEET_ID = '1M8Zi_FzRu2epzJXo4KRkLvCbU-33X4_r1yVRfm-4Rok'
SAMPLE_RANGE_NAME = 'A:B'
 
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        s = self.path
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        values = get_data_lambda()
        service_account_credentials = {
            "type": os.environ.get("type"),
            "project_id": os.environ.get("project_id"),
            "private_key_id": os.environ.get("private_key_id"),
            "private_key": os.environ.get("private_key"),
            "client_email": os.environ.get("client_email"),
            "client_id": os.environ.get("client_id"),
            "auth_uri": os.environ.get("auth_uri"),
            "token_uri": os.environ.get("token_uri"),
            "auth_provider_x509_cert_url": os.environ.get("auth_provider_x509_cert_url"),
            "client_x509_cert_url": os.environ.get("client_x509_cert_url")
        }
        print(service_account_credentials)
        credentials = service_account.Credentials.from_service_account_info(
            service_account_credentials, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=credentials)
        values_list = list(values.values())
        final_list = []
        final_list.append(values_list)
        dict_me = dict(values=final_list)
        service.spreadsheets().values().append(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            valueInputOption='RAW',
            range=SAMPLE_RANGE_NAME,
            body=dict_me).execute()
 
        print('Sheet successfully Updated')
        return