from flask import Blueprint, render_template, redirect, url_for, request

from autotrackr.lib.db import get_attendee, get_attendees, get_event, get_events, add_event, delete_event, del_attendee_db, add_attendee_db, edit_attendee_db, edit_event
from autotrackr.lib.utils import eventcheck, attendeecheck

autotrackr = Blueprint(
    'autotrackr',
    __name__,
    template_folder='templates'
)

@autotrackr.route('/', methods=['GET'])
def index():
    if request.method == "GET":
        return render_template('autotrackr/index.html' )

# ------------------------------------------------------------------------------------
# Event routes
# ------------------------------------------------------------------------------------

@autotrackr.route("/events", methods=["GET"])
def events():
    if request.method == "GET":
        events = get_events()

        return render_template('autotrackr/events/index.html',events=events)
    
@autotrackr.route('/events/<event_id>', methods=["GET"])
def events_details(event_id):
    if request.method == "GET":
        attendees = get_attendees(event_id)
        event = get_event(event_id)

        return render_template('autotrackr/events/details.html', event=event, attendees=attendees)

@autotrackr.route("/events/create", methods=["GET"])
def events_create(error=None):
    if request.method == "GET":
        return render_template('autotrackr/events/create.html', error=error)
    
@autotrackr.route('/events/<event_id>/update', methods=['GET'])
def events_update(event_id, error=None):
    if request.method == "GET":
        event = get_event(event_id)
        return render_template('autotrackr/events/update.html', event=event, error=error)
        
@autotrackr.route('/events/<event_id>/delete', methods=['GET'])
def events_delete(event_id):
    if request.method == "GET":
        event = get_event(event_id)
        return render_template('autotrackr/events/delete.html', event=event)
    
@autotrackr.route("/api/events/create", methods=["POST"])
def api_events_create():
    if request.method == "POST":
        name = request.form['name']
        date = request.form['date']
        host = request.form['host']
        description = request.form['description']

        error = eventcheck(name,date,host,description)

        if error:
            return redirect(url_for('autotrackr.events', error=error))
        
        add_event(name,date,host,description)

        return redirect(url_for('autotrackr.events'))

@autotrackr.route("/api/events/<event_id>/update", methods=["POST"])
def api_events_update(event_id):
    if request.method == "POST":
        name = request.form['name']
        date = request.form['date']
        host = request.form['host']
        description = request.form['description']

        error = eventcheck(name,date,host,description)

        if error:
            return redirect(url_for('autotrackr.events_update', event_id=event_id, error=error))
        
        edit_event(event_id,name,date,host,description)

        return redirect(url_for('autotrackr.events_details', event_id=event_id))

@autotrackr.route("/api/events/<event_id>/delete", methods=["POST"])
def api_events_delete(event_id):
    if request.method == "POST":
        delete_event(event_id)

        return redirect(url_for('autotrackr.events'))
    
# ------------------------------------------------------------------------------------
# Attendee routes
# ------------------------------------------------------------------------------------

@autotrackr.route('/events/<event_id>/attendees/create', methods=['GET'])
def events_attendee_create(event_id, error=None):
    if request.method == "GET":
        event = get_event(event_id)
        
        return render_template('autotrackr/attendees/create.html', event=event, error=error)

@autotrackr.route('/events/<event_id>/attendees/<attendee_id>/update', methods=['GET'])
def events_attendee_update(event_id, attendee_id, error=None):
    if request.method == "GET":
        event = get_event(event_id)
        attendee = get_attendee(attendee_id)

        return render_template('autotrackr/attendees/update.html', attendee=attendee, event=event, error=error)
    
@autotrackr.route("/api/events/<event_id>/attendees/create", methods=["POST"])
def api_events_attendee_create(event_id):
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        comment = request.form['comment']

        error = attendeecheck(name,email,comment)

        if error:
            return redirect(url_for('autotrackr.events_attendee_create', event_id=event_id, error=error))
        
        add_attendee_db(event_id,name,email,comment)

        return redirect(url_for('autotrackr.events_details', event_id=event_id))

@autotrackr.route("/api/events/<event_id>/attendees/<attendee_id>/update", methods=["POST"])
def api_events_attendee_update(event_id, attendee_id):
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        comment = request.form['comment']

        error = attendeecheck(name,email,comment)

        if error:
            return redirect(url_for('autotrackr.events_attendee_update', event_id=event_id, attendee_id=attendee_id, error=error))
        
        edit_attendee_db(attendee_id,event_id,name,email,comment)

        return redirect(url_for('autotrackr.events_details', event_id=event_id))

@autotrackr.route("/api/events/<event_id>/attendees/<attendee_id>/delete", methods=["GET"])
def api_events_attendee_delete(attendee_id,event_id):
    del_attendee_db(attendee_id,event_id)

    return redirect(url_for('autotrackr.events_details', event_id=event_id))