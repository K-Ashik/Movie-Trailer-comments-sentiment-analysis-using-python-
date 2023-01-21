# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 01:45:45 2022

@author: Meghna
"""


import requests

import json
import csv


def get_params():
    params={'key': 'your api key', 'videoId': video_id, 'part': 'snippet,id,replies',
                 'maxResults': 1000 , 'textFormat'  : 'plainText'}
    return params

#Getting the comments from youtube through the id
def get_all_comments_replies(video_id, params, max_count = 1000):
    content_thread_url = r'https://www.googleapis.com/youtube/v3/commentThreads'
    response = requests.get('{}/{}'.format(content_thread_url, ''),params )
    parsed_response = json.loads(response.text)
    texts = [ resp['snippet']['topLevelComment']['snippet']['textDisplay'] 
             for resp in parsed_response['items']]
    all_texts = texts
    while 'nextPageToken' in parsed_response :
        next_page_token = parsed_response['nextPageToken']
        print(f"requesting for {next_page_token} ")

        params['pageToken']  = next_page_token 
        response = requests.get('{}/{}'.format(content_thread_url, ''),params )
        parsed_response = json.loads(response.text)
        texts = [ resp['snippet']['topLevelComment']['snippet']['textDisplay'] 
             for resp in parsed_response['items']]
        all_texts.extend(texts)
        print(f"current response count {len(texts)} total count {len(all_texts)}")

        if(len(all_texts))>max_count:
               break
               
    return all_texts[:max_count]

#getting video ID
video_id = r'fb5ELWi-ekk'
params = get_params()
comments = get_all_comments_replies(video_id,params, 4000)


# Converting into csv
with open('path of output csv', 'w',encoding='utf8',newline='') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    for word in comments:
        wr.writerow([word])