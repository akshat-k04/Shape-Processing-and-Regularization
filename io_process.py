import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

def read_csv ( csv_path ):
    np_path_XYs = np . genfromtxt ( csv_path , delimiter = ',')
    path_XYs = []
    for i in np . unique ( np_path_XYs [: , 0]):
        npXYs = np_path_XYs [ np_path_XYs [: , 0] == i ][: , 1:]
        XYs = []
        for j in np . unique ( npXYs [: , 0]):
            XY = npXYs [ npXYs [: , 0] == j ][: , 1:]
            XYs . append ( XY )
        path_XYs . append ( XYs )
    return path_XYs


def plot ( paths_XYs ):
    paths_XYs = np.vstack(paths_XYs) 
    fig , ax = plt . subplots ( tight_layout = True , figsize =(8 , 8))
    ax.plot(paths_XYs[:,0],paths_XYs[:,1]) 
    ax . set_aspect ( 'equal')
    plt . show ()


def plot_all_polylines ( paths_XYs ):
    fig , ax = plt . subplots ( tight_layout = True , figsize =(8 , 8))
    for i , XYs in enumerate (paths_XYs):
        for XY in XYs :
            ax . plot ( XY [: , 0] , XY [: , 1] ) 
        
    ax . set_aspect ( 'equal')
    plt . show ()


def plot_two_sets(paths_XYs1, paths_XYs2):
    fig, (ax1, ax2) = plt.subplots(1, 2, tight_layout=True, figsize=(16, 8))
    
    # Plot the first set of paths
    for XYs in paths_XYs1:
        for XY in XYs:
            ax1.plot(XY[:, 0], XY[:, 1])
    ax1.set_aspect('equal')
    ax1.set_title('Paths XYs 1')
    
    # Plot the second set of paths
    for XYs in paths_XYs2:
        for XY in XYs:
            ax2.plot(XY[:, 0], XY[:, 1])
    ax2.set_aspect('equal')
    ax2.set_title('Paths XYs 2')
    
    plt.show()