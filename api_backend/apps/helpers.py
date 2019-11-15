import csv
import hashlib
import requests
from uuid import UUID
from ast import literal_eval

class Helpers:
    @staticmethod
    def hash_values(text):
        md5_value = hashlib.md5(text.encode('utf-8')).hexdigest()
        return md5_value

    @staticmethod
    def checkUUID(uuid_to_test, version=4):
        try:
            uuid_obj = UUID(uuid_to_test, version=version)
            return uuid_obj
        except ValueError:
            return None

    @staticmethod
    def extractUUID(text):
        temp_results = text.splitlines()
        if len(temp_results) > 0:
            return temp_results[0].replace('#', '')
        else:
            return False

    @staticmethod
    def find_between(s, first, last):
        try:
            # representation of string
            s = repr(s)
            start = s.index(first) + len(first)
            end = s.index(last, start)
            return s[start:end]
        except ValueError:
            return ""

    @staticmethod
    def evaluate_execution_count():
        pass

    @staticmethod
    def is_number(text):
        text = literal_eval(text)
        return isinstance(text, (int, float, complex))
        

    @staticmethod
    def keys_exists(element, *keys):
        '''
        Check if *keys (nested) exists in `element` (dict).
        '''
        if not isinstance(element, dict):
            raise AttributeError('keys_exists() expects dict as first argument.')
        if len(keys) == 0:
            raise AttributeError('keys_exists() expects at least two arguments, one given.')

        _element = element
        for key in keys:
            try:
                _element = _element[key]
            except KeyError:
                return False
        return True

class DownloadHelpers:
    #todo implement md5_checksum
    def download_file_from_google_drive(self, gid, destination):
        URL = "https://docs.google.com/uc?export=download"

        session = requests.Session()

        response = session.get(URL, params={'id': gid}, stream=True)
        token = self.get_confirm_token(response)

        if token:
            params = {'id': gid, 'confirm': token}
            response = session.get(URL, params=params, stream=True)

        self.save_response_content(response, destination)

    def download_object_from_google_drive(self, gid):
        URL = "https://docs.google.com/uc?export=download"

        session = requests.Session()
        response = session.get(URL, params={'id': gid}, stream=True)
        return response

    def get_confirm_token(self, response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value

        return None

    def save_response_content(self, response, destination):
        CHUNK_SIZE = 32768

        with open(destination, "wb") as f:
            for chunk in response.iter_content(CHUNK_SIZE):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)