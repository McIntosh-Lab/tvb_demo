This demo showcases a parameter search within the Montbrio model, focusing on optimizing Global Coupling (G) and Noise parameters to achieve the highest Functional Connectivity Dynamics (FCD) variance for each subject. Each simulation runs using a unique G and Noise parameter combination for a specific subject. The primary outputs include: 1) `maxFCDvar_log.txt`, a log file capturing the FCD variance for each simulation; and 2) Time series plots of simulated brain activity.

Much of our workflow adapts from [Virtual Aging Brain](https://github.com/ins-amu/virtual_aging_brain) and [Virtual Ageing Showcase](https://lab.ch.ebrains.eu/user-redirect/lab/tree/shared/SGA3%20D1.2%20Showcase%201/virtual_ageing). Please see [Virtual Aging Brain Notebooks]([https://github.com/ins-amu/virtual_aging_brain](https://github.com/ins-amu/virtual_aging_brain/tree/main/notebooks)) and [Virtual Ageing Showcase](https://lab.ch.ebrains.eu/user-redirect/lab/tree/shared/SGA3%20D1.2%20Showcase%201/virtual_ageing) for more detailed tutorials. 

# Initial Setup on Compute Canada
You will only need to run these steps **once** per Compute Canada user. 

1. Open Terminal.

2. Start a new SSH session on Compute Canada with `ssh <username>@cedar.computecanada.ca`. You will be prompted for a password. The username and password should be your Digital Research Alliance of Canada or CCDB username and password.

3. You will be logged into your home directory on Cedar.

4. Create a TVB directory with `mkdir TVB` and go into it with `cd TVB`.

5. Run steps 1 and 2 from [Virtual Aging Brain](https://github.com/ins-amu/virtual_aging_brain) under "Python Environment in Linux and MacOS". Alternatively, run the following commands:
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

6. Go back into the TVB directory with `cd ..`.

7. Create another directory called "virtual_ageing" with `mkdir virtual_ageing` and move into it with `cd virtual_ageing`.

8. Create a file called "setup.py" by running `nano setup.py` and pasting in the following lines:
```
from setuptools import find_packages, setup

setup(
    name='showcase1_ageing',
    packages=find_packages(),
    version='0.1.0',
    install_requires=[
        'numpy<=1.20',
        'pingouin',
        'joblib',
        'siibra',
        'ipywidgets',
        'seaborn',
        'pandas',
        'pyunicore==0.9.12',
        'dataclasses',
        'ebrains-drive',
        'pyro-ppl==1.3.1',
        'torch==1.6.0',
        'sbi==v0.14.2',
        'tvb-library @ git+https://github.com/the-virtual-brain/tvb-root/@parameters-api#egg=tvb-library&subdirectory=scientific_library',
        'tvb-ebrains-data @ git+https://gitlab.ebrains.eu/fousekjan/tvb-ebrains-data.git@0.2.5'
    ]
)
```

9. Press "ctrl+x", followed by "y" and then "enter" to save setup.py.

10. Run `module load scipy-stack`.

11. Activate the virtual_aging_brain Python environment with `. ~/TVB/virtual_aging_brain/env/bin/activate`.

12. Install some more packages outlined in setup.py using:
 ```
 pip install --upgrade pip
 pip install -e .
 ```

13. Move back into the TVB folder and install this repository with:    
```
cd ~/TVB
git clone https://github.com/McIntosh-Lab/tvb_demo.git
```

14. Your setup is complete! You may start running code, but we recommend allocating a node (see the relevant steps in "Every time you relog").


<br>

# Subsequent Sessions
Once initial setup has been completed, you can run the following in subsequent SSH sessions.

1. Open Terminal and run `ssh <username>@cedar.computecanada.ca`. Enter password when prompted.

2. Proceed below with either an Interactive Session/Job for a single simulation or Job Submission for multiple simulations 


<br>


### Interactive Session/Job (Single simulation)
You will often use an interactive session/job if you wish to run a single simulation and/or debug your workflow. This will allow you to use a compute node more directly - see: https://docs.alliancecan.ca/wiki/Running_jobs#Interactive_jobs

1. Allocate a compute node with `salloc --time=3:00:00 --mem=8000MB --account=<account>`. What you put in "\<account\>" will depend on which Compute Canada allocation you are working under. For the McIntosh lab, this will be `def-rmcintos` or `rrg-rmcintos`. 

2. `module load scipy-stack`

3. `. ~/TVB/virtual_aging_brain/env/bin/activate`

4. `cd ~/TVB/tvb_demo`

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

1. `cd ~/TVB/tvb_demo` 

2. Edit simulation configurations in `model_montbrio.py` to your needs. Pay attention to lines commented with "TO EDIT". Line 11 is especially important, as you will need to specify how your Structural Connectivity (SC) matrix files are named.

3. Edit job submitter `./batch_job_submitter.sh` to your needs. Pay attention to lines commented with "TO EDIT".

4. Submit jobs. Sample usage: `./batch_job_submitter.sh 1.65 2.05 25 0.02 0.05 7 param.txt /path/to/log_dir subjects.txt`. Run `./batch_job_submitter.sh` for help.


