import requests

def run():

    print("runscript")

    response=requests.get('http://133.130.96.237/api/transcript/test')
    print(response.text)