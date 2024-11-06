from cryptography.fernet import Fernet
import json
import os
from dotenv import load_dotenv
import base64

key = Fernet.generate_key()
cipher_suite = Fernet(key)

print(key)

load_dotenv()

def generate_key():
    """Generate a valid Fernet key and return it in base64 format"""
    return Fernet.generate_key().decode()

def get_or_create_key():
    """Get the encryption key from environment or generate a new one"""
    key = os.getenv('ENCRYPTION_KEY')
    if not key:
        # Generate a new key if none exists
        key = generate_key()
        print(f"Generated new key: {key}")
        print("Please add this key to your .env file as ENCRYPTION_KEY=<key>")
    return key

def validate_key(key):
    """Validate if the key is properly formatted"""
    try:
        # Check if key is base64 encoded
        decoded = base64.urlsafe_b64decode(key.encode())
        # Check if key is 32 bytes
        return len(decoded) == 32
    except Exception:
        return False

# Initialize encryption key
key = get_or_create_key()

if not validate_key(key):
    raise ValueError("Invalid encryption key format. Key must be 32 url-safe base64-encoded bytes.")

cipher_suite = Fernet(key.encode())

def save_session_encrypted(data):
    """
    Encrypt and save session data to file
    
    Args:
        data: Dictionary containing session data
    """
    encrypted_data = cipher_suite.encrypt(json.dumps(data).encode())
    with open("session.txt", "wb") as f:
        f.write(encrypted_data)

def load_session_encrypted():
    """
    Load and decrypt session data from file
    
    Returns:
        dict: Decrypted session data or None if error occurs
    """
    try:
        with open("session.txt", "rb") as f:
            encrypted_data = f.read()
        decrypted_data = cipher_suite.decrypt(encrypted_data)
        return json.loads(decrypted_data.decode())
    except FileNotFoundError:
        print("No session file found")
        return None
    except Exception as e:
        print(f"Error loading session: {e}")
        return None