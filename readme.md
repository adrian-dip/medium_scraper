# Medium Scraper

This is an updated scraper based on https://www.kaggle.com/datasets/aiswaryaramachandran/medium-articles-with-content. 

The current code works in 2023, and it returns engagement metrics such as the number of claps and comments. If you want to get the images also, the original on Kaggle has a function for that. 

My own testing indicated that images were not necessary to predict engagement, traffic, or document category, which is sensible given type of content that is published (academic/formal) and that most of the traffic comes from social and organic channels. 

## Overview

### number_of_days=365
Number of days to sample. 

### years=[2018, 2019, 2020, 2021, 2022]
Years to sample from.

### n_save=0
Number of articles saved so far. If the script hangs for any reason, you can pick up where you left off.

### save_frequency=100
Number of articles to scrape before saving your progress. 

## License

Attribution-NonCommercial 3.0 Unported (CC BY-NC 3.0)

https://creativecommons.org/licenses/by-nc/3.0/