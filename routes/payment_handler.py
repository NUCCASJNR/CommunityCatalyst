#!/usr/bin/env python3

"""Paystack payment handler"""
import json
from os import getenv
import requests
from flask_login import current_user
from flask import request, render_template, redirect, url_for, flash, session
import time
from models.project import Project
from forms.payment import PaymentForm, AuthPaymentForm
from routes import frontend
from models.contribution import Contribution
from models.user import User
from models.withdraw import WithDraw
from forms.withdraw import WithdrawalForm
import logging
from paystackapi.paystack import Paystack
import secrets
from utils.redis_client import RedisClient
from decimal import Decimal

paystack_key = getenv('PAYSTACK_KEY')

logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='w')


def create_payment_link(project_id, amount, user_id, email):
    """
    Create a Paystack payment link for a given project and amount.

    Args:
        project_id (int): The ID of the project to be funded.
        amount (float): The amount to be funded.

    Returns:
        str: The Paystack authorization URL for payment initiation, or an error message if there was an error.

    Raises:
        None

    This function initializes the Paystack payment link for a specific project and amount, then returns
    the authorization URL for payment initiation. In case of an error, it logs an error message and returns an error message.
    """
    try:
        token = secrets.token_hex(6)
        reference = f'project_{project_id}_user_{user_id}_time_{token}'
        paystack_endpoint = "https://api.paystack.co/transaction/initialize"
        headers = {
            'Authorization': f'Bearer {paystack_key}',
            'Content-Type': 'application/json',
        }
        data = {
            'amount': float(amount) * 100,  # Convert to float and then to kobo
            'email': email,
            'reference': reference,
            'currency': 'NGN',
            'callback_url': 'https://community-catalyst.codewithalareef.tech/callback',
            'metadata': {
                'project_id': project_id,
            }
        }
        response = None
        response = requests.post(paystack_endpoint, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            return result
        else:
            # Log the error response for debugging
            logging.error(f'Error creating payment link: {response.status_code}')
            logging.error(f'Response from Paystack API: {response.text}')
            return f"Error: {response.status_code} - {response.text}"
    except requests.exceptions.RequestException as network_error:
        logging.error(f'Network error creating payment link: {network_error}')
        return f'Network error creating payment link: {network_error}'
    except Exception as e:
        logging.error(f'Error creating payment link: {e}')
        return f'Error creating payment link: {e}'


def verify_transaction_status(reference):
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {
        'Authorization': f'Bearer {paystack_key}'
    }
    response = requests.get(url, headers=headers)  # Make the API call to verify the transaction

    if response.status_code == 200:
        result = response.json()
        if result['status'] == True and result['data']['status'] == 'success':
            return True
    return False


def send_user_project_funded_notification(project_id, amount, email, username):
    """
    Send a notification to the project owner when their project is funded.

    Args:
        project_id (int): The ID of the project that was funded.

    Returns:
        None

    Raises:
        None

    This function sends a notification to the project owner when their project is funded.
    """
    API_KEY = getenv("ELASTIC_EMAIL")
    sender = 'community-catalyst@polyglotte.tech'
    receiver = email
    subject = 'Project funded notification'
    html_body = render_template('fund_notification.html', email=email, amount=amount, username=username, project_id=project_id)
    url = 'https://api.elasticemail.com/v2/email/send'

    request_payload = {
        'apikey': API_KEY,
        'from': sender,
        'to': receiver,
        'subject': subject,
        'bodyHtml': html_body,
        'isTransactional': False
    }
    response = requests.post(url, data=request_payload)
    if response.status_code == 200:
        print(response.json())
    else:
        print(f'Error occurred with error code: {response.status_code}')


def send_donor_email(project_id, amount, email, username):
    """Docs soon"""
    API_KEY = getenv("ELASTIC_EMAIL")
    sender = 'community-catalyst@polyglotte.tech'
    receiver = email
    subject = "Your Support Makes a Difference"
    html_body = render_template('donor.html', email=email, amount=amount, username=username,
                                project_id=project_id)
    url = 'https://api.elasticemail.com/v2/email/send'

    request_payload = {
        'apikey': API_KEY,
        'from': sender,
        'to': receiver,
        'subject': subject,
        'bodyHtml': html_body,
        'isTransactional': False
    }
    response = requests.post(url, data=request_payload)
    if response.status_code == 200:
        print(response.json())
    else:
        print(f'Error occurred with error code: {response.status_code}')

def verify_project_raised_amount(amount, project_id):
    """
    Verify if the project has reached its target amount.

    Args:
        amount (float): The amount to be contributed.
        project_id (str): The ID of the project.

    Returns:
        bool: True if the project has reached its target amount, False otherwise.

    Raises:
        None

    This function verifies if the project has reached its target amount by comparing the current amount
    to the target amount.
    """
    project = Project.find_obj_by(id=project_id)
    if project:
        if project.amount_left <= amount:
            flash(f'The project has already reached its target amount. You can no longer contribute.', 'success')
            return True
        else:
            return False
    else:
        flash(f'Project with id {project_id} not found', 'error')
        logging.debug(f'Creating payment link for project_id {project_id} and amount {amount}')


def update_project_raised_amount(project_id, amount):
    """
    Update the raised amount of a project after receiving a contribution.

    Args:
        project_id (int): The ID of the project being funded.
        amount (float): The amount contributed by the user.

    Returns:
        None

    Raises:
        None

    This function updates the raised amount of a project by adding the amount contributed by the user.
    If the project is not found, it logs an error message.

    """
    project = Project.find_obj_by(id=project_id)
    query = User.find_obj_by(**{'id': project.user_id })
    email = query.email
    username = query.username
    if project:
        amount = Decimal(amount)
        project.current_amount += amount
        project.save()
        send_user_project_funded_notification(project_id, amount, email, username)
    else:
        flash(f'Project with id {project_id} not found', 'error')
        logging.debug(f'Creating payment link for project_id {project_id} and amount {amount}')


def record_contribution(project_id, amount, user_id):
    """
      Record a contribution in the contributions table for tracking.

      Args:
          project_id (int): The ID of the project to which the contribution is made.
          amount (float): The amount contributed by the user.

      Returns:
          None

      Raises:
          None

      This function records a contribution in the contributions table, associating it with the specific project.
    """
    try:
        # Log the inputs for debugging
        logging.info(f'Recording contribution - project_id: {project_id}, amount: {amount}')

        contribution = Contribution(
            user_id=user_id,
            project_id=project_id,
            amount=amount
        )
        contribution.save()
    except Exception as e:
        logging.error(f'Error recording contribution: {e}')



@frontend.route('/pay/<string:project_id>', methods=['GET', 'POST'])
def initiate_payment(project_id):
    """
    Initialize the payment process for a project by rendering the payment form.

    Args:
        project_id (int): The ID of the project to be funded.

    Returns:
        Renders the payment form template.

    Raises:
        None

    This function renders the payment form template for the user to enter the contribution amount.
    Upon successful form submission, it initiates the payment process by redirecting to the Paystack payment page.
    """
    amount = 0
    user_id = ''
    user_email = ''

    # Attempt to find the project by its ID
    project = Project.find_obj_by(id=project_id)

    # Check if the project was found
    if project is None:
        flash("Project not found", 'error')
        return redirect(url_for('frontend.home'))

    if not current_user.is_anonymous:
        user_id = current_user.id

        # Check if the user is the owner of the project
        if project.user_id == user_id:
            flash("You can't fund your own project", 'danger')
            return redirect(url_for('frontend.home'))

    form = PaymentForm()
    auth_form = AuthPaymentForm()

    if form.validate_on_submit():
        amount = form.amount.data
        user_id = secrets.token_hex(6)
        user_email = form.email.data

        if verify_project_raised_amount(amount, project_id):
            flash("The project has already reached its target amount. You can no longer contribute.", 'success')
            return redirect(url_for('frontend.home'))

    if auth_form.validate_on_submit():
        amount = auth_form.amount.data

        if not current_user.is_anonymous:
            username = current_user.username
            user_id = current_user.id
            user_email = current_user.email

        # Ensure the project is still available
        project = Project.find_obj_by(id=project_id)

        if project is None:
            flash("Project not found", 'error')
            return redirect(url_for('frontend.home'))

        if verify_project_raised_amount(amount, project_id):
            flash("The project has already reached its target amount. You can no longer contribute.", 'success')
            return redirect(url_for('frontend.home'))

        url = create_payment_link(project_id, amount, user_id, user_email)
        authorization_url = url['data']['authorization_url']

        if not authorization_url.startswith('Error'):
            if amount <= 50000:
                amount -= 50
            else:
                amount -= 100

            session['payment_reference'] = url['data']['reference']
            session['amount'] = amount
            session['project_id'] = project_id
            session['user_id'] = user_id
            session['donor_email'] = user_email
            session['donor_username'] = username or ''
            return redirect(authorization_url)

    return render_template('payment.html', form=form, auth_form=auth_form, project_id=project_id)



@frontend.route('/callback', methods=['GET'])
def paystack_callback():
    # Retrieve the payment reference and other necessary data from the session
    payment_reference = session.get('payment_reference')
    amount = session.get('amount')
    project_id = session.get('project_id')
    user_id = session.get('user_id')
    email = session.get('donor_email')
    username = session.get('donor_username')

    if payment_reference is not None:
        # Call verify_transaction_status with the payment reference
        if verify_transaction_status(payment_reference):
            # Update project raised amount and record contribution
            update_project_raised_amount(project_id, amount)
            record_contribution(project_id, amount, user_id)
            send_donor_email(project_id, amount, email, username)
            flash('Payment successful', 'success')
            logging.info(f'Payment successful for project_id {project_id} and amount {amount}')
        else:
            flash('Payment failed', 'danger')
            logging.info(f'Payment failed for project_id {project_id} and amount {amount}')
    else:
        flash('Payment reference not found', 'danger')

    return redirect(url_for('frontend.home'))

