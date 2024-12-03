from database_connector import  DatabaseConnector
from password_hashing import verify_password
from logger import logging


def verify_login(useremail, password):
    logging.info(f"Verifying login for user '%s'", useremail)
    cursor = None  # Initialize cursor to None
    with DatabaseConnector() as connection:
        cursor = connection.cursor()
        # Check if the phone_no already exists
        cursor.execute("SELECT top(1) * FROM dbo.users WHERE email = ? and is_active=1", (useremail,))
        columns = [column[0] for column in cursor.description]  # Get column names
        user = cursor.fetchone()
        if user:
            user_dict = dict(zip(columns, user))  # Map column names to values
            return verify_password(password, user_dict['password']), user_dict['user_id']
        else:
            logging.info(f"User {useremail} does not exist")
            return False, None