from pathlib import Path
from database_connector import DatabaseConnector
import shutil
from logger import logging

def update_profile_picture(user_id, file, directory):
    """
    Updates the profile picture for a user by saving it to the specified directory.

    Args:
        user_id (str): ID of the user.
        file (file-like object): File-like object containing the image data.
        directory (str): Target directory where the image will be saved.

    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    try:
        
        target_directory = Path(directory)
        target_directory.mkdir(parents=True, exist_ok=True)
        
        # Construct the target file path
        profile_name=f"userid_{user_id}.png"
        image_path = target_directory / profile_name
        
        # Save the file
        with open(image_path, 'wb') as destination:
            shutil.copyfileobj(file, destination)
            logging.info(f"File written to {image_path}")
        
        
        with DatabaseConnector() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE dbo.user_details
                SET profile_pic =?
                WHERE user_id =?
            """, (str(profile_name), user_id))
            connection.commit()
        return True
    except Exception as e:
        logging.error(f"Failed to update profile picture: {e}")
        return False
