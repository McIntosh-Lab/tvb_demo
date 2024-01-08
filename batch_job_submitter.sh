#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 9 ]; then
    echo "Usage: $0 min_g max_g num_g_values min_noise max_noise num_noise_values paramfile log_directory list_of_subjects"
    echo "Example: $0 1.65 2.05 25 0.02 0.05 7 param.txt /path/to/log_dir subjects.txt"
    echo "G and noise values will be explored within their specified minimum and maximum ranges. The script will generate 'num_X_values' distinct values for both G and noise, ensuring these values are evenly distributed within their respective ranges."
    echo "paramfile is the name of a file to be created, which will contain your desired paramater combinations for the parameter space search"
    echo "log directory will contain the job logs"
    echo "list_of_subjects is the path to a file containing a list of your subjects, one per line"

    exit 1
fi

# Assign the input arguments to variables
min_g=$1
max_g=$2
num_g_values=$3
min_noise=$4
max_noise=$5
num_noise_values=$6
paramfile=$7
log_directory=$8 # Directory for log files, no trailing forward slash
list_of_subjects=$9 # File containing list of subjects

# Function to generate equally spaced values between min and max, inclusive
generate_values() {
    local min=$1
    local max=$2
    local num_values=$3
    local increment
    increment=$(bc -l <<< "($max - $min) / ($num_values - 1)") # Calculate increment

    local values=()
    for ((i=0; i<num_values; i++)); do
        local value
        value=$(bc -l <<< "$min + ($increment * $i)") # Calculate each value
        values+=($value)
    done
    echo "${values[@]}"
}

# Generate G and noise values
g_values=($(generate_values $min_g $max_g $num_g_values))
noise_values=($(generate_values $min_noise $max_noise $num_noise_values))

# Create combinations and write them to the file
> "$paramfile"  # Clear the file before writing
for g in "${g_values[@]}"; do
    for noise in "${noise_values[@]}"; do
        echo "$g $noise" >> "$paramfile" # Write each combination to the file
    done
done

# Read subjects and parameter combinations, then submit batch jobs
while IFS=$' ' read -r subject; do
    while IFS=$' ' read -r noise G; do
        # Submit a batch job for each combination of subject, noise, and G
        sbatch -J "${subject}_noise_${noise}_G_${G}_sim" -o "${log_directory}/${subject}_noise-${noise}_G_${G}_sim.out" "/home/${USER}/TVB/tvb_demo/sbatch.sh" "${subject}" "${noise}" "${G}"   # TO EDIT
        
        # No enforced time limit, check for missing outputs for overtime simulations
    done < "$paramfile"
done < "$list_of_subjects"
