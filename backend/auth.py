import firebase_admin
from firebase_admin import credentials, auth
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Firebase Admin SDK
def initialize_firebase():
    if not firebase_admin._apps:
        # Use service account credentials or default credentials
        cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH")
        if cred_path and os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
        else:
            # Try to use default credentials (for development/testing)
            try:
                firebase_admin.initialize_app()
            except Exception as e:
                print(f"Warning: Could not initialize Firebase: {e}")
                print("Please set FIREBASE_CREDENTIALS_PATH environment variable")

# Initialize Firebase on module import
initialize_firebase()

security = HTTPBearer()

async def verify_firebase_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> str:
    """
    Verify Firebase ID token and return the user's Firebase UID
    
    Args:
        credentials: HTTP Authorization credentials from request header
        
    Returns:
        str: Firebase UID of the authenticated user
        
    Raises:
        HTTPException: If token is invalid or verification fails
    """
    try:
        # Verify the ID token
        decoded_token = auth.verify_id_token(credentials.credentials)
        return decoded_token['uid']
    except auth.InvalidIdTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token"
        )
    except auth.ExpiredIdTokenError:
        raise HTTPException(
            status_code=401,
            detail="Expired authentication token"
        )
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Authentication failed: {str(e)}"
        )

def get_user_info(uid: str) -> dict:
    """
    Get user information from Firebase Auth
    
    Args:
        uid: Firebase UID
        
    Returns:
        dict: User information including email, name, etc.
    """
    try:
        user_record = auth.get_user(uid)
        return {
            "uid": user_record.uid,
            "email": user_record.email,
            "display_name": user_record.display_name,
            "photo_url": user_record.photo_url,
            "email_verified": user_record.email_verified
        }
    except Exception as e:
        print(f"Error getting user info: {e}")
        return {"uid": uid} 