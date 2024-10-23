import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np
from api_calls import *

def rotate(xy, *, angle):
    rot_mat = np.array([[np.cos(angle), np.sin(angle)],
                        [-np.sin(angle), np.cos(angle)]])
    return np.matmul(xy, rot_mat)

def draw_track_map(track_name,year):
    try:
        pos, circuit_info = get_data_for_track_map(track_name,year)
    except ValueError as e:
        print(e)
        return
    
    track = pos.loc[:,('X','Y')].to_numpy()

    track_angle = circuit_info.rotation / 180 * np.pi
    rotated_track  = rotate(track, angle=track_angle)
    fig = plt.figure(figsize=(5,5))
    track_plot = fig.add_subplot()
    track_plot.plot(rotated_track[:,0], rotated_track[:,1])

    offset_vector = [500,0]

    for _, corner in circuit_info.corners.iterrows():
        txt = f"{corner['Number']}{corner['Letter']}"

        offset_angle = corner['Angle'] / 180 * np.pi
        offset_x, offset_y = rotate(offset_vector, angle=offset_angle)

        text_x = corner['X'] + offset_x
        text_y = corner['Y'] + offset_y

        text_x, text_y = rotate([text_x, text_y], angle=track_angle)

        track_x, track_y = rotate([corner['X'], corner['Y']], angle=track_angle)

        track_plot.scatter(text_x, text_y, color='black', s=140)

        track_plot.plot([track_x,text_x],[track_y,text_y], color='black')

        track_plot.text(text_x, text_y, txt, va='center_baseline',ha='center',size='small',color='white')

    plt.yticks([])
    plt.xticks([])
    track_plot.axis('equal')
    plt.tight_layout()

    return fig
