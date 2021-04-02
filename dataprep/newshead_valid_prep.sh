#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=5
#SBATCH --time=5:00:00
#SBATCH --mem-per-cpu=10GB
#SBATCH --job-name=newshead_valid
#SBATCH --mail-type=END
#SBATCH --mail-user=mtp363@nyu.edu
#SBATCH --output=delete_errorMessage_%j.out
#SBATCH --gres=gpu
  
# Refer to https://sites.google.com/a/nyu.edu/nyu-hpc/documentation/prince/batch/submitting-jobs-with-sbatch
# for more information about the above options

# Remove all unused system modules
module purge

# Activate the conda environment
module load anaconda3
source activate nlp_env
DATA_PATH=//misc/vlgscratch5/PichenyGroup/s2i-common/headline-generation/data

# Execute the script

python dataprep_main.py $DATA_PATH/newshead_raw/valid.json $DATA_PATH/newshead_valid.csv
# And we're done!
