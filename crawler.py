# Crawls wikipedia for each state to populate state_config.yaml
# The script will clear the file and repopulate it
# TODO: Detect if state is already in yaml and leave it
import pywikibot
from pywikibot import textlib

site = pywikibot.Site("wikipedia:en")


def get_state_info(state: str):
    state_page = pywikibot.Page(site, state)
    sect = textlib.extract_sections(state_page.text, site)
    # test_parser = textlib.GetDataHTML(keeptags = ['infobox'])

    pass
