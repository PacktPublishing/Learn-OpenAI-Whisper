import feedparser
import requests
import os
from urllib.parse import urlparse
import subprocess


def list_episodes(feed_url):
    """
    Lists all episodes in the given RSS feed.

    Parameters:
    - feed_url: The RSS feed URL.

    Returns:
    - A list of tuples containing episode titles, their URLs and published dates in 'YYYYMMDD' format.
    """
    d = feedparser.parse(feed_url)

    episodes = []
    for entry in d.entries:
        title = entry.title
        published = time.strftime('%Y%m%d', time.gmtime(time.mktime(entry.published_parsed)))
        url = None
        for link in entry.links:
            if link.type == "audio/mpeg":
                url = link.href
                break
        if url:
            episodes.append((title, url, published))

    return episodes

def download_episode(url, filename=None):
    """
    Downloads the podcast episode from the given URL.

    Parameters:
    - url: The URL of the podcast episode.
    - filename: The desired filename to save the podcast. If not provided, it'll use the last part of the URL.

    Returns:
    - The path to the downloaded file.
    """
    # If a custom filename is provided, append the appropriate extension from the URL
    if filename:
        parsed_url = urlparse(url)
        # Extract only the base path without any query parameters
        base_path = os.path.basename(parsed_url.path)
        ext = os.path.splitext(base_path)[1]
        filename += ext
    else:
        filename = os.path.basename(parsed_url.path)

    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    return filename

def download_episode_start_at(url, filename=None, start_at=0):
    """
    Downloads the podcast episode from the given URL and trims it starting from 'start_at' seconds.

    Parameters:
    - url: The URL of the podcast episode.
    - filename: The desired filename to save the podcast. If not provided, it'll use the last part of the URL.
    - start_at: The start time in seconds from where the audio should be trimmed.

    Returns:
    - The path to the downloaded and trimmed file.
    """
    parsed_url = urlparse(url)
    if filename:
        # Ensure the filename has the correct extension
        ext = os.path.splitext(parsed_url.path)[1]
        filename += ext
    else:
        filename = os.path.basename(parsed_url.path)

    # Download the file
    response = requests.get(url, stream=True)
    response.raise_for_status()

    temp_filename = "temp_" + filename
    with open(temp_filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    # Use ffmpeg to trim the audio file
    trimmed_filename = "trimmed_" + filename
    command = ['ffmpeg', '-y', '-i', temp_filename, '-ss', str(start_at), '-c', 'copy', trimmed_filename]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Remove the original downloaded file
    os.remove(temp_filename)

    return trimmed_filename
