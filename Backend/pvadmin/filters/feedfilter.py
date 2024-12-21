from dbconfig import db
from pvadmin.models.feed import FeedInfo



def get_all_feed_data():
    
    # Retrieve all feed entries from the 'feed' table
    feed_entries = db.session.query(FeedInfo).all()

    # Convert the query results into a list of dictionaries
    feed_data = []
    for entry in feed_entries:
        feed_data.append({
            "id_feed":entry.id_feed,
            "title": entry.title,
            "author": entry.author,
            "feed": entry.feed,
            "date": entry.date,
            "selected": False
        })

    db.session.close()
    return feed_data
