#!/usr/bin/env python3

"""Paystack payment handler"""
import json
from os import getenv
import requests
from flask_login import current_user
from flask import request, render_template, redirect, url_for, flash
import time
from models.project import Project
from forms.payment import PaymentForm
from routes import frontend
from models.contribution import Contribution
import logging
from paystackapi.paystack import  Paystack
import secrets
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
            'callback_url': 'https://community-catalyst.codewithalareef.tech',
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
            'Authorization': f'Bearer {paystack_key}',
            'Content-Type': 'application/json',
        }
    response = requests.get(url, headers=headers)  # Make the API call to verify the transaction

    if response.status_code == 200:
        result = response.json()
        if result['status'] == True and result['data']['status'] == 'success':
            return True
    return False


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
    if project:
        project.current_amount += amount
        project.save()
    else:
        # flash(f'Project with id {project_id} not found', 'error')
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
    form = PaymentForm()
    if form.validate_on_submit():
        amount = form.amount.data
        if current_user.is_authenticated:
            user_id = current_user.id
            user_email = current_user.email
        else:
            user_id = secrets.token_hex(6)
            user_email = 'anon@gmail.com'
        project = Project.find_obj_by(id=project_id)
        if project.user_id == user_id:
            flash("You can't fund your own project", 'danger')
            return redirect(url_for('frontend.home'))
        url = create_payment_link(project_id, amount, user_id, user_email)
        authorization_url = url['data']['authorization_url'] 
        # Check if the authorization URL is successfully generated
        if not authorization_url.startswith('Error'):
            if amount <= 50000:
                amount -= 50
            else:
                amount -= 100

            # Redirect to Paystack payment page
            return redirect(authorization_url)

    # Capture the Paystack reference when the user returns
    reference = request.args.get('reference') or request.args.get('trxref')

    if reference:
        if verify_transaction_status(reference):
            # Payment was successful, update project and record contribution
            update_project_raised_amount(project_id, amount)
            record_contribution(project_id, amount, user_id)
            flash('Payment was successful!', 'success')
        else:
            flash('Payment was not successful!', 'error')

    return render_template('payment.html', form=form, project_id=project_id)
