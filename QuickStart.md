## Quick Start
You will only need to run these steps once per Compute Canada user. The following instructions are meant to be a quickstart for installing TVB. If you come across any errors or unexpected outputs (e.g. one of the below `python3 --version` calls does not produce the expected output) then try the detailed installation [here](https://github.com/McIntosh-Lab/tvb_demo/tree/main).

The below instructions assume that you have not installed TVB before.


### Instructions

Perform the following with a clean, new Cedar session - do not load any modules before running these steps:

```
# Reset module environment
module reset

# Move to home directory
cd ~

# Create and navigate to the installation directory
mkdir TVB  # Skip this if TVB already exists
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
wget https://raw.githubusercontent.com/McIntosh-Lab/tvb_demo/refs/heads/dev/TVB_requirements.txt

```


Obtain the `virtual_ageing` directory using steps 7 and 8 from `Initial Setup on Compute Canada` [here](https://github.com/McIntosh-Lab/tvb_demo/tree/main).

```
# Install all dependencies, including virtual_aging_brain and virtual_ageing
pip install -r requirements_freeze.txt

python3 --version   # This should return 3.7.7

#
mkdir -p ~/.local/share/jupyter/kernels
pip install --no-index ipykernel
python -m ipykernel install --user --name "PythonTVB" --display-name "PythonTVB"   # Assuming you have not created a PythonTVB kernel before. Use a new name if you have.
```
