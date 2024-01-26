import requests
from bs4 import BeautifulSoup
from .default_headers import DEFAULT_HEADERS
import xml.etree.ElementTree as ET


session = requests.Session()

class GetStaticSoup:     # This class return soup object from static page!

    def __new__(cls, link, custom_headers=None):
        headers = DEFAULT_HEADERS.copy()

        if custom_headers:
            headers.update(custom_headers)

        response = session.get(link, headers=headers)

        # return soup object from static page
        return BeautifulSoup(response.text, 'lxml')


class GetRequestJson:     # This class return JSON object from get requests!

    def __new__(cls, link, custom_headers=None):

        headers = DEFAULT_HEADERS.copy()

        if custom_headers:
            headers.update(custom_headers)

        response = session.get(link, headers=headers)

        # Parse response to JSON and return dict object
        try:
            json_response = response.json()
            return json_response
        except ValueError:
            return BeautifulSoup(response.text, 'lxml')
        finally:
            response.close()


class PostRequestJson:     # This class return JSON object from post requests!

    def __new__(cls, url, custom_headers=None, data_raw=None):
        headers = DEFAULT_HEADERS.copy()

        # Post requests headers, if not provided
        if custom_headers:
            headers.update(custom_headers)

        response = session.post(url, headers=headers, data=data_raw)

        try:
            return response.json()
        except ValueError:
            return BeautifulSoup(response.text, 'lxml')
        finally:
            response.close()


class GetHtmlSoup:     # Method if server return html response, after post requests.

    def __new__(cls, html_response):
        return BeautifulSoup(html_response, 'lxml')


class GetHeadersDict:     # Method if server return headers response, after session.headers

    def __new__(cls, url, custom_headers=None):
        headers = DEFAULT_HEADERS.copy()

        # Post requests headers, if not provided
        if custom_headers:
            headers.update(custom_headers)

        response = session.head(url, headers=headers).headers

        return response


class GetXMLObject:     # this class will return data from XML stored in a list

    def __new__(cls, url, custom_headers=None):
        headers = DEFAULT_HEADERS.copy()

        # if custom headers
        if custom_headers:
            headers.update(custom_headers)

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return ET.fromstring(response.text)