#!/usr/bin/env python3

"""Paystack payment handler"""
import json
from os import getenv
import requests
from flask import request, jsonify, render_template
from models.project import Project
from routes import frontend
from config import app
from models.contribution import Contribution

paystack_key = getenv('PAYSTACK_KEY')


def create_payment_link(project_id, amount):
    """
    Initialized the paystack payment link
    project_id: Id of the project to be funded
    amount: Amount to be funded
    """
    paystack_endpoint = "https://paystack.com/pay/zp9vahq-0s"
    headers = {
        'Authorization': f'Bearer {paystack_key}',
        'Content-Type': 'application/json',
    }
    data = {
        'amount': amount * 100,  # Paystack expects amount in kobo
        'reference': f'project_{project_id}_payment',
        'currency': 'NGN',
        'callback_url': 'https://community-catalyst.codewithalareef.tech/callback',
        'metadata': {
            'project_id': project_id,
        }
    }
    requests.post(paystack_endpoint, headers=headers, data=json.dumps(data))
#     print(response.json())
#
# create_payment_link(23, 200)
#


def update_project_raised_amount(project_id, amount):
    """
    Updates a project raised amount
    project_id: project id
    amount: amount funded
    """
    obj = {"id": project_id}
    query = Project.find_obj_by(**obj)
    if query:
        query.raised += amount
    return f'Project with id: {project_id} not found'


def record_contribution(project_id, amount):
    contribution = Contribution(
        project_id=project_id,
        amount=amount
    )
    contribution.save()


@frontend.route('/paystack-callback', methods=['POST'])
def paystack_callback():
    data = request.get_json()
    if data['status'] == 'success':
        project_id = data['metadata']['project_id']
        amount_funded = data['amount'] / 100
        if amount_funded <= 50000:
            amount_funded = amount_funded - 50
        else:
            amount_funded = amount_funded - 100
        update_project_raised_amount(project_id, amount_funded)


@frontend.route('/pay/<int:project_id>', methods=['GET'])
def initiate_payment(project_id):
    if request.method == 'POST':
        amount = float(request.form.get('amount'))
        create_payment_link(project_id, amount)
        return render_template('payment.html')
    else:
        return render_template('payment-form.html')