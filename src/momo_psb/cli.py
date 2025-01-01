import json
import uuid

import click

from .api import MoMoPSBAPI


class Config:
    def __init__(self):
        self.api = None


pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@click.option("--base-url", required=True, help="Base URL for the Wallet Platform API")
@click.option(
    "--subscription-key",
    required=True,
    help="Subscription key for the API Manager portal",
)
@pass_config
def cli(config, base_url: str, subscription_key: str):
    """MTN MoMo Payment Service Bank CLI tool"""
    config.api = MoMoPSBAPI(base_url, subscription_key)


# User Management Commands
@cli.group()
def user():
    """User management commands"""
    pass


@user.command("create")
@click.option("--callback-host", required=True, help="Provider callback host")
@pass_config
def create_user(config, callback_host: str):
    """Create a new API user"""
    reference_id = str(uuid.uuid4())
    response = config.api.create_api_user(reference_id, callback_host)
    click.echo(f"API User created with reference ID: {reference_id}")
    click.echo(f"Status Code: {response.status_code}")


@user.command("create-key")
@click.argument("api-user")
@pass_config
def create_key(config, api_user: str):
    """Create a new API key for user"""
    response = config.api.create_api_key(api_user)
    click.echo(f"API Key created for user {api_user}")
    click.echo(f"Response: {response.text}")


@user.command("get-details")
@click.argument("api-user")
@pass_config
def get_user_details(config, api_user: str):
    """Get API user details"""
    response = config.api.get_api_user_details(api_user)
    click.echo(f"User Details: {response.text}")


@user.command("get-token")
@click.argument("api-user")
@click.argument("api-key")
@pass_config
def get_token(config, api_user: str, api_key: str):
    """Get OAuth token"""
    response = config.api.get_oauth_token(api_user, api_key)
    click.echo(f"OAuth Token Response: {response.text}")


# Account Commands
@cli.group()
def account():
    """Account management commands"""
    pass


@account.command("balance")
@click.option("--access-token", required=True, help="Bearer Authentication Token")
@click.option("--environment", default="sandbox", help="Target environment")
@pass_config
def get_balance(config, access_token: str, environment: str):
    """Get account balance"""
    try:
        result = config.api.get_account_balance(access_token, environment)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)


@account.command("validate-holder")
@click.option("--access-token", required=True, help="Bearer Authentication Token")
@click.option("--id-type", required=True, help="Account holder ID type")
@click.option("--id", required=True, help="Account holder ID")
@click.option("--environment", default="sandbox", help="Target environment")
@pass_config
def validate_account_holder(
    config, access_token: str, id_type: str, id: str, environment: str
):
    """Validate account holder status"""
    result = config.api.validate_account_holder_status(
        access_token, id_type, id, environment
    )
    click.echo(json.dumps(result, indent=2))


@account.command("basic-info")
@click.option("--access-token", required=True, help="Bearer Authentication Token")
@click.option("--id-type", required=True, help="Account holder ID type")
@click.option("--id", required=True, help="Account holder ID")
@click.option("--environment", default="sandbox", help="Target environment")
@pass_config
def get_basic_info(config, access_token: str, id_type: str, id: str, environment: str):
    """Get basic user information"""
    result = config.api.get_basic_user_info(access_token, id_type, id, environment)
    click.echo(json.dumps(result, indent=2))


# Payment Commands
@cli.group()
def payment():
    """Payment management commands"""
    pass


@payment.command("request")
@click.option("--access-token", required=True, help="Bearer Authentication Token")
@click.option("--amount", required=True, type=float, help="Amount to request")
@click.option("--currency", required=True, help="Currency code (e.g., NGN)")
@click.option("--payer-id", required=True, help="Payer ID")
@click.option("--payer-id-type", required=True, help="Payer ID type (e.g., MSISDN)")
@click.option("--message", required=True, help="Payer message")
@click.option("--note", required=True, help="Payee note")
@click.option("--environment", default="sandbox", help="Target environment")
@pass_config
def request_payment(
    config,
    access_token: str,
    amount: float,
    currency: str,
    payer_id: str,
    payer_id_type: str,
    message: str,
    note: str,
    environment: str,
):
    """Request payment from a payer"""
    reference_id = str(uuid.uuid4())
    external_id = str(uuid.uuid4())
    payer = {"partyIdType": payer_id_type, "partyId": payer_id}

    response = config.api.request_to_pay(
        reference_id=reference_id,
        access_token=access_token,
        amount=amount,
        currency=currency,
        external_id=external_id,
        payer=payer,
        payer_message=message,
        payee_note=note,
    )

    click.echo(f"Payment request created with reference ID: {reference_id}")
    click.echo(f"Status Code: {response.status_code}")


