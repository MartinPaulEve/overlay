import requests


class FetchDOI(object):
    """A class to fetch DOI information"""
 
    @staticmethod
    def fetch(doi):
        """Fetch DOI information and return a JSON-serialized DOI.

        Keyword arguments:
        doi -- the DOI to fetch, in either URL or handle form
        """

        # Sanitize the supplied DOI into a URL.
        # If the URL doesn't start with htt we will assume that it is in handle form.
        if doi.startswith("htt"):
            url = doi
        else:
            url = "http://dx.doi.org/{0}".format(doi)

        return requests.get(url, headers={'accept': 'application/vnd.citationstyles.csl+json'}).json(), url

    @staticmethod
    def fetch_and_parse(doi):
        """Fetch DOI information and return a minimal dictionary of information.

        Keyword arguments:
        doi -- the DOI to fetch, in either URL or handle form
        """

        # Fetch the DOI information.
        parsed_json, url = FetchDOI.fetch(doi)

        # Parse the returned JSON into a minimal dictionary.
        ret = {'url': url, 'authors': parsed_json['author'], 'title': parsed_json['title'],
               'journal': parsed_json['container-title'], 'issue': parsed_json['issue'],
               'volume': parsed_json['volume'], 'date-parts': parsed_json['issued']['date-parts']}

        return ret
