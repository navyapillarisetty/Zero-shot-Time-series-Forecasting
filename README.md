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
