# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 19:01:17 2021

@author: Rashid Haffadi
"""

import matplotlib
from pylab import *
import networkx as nx
import random as rd
import pycxsimulator as pycx
from functools import partial
import pickle

matplotlib.use('TkAgg')

class History:
    def __init__(self):
        self.iter = -1
        self.n_infections = []
        self.n_removed = []
        self.n_susceptible = []
        self.R = []

def init_status(network, p=0.01):

    for n in g.nodes:
        if rd.uniform(0, 1) <= p:
            g.nodes[n]["status"] = 1
            network.nodes[n]["time"] = 0
        else:
            g.nodes[n]["status"] = 0


def get_colors(network):
    def get_color(status):
        if status == 0: return "y"
        elif status == 1: return "r"
        else: return "g"
    return [get_color(network.nodes[n]["status"]) for n in network.nodes]
    
def update_infections(network, p=0.25):
    for n in network.nodes:
        if network.nodes[n]["status"] == 1:
            nbs = list(network.neighbors(n))
            for m in nbs:
                if network.nodes[m]["status"] == 2: continue
                if rd.uniform(0, 1) <= p:
                    network.nodes[m]["status"] = 1
                    network.nodes[m]["time"] = 0
                    
def update_removed(network, T, p_qt):
    for n in network.nodes:
        if network.nodes[n]["status"] == 1:
            if network.nodes[n]["time"] >= T:
                network.nodes[n]["status"] = 2
                network.nodes[n]["time"] = 0 
            else:
                if rd.uniform(0, 1) <= p_qt:
                    network.nodes[n]["status"] = 2
                    network.nodes[n]["time"] = 0
                else: network.nodes[n]["time"] += 1
                
def update_statistics(network, H):
    H.iter += 1
    H.n_infections.append(sum([1 for n in network.nodes if network.nodes[n]["status"] == 1]))
    H.n_removed.append(sum([1 for n in network.nodes if network.nodes[n]["status"] == 2]))
    H.n_susceptible.append(sum([1 for n in network.nodes if network.nodes[n]["status"] == 0]))
    

def init(p_sd, p):
    global g, H
    g = nx.read_gexf("enronMailNetwork.gexf")
    ids = list(range(g.number_of_edges()))
    rd.shuffle(ids)
    ids = ids[:int(p_sd*g.number_of_edges())]
    edges = list(g.edges)
    g = g.edge_subgraph([edges[id_] for id_ in ids])
    init_status(g, p)
    
    H = History()
    update_statistics(g, H)
    
    with open("H_enron.pkl", "wb") as fp:
        pickle.dump(H, fp)

def update(p, T, p_qt):
    global g, H
    if H.n_infections[H.iter] != 0:
        update_infections(g, p)
        update_removed(g, T, p_qt)
        update_statistics(g, H)
        #gnext = g.edge_subgraph(list(g.edges)[:int(p_sd*g.number_of_edges())])
        with open("H_enron.pkl", "wb") as fp:
            pickle.dump(H, fp)       
    

def visual():
    global g, H
    cla()
    
    ax = subplot()
    pos = nx.spring_layout(g)
    nx.draw(g, pos, node_color=get_colors(g), node_size=10, width=0.1, ax=ax)
    r = ((H.n_infections[H.iter] - H.n_infections[H.iter-1])/H.n_infections[H.iter-1])*100 if H.iter > 0 and H.n_infections[H.iter-1] != 0 else 0
    ax.set_title("Covid-19 Simulation Using Enron Network, Run: "+str(H.iter)
                 +", Population: "+str(g.number_of_nodes())
                 +", Cases: "+str(H.n_infections[H.iter])
                 +", Difference: "+str(round(r, 2))+"%.")
    
    draw()
    
p_sd, p_init, p, T, p_qt = 0.15, 0.01, 0.2, 14, 0.0
init = partial(init, p_sd, p_init)
update = partial(update, p, T, p_qt)

pycx.GUI().start(func=[init, visual, update])
    
    
    
    
    
    
    
    
    