#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=5
#SBATCH --time=10:00:00
#SBATCH --mem-per-cpu=10GB
#SBATCH --job-name=head-gen-process-data
#SBATCH --mail-type=END
#SBATCH --mail-user=mtp363@nyu.edu
#SBATCH --output=delete_errorMessage_crawlagain_%j.out
#SBATCH --gres=gpu:v100:1
  
# Refer to https://sites.google.com/a/nyu.edu/nyu-hpc/documentation/prince/batch/submitting-jobs-with-sbatch
# for more information about the above options

# Remove all unused system modules
module purge

# Activate the conda environment
module load anaconda3
source activate nhnet_env

DATA_FOLDER=/misc/vlgscratch5/PichenyGroup/s2i-common/headline-generation/models/official/nlp/nhnet
MODEL_DIR=/misc/vlgscratch5/PichenyGroup/s2i-common/headline-generation/nlp/nhnet/model_output

# Execute the script

# Training
news-please -c $DATA_FOLDER/news_please_valtest

# And we're done!
