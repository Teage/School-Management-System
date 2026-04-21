from flask import  session, flash, redirect, url_for


def logout_user():
    # session.pop('logged_in', None)  # Remove the logged_in key from the session
    # session.pop('user_type', None)  # Remove the user_type key from the session
    session.clear()  # Clear all session data
    flash("You have been logged out.", "success")
    return redirect(url_for('login_page'))