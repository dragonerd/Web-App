from flask import Blueprint, jsonify
from pvadmin.models.feed import FeedInfo
from dbconfig import db

feed = Blueprint('feed', __name__)

@feed.route('/feed')
def get_news():
    news = db.session.query(FeedInfo).order_by(FeedInfo.date.desc()).limit(4).all()
    return jsonify([item.to_dict() for item in news])