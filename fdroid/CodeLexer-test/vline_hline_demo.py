# -*- coding:utf-8 -*-
"""
Small demonstration of the hlines and vlines plots.
"""

import matplotlib.pyplot as plt
import numpy as np
import numpy.random as rnd
import statistics2Distance, json


def show(f1='lexer/CodeDistanceDict.pkl', f2='lexer/tokenDistanceDict.pkl'):
    f = open(f1,'r')
    d = json.load(f)
    t = statistics2Distance.byteify(d).keys()
    s = statistics2Distance.byteify(d).values()
    t = [int(x) for x in t]
    # t = np.arange(0, 128, 1)
    # s = np.arange(0.0,1000, 0.2)

    fig = plt.figure(figsize=(12, 6))
    # 将图分为一行两列，分别为1，2个子图
    vax1 = fig.add_subplot(1,2,1)
    vax2 = fig.add_subplot(1,2,2)
    # hax = fig.add_subplot(1,2,2)

    vax1.vlines(t, [0], s)
    vax1.set_xlabel('haming distance')
    vax1.set_title('source code')

    f = open(f2,'r')
    d = json.load(f)
    t = statistics2Distance.byteify(d).keys()
    s = statistics2Distance.byteify(d).values()
    t = [int(x) for x in t]

    vax2.vlines(t, [0], s)
    vax2.set_xlabel('haming distance')
    vax2.set_title('code token')
    # hax.hlines(t, [0], s, lw=2)
    # hax.set_xlabel('time (s)')
    # hax.set_title('Horizontal lines demo')

    plt.show()


if __name__ == '__main__':
    show('lexer/betweenCodeDistanceDict.pkl', 'lexer/betweenTokenDistanceDict.pkl')
    #show()