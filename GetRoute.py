import networkx as nx
import numpy as np
import pandas as pd
import json
import os
import matplotlib.pyplot as plt
from ipywidgets import FloatProgress
from IPython.display import display
from osgeo import gdal, ogr

# 
def connected_component_subgraphs(G):
    for c in nx.connected_components(G):
        yield G.subgraph(c)

def get_path(n0, n1):
    """If n0 and n1 are connected nodes in the 
    graph, this function returns an array of point
    coordinates along the road linking these two nodes."""
    return np.array(json.loads(
                sg[n0][n1]['Json'])['coordinates'])

def get_path(n0, n1):
    """If n0 and n1 are connected nodes in the 
    graph, this function returns an array of point
    coordinates along the road linking these two nodes."""
    return np.array(json.loads(
                sg[n0][n1]['Json'])['coordinates'])


def get_path_length(path):
    return np.sum(geocalc(
                    path[1:,0], path[1:,1],
                    path[:-1,0], path[:-1,1]))#change these two 
# to iterate over all crime incidents w/in X radius of edge first
#two points.

def get_crime_path_length(path,crime):
    return np.sum(geocalc(
                    path[1:,0], path[1:,1],
                    path[:-1,0], path[:-1,1]))#change these two 

#Get POI Data
poi_df = pd.read_csv(os.path.join('data files','POI-Holidays.csv'))

# Read London shape file
g = nx.read_shp(os.path.join('data files',"gis_osm_roads_free_1.shp"))

#Undirected subgraphs
sgs = list(connected_component_subgraphs(
                   g.to_undirected()))
print('connected g')

#Largest Subgraph
largest = np.argmax([len(sg) 
                    for sg in sgs])
print('found largest sg')
sg = sgs[largest]

for v in sg.edges():
    
    d = {'longitude':(v[0][0]),'latitude':v[0][1]}
d

for n0, n1 in sg.edges_iter():
    path = get_path(n0, n1)
    distance = get_path_length(path)
    #print(distance)
    sg.edge[n0][n1]['distance'] = distance
#print(sg)
print('Step 1 Done')

f = FloatProgress(min=0, max=len(sg))
display(f)

# for n0,n1 in sg.edges_iter():
#     f.value+=1
#     cdistance=0
#     path = get_path(n0,n1)
#     for i in range(round(len(crime_df)/10)):
#         cdistance+= geocalc(path[0,0],path[0,1],
#                             crime_df.at[i,'Latitude'],
#                             crime_df.at[i,'Longitude'])
#         +geocalc(path[:-1,0],path[:-1,1],
#                             crime_df.at[i,'Latitude'],
#                             crime_df.at[i,'Longitude'])
#         +float(crime_df.at[i,'Final Score 2'])
#     sg.edge[n0][n1]['Crime_Weight']=cdistance
                                      
# print('Step 2 done')

for n0,n1 in sg.edges_iter():
    cdistance=0
    #print(n0)
    #print(n1)
    path = get_path(n0,n1)
    #print(path)
    for i in range(len(poi_df)):
        cdistance+= geocalc(path[:-1,0],path[:-1,1],
                            poi_df.at[i,'latitude'],
                            poi_df.at[i,'longitude'])
        #+ geocalc(path[1,0],path[1,-1],
        #         poi_df.at[i,'latitude'],
        #                    poi_df.at[i,'longitude'])
    sg.edge[n0][n1]['POI_Weight']=np.sum(cdistance)
                                      
print('Step 3 done')

nodes = np.array(sg.nodes())

# Get the closest nodes in the graph.

pos0_i = np.argmin(np.sum(
                    (nodes[:,::-1] - pos0)**2,
                     axis=1))

pos1_i = np.argmin(np.sum(
                        (nodes[:,::-1] - pos1)**2,
                         axis=1))


path = nx.shortest_path(sg, 
            source=tuple(nodes[pos0_i]), 
            target=tuple(nodes[pos1_i]),
            weight='POI_Weight')
len(path)
print(type(path))
print(path)

i = 1
endlist = []
for tup in path:
    pair = list(tup)
    pair.insert(0,i)
    i+=1
    endlist.append(pair)
print(endlist)
df = pd.DataFrame(endlist, columns=["path","longitude", "latitude"] )
df.to_csv('pathpointstb2.csv', index=False)