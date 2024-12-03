from database_connector import DatabaseConnector
from logger import logging
from password_hashing import hash_password

class Usercreation():

    def create_user(self, username, name,phone_no,email,password)->int:
        cursor = None  # Initialize cursor to None
        logging.debug(f"Details {username} {name} {phone_no} {email}")
        with DatabaseConnector() as connection:
            cursor = connection.cursor()
            hashed_password=hash_password(password)
            try:
                cursor.execute("INSERT INTO dbo.users (username,name,phone_no,email,password) VALUES (?,?,?,?,?)", (username,name,phone_no,email,hashed_password))
                
                # Retrieve the last inserted user ID ( primary key is auto-incremented)
                cursor.execute("SELECT @@IDENTITY")
                user_id = cursor.fetchone()[0]
                # Insert into user_details table
                cursor.execute("""
                    INSERT INTO dbo.user_details (user_id, phone,first_name)
                    VALUES (?, ?, ?)
                """, (user_id, phone_no, name)) 
                
                # Commit the transaction for user details
                connection.commit()
                return 1
            except Exception as e:
                logging.error(f"Failed to create user: {str(e)}")
                return 0
           
    def user_availbilty(self,username,phone_no):
        cursor = None  # Initialize cursor to None
        logging.debug(f"details {username} {phone_no} ") 
        with DatabaseConnector() as connection:
            cursor = connection.cursor()
         # Check if the phone_no already exists
            query = """
            SELECT 'phone_no' AS field FROM dbo.users WHERE phone_no = ?
            UNION
            SELECT 'username' AS field FROM dbo.users WHERE username = ?
            """
            cursor.execute(query, (phone_no, username))
            result = cursor.fetchall()
            print(result)
            fields = [row[0] for row in result]
            if 'phone_no' in fields and 'username' in fields:
                return "Phone No And Username Already Exists"
            elif 'username' in fields:
                return "Username already Exists"
            elif 'phone_no' in fields:
                return "Phone No Already Exists"
            # # indicate that user/phone_no is available to be used for account creation
            return "UserAccount available"

# if __name__ == "__main__":
#     logging_verifier = Usercreation()
#     logging_verifier.create_user('Shane','shivam',9988552244,'test@gmail.com','test@12345')

    
