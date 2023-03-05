from flask import (
    Flask,
    request,
    flash,
    session,
    url_for,
    redirect,
    Blueprint,
    render_template,
)

import logging
import modules.users.readwrite_validusers
from modules.authentication import get_user_role_db, validate_user_role
from passlib.context import CryptContext
import os

logging.basicConfig(level=logging.WARN)
logging.debug("program users")
logging.captureWarnings(True)

users_blueprint_routes = Blueprint("users_blueprint_routes", __name__)


ctx = CryptContext(
    schemes=["bcrypt", "argon2", "scrypt"], default="bcrypt", bcrypt__rounds=14
)
roles = ["admin", "read"]

#from dotenv import dotenv_values


@users_blueprint_routes.route("/users", methods=["GET"])
def index():
    if not validate_user_role(session["username"], session["role"], "admin"):
        logging.warn(
            "/users %s attempt with role %s" % (session["username"], session["role"])
        )
        flash("Not admin")
        return render_template("flash.html", header="wa wa wah")
    valid_users = modules.users.readwrite_validusers.read_user_records_db()
    return render_template(
        "users/index.html", header="User Management", valid_users=valid_users
    )


@users_blueprint_routes.route("/user-edit", methods=["GET"])
def edit():
    if not validate_user_role(session["username"], session["role"], "admin"):
        logging.warn(
            "user-edit %s attempt with role %s" % (session["username"], session["role"])
        )
        flash("Not admin")
        return render_template("flash.html", header="wa wa wah")
    params = {"username": request.args.get("username")}
    records = modules.users.readwrite_validusers.read_user_record_db(params["username"])
    return render_template("users/edit.html", header="Edit User", user=records[0])


@users_blueprint_routes.route("/user-update", methods=["POST"])
def update():
    logging.getLogger().setLevel(logging.DEBUG)
    if not validate_user_role(session["username"], session["role"], "admin"):
        logging.warn(
            "user-update %s attempt with role %s" % (session["user"], session["role"])
        )
        flash("Not admin")
        return render_template("flash.html", header="wa wa wah")
    username = request.form["username"]
    role = request.form["role"]
    fullname = request.form["fullname"]
    email = request.form["email"]
    password = request.form["password"]
    roles = ["admin", "read"]
    if username == None:
        flash("update() username is empty")
        return render_template("flash.html", header="Error in update()")
    logging.debug(f"reaading username {username} before and ")
    records = modules.users.readwrite_validusers.read_user_record_db(username)
    if len(records) == 0:
        flash("update() no records retrieved")
        return render_template("flash.html", header="Error in update()")
    record = records[0]
    changed = False
    addhelp={}
    if role != record["role"] and role in roles:
        record["role"] = role
        logging.info("change of role")
        changed = True
    if fullname != record["fullname"]:
        record["fullname"] = fullname
        logging.info("change of fullname")
        changed = True
    if email != record["email"]:
        record["email"] = email
        logging.info("change of email")
        changed = True
    logging.debug(f"password is {password}")
    if len(password) != 0 and len(password) > 6:
        logging.debug(f"password change for {username}")
        mail_password_changed(username, email, password)
        record["password"] = ctx.hash(password)
        logging.info("you set the password")
        changed = True
    if len(password) >0 and len(password) <= 6:
        logging.debug(f"Password length too short")
        flash(f'password {record["username"]} not >6')
        addhelp["password"] = "password to be > 6"
    if changed:
        logging.info("will change", record)
        flash(f'User {record["username"]} changed')
        modules.users.readwrite_validusers.update_user_record_db(record)
    else:
        flash(f"No change")
    return render_template("users/edit.html", header="Update User", user=records[0],addhelp=addhelp)


@users_blueprint_routes.route("/user-delete", methods=["GET"])
def delete():
    if not validate_user_role(session["username"], session["role"], "admin"):
        logging.warn(
            "user-delete %s attempt with role %s" % (session["user"], session["role"])
        )
        flash("Not admin")
        return render_template("flash.html", header="wa wa wah")
    username = request.args.get("username")
    records = modules.users.readwrite_validusers.read_user_record_db(username)
    logging.debug("002 marker delete ")
    record = records[0]
    if modules.users.readwrite_validusers.delete_user_record_db(record):
        flash(
            "Deleted %s %s %s %s"
            % (record["username"], record["role"], record["fullname"], record["email"])
        )
        logging.debug("002 marker delete ")
        return redirect(url_for("users_blueprint_routes.index"))
    else:
        flash(f"Failed to Delete {username}", "warning")
        return render_template("flash.html", header="Failed")


