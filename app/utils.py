import requests
import base64
from datetime import datetime
from requests.auth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

import logging
import json  # Make sure to import json

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def hash_password(password):
    return generate_password_hash(password)

def verify_password(password, hashed_password):
    return check_password_hash(hashed_password, password)

def get_access_token():
    consumer_key = 'cHnkwYIgBbrxlgBoneczmIJFXVm0oHky'
    consumer_secret = '2nHEyWSD4VjpNh2g'
    api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    
    logger.debug(f"Requesting access token from: {api_url}")

    try:
        # Using HTTPBasicAuth for authorization
        response = requests.get(api_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
        logger.debug(f"Access token response status: {response.status_code}")
        
        # Log the response content
        logger.debug(f"Response content: {response.text}")

        response.raise_for_status()  # Raise an error for bad responses

        # Parse the response JSON
        mpesa_access_token = response.json()
        validated_mpesa_access_token = mpesa_access_token.get('access_token')

        if validated_mpesa_access_token:
            logger.debug(f"Access Token: {validated_mpesa_access_token}")
            return validated_mpesa_access_token
        else:
            logger.error("Access token not found in the response.")
            return None
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting access token: {e}")
        return None

def format_phone_number(phone_number):
    if phone_number.startswith('0'):
        return '254' + phone_number[1:]
    return phone_number  # Return as is if already in the correct format


def send_stk_push(phone_number, amount):
    access_token = get_access_token()
    if not access_token:
        logger.error("Failed to obtain access token.")
        return False
    
    # Format phone number to the correct international format
    formatted_phone_number = format_phone_number(phone_number)


    api_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    headers = {"Authorization": f"Bearer {access_token}"}
    
    payload = {
        "BusinessShortCode": "4084887",  # Replace with your shortcode
        "Password": generate_password(),  # Ensure this function returns a valid password
        "Timestamp": get_timestamp(),      # Ensure this function returns a valid timestamp
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": formatted_phone_number,
        "PartyB": "4084887",                # Replace with your shortcode
        "PhoneNumber": formatted_phone_number,
        "CallBackURL": "https://mydomain.com/pth",  # Replace with your callback URL
        "AccountReference": "Daily Payment",
        "TransactionDesc": "Payment for passed day"
    }

    logger.debug(f"STK Push Payload: {json.dumps(payload)}")
    
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        logger.debug(f"STK Push Response Status: {response.status_code}")
        logger.debug(f"STK Push Response Content: {response.text}")  # Log the response content
        
        response.raise_for_status()  # Raise an error for bad responses
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        logger.error(f"Error sending STK push: {e}")
        if response is not None:
            logger.error(f"Response content: {response.content}")  # Log the response content
        return False

def generate_password():
    shortcode = "4084887"  # Replace with your shortcode
    passkey = "a5ce9f8f9b6621de9573b4f3eac5d2f3c245e4fefe96722be3ce2c421277f960"  # Ensure this is the correct passkey
    timestamp = get_timestamp()
    data = shortcode + passkey + timestamp
    return base64.b64encode(data.encode()).decode('utf-8')

def get_timestamp():
    return datetime.now().strftime('%Y%m%d%H%M%S')
