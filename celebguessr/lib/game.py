from flask import session
from datetime import datetime

import networkx as nx
from tmdbv3api import Person

from celebguessr.lib.db import updateToday, getToday, bestPerformance
from celebguessr.lib.randomActorPicker import randomActorPicker

G = nx.read_edgelist(
    "dataset.edgelist",
    delimiter='|',
    data=[('movie', str)]
)
G = nx.relabel_nodes(G, str.lower)
person = Person()

def Game(userInput):
        # getting today's date and first date
        actorOfTheDay = randomActorPicker()
        actorInfo = person.details(actorOfTheDay['id'])
        moviesIn = []
        for i in actorOfTheDay['known_for']:
            try:
                moviesIn.append(i['original_title'])
            except:
                try:
                    moviesIn.append(i['original_name'])
                except:
                    moviesIn.append("No known feature films for this celebrity.")

        # tips handling
        tips = {'birthday': actorInfo['birthday'], 'location': actorInfo['place_of_birth'], 'gender': actorInfo['gender'], 'knownfor': moviesIn}
        actorOfTheDay = actorOfTheDay['name']
        if tips['gender'] == 1:
            tips['gender'] = 'Female'
        elif tips['gender'] == 2:
            tips['gender'] = 'Male'
        bdayprintout = ("This celebrity was born on "+tips['birthday']+" in "+tips['location']+'.')
        genderprintout = ("The celebrity identifies as a "+tips['gender']+'.')
        movieprintout = "Some movies today's celebrity has performed in:<br>"
        for m in moviesIn:
            movieprintout = movieprintout + m + '<br>'

        # if already guessed
        if userInput.lower() in session["actorGuesses"] and session['status'] == True:
            return ["You already guessed this celebrity."]

        elif session['status'] == False:
            return ["You already won!"]

        # if requesting tip
        elif userInput in ['tip'] and session['status'] == True:
            if bdayprintout not in session['tipList']:
                session['tipList'].append(bdayprintout)
            elif genderprintout not in session['tipList']:
                session['tipList'].append(genderprintout)
            elif movieprintout not in session['tipList']:
                session['tipList'].append(movieprintout)
            else:
                return ["Sorry, you've used all your tips."]

        # if guess is in actor list
        elif userInput.lower() in G.nodes and session['status'] == True:
            session["guessCount"] = session["guessCount"] + 1
            try:
                # if correct
                if len(nx.shortest_path(G,userInput.lower(),actorOfTheDay.lower()))-1 == 0:
                    today = datetime.now().date()
                    updateToday("won",today, 1)
                    updateToday("guesses",today, int(session['guessCount']))
                    updateToday("tips",today, len(session['tipList']))
                    data = getToday(today)
                    if data['bestguesses'] == 0:
                        bestPerformance(int(session['guessCount']),len(session['tipList']),today)
                    elif session['guessCount'] < data['bestguesses']:
                        bestPerformance(int(session['guessCount']),len(session['tipList']),today)
                    elif session['guessCount'] == data['bestguesses'] and len(session['tipList']) < data['besttips']:
                        bestPerformance(int(session['guessCount']),len(session['tipList']),today)
                    if session["guessCount"] == 1:
                        session['guessList'].append(["You guessed it! Today's Celeb of the Day is "+actorOfTheDay+"! You guessed in "+str(session['guessCount'])+" attempt.",0,"https://image.tmdb.org/t/p/w500"+person.images(person.search(userInput.lower())[0]['id'])['profiles'][0]['file_path']])
                    else:
                        session['guessList'].append(["You guessed it! Today's Celeb of the Day is "+actorOfTheDay+"! You guessed in "+str(session['guessCount'])+" attempts.",0,"https://image.tmdb.org/t/p/w500"+person.images(person.search(userInput.lower())[0]['id'])['profiles'][0]['file_path']])
                    session['guessList'].sort(key=lambda x: x[1])
                    session['status'] = False
                # if one away
                elif len(nx.shortest_path(G,userInput.lower(),actorOfTheDay.lower()))-1 == 1:
                    session['actorGuesses'].append(userInput.lower())
                    session['guessList'].append(["Close! "+userInput.title()+" is 1 actor from the Celeb of the Day. They were together in "+G.get_edge_data(userInput.lower(),actorOfTheDay.lower())['movie'],1,"https://image.tmdb.org/t/p/w500"+person.images(person.search(userInput.lower())[0]['id'])['profiles'][0]['file_path']])
                    session['guessList'].sort(key=lambda x: x[1])
                # if many away
                else:
                    session['actorGuesses'].append(userInput.lower())
                    session['guessList'].append([userInput.title()+" is "+str(len(nx.shortest_path(G,userInput.lower(),actorOfTheDay.lower()))-1)+" celebrities away from the Celeb of the Day.",len(nx.shortest_path(G,userInput.lower(),actorOfTheDay.lower()))-1,"https://image.tmdb.org/t/p/w500"+person.images(person.search(userInput.lower())[0]['id'])['profiles'][0]['file_path']])
                    session['guessList'].sort(key=lambda x: x[1])

            # if no shortest path
            except:
                session['actorGuesses'].append(userInput.lower())
                session['guessList'].append([userInput.title()+" doesn't have any connection with the Celeb of the Day.",10,"https://image.tmdb.org/t/p/w500"+person.images(person.search(userInput.lower())[0]['id'])['profiles'][0]['file_path']])
                session['guessList'].sort(key=lambda x: x[1])
        # if not in DB
        else:
            return ["That's not a celebrity in our database, sorry."]