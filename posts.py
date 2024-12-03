from logger import logging
from database_connector import DatabaseConnector
from pathlib import Path
import shutil
import os
from datetime import datetime

def post_fetcher():
    with DatabaseConnector() as connection:
        cursor = connection.cursor()
        cursor.execute("""
           SELECT 
                u.user_id,
                p.PostContent,
                p.PostImageURL,
                p.CreatedAt AS PostCreatedAt,
				u.UserName,
				ud.profile_pic,
				ud.designation,
				ud.company,
				p.Status
            FROM 
                Posts p
            JOIN 
                Users u ON p.UserID = u.user_id

			join user_details ud on u.user_id=ud.user_id
            WHERE 
                p.Status = 'Active'  -- 
            ORDER BY 
                p.CreatedAt DESC;
        """)
        
        # Fetch all the results from the query
        rows = cursor.fetchall()

        # Convert rows into a list of dictionaries
        posts = []
        for row in rows:
            post = {
    
                'UserID': row[0],
                'PostContent': row[1],
                'PostImageURL': row[2],
                'PostCreatedAt': row[3],
                'UserName': row[4],
                'postuserprofile_pic': row[5],
                'designation': row[6],
                'company': row[7],

            }
            posts.append(post)
        
        return posts
    

def post_creater(user_id,postContent,postURL,directory=None):
    PostImageURL=None
    if postURL:
        target_directory = Path(directory)
        target_directory = Path(os.path.join(directory,'postData'))
        target_directory.mkdir(parents=True, exist_ok=True)
        
        # Construct the target file path
        timenow=datetime.now().strftime(format="%d%d%Y%H%M")
        profile_name=f"userid{user_id}{timenow}post.png"
        image_path = target_directory / profile_name
        PostImageURL="postData/"+profile_name
        # Save the file
        with open(image_path, 'wb') as destination:
            shutil.copyfileobj(postURL, destination)
            logging.info(f"File written to {image_path}")
    
        
    with DatabaseConnector() as connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO dbo.Posts (UserID, PostContent, PostImageURL)
                VALUES (?, ?, ?)
            """, (user_id, postContent, PostImageURL))
            connection.commit()
            return True

        except Exception as e:
            logging.error(f"Failed to create post: {str(e)}")
            return False