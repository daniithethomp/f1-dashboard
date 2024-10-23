from tkinter import *
import tkinter.ttk as ttk
from api_calls import *
from graphing import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import datetime

def driver_standings(track, season):
    driver_standings_results = get_driver_standings(track, season)[0]
    count = 0
    global canvas
    try:
        canvas.get_tk_widget().grid_forget()
    except Exception as e:
        canvas.grid_forget()
    canvas = Frame(canvasFrame)
    for driver in driver_standings_results["DriverStandings"]:
        text = f"{driver['position']} {driver['Driver']['driverId']} - {driver['points']}"
        label = Label(canvas, text=text)
        label.grid(row=(count % 10),column=(count // 10))
        count += 1
    canvas.grid(row=0,column=0)

def constructor_standings(track, season):
    global canvas
    try:
        canvas.get_tk_widget().grid_forget()
    except Exception as e:
        canvas.grid_forget()
    canvas = Frame(canvasFrame)
    count = 0
    constructor_standings_results = get_constructor_standings(track,season)[0]
    for constructor in constructor_standings_results["ConstructorStandings"]:
        text = f"{constructor['position']} {constructor['Constructor']['name']} - {constructor['points']}"
        label = Label(canvas, text=text)
        label.grid(row=(count % 10),column=(count // 10))
        count += 1
    canvas.grid(column=0,row=0)

def track_map():
    track = track_select.get()
    season = season_select.get()
    print(track,season)
    fig = draw_track_map(track,season)
    global canvas
    canvas.grid_forget()
    canvas = FigureCanvasTkAgg(fig, master=canvasFrame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=4,column=0)

def show_session_results(session, track, season):
    results = get_session_results(season, track, session)
    global canvas
    canvas.grid_forget()
    canvas = Label(canvasFrame,text=results.to_string(columns=['Position','FullName','DriverNumber','TeamName','Time','Points'],justify='left',max_colwidth=25,col_space=30,index=False))
    canvas.grid(row=0,column=0)

def draw_fastest_lap(season, track, session):
    fig = plot_fastest_lap(season, track, session)
    
    global canvas
    canvas.grid_forget()
    canvas = FigureCanvasTkAgg(fig, master=canvasFrame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0,column=0)


def driver_view(root):
    pass

def reset():
    pass

def updateComboBoxes(e):
    print("updating")
    if season_select.get():
        season = int(season_select.get())
        if season < 2021:
            session_select.config(values=['Practice 1', 'Practice 2', 'Practice 3', 'Qualifying', 'Race'])
        elif season > 2020 and season < 2023:
            session_select.config(values=['Practice 1', 'Qualifying', 'Practice 2', 'Sprint', 'Race'])
        elif season > 2022:
            session_select.config(values=['Practice','Qualifying','Sprint Shootout','Sprint','Race'])
        tracks = get_all_tracks(season)
        track_select.config(values=tracks['circuitId'].tolist())
    if track_select.get():
        seasons = get_all_seasons(track_select.get())
        season_select.config(values=seasons['season'].tolist())
    if session_select.get():
        if session_select.get() in ['Sprint']:
            seasons = [*range(2021,datetime.datetime.now().year+1)]
            season_select.config(values=seasons)
            tracks = get_tracks_over_seasons(seasons)
            track_select.config(values=list(tracks))
    if season_select.get() and track_select.get():
        event = get_event(int(season_select.get()), track_select.get())
        if event['EventFormat'] == 'conventional':
            session_select.config(values=['Practice 1', 'Practice 2', 'Practice 3', 'Qualifying', 'Race'])
        elif event['EventFormat'] == 'sprint':
            session_select.config(values=['Practice 1', 'Qualifying', 'Practice 2', 'Sprint', 'Race'])
        elif event['EventFormat'] == 'sprint_shootout':
            session_select.config(values=['Practice','Qualifying','Sprint Shootout','Sprint','Race'])

def gp_view(root):
    reset()
    all_tracks = get_all_tracks()
    all_seasons = get_all_seasons()
    global track_select, season_select, session_select
    track_select = ttk.Combobox(drop_down_frame, values=all_tracks['circuitId'].tolist(),state='readonly')
    season_select = ttk.Combobox(drop_down_frame,values=all_seasons['season'].tolist(),state='readonly')
    session_select = ttk.Combobox(drop_down_frame,values=['Practice 1', 'Practice 2', 'Practice 3', 'Sprint', 'Sprint Shootout', 'Sprint Qualifying', 'Qualifying', 'Race'],state='readonly')

    track_select.grid(row=0,column=0,padx=10)
    season_select.grid(row=0,column=1,padx=10)
    session_select.grid(row=0,column=2,padx=10)

    track_select.bind('<<ComboboxSelected>>', updateComboBoxes)
    season_select.bind('<<ComboboxSelected>>', updateComboBoxes)
    session_select.bind('<<ComboboxSelected>>', updateComboBoxes)

    driver_stand_b = Button(action_button_frame, text="Show Driver Standings",command=lambda: driver_standings(track_select.get(),season_select.get()))
    driver_stand_b.grid(row=1,column=0,pady=10)
    constructor_stand_b = Button(action_button_frame, text="Show Constructor Standings",command=lambda : constructor_standings(track_select.get(),season_select.get()))
    constructor_stand_b.grid(row=2,column=0,pady=10)
    track_map_b = Button(action_button_frame, text="Show Track", command=track_map)
    track_map_b.grid(row=3,column=0,pady=10)
    results_b = Button(action_button_frame, text="Show Results",command=lambda : show_session_results(session_select.get(),track_select.get(),season_select.get()))
    results_b.grid(row=4,column=0,pady=10)
    fastest_lap_b = Button(action_button_frame, text="Show Fastest Lap",command=lambda : draw_fastest_lap(season_select.get(),track_select.get(),session_select.get()))
    fastest_lap_b.grid(row=5,column=0,pady=10)
    


root = Tk()
root.title("F1 Dashboard")
root.geometry("500x500")

button_frame = Frame(root,pady=10)
button_frame.grid(row=0,column=3)
drive_b = Button(button_frame, text="Driver View")
drive_b.grid(row=0,column=0,padx=10)
gp_b = Button(button_frame, text="Grand Prix View",command=lambda : gp_view(root))
gp_b.grid(row=0,column=1,padx=10)
season_b = Button(button_frame,text="Season View")
season_b.grid(row=0,column=2,padx=10)

action_button_frame = LabelFrame(root,text="Actions")
action_button_frame.grid(row=1,column=4,columnspan=2,rowspan=10)

drop_down_frame = Frame(root)
drop_down_frame.grid(row=1,column=0,columnspan=4)

canvasFrame = Frame(root)
canvasFrame.grid(row=2,column=0,columnspan=4)
canvas = Canvas(canvasFrame)
canvas.grid()

create_api()

root.mainloop()