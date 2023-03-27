import json
from datetime import datetime
import requests
from fastapi import FastAPI, Request

from config.config import get_env
from schemas.api_logs import ApiLogs
import repository.api_logs as api_logs

PERDIX_SERVER = 'perdix-server'
PERDIX_URL = get_env(PERDIX_SERVER, 'url', PERDIX_SERVER + 'perdix-base-url not configured')
PERDIX_USERNAME = get_env(PERDIX_SERVER, 'username', PERDIX_SERVER + 'perdix-username not configured')
PERDIX_PASSWORD = get_env(PERDIX_SERVER, 'password', PERDIX_SERVER + 'perdix-password not configured')
FORM_URL = get_env(PERDIX_SERVER, 'form-url', PERDIX_SERVER + 'form-url not configured')

def get_token(tokenRefresh=False):
        if(tokenRefresh == True):
                print("Refresh token")
                url = PERDIX_URL + f"/oauth/token"
                payload=f"username={PERDIX_USERNAME}&password={PERDIX_PASSWORD}&grant_type=password&scope=read%20write&client_secret=mySecretOAuthSecret&client_id=application"
                headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
                }

                response = requests.request("POST", url, headers=headers, data=payload)
                res = response.json()
                # api.log(channel, url, "POST", payload, json.dumps(response.json()), response.status_code, response.elapsed)
                with open('.perdixauthcache', 'w') as f:
                        f.write(res["access_token"])

                return res["access_token"]
        else:
                f = open(".perdixauthcache", "r")
                return f.read()
                

async def get_loan_details(loan_id):
        token = get_token(True)
        url = PERDIX_URL + f"/api/individualLoan/{loan_id}"
        payload = {}
        headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer'+ token
        }

        loan_account_response = requests.request("GET", url, headers=headers, data=payload)
        loan_account_dict = str(json.loads(loan_account_response.text))
        api_call_duration = str(loan_account_response.elapsed.total_seconds()) + ' sec'
        log_info = ApiLogs(
            channel='Perdix',
            request_url=str(url),
            request_method='GET',
            params=str(loan_id),
            request_body="",
            response_body=loan_account_dict,
            status_code=str(loan_account_response.status_code),
            api_call_duration=api_call_duration,
            request_time=str(datetime.now())
        )
        await api_logs.insert(log_info)
        return loan_account_response


async def update_loan_account(payload):
        token = get_token(True)
        url = f"{PERDIX_URL}/api/individualLoan"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer'+token
        }

        loan_account_response = requests.request("PUT", url, headers=headers, data=payload)
        loan_account_dict = str(json.loads(loan_account_response.text))
        api_call_duration = str(loan_account_response.elapsed.total_seconds()) + ' sec'
        log_info = ApiLogs(
            channel='Perdix',
            request_url=str(url),
            request_method='PUT',
            params=None,
            request_body=str(payload),
            response_body=loan_account_dict,
            status_code=str(loan_account_response.status_code),
            api_call_duration=api_call_duration,
            request_time=str(datetime.now())
        )
        await api_logs.insert(log_info)
        return loan_account_response

async def get_customer(customerId):
        token = get_token(False)
        url = PERDIX_URL + f"/api/enrollments/{customerId}"
        payload={}
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer'+ token
        }

        customer_response = requests.request("GET", url, headers=headers, data=payload)
        customer_response__dict = str(json.loads(customer_response.text))
        api_call_duration = str(customer_response.elapsed.total_seconds()) + ' sec'
        log_info = ApiLogs(
            channel='Perdix',
            request_url=str(url),
            request_method='GET',
            params=str(customerId),
            request_body="",
            response_body=customer_response__dict,
            status_code=str(customer_response.status_code),
            api_call_duration=api_call_duration,
            request_time=str(datetime.now())
        )
        await api_logs.insert(log_info)
        return customer_response

async def download_form(loan_id):
        url = f"{FORM_URL}?form_name=ach_loan&record_id={loan_id}"
        return requests.get(url)


