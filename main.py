# after receiving statistical information results
# run the following code for informer output
seq_length= 24

# to get the index of reconstructed blocks
from statistical_information.IDEALEM import encoder

# if statistical information from IDEALEM is to be used 
numberOfbuffers= 255
exchan= encoder(seq_length, numberOfbuffers)

import numpy as np
import pandas as pd
import os
import subprocess

sequence_len= 24

def merging(pred,hint_i):
    pred= np.array(pred)
    hint_i= np.array(hint_i)
    pred1= pred.reshape(1*sequence_len*1)
    index= np.argsort(pred1)
    hint1= hint_i.reshape(1*sequence_len*1)
    sorted_hint= list(sorted(hint1))
    merged= list(np.zeros(len(sorted_hint)))
    for i in range(0,len(sorted_hint)):
        merged[index[i]]= sorted_hint[i]
    merged= np.array(merged)
    return merged
    

def IDEALEM_informer(train_data: str,test_data: str, hint: str):
    testing_data_loc= f"./Data/{test_data}.csv"
    #testing_data= np.loadtxt(testing_data_loc)
    for j in range(0,5,1):
        testing_data= np.loadtxt(testing_data_loc)
        overall_prediction= []
        overall_merged=[]
        test_data1_loc= f"./Data/{test_data}_{j}.csv"
        np.savetxt(test_data1_loc,testing_data)
        test_data1= f"{test_data}_{j}"
        hint_data_loc= f"./Data/{hint}_part2_decoded_incomplete.csv.bin"
        #hint_data_loc= f"./Data/{hint}_part2_stat_info.csv"
        hinting= np.fromfile(hint_data_loc)
        for i in range(0,157,1):
            subprocess.run(["python","../Informer2020-main/main_informer.py",
            "--model", "informer",
            "--data", "Part2",
            "--features", "S",
            "--attn", "prob",
            "--train_data_path", train_data,
            "--test_data_path", test_data1,
            "--label_len","48",
            "--train_epochs","6",
            "--do_predict"])
            block_pred= np.loadtxt(r"./Pred/pred_results.csv")
            testing=testing_data[sequence_len:]
            hinting1= hinting[i*sequence_len:(i*sequence_len)+sequence_len]
            merged_dat= merging(block_pred,hinting1)
            testing1= np.append(testing,merged_dat)
            testing_data= testing1
            np.savetxt(test_data1_loc,testing_data)
            overall_prediction.append(block_pred)
            overall_merged.append(merged_dat)
        overall_prediction= np.array(overall_prediction)
        overall_merged= np.array(overall_merged)
        if train_data=="ETTh1_train":
            prediction_loc= f"./Pred/{train_data}_trained_{hint}_test_{j}.csv"
            merged_loc= f"./Pred/merged_pred/{train_data}_trained_{hint}_test_{j}.csv"
        else:
            prediction_loc= f"./Pred/{train_data}_trained_{test_data}_{j}.csv"
            merged_loc= f"./Pred/merged_pred/{train_data}_trained_{test_data}_{j}.csv"
        np.savetxt(prediction_loc,overall_prediction)
        np.savetxt(merged_loc,overall_merged)
        print("#"*150, f"End of round {j}")
        
train_data= ["L1MAG_train","L2MAG_train","L3MAG_train","LIC_train","gold_price_train","bike_rentals_train","ETTh1_train"]
test_data= ["L1MAG_test","L2MAG_test","L3MAG_test","LIC_test","gold_price_test","bike_rentals_test","ETTh1_test"]
hint_data= ["L1MAG","L2MAG","L3MAG","LIC","gold_price","bike_rentals","ETTh1"]

for k in range(len(train_data)):
    if train_data[k] == "ETTh1_train":
        for l in range(len(hint_data)):
            print("ETTh1_train",hint_data[l])
            IDEALEM_informer("ETTh1_train","ETTh1_test",hint_data[l])
    else:
        print(train_data[k],test_data[k])
        IDEALEM_informer(train_data[k],test_data[k],hint_data[k])




