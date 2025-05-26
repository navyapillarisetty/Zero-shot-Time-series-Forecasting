import struct
from scipy import stats
import math
import numpy as np
import random

def encoder(seq_length,numberOfbuffers):
    size=blockLength*8
    alpha=0.02
    counter=0
    # list which stores distribution
    distribution=[]

    #KStest

    def nint(x):
            if x >= 0:
            i = int(x + 0.5)
            if (i & 1) and (x + 0.5) == i:
                i-=1
        else:
            i = int(x - 0.5)
            if (i & 1) and (x - 0.5) == i:
                i+=1
        return i;

    def KolmogorovProb(z):
        
        fj = [-2,-8,-18,-32]
        r=[None]*4
        w = 2.50662827

        const1 = -1.2337005501361697
        const2 = -11.103304951225528
        const3 = -30.842513753404244

        u = abs(z)
        if u < 0.2:
            p = 1
        elif u < 0.755:
            v = 1.0/(u*u)
            p = 1 - w*(math.exp(const1*v) + math.exp(const2*v) + math.exp(const3*v))/u
        elif u < 6.8116:
            r[1] = 0
            r[2] = 0
            r[3] = 0
            v = u*u;
            maxj = max(1,nint(3.0/u))
            for j in range (maxj):
                r[j] = math.exp(fj[j]*v)
            p = 2*(r[0] - r[1] + r[2] - r[3])
        else:
            p = 0
        return p

    def KolmogorovTest(na, a, nb, b):
        prob = -1

        if not a or not b:
            print("KolmogorovTest : NULL pointer")
            return prob
        if not a or not b or na <= 2 or nb <= 2:
            return 0
        #   //  Constants needed
        rna = na
        rnb = nb
        sa  = 1.0/rna
        sb  = 1.0/rnb
        rdiff = 0
        rdmax = 0
        ia = 0
        ib = 0
        #   // Main loop over point sets to find max distance
        #   // rdiff is the running difference, and rdmax the max.
        done = 0

        for i in range(na+nb):
            if a[ia] < b[ib]:
                rdiff -= sa
                ia+=1
                if ia >= na:
                    done = 1
                    break
            elif a[ia] > b[ib]:
                rdiff += sb
                ib+=1;
                if ib >= nb:
                    done = 1
                    break
            else:
                x = a[ia]
                while(ia < na and a[ia] == x):
                    rdiff -= sa
                    ia+=1
                while(ib < nb and b[ib] == x ):
                    rdiff += sb
                    ib+=1
                if (ia >= na):
                    done = 1
                    break
                if (ib >= nb):
                    done = 1
                    break
            rdmax = np.fmax(rdmax,abs(rdiff))

        if done==1:
            rdmax = np.fmax(rdmax,abs(rdiff))
            z = rdmax * math.sqrt(rna*rnb/(rna+rnb))
            prob = KolmogorovProb(z)
            return prob

    #encoder
    cnt= 0
    exchan=[]

    with open(r"..\L1MAG_part2.csv.bin", "rb") as binary_file: #reading file
        with open(r"..\L1MAG_part2_encoded.csv.bin.idealem", "wb",buffering = 1000000) as idealem_file: #output to file


            while True:
                exchangeability=False
                # when file has remain, unpack the file
                try: # converting binary to decimal
                    data=struct.unpack('d'*blockLength, binary_file.read(size))
                # when all file are unpacked, out of loop
                except:
                    break

                # This for loop starts when number of length of distribution is bigger than number of buffers 
                for i in range(min(len(distribution),numberOfbuffers)):
                    # pvalue is calculated by KS test
                    pvalue = KolmogorovTest( blockLength, sorted(distribution[i]), blockLength, sorted(data) )
                    # if data is exchangeable, the data compress to 1 byte which is index of distribution
                    if pvalue>=alpha:
                        exchangeability=True
                        #print(i)
                        #converting decimal to binary
                        b_i=struct.pack('B',i)
                        #writing to compressed file
                        idealem_file.write(b_i)
                        exchan.append(cnt)
                        break

                b_data=struct.pack('d'*blockLength, *data)
                #non-exchangeable
                if exchangeability==False:
                    # changingIndex indicates the index which is going to be overwritten
                    changingIndex=counter%numberOfbuffers
                    #print(changingIndex)
                    # converting decimal to binary
                    b_changingIndex=struct.pack('B',changingIndex)

                    # if length of distribution is less than number of buffers, data will be appended in the list and the compressed file
                    if len(distribution)<numberOfbuffers:
                        distribution.append(data)
                        #print(changingIndex)
                        # writing binary index into compressed file
                        idealem_file.write(b_changingIndex)
                        # print(data)
                        # writing binary data into compressed file
                        idealem_file.write(b_data)
                    else:
                        # delete oldest index and add new index to the oldest index position
                        distribution.pop(changingIndex)
                        distribution.insert(changingIndex,data)
                        b_ff=struct.pack('B',255)
                        idealem_file.write(b_ff)
                        # print('FF')
                        # writing binary index into compressed file
                        idealem_file.write(b_changingIndex)
                        # print(changingIndex)
                        # writing binary data into compressed file
                        idealem_file.write(b_data)
    #                    print(data)
                    counter+=1
                cnt+=1
    return exchan



def decoder(seq_length,numberOfbuffers):

    size=blockLength*8
    alpha=0.02
    size=blockLength*8
    counter=0
    place=[]
    index=[]



    with open(r"..\L1MAG_part2_encoded.csv.bin.idealem", "rb") as binary_file: # read compressed file
        with open(r"..\L1MAG_part2_decoded.csv.bin.idealem.bin", "wb") as idealem_file: # write decompressed data
            # converting binary index to decimal
            data=struct.unpack('B', binary_file.read(1))
            #for q, data in enumerate(data, start=1):
                #print(q,data)
            #print(data)

            while data:
                # if there is no index same with data[0] in the place list, skip this statements
                if data[0] not in place:
                    changingIndex=counter%numberOfbuffers
                    # if the data is 255 which indicates replace the oldest index to new index, delete changingIndex in the place list and the index list.
                    if data[0]==255:
                        place.pop(changingIndex)
                        index.pop(changingIndex)
                        # read binary index and convert decimal
                        data=struct.unpack('B', binary_file.read(1))
                        #print(data)
                    # write index into place list
                    place.insert(changingIndex,data[0])
                    # read binary data1(not index) and convert to decimal
                    data1=struct.unpack('d'*blockLength, binary_file.read(size))
                    # convert decimal data to binary
                    b_data1=struct.pack('d'*blockLength,*data1)
                    # write into decompressed file
                    idealem_file.write(b_data1)
                    # write data1(not index) into index list
                    index.insert(changingIndex,list(data1))
                    counter+=1

                else:
                    # exchangeable index comes to here and exchangeable index will be exchangeable data
                    data=index[data[0]]
                    b_data=struct.pack('d'*blockLength, *data)
                    # write b_data into decompressed file
                    idealem_file.write(b_data)
                    #print(data)  
                try:
                    # read binary index and convert to decimal
                    data=struct.unpack('B', binary_file.read(1))
                except:
                    break
    return
