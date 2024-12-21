from flask import redirect, request, flash, url_for, render_template, Blueprint
from pvadmin.models.feed import FeedInfo, FeedForm
from dbconfig import app, db
from text import text_data
from pvadmin.filters.feedfilter import get_all_feed_data
from routes.csrf import csrf_admin_status

admin_feed = Blueprint('admin_feed', __name__)

@admin_feed.route('/feed', methods=['GET', 'POST'])
def pvadminfeed():
    form = FeedForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            author = request.form.get('author')
            date = request.form.get('date')
            feed = request.form.get('feed')
            title = request.form.get('title')
            new_feed = FeedInfo(author=author, date=date, feed=feed, title=title)
            db.session.add(new_feed)
            db.session.commit()
            app.logger.info('\033[1;32m[PVADMIN][FEED][ADD][TOKEN]\033[0m %s', str(csrf_admin_status()))
            return redirect(url_for('admin_feed.pvadminfeed'))
    else:
            flash('Agrega tu noticia al feed', 'info')
            return render_template('pvadmin_templates/pvadmin_feed.html', text_data=text_data)
        
@admin_feed.route('/all-feeds')
def show_all_feeds():
    feed_data = get_all_feed_data()
    return render_template('pvadmin_templates/pvadmin_allfeed.html', feed_data=feed_data, text_data=text_data)



@admin_feed.route('/delete-feed', methods=['POST'])
def delete_feed():
    form = FeedForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            feed_ids = request.form.getlist('feed_ids')
            app.logger.info('\033[1;32m[PVADMIN][FEED][DELETE][TOKEN]\033[0m %s', str(csrf_admin_status()))
        if feed_ids:
            session = db.session()
            try:
                for feed_id in feed_ids:
                    feed_entry = session.query(FeedInfo).filter_by(id_feed=feed_id).first()
                    if feed_entry:
                        session.delete(feed_entry)
                session.commit()
                flash('Noticias eliminadas con éxito', 'success')
            except Exception as e:
                session.rollback()
                flash(f'Error al eliminar noticias: {str(e)}', 'error')
        else:
            flash('No se seleccionaron noticias para eliminar', 'warning')

        return redirect(url_for('admin_feed.show_all_feeds'))
    else:
        
        pass 
