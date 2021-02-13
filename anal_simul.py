# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 03:26:53 2021

@author: Rashid Haffadi
"""

import matplotlib
from pylab import *
import pickle
import pycxsimulator as pycx
from functools import partial

matplotlib.use("TKAgg")
style.use("dark_background")

class History:
    def __init__(self):
        self.iter = 0
        self.n_infections = []
        self.n_removed = []
        self.n_susceptible = []
        self.R = []


def init():
    """
    Covid-19 Simulation Results
    """
    
    global H, susceptible, removed

    
    with open("H.pkl", "rb") as fp:
        H = pickle.load(fp)
    
    susceptible = [i + s for i, s in zip(H.n_infections, H.n_susceptible)]
    removed = [r + s for r, s in zip(H.n_removed, susceptible)]

    

def update(f="H.pkl"):
    global H, susceptible, removed

    with open(f, "rb") as fp:
        H = pickle.load(fp)
    
    susceptible = [i + s for i, s in zip(H.n_infections, H.n_susceptible)]
    removed = [r + s for r, s in zip(H.n_removed, susceptible)]

def draw():
    global H, susceptible, removed, step_
    
    cla()
    
    plot(range(H.iter+1), H.n_infections, "r-", label="Infections")
    plot(range(H.iter+1), removed , "g-", label="Rmoved")
    plot(range(H.iter+1), susceptible , "y-", label="Susceptible")
    
    fill_between(range(H.iter+1), H.n_infections, color="r")
    fill_between(range(H.iter+1), susceptible, H.n_infections, color="y")
    fill_between(range(H.iter+1), removed, susceptible, color="g")
    
    legend(loc="lower right")
    xlabel("Runs/Days")
    ylabel("Cases")
    title("Covid-19 Simulation Results")
    show()

f = "H.pkl"
update = partial(update, f=f)
pycx.GUI().start(func=[init, draw, update])













