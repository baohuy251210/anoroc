import json
import requests


def get_json(_url, _params):
    """

    Arguments:
        _url {[type]} -- [description]
        _params {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    baseurl = _url
    paramdict = _params
    prepped_url = request_url(baseurl, paramdict)
    response = requests.get(prepped_url)
    print("Data Request Status: ", response.status_code)
    try:
        # return python object
        return json.loads(response.text, encoding='cp1252')
    except json.decoder.JSONDecodeError:
        return str(response.status_code)


def request_url(baseurl, params={}):
    """[summary]
    # This function accepts a URL path and a params diction as inputs.
    # It calls requests.get() with those inputs,
    # and returns the full URL of the data you want to get.
    Arguments:
        baseurl {[type]} -- [description]

    Keyword Arguments:
        params {dict} -- [description] (default: {{}})

    Returns:
        [type] -- [description]
    """

    req = requests.Request(method='GET', url=baseurl, params=params)
    prepped = req.prepare()
    return prepped.url
