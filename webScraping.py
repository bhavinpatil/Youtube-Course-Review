from bs4 import BeautifulSoup
import urllib.request, json
import requests


def WebScraping(link, platform):
    site = platform
    c_url = link
    comments = []
    c = []
    result = {}
    if site =="Youtube":
        result['v'] = link[link.index('=')+1:]
        videoId = c_url[(c_url.index("=") + 1):]
        url = 'https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&id={}&key={}'.format(
            videoId, 'AIzaSyAId96TrNTCJd3NJRUrqun-SbiS3eWQ8rM')
        response = urllib.request.urlopen(url)
        data = response.read()
        data = json.loads(data)
        duration = data["items"][0]["contentDetails"]["duration"]
        result["duration"] = ''
        if duration.find('H')!=-1:
            result["duration"] = result["duration"] + (duration[duration.find('T') + 1:duration.find('H')] + ' Hr ')
        if duration.find('M')!=-1 and duration.find('H')!=-1:
            result["duration"] = result["duration"] + ' ' + (duration[duration.find('H') + 1:duration.find('M')] + ' Mins')
        elif duration.find('M')!=-1:
            result["duration"] = result["duration"] + ' ' +(duration[duration.find('T') + 1:duration.find('M')] + ' Mins')

        url = 'https://youtube.googleapis.com/youtube/v3/videos?part=statistics&id={}&key={}'.format(
            videoId, 'AIzaSyAId96TrNTCJd3NJRUrqun-SbiS3eWQ8rM')
        response = urllib.request.urlopen(url)
        data = response.read()
        data = json.loads(data)
        result["learner_count"] = data["items"][0]["statistics"]["viewCount"] + ' views'

        url = 'https://youtube.googleapis.com/youtube/v3/videos?part=snippet&id={}&key={}'.format(
            videoId, 'AIzaSyAId96TrNTCJd3NJRUrqun-SbiS3eWQ8rM')
        response = urllib.request.urlopen(url)
        data = response.read()
        data = json.loads(data)
        result["platform"] = "YouTube"
        result["title"] = data["items"][0]["snippet"]["title"]
        result["instructor"] = data["items"][0]["snippet"]["channelTitle"]
        result["description"] = data["items"][0]["snippet"]["description"]

        url = 'https://youtube.googleapis.com/youtube/v3/commentThreads?part=snippet&maxResults=100&videoId={}&key={}'.format(
            videoId, 'AIzaSyAId96TrNTCJd3NJRUrqun-SbiS3eWQ8rM')
        response = urllib.request.urlopen(url)
        data = response.read()
        data = json.loads(data)
        for i in range(len(data["items"])):
            if data['items'][i]['snippet']['topLevelComment']['snippet']['textDisplay'] is not None:
                comments.append(data['items'][i]['snippet']['topLevelComment']['snippet']['textDisplay'])
        result["comments"] = comments
        return result
    