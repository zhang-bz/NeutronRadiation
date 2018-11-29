import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

hour = 3600

energies = [0.250,0.230,0.200,0.150,0.100,0.07]  # MeV
spread   = [0.1020,0.0979,0.0913,0.0790,0.0645,0.0540]
thickness = [1.,2.,3.,5.]   # cm

input_protons  = 1e7
actual_protons = 1e11
beam_time = 60  # 1 min beam time

rows = []
mean=[]

# Loop over every energy & thickness
for i, e in enumerate(energies):
    for t in thickness:
        directory = "/{rThickness}-{bEnergy:03}/".format(rThickness=round(t), bEnergy=round(1000*e))

        # Read uprange data
        with open(os.getcwd() + directory + "in001_fort.27", 'r') as f:
            binwidth = 2*e*1000/140  # Gev
            lines = f.readlines()
            mergedata = []
            data = []
            data = lines[17:31]
            for i in range(len(data)):
                data[i] = data[i].split()
            for i in range(len(data)):
                mergedata = mergedata + data[i]
            for i in range(len(mergedata)):
                mergedata[i]=float(mergedata[i])*2*(np.pi)*100*binwidth/1000
                """
                print(mergedata2[i])
                print(sum(mergedata2)/sum(mergedata))
                print(len(mergedata))
                """

        # Open downrange data
        with open(os.getcwd() + directory + "in001_fort.28", 'r') as g:
            lines2 = g.readlines()
            mergedata2 = []
            data2 = []
            data2 = lines2[17:31]
            for i in range(len(data2)):
                data2[i] = data2[i].split()
            for i in range(len(data2)):
                mergedata2 = mergedata2 + data2[i]
            for i in range(len(mergedata2)):
                mergedata2[i]=float(mergedata2[i])*2*(np.pi)*100*binwidth/1000

                """
                print(mergedata2[i])
                print(sum(mergedata2)/sum(mergedata))
                print(len(mergedata))
                """

        length = np.linspace(0,(139*binwidth),num=140) + binwidth/2

        # ==== Plot the results ====
        plt.bar(x=length,height=mergedata, width=binwidth, color=(0.4,0.4,1))       # Uprange
        plt.bar(x=length,height=mergedata2, width=binwidth, color=(1,0.1,0.1,0.6))  # Downrange

        # Annotations
        plt.xlabel("Energy (GeV)")
        plt.ylabel("Ratio of number of protons leaving to number of protons entering")
        plt.title("E= {:.3f} MeV, x= {:.3f} cm".format(e, t))
        # plt.show()

        print("E= {:.3f} MeV, x= {:.3f} cm".format(e, t))

        # Calculate
        totalp = []

        meanE = np.sum([mergedata[i]*length[i] for i in range(len(mergedata))])/np.sum(mergedata)

        print(meanE)

        varE = np.sum([mergedata[i]*np.square(length[i]-meanE) for i in range(len(mergedata))])/(np.sum(mergedata))
        shepcor = varE - np.square(binwidth)/12
        print(np.sqrt(shepcor))

        """
        for i in range(len(mergedata)):
            totalp.append((mergedata[i])*(length[i]))
        print(sum(totalp)/(sum(mergedata)) - binwidth/2)

         for i in range(len(mergedata)):
            totalp.append(mergedata[i]*np.square(length[i]-meanE))
        print(sum(totalp)/(sum(mergedata)-1))

        """
