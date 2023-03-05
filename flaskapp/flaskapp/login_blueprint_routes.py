from flask import Blueprint, render_template, session, request, url_for, redirect, flash
from modules.users.readwrite_validusers import (
    read_user_records_db,
    read_user_record_db,
    update_user_record_db,
    read_user_record_db_ext,
    insert_user_record_db,
    delete_user_record_db,
    read_user_record_db_ext,
)
from modules.authentication import (
    get_user_role_db,
    validate_user_role,
    validate_user_db,
)

login_blueprint_routes = Blueprint(
    "login_blueprint_routes",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="assets",
)

import logging


@login_blueprint_routes.route("/")
def login():
    try:
        session["username"]
    except:
        pass
    return render_template("login/login.html")


@login_blueprint_routes.route("/logout")
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect(url_for("login_blueprint_routes.login"))


@login_blueprint_routes.route("/authenticate", methods=["POST"])
def authenticate():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            flash("Must set both username and password", "error")
            return render_template("login/login.html")
    if validate_user_db(username, password):
        results = read_user_record_db(username)
        logging.debug("login_blueprint_routes.authenticate %s " % results)
        session["role"] = results[0]["role"]
        session["username"] = username
    else:
        flash(f"Authentication failure {username}/{password}", "warning")
    return redirect(url_for("cert_blueprint_routes.index"))
