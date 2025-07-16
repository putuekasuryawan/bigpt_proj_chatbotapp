import time
import logging
import requests
from twilio.rest import Client
from requests.auth import HTTPBasicAuth
from chatbotappbianco.models import *

account_sid = tbl_twiliocredentials.objects.using("chatbotdb").filter(type="production").last().account_sid
auth_token = tbl_twiliocredentials.objects.using("chatbotdb").filter(type="production").last().auth_token
client = Client(account_sid, auth_token)
twilio_number = tbl_twiliocredentials.objects.using("chatbotdb").filter(type="production").last().number

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_message(to_number, body_text):
    url = f'https://api.twilio.com/xxxxxxxx/{account_sid}/Messages.json'
    try:
        data = {
            'To': f'whatsapp:{to_number}',
            'From': f'whatsapp:{twilio_number}',
            'Body': body_text
        }
        response = requests.post(url, data=data, auth=HTTPBasicAuth(account_sid, auth_token))
        logger.info(f"Message sent to {to_number}")
    except Exception as e:
        data = {
            'To': f'whatsapp:{to_number}',
            'From': f'whatsapp:{twilio_number}',
            'Body': 'There was a failure in processing the message. The error is as follows, ' + str(e)
        }
        response = requests.post(url, data=data, auth=HTTPBasicAuth(account_sid, auth_token))
        logger.error("Error sending message to " + to_number + ": " + str(e))

def send_bulk_template_message(content_sid, recipients):
    delay = 1
    url = f'https://api.twilio.com/xxxxxxx/{account_sid}/Messages.json'
    results = []
    for recipient in recipients:
        to_number = recipient.get("number")
        content_variables = {
            key: value for key, value in recipient.items() if key != "number"
        }
        data = {
            'To': f'whatsapp:+{to_number}',
            'From': f'whatsapp:{twilio_number}',
            'ContentSid': content_sid,
        }
        if content_variables:
            data['ContentVariables'] = str(content_variables).replace("'", '"')            
        print(data)
        try:
            response = requests.post(
                url,
                data=data,
                auth=HTTPBasicAuth(account_sid, auth_token)
            )
            response.raise_for_status()
            logger.info(f"✔️ Template sent to {to_number}")
            results.append({"to": to_number, "status": "sent", "response": response.json()})
        except Exception as e:
            logger.error(f"❌ Failed to send to {to_number}: {str(e)}")
            logger.error(f"Response: {e.response.text}")
            results.append({"to": to_number, "status": "failed", "error": str(e)})
        time.sleep(delay)
    return results
