from urllib import request, error
from PyQt5.QtCore import pyqtSignal, QThread, QVariant

import urllib.parse
import json


def getData(url, params=None):
    """
    Sends a request to the indicated URL using the GET method, and in case
    of passing a dictionary in the parameters, add them and wait for a
    response in JSON format.

    Once the data is obtained, it is returned as a dictionary
    after parsing the returned JSON.

    Args:
        url (str): The URL of the request
        params (dict, optional): A dictionary with the parameters
            to be added to the request. Defaults to None.

    Returns:
        dict: A dictionary with the request result
    """

    if params:
        url_values = urllib.parse.urlencode(params)
        full_url = url + '?' + url_values
    else:
        full_url = url

    try:
        with request.urlopen(full_url) as response:
            rawData = response.read().decode('utf-8')
            data = json.loads(rawData)
            return data
    except error.HTTPError:
        return False


class searchTrackInfo(QThread):
    result = pyqtSignal(QVariant)

    def __init__(self, artist, release):
        super().__init__()
        self.params = {
            'fmt': 'json',
            'query': 'artist:"{}" AND release:"{}"'.format(artist, release)
        }

        self.url = 'https://musicbrainz.org/ws/2/release/'

    def run(self):
        data = getData(self.url, self.params)
        if data:
            self.result.emit(data)


class downCover(QThread):
    downloaded = pyqtSignal(QVariant)

    def __init__(self, parent, albumId, filename):
        super(downCover, self).__init__(parent)
        self.url = 'https://coverartarchive.org/release/{}/front-250'.format(albumId)
        self.filename = filename

    def run(self):
        try:
            request.urlretrieve(self.url, self.filename, self.progress)
        except error.HTTPError:
            self.downloaded.emit(False)

    def progress(self, block_num, block_size, total_size):
        downloaded = (block_num * block_size / total_size)*100
        if downloaded >= 100:
            self.downloaded.emit(self.filename)