@payment.command("status")
@click.option("--access-token", required=True, help="Bearer Authentication Token")
@click.argument("reference-id")
@click.option("--environment", default="sandbox", help="Target environment")
@pass_config
def get_payment_status(config, access_token: str, reference_id: str, environment: str):
    """Get payment request status"""
    result = config.api.get_request_to_pay_status(
        reference_id, access_token, environment
    )
    click.echo(json.dumps(result, indent=2))


@payment.command("create")
@click.option("--access-token", required=True, help="Bearer Authentication Token")
@click.option("--external-id", required=True, help="External transaction ID")
@click.option("--amount", required=True, type=float, help="Amount")
@click.option("--currency", required=True, help="Currency code")
@click.option("--customer-ref", required=True, help="Customer reference")
@click.option("--provider-user", required=True, help="Service provider username")
@click.option("--environment", default="sandbox", help="Target environment")
@pass_config
def create_payment(
    config,
    access_token: str,
    external_id: str,
    amount: float,
    currency: str,
    customer_ref: str,
    provider_user: str,
    environment: str,
):
    """Create a payment"""
    reference_id = str(uuid.uuid4())
    response = config.api.create_payment(
        reference_id=reference_id,
        access_token=access_token,
        external_transaction_id=external_id,
        amount=amount,
        currency=currency,
        customer_reference=customer_ref,
        service_provider_user_name=provider_user,
        target_environment=environment,
    )
    click.echo(f"Payment created with reference ID: {reference_id}")
    click.echo(f"Status Code: {response.status_code}")


# Withdrawal Commands
@cli.group()
def withdraw():
    """Withdrawal management commands"""
    pass


@withdraw.command("request")
@click.option("--access-token", required=True, help="Bearer Authentication Token")
@click.option("--amount", required=True, type=float, help="Amount to withdraw")
@click.option("--currency", required=True, help="Currency code")
@click.option("--payer-id", required=True, help="Payer ID")
@click.option("--payer-id-type", required=True, help="Payer ID type")
@click.option("--message", required=True, help="Payer message")
@click.option("--note", required=True, help="Payee note")
@click.option("--environment", default="sandbox", help="Target environment")
@pass_config
def request_withdrawal(
    config,
    access_token: str,
    amount: float,
    currency: str,
    payer_id: str,
    payer_id_type: str,
    message: str,
    note: str,
    environment: str,
):
    """Request a withdrawal"""
    reference_id = str(uuid.uuid4())
    external_id = str(uuid.uuid4())
    payer = {"partyIdType": payer_id_type, "partyId": payer_id}

    response = config.api.request_to_withdraw(
        reference_id=reference_id,
        access_token=access_token,
        amount=amount,
        currency=currency,
        external_id=external_id,
        payer=payer,
        payer_message=message,
        payee_note=note,
        target_environment=environment,
    )
    click.echo(f"Withdrawal request created with reference ID: {reference_id}")
    click.echo(f"Status Code: {response.status_code}")


@withdraw.command("status")
@click.option("--access-token", required=True, help="Bearer Authentication Token")
@click.argument("reference-id")
@click.option("--environment", default="sandbox", help="Target environment")
@pass_config
def get_withdrawal_status(
    config, access_token: str, reference_id: str, environment: str
):
    """Get withdrawal request status"""
    result = config.api.get_request_to_withdraw_status(
        reference_id, access_token, environment
    )
    click.echo(json.dumps(result, indent=2))


# Invoice Commands
@cli.group()
def invoice():
    """Invoice management commands"""
    pass


@invoice.command("create")
@click.option("--access-token", required=True, help="Bearer Authentication Token")
@click.option("--external-id", required=True, help="External ID")
@click.option("--amount", required=True, type=float, help="Amount")
@click.option("--currency", required=True, help="Currency code")
@click.option("--validity", required=True, help="Validity duration in seconds")
@click.option("--payer-id", required=True, help="Intended payer ID")
@click.option("--payer-id-type", required=True, help="Intended payer ID type")
@click.option("--payee-id", required=True, help="Payee ID")
@click.option("--payee-id-type", required=True, help="Payee ID type")
@click.option("--description", help="Invoice description")
@click.option("--environment", default="sandbox", help="Target environment")
@pass_config
def create_invoice(
    config,
    access_token: str,
    external_id: str,
    amount: float,
    currency: str,
    validity: str,
    payer_id: str,
    payer_id_type: str,
    payee_id: str,
    payee_id_type: str,
    description: str,
    environment: str,
):
    """Create an invoice"""
    reference_id = str(uuid.uuid4())
    intended_payer = {"partyIdType": payer_id_type, "partyId": payer_id}
    payee = {"partyIdType": payee_id_type, "partyId": payee_id}

    response = config.api.create_invoice(
        reference_id=reference_id,
        access_token=access_token,
        external_id=external_id,
        amount=amount,
        currency=currency,
        validity_duration=validity,
        intended_payer=intended_payer,
        payee=payee,
        description=description,
        target_environment=environment,
    )
    click.echo(f"Invoice created with reference ID: {reference_id}")
    click.echo(f"Status Code: {response.status_code}")


