from datetime import date, datetime
from flask import Blueprint, render_template, redirect, url_for, request, session

from celebguessr.lib.game import Game
from celebguessr.lib.randomActorPicker import randomActorPicker
from celebguessr.lib.db import getToday, updateToday, newFeedback

celebguessr = Blueprint(
    'celebguessr',
    __name__,
    template_folder='templates'
)

START_DATE = date(2023, 4, 12)

# ------------------------
# Helpers
# ------------------------

def init_session(today):
    session.setdefault('guessList', [])
    session.setdefault('tipList', [])
    session.setdefault('guessCount', 0)
    session.setdefault('actorGuesses', [])
    session.setdefault('status', True)
    session.setdefault('date', today)
    session.setdefault('hasPlayedToday', False)

def reset_session(today):
    session.update({
        'guessList': [],
        'tipList': [],
        'guessCount': 0,
        'actorGuesses': [],
        'status': True,
        'date': today,
        'hasPlayedToday': False
    })


def render_index(**extra):
    today = date.today()
    data = getToday(today)

    context = dict(
        date=today,
        guessCount=session['guessCount'],
        guesses=session['guessList'],
        tips=session['tipList'],
        numTips=len(session['tipList']),
        status=session['status'],
        daysSince=(today - START_DATE).days,
        todayguesses=data['guesses'],
        todayplayers=data['players'],
        todaytips=data['tips'],
        todaywon=data['won'],
        minguessestips=[data['bestguesses'], data['besttips']]
    )

    context.update(extra)
    return render_template('celebguessr/index.html', **context)


# ------------------------
# Routes
# ------------------------

@celebguessr.route('/', methods=['GET', 'POST'])
def index():
    today = date.today()
    init_session(today)

    # New day → reset user session + increment players
    if session['date'] != today:
        updateToday("players", today, 1)
        reset_session(today)

    randomActorPicker()

    if request.method == 'POST':
        if not session.get('hasPlayedToday', False):
            updateToday("players", today, 1)
            session['hasPlayedToday'] = True

        if request.form.get('action') == 'tip':
            result = Game('tip')
        else:
            user_input = request.form.get('userInput', '').strip()
            result = Game(user_input)

        return render_index(result=result)

    return render_index()


@celebguessr.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        newFeedback(
            request.form.get('email', ''),
            request.form.get('rating', 1),
            request.form.get('description', '')
        )
        return redirect(url_for('celebguessr.index'))

    return render_template('celebguessr/feedback.html')
