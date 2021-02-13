# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 21:12:13 2021

@author: Rashid Haffadi
"""

import matplotlib
from pylab import *
matplotlib.use("TKAgg")
style.use("dark_background")
import pycxsimulator as pycx

import random as rd
import pickle

n = 1000
# mu, sigma, sd = 0, 0.5, 5
p_infection, t_remove, r_infection = 0.25, 14, 1
p_hub = 0.01

def color_(i):
    if i == 0: return "y"
    elif i == 1: return "r"
    else: return "g"
    
    
def test_(i):
    if i == 1: return 1
    else: return 0
    

class Particle:
    def __init__(self, x=None, y=None, status=0, ds={}, name="unknown"):
        self.x = rd.uniform(-5, 5)
        self.y = rd.uniform(-5, 5)
        self.status = status
        self.ds = ds
        self.t_infection = 0
        
        
class History:
    def __init__(self):
        self.iter = 0
        self.n_infections = []
        self.n_removed = []
        self.n_susceptible = []
        self.R = []
        
        
def init():
    """
    This is my first PyCX simulator code.\nIt simulates the growth of COVID-19.
    """
    global particles, H
    particles = []
    for i in range(n):
        if rd.uniform(0, 1) <= 0.01:
            particles.append(Particle(status=1))
        else:
            particles.append(Particle())
    H = History()
    H.iter = 0
    H.n_infections.append(int(sum([test_(p.status) for p in particles])))
    H.n_removed.append(0)
    H.n_susceptible.append(n - H.n_infections[H.iter])
    with open("H.pkl", "wb") as fp:
        pickle.dump(H, fp)
        
def visual():
    global particles, H
    cla()
    
    ax = subplot()
    
    ax.plot([p.x for p in particles if p.status == 0], [p.y for p in particles if p.status == 0], "oy", label="Susceptible")#S
    ax.plot([p.x for p in particles if p.status == 1], [p.y for p in particles if p.status == 1], "or", label="Infected")#I
    ax.plot([p.x for p in particles if p.status == 2], [p.y for p in particles if p.status == 2], "og", label="Rmoved")#R
    
    ax.legend(loc="lower right")
    r = ((H.n_infections[H.iter] - H.n_infections[H.iter-1])/H.n_infections[H.iter-1])*100 if H.iter > 0 and H.n_infections[H.iter-1] != 0 else 0
    ax.set_title("Covid-19 Simulation, Run: "+str(H.iter)
                 +", Population: "+str(n)
                 +", Cases: "+str(H.n_infections[H.iter])
                 +", Difference: "+str(round(r, 2))+"%.")
    
    ax.add_patch(Rectangle((-1, -1), 1, 1, edgecolor = 'pink'))
    ax.set_xlim((-5, 5))
    ax.set_ylim((-5, 5))
    show()
    
    
def update():
    global particles, H
    H.iter += 1
    #update positions    
    for i in range(n):
        if rd.uniform(0, 1) <= p_hub:
            particles[i].x = rd.uniform(-1, 1)
            particles[i].y = rd.uniform(-1, 1)
        else:
            if particles[i].x <= 10:
                particles[i].x += rd.uniform(-1, 1)
            if particles[i].y <= 10:
                particles[i].y += rd.uniform(-1, 1)
        
    #update distances
    for i in range(n):
        for j in range(i+1, n):
            d = ((particles[i].x - particles[j].x)**2 + (particles[i].y - particles[j].y)**2)**0.5
            particles[i].ds[j] = d
            particles[j].ds[i] = d
    
    #update infection             
    for i in range(n):
        if particles[i].status == 1:
            for j in range(n):
                if i == j: continue #same point
                if particles[j].status == 2: continue #removed
                if particles[i].ds.get(j) <= r_infection: #in the infection radius
                    if rd.uniform(0, 1) <= p_infection:
                        particles[j].status = 1 #infected
                        
    for i in range(n):
        if particles[i].status == 1:
            particles[i].t_infection += 1
            if particles[i].t_infection >= t_remove:
                particles[i].status = 2 #removed
                particles[i].t_infection = 0
                
    tmp_inf = int(sum([test_(p.status) for p in particles]))
    tmp_rem = int(sum([1 if p.status == 2 else 0 for p in particles]))
    H.n_infections.append(tmp_inf)
    H.n_removed.append(tmp_rem)
    H.n_susceptible.append(n - tmp_inf - tmp_rem)
    with open("H.pkl", "wb") as fp:
        pickle.dump(H, fp)
    
    
pycx.GUI().start(func=[init, visual, update])
