import json
from ReadGoogleSheet import *

with open('output.json', 'r') as f:
    data = json.load(f)
sheet = getSheetData()
ridingSheet = getRidingSheetData()
toSheet = []
count = 0
for user in data:
    try:
        author = user['includes']['users'][0]['id']
        tweets = user['data']
        name = 'Unknown'  # Default value
        handle = 'Unknown'  # Default value
        ridingCode = 'Unknown'  # Default value
        for dictionary in sheet:
            for key, value in dictionary.items():
                if str(value) == str(author):  # Convert both to strings before comparing
                    name = dictionary['FullName']
                    handle = dictionary['Twitter Handle']
                    break
        for dictionary in ridingSheet:
            for key, value in dictionary.items():
                if key == '5':
                    if str(value) == str(name):  # Convert both to strings before comparing
                        ridingCode = dictionary['1']
                        break
        for tweet in tweets:
            text = tweet['text']
            date = tweet['created_at']
            url = tweet['entities']['urls'][0]['url']
            toSheet.append([ridingCode, name, handle, author, url, text, date])
    except:
        pass

write_toSheet(toSheet)
