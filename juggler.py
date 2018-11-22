# coding: utf-8
# python 2.7
# juggler.py

import numpy as np

class ImJugglerEX:

    def __init__(self, settei=1):

        self.big_prob = np.array([1./287.4, 1./282.5, 1./282.5, 1./273.1, 1./273.1, 1./268.6])
        self.reg_prob = np.array([1./455.1, 1./442.8, 1./348.6, 1./321.3, 1./268.6, 1./268.6])
        self.grape_prob = np.array([1./6.49, 1./6.49, 1./6.49, 1./6.49, 1./6.49, 1./6.18])
        self.cherry_prob = np.array([1./33.6, 1./33.6, 1./33.4, 1./33.2, 1./33.0, 1./33.0])
        self.big = self.big_prob[settei-1]
        self.reg = self.reg_prob[settei-1]
        self.grape = self.grape_prob[settei-1]
        self.cherry = self.cherry_prob[settei-1]
        self.setting = settei