import bcrypt
from logger import logging

def hash_password(password):
    # Hash the password using bcrypt
    # The gensalt method generates a random salt for each password
    # The hashpw method then hashes the password with the salt
    # The resulting hash is a byte string, so we decode it to a string before returning it
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')
# Verify Password
def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())
