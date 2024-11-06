from appwrite.client import Client
from appwrite.services.account import Account
from appwrite.id import ID
from utils.logger import setup_logger 
import time
from utils.helpers import save_session_encrypted,load_session_encrypted
import os

logger = setup_logger()

APPWRITE_ENDPOINT = "https://cloud.appwrite.io/v1"
PROJECT_ID = "672a2a74003a8451a248"

client = Client()
client.set_endpoint(APPWRITE_ENDPOINT).set_project(PROJECT_ID)
account = Account(client)
def register(email, password, name):
    try:
        user = account.create(
            user_id=ID.unique(),
            email=email,
            password=password,
            name=name
        )
        if user:
            # Create session after successful registration
            session = account.create_email_password_session(email, password)
            save_session_encrypted(session)
            logger.info(f"User registered successfully: {email}")
            return session
    except Exception as error:
        logger.error(f"Registration error: {str(error)}")
        raise Exception(f'Could not register user: {str(error)}')

def login(email, password):
    try:
        session = account.create_email_password_session(email=email, password=password)
        logger.info(f"User logged in successfully: {email}")
        save_session_encrypted(session)
        return session
    except Exception as error:
        logger.error(f"Login error: {str(error)}")
        raise Exception(f'Could not login user: {str(error)}')

def logout():
    try:
        os.remove("session.txt")
        logger.info("User logged out successfully")
    except Exception as error:
        logger.error(f"Logout error: {str(error)}")
        raise Exception(f'Could not logout user: {str(error)}')

def get_user():
    try:
        user = load_session_encrypted()
        return user
    except Exception:
        return None

def is_authenticated():
    try:
        user = get_user()
        logger.info(f"is_authenticated check | Retrieved User: {user}")
        return user is not None
    except Exception as error:
        logger.error(f"is_authenticated error: {error}")
        return False
