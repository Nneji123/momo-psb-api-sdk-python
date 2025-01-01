from typing import Dict, Any, Optional, List

class MoMoPSBAPI:
    """
    A Python SDK for integrating with the MTN MoMo API (Payment Service Bank).
    """

    def __init__(self, base_url: str, subscription_key: str):
        """
        Initialize the MoMoPSBAPI.

        :param base_url: Base URL for the Wallet Platform API.
        :param subscription_key: Subscription key for the API Manager portal.
        """
        self.base_url = base_url.rstrip("/")
        self.subscription_key = subscription_key
        self.headers = {
            "Ocp-Apim-Subscription-Key": self.subscription_key
        }

    def create_api_user(self, reference_id: str, provider_callback_host: str) -> requests.Response:
        """
        Create a new API User.

        :param reference_id: UUID Reference ID to be used as the User ID.
        :param provider_callback_host: Callback host for the provider.
        :return: Response object.
        """
        url = f"{self.base_url}/v1_0/apiuser"
        self.headers["X-Reference-Id"] = reference_id
        payload = {"providerCallbackHost": provider_callback_host}
        response = requests.post(url, json=payload, headers=self.headers)
        return response

    def create_api_key(self, api_user: str) -> requests.Response:
        """
        Create a new API Key for an existing API User.

        :param api_user: The API User ID.
        :return: Response object containing the API Key.
        """
        url = f"{self.base_url}/v1_0/apiuser/{api_user}/apikey"
        response = requests.post(url, headers=self.headers)
        return response

    def get_api_user_details(self, api_user: str) -> requests.Response:
        """
        Retrieve details of an API User.

        :param api_user: The API User ID.
        :return: Response object containing API User details.
        """
        url = f"{self.base_url}/v1_0/apiuser/{api_user}"
        response = requests.get(url, headers=self.headers)
        return response

    def get_oauth_token(self, api_user: str, api_key: str) -> requests.Response:
        """
        Obtain an OAuth 2.0 access token.

        :param api_user: API User ID for basic authentication.
        :param api_key: API Key for basic authentication.
        :return: Response object containing the access token.
        """
        url = f"{self.base_url}/collection/token/"
        auth = HTTPBasicAuth(api_user, api_key)
        headers = {
            "X-Target-Environment": "sandbox",
            **self.headers  # Include other headers like 'Ocp-Apim-Subscription-Key'
        }
        payload = {"grant_type": "client_credentials"}
        
        # Use `auth` to handle the Authorization header
        response = requests.post(url, data=payload, headers=headers, auth=auth)
        
        # Debugging output to inspect the Authorization header
        prepared_request = response.request
        print(f"Request Headers: {prepared_request.headers}")
        
        return response

    def request_to_pay(self, reference_id: str, access_token: str, amount: float, currency: str, external_id: str, payer: Dict[str, str], payer_message: str, payee_note: str) -> requests.Response:
        """
        Request a payment from a consumer (Payer).

        :param reference_id: UUID Reference ID for the transaction.
        :param access_token: Bearer Authentication Token.
        :param amount: Amount to be debited from the payer account.
        :param currency: ISO4217 Currency code.
        :param external_id: External ID used as a reference to the transaction.
        :param payer: Dictionary with 'partyIdType' and 'partyId' keys identifying the payer.
        :param payer_message: Message written in the payer transaction history message field.
        :param payee_note: Message written in the payee transaction history note field.
        :return: Response object.
        """
        url = f"{self.base_url}/collection/v1_0/requesttopay"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "X-Callback-Url": "https://clinic.com",  # Add your callback URL here if needed
            "X-Reference-Id": reference_id,
            "X-Target-Environment": "sandbox",
            **self.headers  # Include other headers like 'Ocp-Apim-Subscription-Key'
        }
        payload = {
            "amount": float(amount),
            "currency": currency,
            "externalId": external_id,
            "payer": payer,
            "payerMessage": payer_message,
            "payeeNote": payee_note
        }
        response = requests.post(url, json=payload, headers=headers)
        return response

    def validate_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        Validate the API response.

        :param response: The response object.
        :return: Parsed JSON data if the response is successful; raises an error otherwise.
        """
        if response.status_code in (200, 201, 202):
            return response.json()
        else:
            response.raise_for_status()

    def get_account_balance(self, access_token: str, target_environment: str = "sandbox") -> Dict[str, Any]:
        """
        Get the balance of the account.

        :param access_token: Bearer Authentication Token.
        :param target_environment: The target environment (default is "sandbox").
        :return: Dictionary containing the account balance.
        """
        url = f"{self.base_url}/collection/v1_0/account/balance"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "X-Target-Environment": target_environment,
            **self.headers
        }
        response = requests.get(url, headers=headers)
        return self.validate_response(response)

    def validate_account_holder_status(self, access_token: str, account_holder_id_type: str, account_holder_id: str, target_environment: str = "sandbox") -> Dict[str, Any]:
        """
        Validate the status of an account holder.

        :param access_token: Bearer Authentication Token.
        :param account_holder_id_type: Type of the account holder ID (e.g., "msisdn", "email").
        :param account_holder_id: The account holder ID.
        :param target_environment: The target environment (default is "sandbox").
        :return: Dictionary containing the account holder status.
        """
        url = f"{self.base_url}/collection/v1_0/accountholder/{account_holder_id_type}/{account_holder_id}/active"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "X-Target-Environment": target_environment,
            **self.headers
        }
        response = requests.get(url, headers=headers)
        return self.validate_response(response)

    def get_request_to_pay_status(self, reference_id: str, access_token: str, target_environment: str = "sandbox") -> Dict[str, Any]:
        """
        Get the status of a request to pay transaction.

        :param reference_id: UUID of the transaction.
        :param access_token: Bearer Authentication Token.
        :param target_environment: The target environment (default is "sandbox").
        :return: Dictionary containing the transaction status.
        """
        url = f"{self.base_url}/collection/v1_0/requesttopay/{reference_id}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "X-Target-Environment": target_environment,
            **self.headers
        }
        response = requests.get(url, headers=headers)
        return self.validate_response(response)

    def get_basic_user_info(self, access_token: str, account_holder_id_type: str, account_holder_id: str, target_environment: str = "sandbox") -> Dict[str, Any]:
        """
        Get basic user information of an account holder.

        :param access_token: Bearer Authentication Token.
        :param account_holder_id_type: Type of the account holder ID (e.g., "MSISDN", "Email").
        :param account_holder_id: The account holder ID.
        :param target_environment: The target environment (default is "sandbox").
        :return: Dictionary containing basic user information.
        """
        url = f"{self.base_url}/collection/v1_0/accountholder/{account_holder_id_type}/{account_holder_id}/basicuserinfo"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "X-Target-Environment": target_environment,
            **self.headers
        }
        response = requests.get(url, headers=headers)
        return self.validate_response(response)

    def request_to_withdraw(self, reference_id: str, access_token: str, amount: float, currency: str, external_id: str, payer: Dict[str, str], payer_message: str, payee_note: str, target_environment: str = "sandbox") -> requests.Response:
        """
        Request a withdrawal from a consumer (Payer).

        :param reference_id: UUID Reference ID for the transaction.
        :param access_token: Bearer Authentication Token.
        :param amount: Amount to be debited from the payer account.
        :param currency: ISO4217 Currency code.
        :param external_id: External ID used as a reference to the transaction.
        :param payer: Dictionary with 'partyIdType' and 'partyId' keys identifying the payer.
        :param payer_message: Message written in the payer transaction history message field.
        :param payee_note: Message written in the payee transaction history note field.
        :param target_environment: The target environment (default is "sandbox").
        :return: Response object.
        """
        url = f"{self.base_url}/collection/v1_0/requesttowithdraw"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "X-Callback-Url": "https://clinic.com",  # Add your callback URL here if needed
            "X-Reference-Id": reference_id,
            "X-Target-Environment": target_environment,
            **self.headers
        }
        payload = {
            "amount": float(amount),
            "currency": currency,
            "externalId": external_id,
            "payer": payer,
            "payerMessage": payer_message,
            "payeeNote": payee_note
        }
        response = requests.post(url, json=payload, headers=headers)
        return response

    def get_request_to_withdraw_status(self, reference_id: str, access_token: str, target_environment: str = "sandbox") -> Dict[str, Any]:
        """
        Get the status of a request to withdraw transaction.

        :param reference_id: UUID of the transaction.
        :param access_token: Bearer Authentication Token.
        :param target_environment: The target environment (default is "sandbox").
        :return: Dictionary containing the transaction status.
        """
        url = f"{self.base_url}/collection/v1_0/requesttowithdraw/{reference_id}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "X-Target-Environment": target_environment,
            **self.headers
        }
        response = requests.get(url, headers=headers)
        return self.validate_response(response)

    def create_invoice(self, reference_id: str, access_token: str, external_id: str, amount: float, currency: str, validity_duration: str, intended_payer: Dict[str, str], payee: Dict[str, str], description: Optional[str] = None, target_environment: str = "sandbox") -> requests.Response:
        """
        Create an invoice that can be paid by an intended payer.

        :param reference_id: UUID Reference ID for the invoice.
        :param access_token: Bearer Authentication Token.
        :param external_id: External ID used as a reference to the transaction.
        :param amount: Amount to be debited from the payer account.
        :param currency: ISO4217 Currency code.
        :param validity_duration: The duration that the invoice is valid in seconds.
        :param intended_payer: Dictionary with 'partyIdType' and 'partyId' keys identifying the intended payer.
        :param payee: Dictionary with 'partyIdType' and 'partyId' keys identifying the payee.
        :param description: Optional description of the invoice.
        :param target_environment: The target environment (default is "sandbox").
        :return: Response object.
        """
        url = f"{self.base_url}/collection/v2_0/invoice"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "X-Callback-Url": "https://clinic.com",  # Add your callback URL here if needed
            "X-Reference-Id": reference_id,
            "X-Target-Environment": target_environment,
            **self.headers
        }
        payload = {
            "externalId": external_id,
            "amount": float(amount),
            "currency": currency,
            "validityDuration": validity_duration,
            "intendedPayer": intended_payer,
            "payee": payee,
            "description": description
        }
        response = requests.post(url, json=payload, headers=headers)
        return response

    def get_invoice_status(self, reference_id: str, access_token: str, target_environment: str = "sandbox") -> Dict[str, Any]:
        """
        Get the status of an invoice.

        :param reference_id: UUID of the invoice.
        :param access_token: Bearer Authentication Token.
        :param target_environment: The target environment (default is "sandbox").
        :return: Dictionary containing the invoice status.
        """
        url = f"{self.base_url}/collection/v2_0/invoice/{reference_id}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "X-Target-Environment": target_environment,
            **self.headers
        }
        response = requests.get(url, headers=headers)
        return self.validate_response(response)

    def cancel_invoice(self, reference_id: str, access_token: str, external_id: str, target_environment: str = "sandbox") -> requests.Response:
        """
        Cancel an invoice.

        :param reference_id: UUID of the invoice.
        :param access_token: Bearer Authentication Token.
        :param external_id: External ID used as a reference to the transaction.
        :param target_environment: The target environment (default is "sandbox").
        :return: Response object.
        """
        url = f"{self.base_url}/collection/v2_0/invoice/{reference_id}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "X-Target-Environment": target_environment,
            **self.headers
        }
        payload = {
            "externalId": external_id
        }
        response = requests.delete(url, json=payload, headers=headers)
        return response

    def create_pre_approval(self, reference_id: str, access_token: str, payer: Dict[str, str], payer_currency: str, payer_message: str, validity_time: int, target_environment: str = "sandbox") -> requests.Response:
        """
        Create a pre-approval for a payment.

        :param reference_id: UUID Reference ID for the pre-approval.
        :param access_token: Bearer Authentication Token.
        :param payer: Dictionary with 'partyIdType' and 'partyId' keys identifying the payer.
        :param payer_currency: ISO4217 Currency code of the payer.
        :param payer_message: Message to the end user.
        :param validity_time: The time duration in seconds that the pre-approval is valid.
        :param target_environment: The target environment (default is "sandbox").
        :return: Response object.
        """
        url = f"{self.base_url}/collection/v2_0/preapproval"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "X-Callback-Url": "https://clinic.com",  # Add your callback URL here if needed
            "X-Reference-Id": reference_id,
            "X-Target-Environment": target_environment,
            **self.headers
        }
        payload = {
            "payer": payer,
            "payerCurrency": payer_currency,
            "payerMessage": payer_message,
            "validityTime": validity_time
        }
        response = requests.post(url, json=payload, headers=headers)
        return response

    def get_pre_approval_status(self, reference_id: str, access_token: str, target_environment: str = "sandbox") -> Dict[str, Any]:
        """
        Get the status of a pre-approval.

        :param reference_id: UUID of the pre-approval.
        :param access_token: Bearer Authentication Token.
        :param target_environment: The target environment (default is "sandbox").
        :return: Dictionary containing the pre-approval status.
        """
        url = f"{self.base_url}/collection/v2_0/preapproval/{reference_id}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "X-Target-Environment": target_environment,
            **self.headers
        }
        response = requests.get(url, headers=headers)
        return self.validate_response(response)

    def cancel_pre_approval(self, preapproval_id: str, access_token: str, target_environment: str = "sandbox") -> requests.Response:
        """
        Cancel a pre-approval.

        :param preapproval_id: UUID of the pre-approval.
        :param access_token: Bearer Authentication Token.
        :param target_environment: The target environment (default is "sandbox").
        :return: Response object.
        """
        url = f"{self.base_url}/collection/v1_0/preapproval/{preapproval_id}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "X-Target-Environment": target_environment,
            **self.headers
        }
        response = requests.delete(url, headers=headers)
        return response

    def get_approved_pre_approvals(self, account_holder_id_type: str, account_holder_id: str, access_token: str, target_environment: str = "sandbox") -> List[Dict[str, Any]]:
        """
        Get approved pre-approvals of an account holder.

        :param account_holder_id_type: Type of the account holder ID (e.g., "msisdn", "email").
        :param account_holder_id: The account holder ID.
        :param access_token: Bearer Authentication Token.
        :param target_environment: The target environment (default is "sandbox").
        :return: List of dictionaries containing pre-approval details.
        """
        url = f"{self.base_url}/collection/v1_0/preapprovals/{account_holder_id_type}/{account_holder_id}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "X-Target-Environment": target_environment,
            **self.headers
        }
        response = requests.get(url, headers=headers)
        return self.validate_response(response)

    def create_payment(self, reference_id: str, access_token: str, external_transaction_id: str, amount: float, currency: str, customer_reference: str, service_provider_user_name: str, target_environment: str = "sandbox") -> requests.Response:
        """
        Create a payment for an external bill or air-time top-up.

        :param reference_id: UUID Reference ID for the payment.
        :param access_token: Bearer Authentication Token.
        :param external_transaction_id: External transaction ID to tie to the payment.
        :param amount: Amount to be debited from the payer account.
        :param currency: ISO4217 Currency code.
        :param customer_reference: Customer reference for the provider.
        :param service_provider_user_name: Service provider name.
        :param target_environment: The target environment (default is "sandbox").
        :return: Response object.
        """
        url = f"{self.base_url}/collection/v2_0/payment"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "X-Callback-Url": "https://clinic.com",  # Add your callback URL here if needed
            "X-Reference-Id": reference_id,
            "X-Target-Environment": target_environment,
            **self.headers
        }
        payload = {
            "externalTransactionId": external_transaction_id,
            "money": {
                "amount": float(amount),
                "currency": currency
            },
            "customerReference": customer_reference,
            "serviceProviderUserName": service_provider_user_name
        }
        response = requests.post(url, json=payload, headers=headers)
        return response

    def get_payment_status(self, reference_id: str, access_token: str, target_environment: str = "sandbox") -> Dict[str, Any]:
        """
        Get the status of a payment.

        :param reference_id: UUID of the payment.
        :param access_token: Bearer Authentication Token.
        :param target_environment: The target environment (default is "sandbox").
        :return: Dictionary containing the payment status.
        """
        url = f"{self.base_url}/collection/v2_0/payment/{reference_id}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "X-Target-Environment": target_environment,
            **self.headers
        }
        response = requests.get(url, headers=headers)
        return self.validate_response(response)
