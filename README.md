# Intro to Data Science Project - Group 12
## _ANALYSIS ON YOUTUBE TRENDING VIDEOS_

## Set-up
Install the following Python libraries:
- Google API Client: 
```
pip install google-api-python-client
```
- NumPy:
```
pip install numpy
```
- Pandas:
```
pip install pandas
```
- Matplotlib:
```
pip install matplotlib
```
- word_cloud:
```
pip install wordcloud
```

## Compile

Our project was written in Python. Therefore, no compilation is necessary.

## Run the program

```
python main.py ...PLOT CODE... [options]

e.g. python main.py 1 --crawl
```
The plot code is mandatory.
### Plot codes
```1``` - Analyze the interest of the 5 regions based on their top trending categories.  
```2``` - Do certain keywords in the videos' titles have anything to do with trending?  
```3``` - Categories of videos that are the most controversial (have the highest dislike-ratio).  
```4``` - Analyze the effect of the holiday season on Youtube trending tab.  
```5``` - We tend to assume the view count, the like & dislike count, the comment count (the public response) are what contribute to a video’s trending ability, but is that entirely true?  
```6``` - Analyze the average view count requirement of a category to enter the trending tab.
### Options
```--crawl```
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Enable crawling for data from Youtube trending tab. The data will be saved in folder *data* under the name *YYY-MM-DD.csv*.  
```--clean```
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Merges the files containing crawled data into one file and filters out invalid entries. The cleaned data is saved in folder *data* under the name *clean.csv*.

### Warning
- Deleting the *data* folder renders the program unusable.
- The clean.py file only merges our already crawled data. Deleting this data renders the clean.py and visualize.py files unusable. Any newly crawled data will not be taken into consideration.
