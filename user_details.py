from logger import logging
from database_connector import DatabaseConnector

def get_user_details(useremail):
    """Get user details
    
    Args:	Useremail: string User details

    Returns: Dictionary of user details 
    """
    with DatabaseConnector() as connector:
        cursor = connector.cursor()
        logging.debug(f"Getting user details from database for the user {useremail}")
        cursor.execute("select top(1) * from dbo.user_details where user_id=(select user_id from dbo.users where email=?)", (useremail,))
        user_detail = cursor.fetchone()
        user_details = {
                "user_id":user_detail[1],
                "phone":user_detail[2],
                "first_name":user_detail[3],
                "last_name":user_detail[4],
                "address":user_detail[5],
                "profile_pic":user_detail[6],
                "birth_date":user_detail[7],
                "designation":user_detail[8],
                "company":user_detail[9],
                "workstartdate":user_detail[10],
                "workenddate":user_detail[11],
                "qualification":user_detail[12]
            }

        return user_details
def update_user_details(user_details):
    """
    Update user details
    Args: (user) User details object

    Returns:
        bool True if successful update else False
    """
    cursor=None
    with DatabaseConnector() as connection:
        cursor=connection.cursor()
        
        query = """
            UPDATE dbo.user_details
            SET  first_name =?, last_name =?, address =?, designation =?, company =?,  qualification =?
            WHERE user_id =?
        """
        cursor.execute(query, (user_details["first_name"], user_details["last_name"], user_details["address"], user_details["designation"], user_details["company"], user_details["qualification"], user_details["user_id"]))
        connection.commit()
        logging.info(f"User details updated successfully for user_id: {user_details['user_id']}")
        return True
        
    