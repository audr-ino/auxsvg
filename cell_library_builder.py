import pandas as pd
import numpy as np
from scipy import signal as si
import os


path = r"C:\Users\user\Documents\auxetics\bistable-auxetics\data"

filenames = []
for root, dirs, files in os.walk(path,topdown=False):
    for name in files:
        filenames.append(os.path.join(root,name))


tuples = []
for filename in filenames:
    
    # filename format : c_l_10.0_t_0.1_theta_0.0_phi_0.0_c_0.25_s_0.125_c2o.csv
    t = filename.split("_")[4]
    theta = filename.split("_")[6]

    df = pd.read_csv(filename)
    # print(df.to_string()) 

    # first col = strain
    # third col = energy
    # looking for local energy max - local energy min (energy barrier)
    # and slope of local energy min (stiffness)
    # and the expansion that causes local energy min

    strain = np.array(df.iloc[:, 0])
    energy = np.array(df.iloc[:, 2])

    try:
        energy_max_index = si.argrelextrema(energy, np.greater)[0][0]
        energy_min_index = si.argrelextrema(energy, np.less)[0][0]

        energy_max = energy[energy_max_index]
        energy_min = energy[energy_min_index]

        energy_barrier = energy_max-energy_min

        expansion = strain[energy_min_index]

        stiffness = (energy[energy_min_index+2]-energy[energy_min_index])/(strain[energy_min_index+2]-strain[energy_min_index])

        tuples.append([expansion,energy_barrier,stiffness,t,theta])

    except:
        tuples.append([None,None,None,t,theta])

cells_df = pd.DataFrame(tuples, columns = ['Expansion', 'Energy_Barrier','Stiffness','t','theta'])

cells_df.to_csv("cells_df.csv", index=False,na_rep='NULL')
