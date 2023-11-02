#!/usr/bin/env python3

from flask import render_template, redirect, url_for, flash, request, jsonify, Response, session
from flask_login import login_required, current_user
from os import getenv
from models.withdraw import WithDraw
from forms.withdraw import WithdrawalForm, ValidationError
from models.project import Project
from routes import frontend

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
        return redirect(url_for("frontend.index"))
    return render_template("withdrawal.html", form=form)
