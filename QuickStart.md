## Quick Start
The following instructions are meant to be a quickstart for installing TVB. If you come across any errors or unexpected outputs (e.g. one of the below `python3 --version` calls does not produce the expected output) then try the detailed installation [here](https://github.com/McIntosh-Lab/tvb_demo/tree/main).



### Instructions

Perform the following with a clean, new Cedar session - do not load any modules before running these steps:

```
cd ~
mkdir TVB    # Assuming you don't already have a TVB install there. Otherwise, either delete the existing TVB install or use a different directory name for the rest of these steps. 
cd TVB
module load StdEnv/2020
python3 --version    # This should return 3.7.7
git clone https://github.com/ins-amu/virtual_aging_brain.git
cd virtual_aging_brain
python3   # To verify that you have python3 available
exit()
rm -rf env
python3 -m venv env
. env/bin/activate
pip3 install --upgrade pip
pip3 install wheel
pip3 install -r requirements.txt
pip3 install -e .
deactivate
cd ..
```

Obtain the `virtual_ageing` directory using steps 7 and 8 from `Initial Setup on Compute Canada` [here](https://github.com/McIntosh-Lab/tvb_demo/tree/main).

```
cd virtual_ageing/
python3 --version   # This should return 3.7.7
module load scipy-stack/2023b
. ~/TVB/virtual_aging_brain/env/bin/activate
python3 --version   # This should return 3.7.7
pip install --upgrade pip
pip install -e .
python3 --version   # This should return 3.7.7
pip install --no-index ipykernel
python -m ipykernel install --user --name "PythonTVB" --display-name "PythonTVB"   # Assuming you have not created a PythonTVB kernel before. Use a new name if you have.
```
