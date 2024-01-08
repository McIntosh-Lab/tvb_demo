#!/bin/bash
#SBATCH --account=def-rmcintos
#SBATCH --mem=8000MB
#SBATCH --time=0-6:36


subject=${1} 
noise=${2} 
G=${3}

python single_sim_runner.py ${subject} ${noise} ${G} 
