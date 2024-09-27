from requests_oauthlib import OAuth1Session
import os
import json
import requests

def getIDFromUsername(username):
    with open('twittertoken.json') as f:
        config = json.load(f)

    bearer_token = config['bearer_token']

    url = f"https://api.twitter.com/2/users/by/username/{username}"
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "User-Agent": "v2UserLookupPython"
    }

    response = requests.request("GET", url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Request returned an error: {response.status_code}, {response.text}")

    return response.json()['data']['id']

def getUserByID(id):
    with open('twittertoken.json') as f:
        config = json.load(f)

    bearer_token = config['bearer_token']

    url = "https://api.twitter.com/2/users"
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "User-Agent": "v2UserLookupPython"
    }

    params = {
        "ids": id,
        "user.fields": "created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,url,username,verified,withheld",
        "expansions": "pinned_tweet_id"
    }

    response = requests.request("GET", url, headers=headers, params=params)

    if response.status_code != 200:
        raise Exception(f"Request returned an error: {response.status_code}, {response.text}")

    return response.json()

def getUserByUsername(username):
    with open('twittertoken.json') as f:
        config = json.load(f)

    bearer_token = config['bearer_token']

    url = f"https://api.twitter.com/2/users/by/username/{username}"
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "User-Agent": "v2UserLookupPython"
    }

    params = {
        "user.fields": "created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,url,username,verified,withheld",
        "expansions": "pinned_tweet_id"
    }

    response = requests.request("GET", url, headers=headers, params=params)

    if response.status_code != 200:
        raise Exception(f"Request returned an error: {response.status_code}, {response.text}")

    return response.json()

def getTweetsByUser(user_id, tweet_count=50):
    with open('twittertoken.json') as f:
        config = json.load(f)

    bearer_token = config['bearer_token']

    url = f"https://api.twitter.com/2/users/{user_id}/tweets"
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "User-Agent": "v2UserLookupPython"
    }

    params = {
        "max_results": tweet_count,
        "expansions": "attachments.poll_ids,attachments.media_keys,author_id,geo.place_id,in_reply_to_user_id,referenced_tweets.id,referenced_tweets.id.author_id",
        "tweet.fields": "attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,public_metrics,possibly_sensitive,referenced_tweets,source,text",
        "user.fields": "created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified",
        "media.fields": "duration_ms,height,media_key,preview_image_url,type,url,width,public_metrics",
        "place.fields": "contained_within,country,country_code,full_name,geo,id,name,place_type",
        "poll.fields": "duration_minutes,end_datetime,id,options,voting_status"
    }

    response = requests.request("GET", url, headers=headers, params=params)

    if response.status_code != 200:
        raise Exception(f"Request returned an error: {response.status_code}, {response.text}")

    return response.json()

def checkTweetCap():
    with open('twittertoken.json') as f:
        config = json.load(f)

    bearer_token = config['bearer_token']

    url = "https://api.twitter.com/2/usage/tweets"
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "User-Agent": "v2UserLookupPython"
    }

    response = requests.request("GET", url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Request returned an error: {response.status_code}, {response.text}")

    return response.json()
