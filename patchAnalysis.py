import numpy as np
import scipy as sp
import pyabf
import matplotlib.pyplot as plt
import axographio as axo

def countAPs():
    abf = pyabf.ABF('C:/Users/mgonzalez91/Dropbox (GaTech)/Research/All Things Emory !/Emory-Patching/1-23-2020/2020_01_23_0016.abf')
    print(abf,'\n')
    # abf.headerLaunch()

    # Access sweep data
    for i in range(3):
        abf.setSweep(i)
        plt.plot(abf.sweepX,abf.sweepY, alpha=.5, label="sweep %d" % (i))
    plt.legend()
    plt.show()
    return