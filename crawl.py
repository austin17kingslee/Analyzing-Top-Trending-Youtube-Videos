from googleapiclient.discovery import build
from datetime import datetime

import pandas as pd

API_KEY = 'AIzaSyDZMcV_XloX1xHvuLyixC9cjDeEATiJKW8'
REGIONS = ['US', 'GB', 'JP', 'KR', 'IN']

def crawl():
	# authenticate to YouTube API
	youtube = build('youtube', 'v3', developerKey=API_KEY)
	# make API call to get video info
	dataset = []
	for region in REGIONS:
		response = youtube.videos().list(\
			part='snippet,statistics',\
			chart='mostPopular',\
			regionCode=region\
		).execute()
		total_items = response.get('pageInfo')['totalResults']
		items = response.get('items')
		while len(items) < total_items:
			response = youtube.videos().list(\
				part='snippet,statistics',\
				chart='mostPopular',\
				regionCode=region,\
				pageToken=response.get('nextPageToken')\
			).execute()
			items.extend(response.get('items'))
		dataset.extend(filter(items))
	return dataset

def filter(items):
	filtered = []
	for item in items:
		filtered_item = {}

		# get video id
		filtered_item['video_id'] = item['id']

		# get title, publish date, channel id and title, category, trending date
		snippet = item['snippet']
		filtered_item['title'] = snippet['title']
		filtered_item['publishedAt'] = snippet['publishedAt']
		filtered_item['channelId'] = snippet['channelId']
		filtered_item['channelTitle'] = snippet['channelTitle']
		filtered_item['categoryId'] = snippet['categoryId']
		filtered_item['trending_date'] = datetime.now().strftime("%d-%m-%YT%H:%M:%SZ")

		# get view count, likes, dislikes, comment count, comments_disabled, ratings_disabled
		statistics = item['statistics']
		try:
			filtered_item['view_count'] = statistics['viewCount']
		except:
			filtered_item['view_count'] = 0
		ratings_disabled = False
		comments_disabled = False
		try:
			filtered_item['likes'] = statistics['likeCount']
			filtered_item['dislikes'] = 0
		except:
			filtered_item['likes'] = 0
			ratings_disabled = True
		try:
			filtered_item['comment_count'] = statistics['commentCount']
			filtered_item['comments_disabled'] = False
		except:
			filtered_item['comment_count'] = 0
			comments_disabled = True
		filtered_item['comments_disabled'] = comments_disabled
		filtered_item['ratings_disabled'] = ratings_disabled

		# get description
		filtered_item['description'] = snippet['description']
		for i in filtered_item:
			filtered_item[i] = str(filtered_item[i])
		filtered.append(filtered_item)
	return filtered

def convertToCSV(data):
	# convert dataset to CSV and export
	df = pd.DataFrame(data)
	df.to_csv('data/{0}.csv'.format(datetime.now().strftime("%Y-%m-%d")), sep='\t', encoding='utf-8', index=False)

def main():
	data = crawl()
	convertToCSV(data)