from password_hashing import hash_password
from database_connector import DatabaseConnector
from logger import logging
from gmail_connector import MailSender
import random
import string

class Password_reset():
    def __init__(self):
        self.password_reset=MailSender()

    def reset_password(self, useremail)->int:
        """Reset password

        Args: Useremail: Mail of user to reset password
        
        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        with DatabaseConnector() as connector:
            cursor = connector.cursor()
            cursor.execute("SELECT top(1) * FROM dbo.users WHERE email = ?", (useremail,))
            user = cursor.fetchone()
            
            if user:
                username=user[1]
                new_random_password =self._generate_random_string()# Generate a new password
                new_password = hash_password(new_random_password)  # hasing and saving the new password
                cursor.execute("UPDATE dbo.users SET password = ? WHERE email = ?", (new_password, useremail))
                self.password_reset.forget_password_sender(useremail, username,new_random_password)  # Send the new password to the user's email
                connector.commit()
                return 1
            else: 
                logging.info(f"User '{useremail}' not found")  # Log the event if user not found in the database
                return 0
            
    def _generate_random_string(self,length=10):
        """Generates a random string 
        Args:
            Length(Int): Length of the string to generate
        Returns:
            A random string with digits having length  of length(Int) 
        """
        # Define the character set: letters (both uppercase and lowercase) and digits
        characters = string.ascii_letters + string.digits
        # Randomly select characters from the set to form a string
        random_string = ''.join(random.choice(characters) for _ in range(length))
        return random_string