# Title:       utils
# Description: Contains utilities.
# Author:      David Nellessen <david.nellessen@familo.net>
# Date:        4/2/14
###########################################
# Description: migrate to python 3 from 2.7
# Date:        06.10.2017
# Author:      Andrew Dorokhin <andrew@dorokhin.moscow>
# License:     The MIT License (MIT)
###########################################
# Description: migrate to python 3 from 2.7
# Date:        14.04.2019
# Author:      Andrew Dorokhin <andrew@dorokhin.moscow>
# License:     The MIT License (MIT)


import re
import urllib
import urllib.parse
from hashids import Hashids
from urllib.parse import urlparse

# TODO: Move HASH_SALT to settings file
HASH_SALT = 'Sample_salt_please_change_me'

# Compile the regular expression for validating URLs.
url_regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'
        r'(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def validate_url(url):
    """
    Validates a given URL.
    :see https://github.com/django/django/blob/master/django/core/validators.py#L58
    """
    if url_regex.match(url):
        return True
    else:
        return False


def normalize_url(url):
    """Sometimes you get an URL by a user that just isn't a real
    URL because it contains unsafe characters like ' ' and so on.  This
    function can fix some of the problems in a similar way browsers
    handle data entered by the user:
    >>> normalize_url(u'http://de.wikipedia.org/wiki/Elf (Begriffsklärung)')
    'http://de.wikipedia.org/wiki/Elf%20%28Begriffskl%C3%A4rung%29'
    :param charset: The target charset for the URL if the url was
                    given as unicode string.
    :see: http://stackoverflow.com/questions/120951/how-can-i-normalize-a-url-in-python
    """
    return urllib.parse.quote(url, safe="%/:=&?~#+!$,;'@()*[]")


def generate_hash(id):
    """
    Generates an URL hash.
    """
    hashids = Hashids(salt=HASH_SALT, min_length=7)
    return hashids.encode(id)


def get_id_from_hash(hash_string):
    """
    Get id from hash string
    """
    hashids = Hashids(salt=HASH_SALT, min_length=7)
    return (hashids.decode(hash_string))[0]


def get_hash_from_url(short_url):
    """
    Gets the hash from a short URL which is the path without the trailing slash.
    """
    p = urlparse(short_url).path
    assert p[0:1] == '/'
    return p.replace('/', '')
