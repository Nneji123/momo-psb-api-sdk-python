from requests.models import Response

from tests.conftest import REFERENCE_ID


def test_create_api_user(api_user):
    assert api_user == REFERENCE_ID


def test_create_api_key(api_key):
    assert isinstance(api_key, str)


def test_get_oauth_token(access_token):
    assert isinstance(access_token, str)


def test_request_to_pay(momo_api, access_token):
    response = momo_api.request_to_pay(
        reference_id=REFERENCE_ID,
        access_token=access_token,
        amount=AMOUNT,
        currency=CURRENCY,
        external_id=EXTERNAL_ID,
        payer=PAYER,
        payer_message=PAYER_MESSAGE,
        payee_note=PAYEE_NOTE,
    )
    assert isinstance(response, Response)
    assert response.status_code in (200, 201)


def test_get_account_balance(momo_api, access_token):
    response = momo_api.get_account_balance(access_token=access_token)
    assert isinstance(response, dict)
    assert "balance" in response


def test_validate_account_holder_status(momo_api, access_token):
    response = momo_api.validate_account_holder_status(
        access_token=access_token,
        account_holder_id_type="MSISDN",
        account_holder_id="1234567890",
    )
    assert isinstance(response, dict)
    assert "status" in response


def test_get_request_to_pay_status(momo_api, access_token):
    response = momo_api.get_request_to_pay_status(
        reference_id=REFERENCE_ID,
        access_token=access_token,
    )
    assert isinstance(response, dict)
    assert "status" in response


def test_get_basic_user_info(momo_api, access_token):
    response = momo_api.get_basic_user_info(
        access_token=access_token,
        account_holder_id_type="MSISDN",
        account_holder_id="1234567890",
    )
    assert isinstance(response, dict)
    assert "userInfo" in response


def test_request_to_withdraw(momo_api, access_token):
    response = momo_api.request_to_withdraw(
        reference_id=REFERENCE_ID,
        access_token=access_token,
        amount=AMOUNT,
        currency=CURRENCY,
        external_id=EXTERNAL_ID,
        payer=PAYER,
        payer_message=PAYER_MESSAGE,
        payee_note=PAYEE_NOTE,
    )
    assert isinstance(response, Response)
    assert response.status_code in (200, 201)


def test_get_request_to_withdraw_status(momo_api, access_token):
    response = momo_api.get_request_to_withdraw_status(
        reference_id=REFERENCE_ID,
        access_token=access_token,
    )
    assert isinstance(response, dict)
    assert "status" in response


def test_create_invoice(momo_api, access_token):
    response = momo_api.create_invoice(
        reference_id=REFERENCE_ID,
        access_token=access_token,
        external_id=EXTERNAL_ID,
        amount=AMOUNT,
        currency=CURRENCY,
        validity_duration="3600",
        intended_payer=PAYER,
        payee=PAYER,
    )
    assert isinstance(response, Response)
    assert response.status_code in (200, 201)


def test_get_invoice_status(momo_api, access_token):
    response = momo_api.get_invoice_status(
        reference_id=REFERENCE_ID,
        access_token=access_token,
    )
    assert isinstance(response, dict)
    assert "status" in response


def test_cancel_invoice(momo_api, access_token):
    response = momo_api.cancel_invoice(
        reference_id=REFERENCE_ID,
        access_token=access_token,
        external_id=EXTERNAL_ID,
    )
    assert isinstance(response, Response)
    assert response.status_code in (200, 204)


def test_create_pre_approval(momo_api, access_token):
    response = momo_api.create_pre_approval(
        reference_id=REFERENCE_ID,
        access_token=access_token,
        payer=PAYER,
        payer_currency=CURRENCY,
        payer_message=PAYER_MESSAGE,
        validity_time=3600,
    )
    assert isinstance(response, Response)
    assert response.status_code in (200, 201)


def test_get_pre_approval_status(momo_api, access_token):
    response = momo_api.get_pre_approval_status(
        reference_id=REFERENCE_ID,
        access_token=access_token,
    )
    assert isinstance(response, dict)
    assert "status" in response


def test_cancel_pre_approval(momo_api, access_token):
    response = momo_api.cancel_pre_approval(
        preapproval_id=REFERENCE_ID,
        access_token=access_token,
    )
    assert isinstance(response, Response)
    assert response.status_code in (200, 204)


def test_get_approved_pre_approvals(momo_api, access_token):
    response = momo_api.get_approved_pre_approvals(
        account_holder_id_type="MSISDN",
        account_holder_id="1234567890",
        access_token=access_token,
    )
    assert isinstance(response, list)
    assert len(response) >= 0


def test_create_payment(momo_api, access_token):
    response = momo_api.create_payment(
        reference_id=REFERENCE_ID,
        access_token=access_token,
        external_transaction_id=EXTERNAL_ID,
        amount=AMOUNT,
        currency=CURRENCY,
        customer_reference="test_customer",
        service_provider_user_name="test_provider",
    )
    assert isinstance(response, Response)
    assert response.status_code in (200, 201)


def test_get_payment_status(momo_api, access_token):
    response = momo_api.get_payment_status(
        reference_id=REFERENCE_ID,
        access_token=access_token,
    )
    assert isinstance(response, dict)
    assert "status" in response
