# What is this about?
A small flask program is no big deal structurally as its all based around a few files and directories. Bigger ones need to use blueprints, separate template directories, and user management for login purposes.

So this is sort of a template to quickstart my projects.

# What are the components?
  - Python
  - Flask
  - Jinga2
  - Bootstrap 5
  - mongodb

# The structure of this template program
```
    ../../myenv.env
            SECRET_KEY
            CONNECTSTRING
            DEFAULT_CONTACT
            DEFAULT_HOST
            SMTPHOST
    flaskapp/
        app.py
        modules/authentication.py
                    def validate_user_db(username,passwordd),
                    def validate_user_role(username,role)
                    def get_user_role_db(username)
        templates/{base,flash,message}.html
        utility_insert_admin_user.py
        cert_blueprint_routes.py
                    def index():
                    def add():
                    def search():
                    def edit():
                    def delete():
        templates/cert/{index,add,edit}.html
        modules/cert/readwrite.py
                    def read_records_db():
                    def read_record_db(record):
                    def read_record_db_ext(record):
                    def insert_record_db(record):
                    def delete_record_db(record):
                    def update_record_db(record):
                    def update_record_db_ext(record):
        users_blueprint_routes.py
                    def index():
                    def edit():
                    def update():
                    def delete():
                    def add():
                def submituser():
                def mail_password_changed(username, email, password):
        templates/users/{index,add,edit}.html
        modules/users/readwrite_validusers.py
				    def read_user_records_db():
				    def read_user_record_db(username):
				    def read_user_record_db_ext(username):
				    def insert_user_record_db(record):
				    def delete_user_record_db(record):
				    def update_user_record_db(record):
				    def update_user_record_db_ext(record):
        login_blueprint_routes.py
                    def login():
                    def logout():
                    def authenticate():
        templates/login/login.html

```
# Getting the environment up the first time
```
python3 -m venv ~/.venv/flask-template
source ~/.venv/flask-template/bin/activate
python3 -m pip install -r requirements.txt
```

# Starting with flask for development
```
. ./source_me
  flask --env-file ../../myenv.env  run
```

# app.py
In a small flask program, we can put all our routes/views in app.py. In this program we are using blueprints, so our app.py is quite small. It mainly registers the blueprints.

# Blueprints
Our blueprints files are to keep routes/view/functions related to databases or distinct functional areas:
    - cert records
    - users management
    - login

# Templates
So our jinga2 templates try to share the same header "base.html" and "message.html" and "flash.html" if they need them.


# Starting with gunicorn in production
Check the gunicorn-conf.py file e.g. to see what port or certificates to use
```
gunicorn --error-logfile gunicorn.error  --log-level=debug  app:app -D --capture-output --pid gunicorn.pid
```

To restart after changing files:
```
kill -HUP $(cat gunicorn.pid)
```
'''capture-output''' is how we get the syslog into the gunicorn.error file.

I was using the main calling app as a module as in app/__init__.py but found that using it with gunicorn was difficult with not much support on the web.



# Using Session
This is surprisingly straight forward. Create and initialise in app.py the Session then in the blueprints, you can use session['username'] to see if its set (the user has logged in.

```
    from flask import session
    ...
    try:
        session['username']
        logging.debug('Can see session[user] %s ' % session['username'])
    except:
        logging.warn('Not logged in!')
```

# Bootstrap 5 and HTML
I have used tidy html5 and bootstrap5 for formatting.
