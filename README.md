# Zero-shot-Time-series-Forecasting

**Zero-Shot Time-Series Forecasting by Statistically Assisted Models**


*Abstract*

 Time-series data stem from many sources such as financial applications, medical ap
plications, environmental monitoring, and traffic monitoring. As such, synthesizing
 time series with generative models or predicting future time series with predictive
 models has received much attention in recent years, since they can create more data
 of similar nature or forecast data of near future, based on the set of time series they
 were trained on. However, generative and predictive models for time-series data
 by themselves are only capable of interpolating from learned data. This leads to
 them suffering from accuracy degradation when they advance deeper into unseen
 time range (i.e., extrapolation), not to mention unseen time series (i.e., zero-shot
 learning). This study proposes zero-shot time-series forecasting from generative
 and predictive models when statistical summary is available. Statistical summary
 can arise from many situations where the full retention of time series is impractical,
 but a quick summary is feasible. We augment existing generative and predictive
 models with the statistical summary to enable zero-shot time-series generation.
 Experimental results show that the proposed method greatly enhances the accuracy
 of generated time series for both unseen time range and unseen time series. This
 allows to train a generator/predictor only once with a generic time series and use
 the same generator/predictor for all other datasets, when their statistical summaries
 are available.
 

 ![Neurips methodology updated jpeg](https://github.com/user-attachments/assets/eec2acb4-80c7-49f4-80c1-1a0305c80a60)
                     
                     Figure 1: Our proposed methodology that enables Zero-shot forecasting 

## Models

The research methodology was applied to various models and their results are shown in the paper. The requirements to reproduce the results varies from model to model. Currently Informer code with its requirements is present within this github. The following links provide code to the other models:

- TimeGAN: https://github.com/jsyoon0823/TimeGAN
- DoppelGANger: https://github.com/fjxmlzn/DoppelGANger
- Informer: https://github.com/zhouhaoyi/Informer2020
- LLMTime: https://github.com/ngruver/llmtime
- Diffusion-TS: https://github.com/Y-debug-sys/Diffusion-TS

## Data

For extrapolation experiments the dataset was divided into two equal halves where the first half was used for training and second half statistical information was used in the inference phase. For current experiments datasets of length 3768*2 are chosen, where each half is 3768 long. Some of the datasets are provided within the Data folder of the code. 
In case of zero-shot experiments, ETTh1 dataset's first half was used as generic dataset to train the models.

### Statistical Information

As mentioned in the paper statistical information derived from datasets of interest are introduced into inference phase. For reproducing the results of the paper, the methodology used to extract statistical information from the second halves of the datasets are given in statistical_information folder. 
The code to derive statistical information is provided in main_stat_info.py file. 
The directories of the data, statistical information and output results are to be adjusted in the informer model - like in data_loader.py file training phase either first half of dataset or ETTh1 first half must be given where as in exp_informer.py file directory to store model's output result.


