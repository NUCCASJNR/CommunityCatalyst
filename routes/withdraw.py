#!/usr/bin/env python3

from flask import render_template, redirect, url_for, flash, request, jsonify, Response, session
from flask_login import login_required, current_user
from os import getenv
from models.withdraw import WithDraw
from forms.withdraw import WithdrawalForm, ValidationError
from models.project import Project
from routes.payment_handler import logging
from routes import frontend

def send_withdrawal_email(email):
    """Send withdrawal email to the admin"""
    API_KEY = getenv("ELASTIC_EMAIL")
    sender = 'community-catalyst@polyglotte.tech'
    receiver = email
    subject = "Withdrawal request"
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

@frontend.route("/withdraw", methods=["GET", "POST"])
@login_required
def withdraw():
    form = WithdrawalForm()
    if form.validate_on_submit():
        # Verify the withdrawal amount
        withdrawal_verification = form.verify_withdrawal_amount(form.amount.data)
        if withdrawal_verification != "Amount verified":
            flash(withdrawal_verification, "danger")
            return render_template("withdrawal.html", form=form)
        
        # Check if the project exists


        project_id = form.project_id.data
        logging.info("Project ID:", project_id)
        project = Project.find_obj_by(id=project_id)
        if not project:
            flash("Project not found", "danger")
            return render_template("withdrawal.html", form=form)

        # Create and save the withdrawal if everything is valid
        withdraw = WithDraw(
            acc_name=form.acc_name.data,
            acc_number=form.acc_number.data,
            bank=form.bank.data,
            user=current_user,
            amount=form.amount.data,
            campaign_name=form.campaign_name.data,
            project_id=project_id,
            status="pending"
        )
        withdraw.save()
        flash("Withdrawal request sent successfully", "success")
        return redirect(url_for("frontend.home"))
    return render_template("withdrawal.html", form=form)

@frontend.route("/user_withdrawals", methods=["GET"])
@login_required
def user_withdrawals():
    """Get all withdrawals made by the current user"""
    user_withdrawals = WithDraw.query.filter_by(user_id=current_user.id).all()
    return render_template("withdraw.html", user_withdrawals=user_withdrawals)
