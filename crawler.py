# Crawls wikipedia for each state to populate state_config.yaml
# The script will clear the file and repopulate it
# TODO: Detect if state is already in yaml and leave it
import pywikibot
from pywikibot import textlib

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en",
}

site = pywikibot.Site("wikipedia:en")


def get_state_info(state: str):
    state_page = pywikibot.Page(site, state)
    sect = textlib.extract_sections(state_page.text, site)

    pass