@users_blueprint_routes.route("/user-add", methods=["GET"])
def add():
    try: 
        session["username"]
    except:
        logging.war('users_blueprint_routes.add no session?')
        return redirect(url_for('users_blueprint_routes.logout'))

    if not validate_user_role(session["username"], session["role"], "admin"):
        logging.warn(
            "users_blueprint_routes.add  %s attempt with role %s"
            % (session["username"], session["role"])
        )
        flash(f'Your user {session["role"]} is not authorised to add users', "warning")
        return redirect(url_for("cert_blueprint_routes.index"))

    logging.info(
        f'users_blueprint_routes.add {session["username"]},{session["role"]}, admin'
    )
    user = {"username": "", "role": "", "fullname": "", "email": "", "password": ""}
    addhelp = []
    return render_template(
        "users/add.html", header="Adding User", user="user", addhelp="addhelp"
    )


@users_blueprint_routes.route("/user-submit", methods=["POST"])
def submituser():
    if not validate_user_role(session["username"], session["role"], "admin"):
        logging.warn(
            "user-add %s attempt with role %s" % (session["user"], session["role"])
        )
        flash("Not admin")
        return render_template("flash.html", header="wa wa wah")
    addhelp = {}
    username = request.form["username"]
    addhelp["username"] = ""
    role = request.form["role"]
    addhelp["role"] = ""
    fullname = request.form["fullname"]
    addhelp["fullname"] = ""
    email = request.form["email"]
    addhelp["email"] = ""
    password = request.form["password"]
    addhelp["password"] = ""
    tryagain = False
    if username == "":
        addhelp["username"] = "*"
        tryagain = True
    if not role in roles:
        addhelp["role"] = "*"
        tryagain = True
    if fullname == "":
        addhelp["fullname"] = "*"
        tryagain = True
    if "@" not in list(email):
        addhelp["email"] = "@"
        tryagain = True
    if password == "" or len(password) < 6:
        addhelp["password"] = ">6"
        tryagain = True
    records = modules.users.readwrite_validusers.read_user_record_db(username)
    if len(records) > 0:
        addhelp["username"] = "exists"
        tryagain = True
    user = {
        "username": username,
        "role": role,
        "fullname": fullname,
        "email": email,
        "password": password,
    }
    if tryagain:
        return render_template(
            "users/add.html", header="Again", user=user, addhelp=addhelp
        )
    # now actually add
    user["password"] = ctx.hash(password)
    if modules.users.readwrite_validusers.insert_user_record_db(user):
        flash("added %s " % user["username"])
        # mail_password_changed(user["username"], user["email"], user["password"])
        return redirect(url_for("users_blueprint_routes.index"))
    else:
        flash(
            "Failed %s %s %s %s %s  " % user["username"],
            user["role"],
            user["fullname"],
            user["email"],
            user["password"],
        )
        return render_template(
            url_for("users_blueprint_routes.add"),
            header="Failed to insert record",
            user=user,
            addhelp=addhelp,
        )


import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def mail_password_changed(username, email, password):
    sender_email = os.environ["DEFAULT_CONTACT"]
    receiver_email = email
    logging.getLogger().setLevel(logging.DEBUG)
    logging.debug("mailing %s about %s " % (username, email))
    logging.getLogger().setLevel(logging.WARN)

    message = MIMEMultipart("alternative")
    message["Subject"] = f" Password Change on {os.environ['DEFAULT_HOST']}"
    message["From"] = sender_email
    message["To"] = receiver_email
    text = f"""\
Hi,

The password for {username} was set to {password} on  freecertiffy.

Thank-you

"""

    html = f"""
<html>
  <body>
    <p>Hi,<br>
    <p>The password for {username} was set to {password} on freecertiffy .</p>
    <p>Thank-you!</p>
  </body>
</html>
"""

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    try:
        server = smtplib.SMTP(os.environ["SMTPHOST"])
        server.set_debuglevel(0)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
    except:
        flash(f"Failed to email user of this password change", "warning")
        logging.warn("Failed to contant SMTPHOST")
