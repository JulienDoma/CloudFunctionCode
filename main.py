
import requests
from bs4 import BeautifulSoup

import json
import datetime

from google.cloud import storage


BUCKET_NAME = "wagon-data-779-bucket"  # 🚨 replace with your bucket name


def storage_upload(request):
    """
    cloud function entry point
    """

    # $CHALLENGIFY_BEGIN
    # get request params
    request_json = request.get_json(silent=True)
    request_args = request.args

    # retrieve current date and time
    now = datetime.datetime.now()

    # retrieve news
    news = top_3_from_hackernews()

    # build content
    content = "# request json" \
        + f"\n{json.dumps(request_json)}" \
        + "# request args" \
        + f"\n{json.dumps(request_args)}" \
        + "# top 3 news" \
        + f"\n{news}"

    # build file name
    file_timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    storage_location = f"content/{file_timestamp}_hackernews_top_3.md"

    # upload content to bucket
    client = storage.Client()

    bucket = client.bucket(BUCKET_NAME)

    blob = bucket.blob(storage_location)

    blob.upload_from_string(content)
    # $CHALLENGIFY_END

    # all printed output will be visible in the Cloud Function logs
    print("it works!")

    # the returned json response
    return {"response": "the Cloud Function json response, if any"}


def top_3_from_hackernews():
    """
    return top 3 news from hackernews
    """

    # $CHALLENGIFY_BEGIN
    url = "https://news.ycombinator.com/"

    response = requests.get(url)

    # test response
    if response.status_code != 200:
        print(
            "error scraping site:"
            + f"\nurl: {url}"
            + f"\nresponse: {response}"
            + f"\nstatus_code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")

    # return datetime and top 3 news
    return [e.text for e in soup.select("td.title > a")[:3]]
    # $CHALLENGIFY_END


if __name__ == '__main__':

    res = top_3_from_hackernews()
    print(res)
