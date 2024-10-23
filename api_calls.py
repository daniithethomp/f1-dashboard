import fastf1
from fastf1.ergast import Ergast
from datetime import datetime

def create_api():
    global ergast 
    ergast = Ergast()

def get_driver_standings(track, season):
    event = fastf1.get_event(int(season), track)
    return ergast.get_driver_standings(season=int(season),round=event['RoundNumber'], result_type='raw')\
    
def get_constructor_standings():
    return ergast.get_constructor_standings(season='current', result_type='raw')

def get_data_for_track_map(track_name,year):
    try:
        session = fastf1.get_session(int(year), track_name,'Q')
    except Exception as e:
        print(e)
        raise ValueError("Invalid Track Name")
    session.load()

    lap = session.laps.pick_fastest()
    pos = lap.get_pos_data()
    circuit_info = session.get_circuit_info()
    return pos, circuit_info

def get_all_tracks(season=None):
    return ergast.get_circuits(limit=1000,season=season)

def get_tracks_over_seasons(seasons):
    track_list = []
    for season in seasons:
        track_list =[*track_list, *get_all_tracks(season)['circuitId'].tolist()]
    return set(track_list)

def get_all_seasons(circuit=None):
    return ergast.get_seasons(limit=1000,circuit=circuit)

def get_event(season, circuit):
    return fastf1.get_event(season,circuit)