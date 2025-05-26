# Methodology to derive statistical information

## IDEALEM

In case of IDEALEM, encoder() and decoder() functions are used to get the statistical information. To get results similar to that of the paper, part2 of the dataset must be provided to the encoder, where block length is 24 and number of buffers are 255. The encoder() also provides the index of the reconstructed blocks. 
The decoder() function provides the statistical information. 

## Summary statistics

To get statistical information from summary statistics, random_data() function is used. To reproduce results from the paper, the function requires part2 dataset as well as sequence length(block length) to be 24. 
To do experiments on LLMTime, where mean and standard deviation are used directly, they can be obtained from the sum_stat() function with arguments similar to that of random_data() function. 
