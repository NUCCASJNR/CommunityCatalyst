#!/usr/bin/env python3

"""Paystack payment handler"""
import json
from os import getenv
import requests
from flask_login import current_user
from flask import request, render_template, redirect, url_for, flash
from models.project import Project
from forms.payment import PaymentForm
from routes import frontend
from models.contribution import Contribution
import logging
from paystackapi.paystack import  Paystack
import secrets
paystack_key = getenv('PAYSTACK_KEY')

logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='w')


def create_payment_link(project_id, amount, user_id):
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
        paystack_endpoint = "https://api.paystack.co/transaction/initialize"
        headers = {
            'Authorization': f'Bearer {paystack_key}',
            'Content-Type': 'application/json',
        }
        data = {
            'amount': float(amount) * 100,  # Paystack expects amount in kobo
            'reference': f'project_{project_id}_user_{user_id}_payment',
            'currency': 'NGN',
            'callback_url': 'https://community-catalyst.codewithalareef.tech/paystack-callback',
            'metadata': {
                'project_id': project_id,
            }
        }
        response = None
        response = requests.post(paystack_endpoint, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            return result['data']['authorization_url']  
        else:
            # Handle the error or return an error message
            logging.error(f'Error creating payment link: {response.status_code}')
            return f"Error: {response.status_code} - {response.text}"
    except requests.exceptions.RequestException as network_error:
        logging.error(f'Network error creating payment link: {network_error}')
        return f'Network error creating payment link: {network_error}'
    except Exception as e:
        logging.error(f'Error creating payment link: {e}')
        logging.error(f'Response from Paystack API: {response.text}')  # Log the response for debugging
        return f'Error creating payment link: {e}'


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
        project.raised += amount
        project.save()
    else:
        # flash(f'Project with id {project_id} not found', 'error')
        logging.debug(f'Creating payment link for project_id {project_id} and amount {amount}')


def record_contribution(project_id, amount):
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
    contribution = Contribution(
        project_id=project_id,
        amount=amount
    )
    contribution.save()


@frontend.route('/paystack-callback', methods=['POST'])
def paystack_callback():
    """
      Handle the callback from Paystack after a payment is completed.

      Args:
          None

      Returns:
          Redirect to the project page.

      Raises:
          None

      This function handles the callback from Paystack after a payment is completed. It updates the project's
      raised amount and displays a success or error message to the user.
      """
    data = request.get_json()
    if data['status'] == 'success':
        project_id = data['metadata']['project_id']
        amount_funded = data['amount'] / 100
        if amount_funded <= 50000:
            amount_funded -= 50
        else:
            amount_funded -= 100
        update_project_raised_amount(project_id, amount_funded)
        flash('Payment successful!', 'success')
    else:
        flash('Payment failed.', 'error')
    return redirect(url_for('frontend.project', project_id=project_id))


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
        else:
            user_id = secrets.token_hex(6)
        authorization_url = create_payment_link(project_id, amount, user_id)
        if authorization_url.startswith('Error'):
            flash('Error creating payment link', 'error')
            return redirect(url_for('frontend.project', project_id=project_id))
        return redirect(authorization_url)
    return render_template('payment.html', form=form)
