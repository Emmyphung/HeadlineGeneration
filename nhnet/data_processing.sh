#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=5
#SBATCH --time=5:00:00
#SBATCH --mem-per-cpu=10GB
#SBATCH --job-name=head-gen-reprocess-big-data
#SBATCH --mail-type=END
#SBATCH --mail-user=mtp363@nyu.edu
#SBATCH --output=delete_errorMessage_preprocess_small_%j.out
#SBATCH --gres=gpu:1
  
# Refer to https://sites.google.com/a/nyu.edu/nyu-hpc/documentation/prince/batch/submitting-jobs-with-sbatch
# for more information about the above options

# Remove all unused system modules
module purge

# Activate the conda environment
module load anaconda3
source activate env_nlp_conda

DATA_FOLDER=/misc/vlgscratch5/PichenyGroup/s2i-common/headline-generation/models/official/nlp/nhnet/crawled_data_small
BERT_CKPT=/misc/vlgscratch5/PichenyGroup/s2i-common/headline-generation/models/official/nlp/nhnet/bert_checkpoint
OUTPUT_FOLDER=/misc/vlgscratch5/PichenyGroup/s2i-common/headline-generation/models/official/nlp/nhnet

# Execute the script
python3 raw_data_process.py \
-crawled_articles=$DATA_FOLDER \
-vocab=$BERT_CKPT/vocab.txt \
-do_lower_case=True \
-len_title=15 \
-len_passage=200 \
-max_num_articles=1 \
-data_folder=$OUTPUT_FOLDER

# And we're done!
