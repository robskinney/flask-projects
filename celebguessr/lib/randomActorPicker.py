from datetime import datetime
from random import randint

import networkx as nx
from tmdbv3api import Movie, Person, TMDb
import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

from celebguessr.lib.db import getActors, saveActor, getToday, newDate

G = nx.read_edgelist(os.path.join(APP_ROOT,'dataset.edgelist'), delimiter='|', data=[('movie', str)])
G = nx.relabel_nodes(G, lambda x: x.lower())

tmdb = TMDb()
tmdb.api_key = os.getenv("TMDB_API_Key") 
movie = Movie()
person = Person()

def randomActorPicker():
        top_100_actors = []
        for i in range(1, 6):
            popular_actors = person.popular(page=i)
            top_100_actors.extend(popular_actors)
            if len(top_100_actors) >= 100:
                break
        for actor in top_100_actors:
            if actor['name'].lower() not in G.nodes:
                top_100_actors.remove(actor)
        history_dict = getActors()
        while True:
            try:
                getToday(datetime.now().date())
            except:
                newDate(datetime.now().date())
            randomActor = top_100_actors[randint(0,len(top_100_actors)-1)]
            if str(datetime.now().date()) in list(history_dict.keys()):
                return person.search(history_dict[str(datetime.now().date())])[0]
            elif str(datetime.now().date()) not in list(history_dict.keys()):
                saveActor(datetime.now().date(),randomActor['name'])
                return randomActor