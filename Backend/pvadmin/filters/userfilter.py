from dbconfig import db
from models.disciplines import get_discipline
from models.models import UserInfo, get_status



def get_all_users_data():
    
  
    users_entries = db.session.query(UserInfo).all()
  
    user_data = []

    for entry in users_entries:
        filter_status = get_status(entry.status)
        filter_discipline = get_discipline(entry.id_discipline)
        user_data.append({
            "id_profile":entry.id_profile,
            "fname": entry.fname,
            "lname": entry.lname,
            "email": entry.email,
            "username": entry.username,
            "discipline":filter_discipline,
            "status":filter_status,
            "temp_password":entry.temp_password,
            "trysend":entry.trysend,
            "selected": False
        })

    db.session.close()
    return user_data

def total_accounts():
    
    total_users = db.session.query(UserInfo).count()
    db.session.close()
    return total_users
