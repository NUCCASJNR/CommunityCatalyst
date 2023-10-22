#!/usr/bin/env python3
import time

from models.user import User, db
from models.base_model import app
from datetime import datetime
import schedule


def delete_expired_users():
    with app.app_context():
        print("delete_expired_users function called")
        current_time = datetime.now()
        users_to_delete = User.query.filter(User.verified == 0, User.verification_expires_at < current_time).all()
        print(f"Checking users at {current_time}")

        for user in users_to_delete:
            User.query.filter_by(id=user.id).delete()
            print(f"Deleted user with ID: {user.id}")

        db.session.commit()
        print("Committing changes")


schedule.every(5).minutes.do(delete_expired_users)
while True:
    schedule.run_pending()
    time.sleep(1)
