import datetime
import numpy as np
import pandas as pd

DATES = ['2021-12-05T00:00:00Z', '2021-12-12T00:00:00Z', '2021-12-19T00:00:00Z', '2021-12-26T00:00:00Z', '2022-01-02T00:00:00Z']
REGIONS = ['US', 'GB', 'JP', 'KR', 'IN']
datasets_filenames = ["data/2021-12-05.csv","data/2021-12-12.csv","data/2021-12-19.csv","data/2021-12-26.csv","data/2022-01-02.csv","data/2022-01-09.csv"]

def merge(filenames):
	list_of_df = []
	for filename in filenames:
		current_df = pd.read_csv(filename,sep='\t')
		list_of_df.append(current_df)

	all_df = pd.concat(list_of_df)
	all_df.reset_index(drop=True, inplace=True)
	return all_df

def clean(dataset):
	clean_df = dataset.copy(deep=True)

    # Replace NaN in description with space
	clean_df["description"].fillna(" ", inplace=True)

    # Delete all rows with a missing values if any
	clean_df.dropna(inplace=True)

	# Change format of trending_date to discard crawl time
	clean_df['trending_date'].mask(clean_df['trending_date'] == '2021-12-05T00:00:00Z','5/12/2021',inplace=True) 
	clean_df['trending_date'].mask(clean_df['trending_date'] == '2021-12-12T00:00:00Z','12/12/2021',inplace=True) 
	clean_df['trending_date'].mask(clean_df['trending_date'] == '2021-12-19T00:00:00Z','19/12/2021',inplace=True) 
	clean_df['trending_date'].mask(clean_df['trending_date'] == '2021-12-26T00:00:00Z','26/12/2021',inplace=True) 
	clean_df['trending_date'].mask(clean_df['trending_date'] == '2022-01-02T00:00:00Z','02/01/2022',inplace=True) 
	clean_df['trending_date'].mask(clean_df['trending_date'] == '2022-01-09T00:00:00Z','09/01/2022',inplace=True) 

    # Only keep rows with ratings_disbled == FALSE
	for x in clean_df.index:
		if str(clean_df.loc[x,'ratings_disabled']) == 'False':
			clean_df.loc[x,'ratings_disabled'] = False
		elif str(clean_df.loc[x,'ratings_disabled']) == 'True':
			clean_df.loc[x,'ratings_disabled'] = True
		if str(clean_df.loc[x,'comments_disabled']) == 'False':
			clean_df.loc[x,'ratings_disabled'] = False
		elif str(clean_df.loc[x,'comments_disabled']) == 'True':
			clean_df.loc[x,'ratings_disabled'] = True
	#print("delete ratings_diabled: " + str(clean_df.shape))
	clean_df = clean_df[(clean_df['ratings_disabled'] == False)]
	#print(clean_df.shape)
	
	# Correct negative values, if any
	for x in clean_df.index:
		clean_df.loc[x,'view_count'] = int(clean_df.loc[x,'view_count'])
		clean_df.loc[x,'likes'] = int(clean_df.loc[x,'likes'])
		clean_df.loc[x,'dislikes'] = int(clean_df.loc[x,'dislikes'])
		clean_df.loc[x,'comment_count'] = int(clean_df.loc[x,'comment_count'])
		if clean_df.loc[x,'view_count'] < 0:
			clean_df.loc[x,'view_count'] = 0
		if clean_df.loc[x,'likes'] < 0:
			clean_df.loc[x,'likes'] = 0
		if clean_df.loc[x,'dislikes'] < 0:
			clean_df.loc[x,'dislikes'] = 0
		if clean_df.loc[x,'comment_count'] < 0 or clean_df.loc[x,'comments_disabled'] == True:
			clean_df.loc[x,'comment_count'] = 0


    # Rename some columns for uniformity
	clean_df.rename(columns={'channelTitle': 'channel_title',
			     'publishedAt': 'published_at',
			     'channelId': 'channel_id',
							 'categoryId' : 'category_id'}, inplace=True)

    # Delete irrelevant columns
	clean_df.drop(['ratings_disabled'], axis=1, inplace=True)

	# Create new empty column for the number of regions the video is trending in
	clean_df['notes'] = "1"

	# Add number of regions the video is trending to 'notes'
	dups = clean_df[clean_df.duplicated(subset=['video_id','trending_date'],keep=False)]	
	for x in dups.index:
		id = dups.loc[x,'video_id']
		date = dups.loc[x,'trending_date']
		temp = clean_df[(clean_df['video_id'] == id) & (clean_df['trending_date'] == date)]
		temp = len(temp.index)
		for i in clean_df.index:
			if clean_df['video_id'][i] == id and clean_df['trending_date'][i] == date:
				clean_df.loc[i,'notes'] = temp
				break

	# Drop duplicates
	clean_df.drop_duplicates(subset=['video_id','trending_date'],keep='first',inplace=True)
	
	clean_df = clean_df.reindex(columns=['video_id', 'title', 'published_at', 'channel_id', 'channel_title',
					 'category_id', 'trending_date', 'view_count', 'likes', 'dislikes', 
										 'comment_count', 'comments_disabled', 'description', 'notes'])

	clean_df.reset_index(drop=True, inplace=True)

	return clean_df

def read():
	return pd.read_csv('data/clean.csv')

def main():
	combined_df = merge(datasets_filenames)
	print(combined_df.shape)
	print(combined_df.columns)

	clean_df = clean(combined_df)

	print(clean_df.shape)
	print(clean_df.columns)
	clean_df.to_csv('data/clean.csv')
