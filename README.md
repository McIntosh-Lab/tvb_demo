This demo showcases a parameter search within the Montbrio model, focusing on optimizing Global Coupling (G) and Noise parameters to achieve the highest Functional Connectivity Dynamics (FCD) variance for each subject. Each simulation runs using a unique G and Noise parameter combination for a specific subject. The primary outputs include: 1) `maxFCDvar_log.txt`, a log file capturing the FCD variance for each simulation; and 2) Time series plots of simulated brain activity.

Much of our workflow adapts from [Virtual Aging Brain](https://github.com/ins-amu/virtual_aging_brain) and [Virtual Ageing Showcase](https://lab.ch.ebrains.eu/user-redirect/lab/tree/shared/SGA3%20D1.2%20Showcase%201/virtual_ageing). Please see [Virtual Aging Brain Notebooks]([https://github.com/ins-amu/virtual_aging_brain](https://github.com/ins-amu/virtual_aging_brain/tree/main/notebooks)) and [Virtual Ageing Showcase](https://lab.ch.ebrains.eu/user-redirect/lab/tree/shared/SGA3%20D1.2%20Showcase%201/virtual_ageing) for more detailed tutorials. 

# Installation Quickstart
Try the [Quickstart installation instructions](https://github.com/McIntosh-Lab/tvb_demo/blob/main/QuickStart.md) first.

# Initial Setup on Compute Canada
You will only need to run these steps **once** per Compute Canada user. 

1. Open Terminal and run `module reset`.

2. Start a new SSH session on Compute Canada with `ssh <username>@cedar.alliancecan.ca`. You will be prompted for a password. The username and password should be your Digital Research Alliance of Canada or CCDB username and password. 

3. You will be logged into your home directory, or `~`,  on Cedar. You should **not** have the `scipy-stack` module loaded yet at this point.

4. Create a TVB directory with `mkdir TVB` and go into it with `cd TVB`.

5. If your current python version (output of `python3 --version`) is 3.9 or greater, then run `module load StdEnv/2020` or `module load python/3.7.7` if the StdEnv/2020 still shows python version 3.9 or greater. Run steps 1 and 2 from [Virtual Aging Brain](https://github.com/ins-amu/virtual_aging_brain) under "Python Environment in Linux and MacOS". Alternatively, run the following commands:
```
git clone https://github.com/ins-amu/virtual_aging_brain.git 
cd virtual_aging_brain 
python3 #to verify that you have python3 available
exit() 
rm -rf env
python3 -m venv env
. env/bin/activate
pip3 install --upgrade pip
pip3 install wheel
pip3 install -r requirements.txt
pip3 install -e .
```

6. Deactivate your Python environment by running `deactivate` and go back into the TVB directory with `cd ..`.

7. Sign up for an EBRAINS account and download the `virtual_ageing` directory from [this page](https://drive.ebrains.eu/library/c8e689b3-b6c6-4c3f-a863-2223def05cbc/SGA3%20D1.2%20Showcase%201/) to your local computer.

&nbsp;&nbsp;&nbsp;&nbsp;![image](https://github.com/McIntosh-Lab/tvb_demo/assets/32205576/22e324d2-1182-4009-8f0d-60107fe903b1) 


8. Upload the downloaded `virtual_ageing` directory to your TVB directory. For instance: using a separate instance of the Terminal app, run `scp -r ./virtual_ageing USERNAME@cedar.computecanada.ca:/home/USERNAME/TVB`

9. Back in your original Terminal instance, you should still be in `~/TVB` or `/home/USERNAME/TVB`. Move into the newly uploaded `virtual_ageing` directory with `cd virtual_ageing`.

10. Run ` module load scipy-stack/2020b`. If `python3 --version` does not show 3.7.7 then run `module load python/3.7.7` as well.

11. Activate the virtual_aging_brain Python environment again with `. ~/TVB/virtual_aging_brain/env/bin/activate`.

12. Install some more packages outlined in setup.py using:
 ```
 pip install --upgrade pip
 pip install -e .
 ```
If you are encountering an error, especially one along the lines of `ERROR: No matching distribution found for numpy<=1.20`, subsequently running one of the following should resolve the error:
```
module load scipy-stack
. ~/TVB/virtual_aging_brain/env/bin/activate
pip install --upgrade pip
pip install -e .
```
or
```
. ~/TVB/virtual_aging_brain/env/bin/activate
module load scipy-stack
pip install --upgrade pip
pip install -e .
```

13. Simulations and jobs in general will need to be run from `/scratch`. Let's create a `TVB_jobs` directory there and install this repository with:    
```
cd ~/scratch
mkdir TVB_jobs
cd TVB_jobs
git clone https://github.com/McIntosh-Lab/tvb_demo.git
```

14. In order to use TVB in [JupyterLab](https://jupyterhub.cedar.computecanada.ca/), you will need to setup a kernel for TVB. After running the following commands, you should be able to create Notebooks with the PythonTVB kernel and run existing TVB Notebooks using the PythonTVB kernel on JupyterLab. You must have the virtual_aging_brain Python environment activated to run the following commands. You should already have the env activated in step 11 if you have not started a new terminal session:
```
mkdir -p ~/.local/share/jupyter/kernels
pip install --no-index ipykernel
python -m ipykernel install --user --name "PythonTVB" --display-name "PythonTVB"
```
If you have JupyterHub already open, log out and restart in order to use the new kernels.

15. Your setup is complete! You may start running code, but we recommend allocating a node (see the relevant steps in "Every time you relog").


<br>

# Subsequent Sessions
Once initial setup has been completed, you can run the following in subsequent SSH sessions.

1. Open Terminal and run `ssh <username>@cedar.computecanada.ca`. Enter password when prompted.

2. Proceed below with either an Interactive Session/Job for a single simulation or Job Submission for multiple simulations 


<br>


### Interactive Session/Job (Single simulation)
You will often use an interactive session/job if you wish to run a single simulation and/or debug your workflow. This will allow you to use a compute node more directly - see: https://docs.alliancecan.ca/wiki/Running_jobs#Interactive_jobs

1. Allocate a compute node with `salloc --time=3:00:00 --mem=8000MB --account=<account>`. What you put in "\<account\>" will depend on which Compute Canada allocation you are working under. For the McIntosh lab, this will be `def-rmcintos` or `rrg-rmcintos`. Make sure you are in `~/scratch` when you run the `salloc` command.

2. `module load scipy-stack`

3. `. ~/TVB/virtual_aging_brain/env/bin/activate`

4. `cd ~/scratch/TVB_jobs/tvb_demo`

5. Edit simulation configurations in `model_montbrio.py` to your needs. Pay attention to lines commented with "TO EDIT". Line 11 is especially important, as you will need to specify how your Structural Connectivity (SC) matrix files are named.

6. You can run a simulation by calling the single simulation runner script: `python single_sim_runner.py <subject> <noise> <G>` or with an interactive python session:
```
python
import sys, os, time, fcntl
import model_montbrio
subject = "sub1"
noise = 0.03
G = 2.0
maxFCD,time_elapsed=model_montbrio.process_sub(subject,noise,G) 
```
   
<br>


### Job Submission (Multiple simulations)
With Job Submission, you can send multiple simulations to be run on multiple compute nodes. See here https://docs.alliancecan.ca/wiki/Running_jobs for more documentation on running jobs on Compute Canada.

1. `module load scipy-stack`

2. `. ~/TVB/virtual_aging_brain/env/bin/activate`

3. `cd ~/scratch/TVB_jobs/tvb_demo` 

4. Edit simulation configurations in `model_montbrio.py` to your needs. Pay attention to lines commented with "TO EDIT". Line 11 is especially important, as you will need to specify how your Structural Connectivity (SC) matrix files are named.

5. Edit job submitter `./batch_job_submitter.sh` to your needs. Pay attention to lines commented with "TO EDIT".

6. Submit jobs. Sample usage: `./batch_job_submitter.sh 1.65 2.05 25 0.02 0.05 7 param.txt /path/to/log_dir subjects.txt`. Run `./batch_job_submitter.sh` for help.


