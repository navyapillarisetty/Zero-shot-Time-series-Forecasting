from statistical_information.IDEALEM import encoder,decoder
import numpy as np
from statistical_information.summary_stat import sum_stat,random_data

seq_length= 24

original= np.fromfile("/content/drive/My Drive/zero_shot_forecasting/Data/L1MAG_part2.csv.bin", dtype= np.float64)

# if statistical information from IDEALEM is to be used 
#numberOfbuffers= 255
#exchan= encoder(seq_length, numberOfbuffers)
#decode= decoder(seq_length, numberOfbuffers)

# for summary statistics statistical information
ran_data= random_data(original,seq_length)
print(ran_data)
np.savetxt(r"./statistical_information/stat_info_results/L1MAG_part2_summary_statistics.csv",ran_data)

# in case of LLMTime use this for summary statistics experiemnts
#mean, std= sum_stat(original,seq_length) # comment out this line

