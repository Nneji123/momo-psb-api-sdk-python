import os
import uuid

import pytest

from momo_psb.api import MoMoPSBAPI

BASE_URL = "https://sandbox.momodeveloper.mtn.com"
SUBSCRIPTION_KEY = os.environ.get("SUBSCRIPTION_KEY")
REFERENCE_ID = str(uuid.uuid4())
CALLBACK_HOST = "https://clinic.com"
AMOUNT = 100.0
CURRENCY = "EUR"
EXTERNAL_ID = str(uuid.uuid4())
PAYER = {"partyIdType": "MSISDN", "partyId": "+2348056042384"}
PAYER_MESSAGE = "Test message"
PAYEE_NOTE = "Test note"
TARGET_ENVIRONMENT = "sandbox"


@pytest.fixture
def momo_api():
    return MoMoPSBAPI(base_url=BASE_URL, subscription_key=SUBSCRIPTION_KEY)


@pytest.fixture
def api_user(momo_api):
    response = momo_api.create_api_user(
        reference_id=REFERENCE_ID, provider_callback_host=CALLBACK_HOST
    )
    assert response.status_code in (200, 201)
    return REFERENCE_ID


@pytest.fixture
def api_key(momo_api, api_user):
    response = momo_api.create_api_key(api_user=api_user)
    assert response.status_code in (200, 201)
    return response.json().get("apiKey")


@pytest.fixture
def access_token(momo_api, api_user, api_key):
    response = momo_api.get_oauth_token(api_user=api_user, api_key=api_key)
    assert response.status_code == 200
    return response.json().get("access_token")
