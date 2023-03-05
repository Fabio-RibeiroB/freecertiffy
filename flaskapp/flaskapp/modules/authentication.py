from modules.users.readwrite_validusers import read_user_record_db


def get_user_role_db(username):
    records = read_user_record_db(username)
    record = records[0]
    return record["role"]


def validate_user_db(username: str, password: str) -> bool:
    from passlib.context import CryptContext
    ctx = CryptContext(
        schemes=["bcrypt", "argon2", "scrypt"], default="bcrypt", bcrypt__rounds=14
    )
    valid_users = []
    records = read_user_record_db(username)
    if len(records) > 0:
        user = records[0]
        if ctx.verify(password, user["password"]):
            return True
    else:
        return False


def validate_user_role(sess_username: str, sess_role: str, desired_role: str) -> bool:
    try:
        sess_username
        sess_role
    except:
        return "Role not %s"
    if sess_role != desired_role:
        return False
    else:
        return True