@invoice.command("status")
@click.option("--access-token", required=True, help="Bearer Authentication Token")
@click.argument("reference-id")
@click.option("--environment", default="sandbox", help="Target environment")
@pass_config
def get_invoice_status(config, access_token: str, reference_id: str, environment: str):
    """Get invoice status"""
    result = config.api.get_invoice_status(reference_id, access_token, environment)
    click.echo(json.dumps(result, indent=2))


@invoice.command("cancel")
@click.option("--access-token", required=True, help="Bearer Authentication Token")
@click.argument("reference-id")
@click.option("--external-id", required=True, help="External ID")
@click.option("--environment", default="sandbox", help="Target environment")
@pass_config
def cancel_invoice(
    config, access_token: str, reference_id: str, external_id: str, environment: str
):
    """Cancel an invoice"""
    response = config.api.cancel_invoice(
        reference_id, access_token, external_id, environment
    )
    click.echo(f"Invoice cancellation status code: {response.status_code}")


# Pre-approval Commands
@cli.group()
def preapproval():
    """Pre-approval management commands"""
    pass


@preapproval.command("create")
@click.option("--access-token", required=True, help="Bearer Authentication Token")
@click.option("--payer-id", required=True, help="Payer ID")
@click.option("--payer-id-type", required=True, help="Payer ID type")
@click.option("--currency", required=True, help="Payer currency")
@click.option("--message", required=True, help="Payer message")
@click.option("--validity", required=True, type=int, help="Validity time in seconds")
@click.option("--environment", default="sandbox", help="Target environment")
@pass_config
def create_preapproval(
    config,
    access_token: str,
    payer_id: str,
    payer_id_type: str,
    currency: str,
    message: str,
    validity: int,
    environment: str,
):
    """Create a pre-approval"""
    reference_id = str(uuid.uuid4())
    payer = {"partyIdType": payer_id_type, "partyId": payer_id}

    response = config.api.create_pre_approval(
        reference_id=reference_id,
        access_token=access_token,
        payer=payer,
        payer_currency=currency,
        payer_message=message,
        validity_time=validity,
        target_environment=environment,
    )
    click.echo(f"Pre-approval created with reference ID: {reference_id}")
    click.echo(f"Status Code: {response.status_code}")


@preapproval.command("status")
@click.option("--access-token", required=True, help="Bearer Authentication Token")
@click.argument("reference-id")
@click.option("--environment", default="sandbox", help="Target environment")
@pass_config
def get_preapproval_status(
    config, access_token: str, reference_id: str, environment: str
):
    """Get pre-approval status"""
    result = config.api.get_pre_approval_status(reference_id, access_token, environment)
    click.echo(json.dumps(result, indent=2))


@preapproval.command("cancel")
@click.option("--access-token", required=True, help="Bearer Authentication Token")
@click.argument("preapproval-id")
@click.option("--environment", default="sandbox", help="Target environment")
@pass_config
def cancel_preapproval(
    config, access_token: str, preapproval_id: str, environment: str
):
    """Cancel a pre-approval"""
    response = config.api.cancel_pre_approval(preapproval_id, access_token, environment)
    click.echo(f"Pre-approval cancellation status code: {response.status_code}")


@preapproval.command("list-approved")
@click.option("--access-token", required=True, help="Bearer Authentication Token")
@click.option("--id-type", required=True, help="Account holder ID type")
@click.option("--id", required=True, help="Account holder ID")
@click.option("--environment", default="sandbox", help="Target environment")
@pass_config
def list_approved_preapprovals(
    config, access_token: str, id_type: str, id: str, environment: str
):
    """List approved pre-approvals for an account holder"""
    result = config.api.get_approved_pre_approvals(
        id_type, id, access_token, environment
    )
    click.echo(json.dumps(result, indent=2))


def main():
    cli()


if __name__ == "__main__":
    main()
