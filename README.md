This demo showcases a parameter search within the Montbrio model, focusing on optimizing Global Coupling (G) and Noise parameters to achieve the highest Functional Connectivity Dynamics (FCD) variance for each subject. Each simulation runs using a unique G and Noise parameter combination for a specific subject. The primary outputs include: 1) `maxFCDvar_log.txt`, a log file capturing the FCD variance for each simulation; and 2) Time series plots of simulated brain activity.

Much of our workflow adapts from [Virtual Aging Brain](https://github.com/ins-amu/virtual_aging_brain) and [Virtual Ageing Showcase](https://lab.ch.ebrains.eu/user-redirect/lab/tree/shared/SGA3%20D1.2%20Showcase%201/virtual_ageing). Please see [Virtual Aging Brain Notebooks]([https://github.com/ins-amu/virtual_aging_brain](https://github.com/ins-amu/virtual_aging_brain/tree/main/notebooks)) and [Virtual Ageing Showcase](https://lab.ch.ebrains.eu/user-redirect/lab/tree/shared/SGA3%20D1.2%20Showcase%201/virtual_ageing) for more detailed tutorials. 

# First-Time Installation 

You will only need to run these steps once per user per Digital Research Alliance of Canada (DRA) cluster, (e.g. Fir, Graham, Narval, etc.). The following instructions are meant to be a quickstart for installing TVB. If you come across any errors or unexpected outputs (e.g. one of the below `python3 --version` calls does not produce the expected output) then try the detailed installation [here](https://github.com/McIntosh-Lab/tvb_demo/tree/main).

The below instructions assume that you have not installed TVB before.



1. Log into your DRA cluster with Terminal or Powershell. Perform the following instructions with a clean, new session on a DRA cluster - do not load any modules before running these steps:

```
# Reset module environment
module reset

# Move to home directory
cd ~

# Create and navigate to the installation directory
mkdir TVB  # If TVB already exists, then either delete it or use a different dir name for this and remaining steps
cd TVB

# Load required modules
module load StdEnv/2020

# Verify Python version
python3 --version  # Ensure this returns 3.7.7

# Create and activate a virtual environment
python3 -m venv env
. env/bin/activate

# Upgrade pip and wheel
pip install --upgrade pip==23.3.1 wheel==0.42.0

#Download TVB_requirements.txt
wget https://raw.githubusercontent.com/McIntosh-Lab/tvb_demo/refs/heads/main/TVB_requirements.txt
```

2. Obtain the `virtual_ageing` directory from EBRAINS. Sign up for an EBRAINS account and download the `virtual_ageing` directory from [this page](https://drive.ebrains.eu/library/c8e689b3-b6c6-4c3f-a863-2223def05cbc/SGA3%20D1.2%20Showcase%201/) to your local computer.

&nbsp;&nbsp;&nbsp;&nbsp;![image](https://github.com/McIntosh-Lab/tvb_demo/assets/32205576/22e324d2-1182-4009-8f0d-60107fe903b1) 


3. Upload the downloaded `virtual_ageing` directory to your TVB directory. For instance: using a separate instance of the Terminal/Powershell app, run `scp -r ./virtual_ageing USERNAME@CLUSTER.computecanada.ca:/home/USERNAME/TVB`

4. Install the remaining packages and setup jupyterlab support. In order to use TVB in [JupyterLab](https://jupyterhub.cedar.computecanada.ca/), you will need to setup a kernel for TVB. After running the following commands, you should be able to create Notebooks with the PythonTVB kernel and run existing TVB Notebooks using the PythonTVB kernel on JupyterLab.:

```
# Install all dependencies, including virtual_aging_brain and virtual_ageing
pip install -r TVB_requirements.txt

python3 --version   # This should return 3.7.7

#
mkdir -p ~/.local/share/jupyter/kernels
pip install --no-index ipykernel
python -m ipykernel install --user --name "TVB" --display-name "TVB"   # Assuming you have not created a PythonTVB kernel before. Use a new name if you have.

```

5. If you are not planning on trying out the tvb-demo quickstart simulations, you may stop here. Otherwise, let's create a `TVB_jobs` directory in your `scratch` directory and install this repository with:    
```
cd ~/scratch
mkdir TVB_jobs
cd TVB_jobs
git clone https://github.com/McIntosh-Lab/tvb_demo.git
```

6. Your setup is complete! You may start running code, but we recommend allocating a node (see the relevant steps in "Every time you relog").


<br>

# Activating the TVB Environment for Subsequent Sessions
Once initial setup has been completed, you can run the following in subsequent SSH sessions. If you need to use TVB, make sure to load the environment you've set up, in command-line or within the script/job you intend to run:

```
. ~/TVB/env/bin/activate
```


<br>


### tvb-demo Quickstart Simulation - Interactive Session/Job (Single simulation)
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


### tvb-demo Quickstart Simulation - Multiple Job Submission (Multiple simulations)
With Job Submission, you can send multiple simulations to be run on multiple compute nodes. See here https://docs.alliancecan.ca/wiki/Running_jobs for more documentation on running jobs on Compute Canada.

1. `module load scipy-stack`

2. `. ~/TVB/virtual_aging_brain/env/bin/activate`

3. `cd ~/scratch/TVB_jobs/tvb_demo` 

4. Edit simulation configurations in `model_montbrio.py` to your needs. Pay attention to lines commented with "TO EDIT". Line 11 is especially important, as you will need to specify how your Structural Connectivity (SC) matrix files are named.

5. Edit job submitter `./batch_job_submitter.sh` to your needs. Pay attention to lines commented with "TO EDIT".

6. Submit jobs. Sample usage: `./batch_job_submitter.sh 1.65 2.05 25 0.02 0.05 7 param.txt /path/to/log_dir subjects.txt`. Run `./batch_job_submitter.sh` for help.


