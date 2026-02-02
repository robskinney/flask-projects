import sqlite3
import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(APP_ROOT, 'Events.db')


# ----------------------------
# Helpers
# ----------------------------

def get_connection():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con


# ----------------------------
# Event functions
# ----------------------------

def get_events():
    with get_connection() as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM events ORDER BY date, name")
        return cur.fetchall()


def add_event(name, date, host, description):
    with get_connection() as con:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO events (name, date, host, description) "
            "VALUES (?, ?, ?, ?)",
            (name, date, host, description)
        )
        con.commit()


def get_event(event_id):
    with get_connection() as con:
        cur = con.cursor()
        cur.execute(
            "SELECT * FROM events WHERE id = ?",
            (event_id,)
        )
        return cur.fetchone()


def edit_event(event_id, name, date, host, description):
    with get_connection() as con:
        cur = con.cursor()
        cur.execute(
            "UPDATE events "
            "SET name = ?, date = ?, host = ?, description = ? "
            "WHERE id = ?",
            (name, date, host, description, event_id)
        )
        con.commit()


def delete_event(event_id):
    with get_connection() as con:
        cur = con.cursor()
        cur.execute(
            "DELETE FROM attendees WHERE event_id = ?",
            (event_id,)
        )
        cur.execute(
            "DELETE FROM events WHERE id = ?",
            (event_id,)
        )
        con.commit()


# ----------------------------
# Attendee functions
# ----------------------------

def get_attendees(event_id):
    with get_connection() as con:
        cur = con.cursor()
        cur.execute(
            "SELECT * FROM attendees WHERE event_id = ? ORDER BY name",
            (event_id,)
        )
        return cur.fetchall()


def get_attendee(attendee_id):
    with get_connection() as con:
        cur = con.cursor()
        cur.execute(
            "SELECT * FROM attendees WHERE id = ?",
            (attendee_id,)
        )
        return cur.fetchone()


def add_attendee_db(event_id, name, email, comment):
    with get_connection() as con:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO attendees (event_id, name, email, comment) "
            "VALUES (?, ?, ?, ?)",
            (event_id, name, email, comment)
        )
        con.commit()


def edit_attendee_db(attendee_id, event_id, name, email, comment):
    with get_connection() as con:
        cur = con.cursor()
        cur.execute(
            "UPDATE attendees "
            "SET name = ?, email = ?, comment = ? "
            "WHERE id = ? AND event_id = ?",
            (name, email, comment, attendee_id, event_id)
        )
        con.commit()


def del_attendee_db(attendee_id, event_id):
    with get_connection() as con:
        cur = con.cursor()
        cur.execute(
            "DELETE FROM attendees WHERE id = ? AND event_id = ?",
            (attendee_id, event_id)
        )
        con.commit()
