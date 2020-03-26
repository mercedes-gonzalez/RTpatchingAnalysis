import numpy as np
import scipy as sp
import scipy.signal as sig
import pyabf
import pyabf.tools.memtest as mem
import matplotlib.pyplot as plt
import axographio as axo

    # Access sweep data
    # for i in range(3):
    #     abf.setSweep(i)
    #     plt.plot(abf.sweepX,abf.sweepY, alpha=.5, label="sweep %d" % (i))
    # plt.legend()
    # plt.show()

def countAPs(abf, sweep_idx, show_plots):
    # Purpose: To count the number of APs in a trace
    # Inputs: N/A
    # Outputs: N/A
    abf.setSweep(sweep_idx, channel=0)
    time = abf.sweepX
    data = abf.sweepY

    abf.setSweep(sweep_idx, channel=1)
    command = abf.sweepY

    # GET COMMAND
    baseline_cmd = np.array(command[0:10]).mean() #get baseline command (no input)
    is_on = command > baseline_cmd # Create logical mask for when command input is on
    input_dur = np.sum(is_on) # number of samples collected with input ON
    input_cmd = np.array(command[is_on]).mean() # get average of input command
#     print("%f pA\n" % input_cmd) 


    # GET NUMBER OF ACTION POTENTIALS
    baseline_data = np.array(data[0:10]).mean() # get baseline data
    peaks, _ = sig.find_peaks(data,height=.5*baseline_data,distance=50,rel_height=0)
    num_APs = len(peaks)

    if show_plots:
        plt.figure(1)
        plt.plot(time,data)
        plt.plot(time[peaks], data[peaks],"x")
        plt.show()
#     print("%i APs\n" % num_APs)

    return input_cmd, num_APs, input_dur

def plotMembraneTest(abf):
    # Purpose: To extract the membrane test parameters from an ABF file
    # Inputs: N/A
    # Outputs: N/A
    memtest = mem.Memtest(abf)
    fig = plt.figure(figsize=(8, 5))

    ax1 = fig.add_subplot(221)
    ax1.grid(alpha=.2)
    ax1.plot(abf.sweepTimesMin, memtest.Ih.values,
            ".", color='C0', alpha=.7, mew=0)
    ax1.set_title(memtest.Ih.name)
    ax1.set_ylabel(memtest.Ih.units)

    ax2 = fig.add_subplot(222)
    ax2.grid(alpha=.2)
    ax2.plot(abf.sweepTimesMin, memtest.Rm.values,
            ".", color='C3', alpha=.7, mew=0)
    ax2.set_title(memtest.Rm.name)
    ax2.set_ylabel(memtest.Rm.units)

    ax3 = fig.add_subplot(223)
    ax3.grid(alpha=.2)
    ax3.plot(abf.sweepTimesMin, memtest.Ra.values,
            ".", color='C1', alpha=.7, mew=0)
    ax3.set_title(memtest.Ra.name)
    ax3.set_ylabel(memtest.Ra.units)

    ax4 = fig.add_subplot(224)
    ax4.grid(alpha=.2)
    ax4.plot(abf.sweepTimesMin, memtest.CmStep.values,
            ".", color='C2', alpha=.7, mew=0)
    ax4.set_title(memtest.CmStep.name)
    ax4.set_ylabel(memtest.CmStep.units)

    for ax in [ax1, ax2, ax3, ax4]:
        ax.margins(0, .9)
        ax.set_xlabel("Experiment Time (minutes)")
        for tagTime in abf.tagTimesMin:
            ax.axvline(tagTime, color='k', ls='--')
    plt.tight_layout()
    plt.show()
    return