from momo_psb import MoMoPSBAPI
import uuid


if __name__ == "__main__":
    manager = MoMoPSBAPI(
        base_url="https://sandbox.momodeveloper.mtn.com",
        subscription_key="put_subscription_key_here"
    )

    # Create API User

    # Generate a random ref_id
    ref_id = str(uuid.uuid4())
    callback_host = "example.com"
    response = manager.create_api_user(ref_id, callback_host)
    print("Create API User Response:", response.status_code, response.text)

    # Create API Key
    response = manager.create_api_key(ref_id)
    print("Create API Key Response:", response.status_code, response.text)
    api_key = response.json().get("apiKey")
    print(f"Json Response: {response.json()}")
    print(f"User API Key: {api_key}")

    # Get API User Details
    response = manager.get_api_user_details(ref_id)
    print("API User Details Response:", response.status_code, response.text)

    # Get OAuth Token
    response = manager.get_oauth_token(ref_id, api_key)
    print("OAuth Token Response:", response.status_code, response.text)

    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data.get("access_token")
        print(f"Access Token: {access_token}")
        
        payer_info = {
            "partyIdType": "MSISDN",
            "partyId": "+2348056042321"
        }
        response = manager.request_to_pay(
            reference_id=str(uuid.uuid4()),
            access_token=access_token,
            amount="100.00",
            currency="EUR",
            external_id=str(uuid.uuid4()),
            payer=payer_info,
            payer_message="Payment for services",
            payee_note="Thank you for your payment"
        )
        print("Request to Pay Response:", response.status_code, response.text)
    else:
        print("Failed to obtain access token.")