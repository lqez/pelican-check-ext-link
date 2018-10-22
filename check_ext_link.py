"""
Check external links plugin for Pelican
=======================================

This plugin checks external links by urllib.

"""

from pelican import signals
from bs4 import BeautifulSoup as Soup
import logging
import urllib


def check_ext_link(instance):
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    if not instance._content:
        return

    html = Soup(instance._content, 'html.parser')
    for link in [a['href'] for a in html.find_all('a')]:
        if not link.startswith('http'):
            continue

        req = urllib.request.Request(link, headers={'User-Agent' : "Pelican external link checker"})
        
        try:
            urllib.request.urlopen(req)
            logger.debug('Checking external link: [ OK ] %s', link)
        except urllib.error.HTTPError as e:
            logger.error('Checking external link: [ %d ERROR ] %s', e.code, link)


def register():
    signals.content_object_init.connect(check_ext_link)
