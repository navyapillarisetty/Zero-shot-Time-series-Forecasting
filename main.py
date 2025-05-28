# after receiving statistical information results
# run the following code for informer output

python -u "./Informer/main_informer.py" --model informer --features S --attn prob --do_predict

# post processing steps



seq_length= 24

# to get the index of reconstructed blocks
from statistical_information.IDEALEM import encoder

# if statistical information from IDEALEM is to be used 
numberOfbuffers= 255
exchan= encoder(seq_length, numberOfbuffers)


import numpy as np
import pandas as pd
import torch
import math
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error


# the statistical information data path
data_path= "./statistical_information/summary_stat_out/L1MAG_part2_summary_statistics.csv"

if data_path.endswith(".csv"):
    hint= np.loadtxt(data_path)
elif data_path.endswith(".bin"):
    hint= np.fromfile(data_path)
else:
    hint= pd.read_csv(data_path,header=0)

hint1= pd.DataFrame(hint)

prediction= np.loadtxt("../results/L1MAG_part2_preds.csv")

class StandardScaler():
    def __init__(self):
        self.mean = 0.
        self.std = 1.

    def fit(self, data):
        self.mean = data.mean(0)
        self.std = data.std(0)

    def transform(self, data):
        mean = torch.from_numpy(self.mean).type_as(data).to(data.device) if torch.is_tensor(data) else self.mean
        std = torch.from_numpy(self.std).type_as(data).to(data.device) if torch.is_tensor(data) else self.std
        return (data - mean) / std

    def inverse_transform(self, data):
        mean = torch.from_numpy(self.mean).type_as(data).to(data.device) if torch.is_tensor(data) else self.mean
        print(mean)
        std = torch.from_numpy(self.std).type_as(data).to(data.device) if torch.is_tensor(data) else self.std
        print(std)
        mean1= pd.Series(mean)
        print(data.shape)
        print(mean1.shape)
        if data.shape[-1] != mean1.shape[-1]:
            mean = mean[-1:]
            std = std[-1:]
        return (data * std) + mean
    

# since informer is predictive model last sequence length block is removed 
hint_x= hint1
scaler= StandardScaler()
scaler.fit(hint_x)
pred= pd.DataFrame(prediction)
pred1= scaler.inverse_transform(pred)
pred1= np.array(pred1)
pred1= pred1[:(len(pred1)-seq_length)]

pred2= pred1.reshape((len(pred1))//seq_length,seq_length,1)

fake= []
length= len(pred2)
for i in range(0,length,seq_length):
    dat2= pred2[i]
    fake.append(dat2)
print(len(fake))

original= np.fromfile("./Data/L1MAG_part2.csv.bin", dtype= np.float64)
original= original[seq_length*4:]
original= np.array(original)
original1= original.reshape((len(original)//seq_length),seq_length,1)

fake= np.array(fake)

y= exchan

original=[]
synthetic_n=[]
for i in range(len(y)):
    ori= original1[y[i]]
    syn= fake[y[i]]
    original.append(ori)
    synthetic_n.append(syn)
#print(len(original))
#print(len(synthetic_n))

original= np.array(original)
synthetic= np.array(synthetic_n)
ori= original.reshape((len(original))*seq_length)
syn= synthetic.reshape((len(synthetic))*seq_length)

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

figure(figsize=(20,5), dpi=80)
plt.plot(ori, color="red", label="Ground truths")
plt.plot(syn, color= "blue", label="Before merging")
plt.grid()
plt.title("Before merging plot")
plt.legend()
plt.show()

def SMAPE(Y_real, Y_fake):
    smape= np.mean((np.abs(Y_real - Y_fake))/(abs(Y_real) + abs(Y_fake)))*100
    return smape

mse= mean_squared_error(ori, syn)
mae= mean_absolute_error(ori, syn)
smape= SMAPE(ori, syn)
print("Before merging error")
print("mse: ",mse, "mae: ", mae)
print("smape: ",smape)

decoded1= hint
decoded= decoded1.reshape((len(decoded1))//seq_length,seq_length)
decode= decoded[4:]

dec=[]
for i in range(len(y)):
    decoding= decode[y[i]]
    dec.append(decoding)
print(len(dec))

index_data=[]
for g in synthetic_n:
    arr= np.array(g)
    arr1= arr.reshape(1*seq_length*1)
    index= np.argsort(arr1)
    index_data.append(index)
sorted_data= []
for h in dec:
    decoded2= np.array(h)
    decoded3= decoded2.reshape(1*seq_length*1)
    #print(decoded3)
    sorted_dec= list(sorted(decoded3))
    sorted_data.append(sorted_dec)


merged_data=[]
for u in range(len(index_data)):
    index1= index_data[u]
    sort= sorted_data[u]
    merged= list(np.zeros(len(sort)))
    for i in range(0,len(sort)):
        merged[index1[i]]= sort[i]
    merged_data.append(merged)
merged_data= np.array(merged_data)
merged_data1= merged_data.reshape((len(merged_data))*seq_length)

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

figure(figsize=(20,5), dpi=80)
plt.plot(ori, color="red", label="Ground truths")
plt.plot(merged_data1, color= "blue", label="After merging")
plt.title("After merging plots")
plt.legend()
plt.show()

mse1= mean_squared_error(ori, merged_data1)
mae1= mean_absolute_error(ori, merged_data1)
smape1= SMAPE(ori, merged_data1)
print("merged error")
print("mse: ",mse1, "mae: ", mae1)
print("smape: ",smape1)
