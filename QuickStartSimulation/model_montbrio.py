import sys, os, time
import numpy as np
import showcase1_ageing as utils
from tvb.simulator.lab import *
from tvb.simulator.backend.nb_mpr import NbMPRBackend
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

#from tvb.simulator.lab import connectivity, simulator, models, coupling, integrators, monitors, noise

def get_connectivity(scaling_factor, subject):
    """
    Loads and scales the structural connectivity matrix for a given subject.
    """
    SC = np.loadtxt('/home/USER/scratch/TVB/SC/' + subject + '_weights.txt')   #TO EDIT - Location of SC files
    SC = SC / scaling_factor
    conn = connectivity.Connectivity(
        weights=SC,
        tract_lengths=np.ones_like(SC),
        centres=np.zeros(np.shape(SC)[0]),
        speed=np.r_[np.Inf]
    )
    conn.compute_region_labels()
    return conn

def compute_fc(bold_d):
    """
    Computes the functional connectivity matrix from BOLD data.
    """
    rsFC = np.corrcoef(bold_d[:,0,:,0].T)
    rsFC = rsFC - np.diag(np.diagonal(rsFC))
    return rsFC

def process_sub(subject, my_noise, my_G):
    """
    Runs the simulation for a given subject, noise, and G value,
    and computes the functional connectivity dynamics.
    """
    start_time = time.time()

    scaling_factor=1 #TO EDIT - number by which to divide all SC values. May require tuning if no simulated brain activity is seen.
    my_dt=0.000625 #TO EDIT
    my_TE=0.03  #TO EDIT - TE
    my_decimate=2500   #TO EDIT - TR in ms
    save_outputs=0 #TO EDIT - Currently set to 0, for no output saving (FC, FCD, BOLD time series). Set to 1 for output saving. Regardless of setting, an ROI-stacked simulated activity plot will be generated for each sim.
    
    output_dirpath="/home/USER/scratch/TVB/outputs/${subject}/"  #TO EDIT - Location to save any outputs.
    maxFCDvar_log="/home/USER/scratch/TVB/outputs/maxFCDvar_log.txt"  #TO EDIT - Location of log file, which will keep track of the FCDvar of each simulation.


    sim = simulator.Simulator(
        connectivity=get_connectivity(scaling_factor, subject),
        model=models.MontbrioPazoRoxin(
            eta=np.r_[-4.6],
            J=np.r_[14.5],
            Delta=np.r_[0.7],
            tau=np.r_[1.],
        ),
        coupling=coupling.Linear(a=np.r_[my_G]),
        integrator=integrators.HeunStochastic(
            dt=my_dt,
            noise=noise.Additive(nsig=np.r_[my_noise, my_noise*2])
        ),
        monitors=[monitors.TemporalAverage(period=0.1)]
    ).configure()

    # Run the simulation
    runner = NbMPRBackend()
    (tavg_t, tavg_d), = runner.run_sim(sim, simulation_length=30e3)
    tavg_t *= 10
    
    
    
    # Process and save the simulation data
    bold_t, bold_d = utils.tavg_to_bold(tavg_t, tavg_d, tavg_period=1.,decimate=my_decimate,TE=my_TE)
    bold_t, bold_d = bold_t[2:], bold_d[2:]  # Cut the initial transient (10s)
    file_suffix = f"{subject}_{my_G}_{my_noise}"

    #save ROI-stacked simulated activity plot  
    ax = utils.plot_ts_stack(tavg_d[1*1000:20*1000:10,0,:,0], x=tavg_t[1*1000:20*1000:10]/1000., width=20)
    ax.set(xlabel='time [s]')
    plt.savefig(f"{output_dirpath}{file_suffix}_ts.png")
    
    if not save_outputs == 0: 
        # Save time series data
        np.save(f"{output_dirpath}{file_suffix}_bold_t.npy", bold_t)
        np.save(f"{output_dirpath}{file_suffix}_bold_d.npy", bold_d)
        
        # Compute and save FCD and FC
        FCD, _ = utils.compute_fcd(bold_d[:,0,:,0], win_len=40)
        FCD_VAR_OV_vect = np.var(np.triu(FCD, k=40))
        np.save(f"{output_dirpath}{file_suffix}_simulated_FCD.npy", FCD)

        FC = compute_fc(bold_d)
        np.save(f"{output_dirpath}{file_suffix}_simulated_FC.npy", FC)

    # Update and save FCD variance to the log file
    df = pd.read_csv(maxFCDvar_log, delimiter='\t', header=None)
    df.loc[(df[0] == subject) & (df[1] == my_noise) & (df[2] == my_G), 3] = FCD_VAR_OV_vect
    df.to_csv(maxFCDvar_log, sep='\t', header=False, index=False)

    end_time = time.time()
    return [FCD_VAR_OV_vect, end_time - start_time]
