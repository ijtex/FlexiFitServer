# Fbq.py by Isaac Texeira
import firebase_admin
from firebase_admin import credentials, firestore
import datetime

_PATH_TO_FIREBASE_CERT = "cert.json"
_TEST_DOUBLES_MODE = True # Controls whether or not to use test doubles, such as a fixed today()

def today(dummy=False):
    if dummy:
        return '02_23_2024'
    return datetime.datetime.now().date().strftime("%d_%m_%Y")

def get_user_data(db: 'FirebaseDatabase', email: str):
    """Input: A live database and an email string
    Output: The data associated with the email in that database"""
    userdat = db.collection('User') # Navigate to the User collection

    # This part of the navigation uses the 'email' field of the documents in the User collection. If that field is removed,
    # simply adjust this to use the .document() method instead
    query = userdat.where('Email', '==', email).limit(1)

    one = query.get()[0]

    user_globals = one.to_dict()
    user_stats = one.reference.collection('Stats')
    user_daily = user_stats.document(today(_TEST_DOUBLES_MODE)).get().to_dict() # if this fails, check _TEST_DOUBLES_MODE

    return user_globals | user_daily