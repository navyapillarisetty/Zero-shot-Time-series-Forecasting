import numpy as np

def sum_stat(data,seq_length):
    reshap_data= data.reshape((len(data))//seq_length,seq_length,1)
    mean_arr= []
    std_arr= []
    for i in range(len(reshap_data)):
        mean_arr.append(np.mean(reshap_data[i]))
        std_arr.append(np.std(reshap_data[i]))
    print(mean_arr)
    print(len(mean_arr))
    return mean_arr, std_arr

def random_data(data,seq_length):
    stat_info= []
    mean, std= sum_stat(data, seq_length)
    for i in range(len(mean)):
        stat_info.append(np.random.normal(mean[i],std[i], seq_length))
    stat_info= np.array(stat_info)
    stat_info1= stat_info.reshape(len(stat_info)*seq_length)
    np.savetxt(r"..\L1MAG_part2_summary_statistics.csv",stat_info1)
    return stat_info1

