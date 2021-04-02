#!/usr/bin/env python
# coding: utf-8
#
# My (Emmy) Phung
# NLP class Spring 2021
#
# Run HMM model and generate POS tags for test set (WSJ_23.words)


from data_processing import *
import time

def main(args):
    dataname = args[1]
    outname = args[2]
    
    cwd = os.getcwd()
    data_dir = os.path.join(cwd, dataname)
    print(data_dir)
    start_time = time.time()
    #Load train_data, dev_data, train_dev_data, test_data
    df = Processor().process(data_dir)
    
    file_dir = os.path.join(cwd, outname)
    df.to_csv(file_dir, encoding='utf-8', index=True)
    print('The code takes {0} seconds'.format(time.time() - start_time))
    
if __name__ == '__main__': 
    sys.exit(main(sys.argv))
       

