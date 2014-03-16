import requests
import lxml.html
import re
from decimal import Decimal
import argparse

class MarketSet(object):
    __set_regular__ = []
    __set_foils__ = []
    total_price = Decimal(0)
    foil_price = Decimal(0)

    def __init__(self, name):
        self.name = name

    def add(self, listing):
        if listing.foil:
            self.__set_foils__.append(listing)
            self.foil_price += listing.price
        else:
            self.__set_regular__.append(listing)
            self.total_price += listing.price

    def __repr__(self):
        return u'<{0} Set: total_price={1}, foil_price={2}, 5levels={3}>'.format(self.name, self.total_price, self.foil_price, self.total_price * 5)

class MarketListing(object):
    foil = False
    price = None
    accurate_price = False

    def __init__(self, **kwargs):
        self.purchase_url = kwargs.get('purchase_url', None)
        self.soft_price = Decimal(kwargs.get('price', None))
        self.price = self.soft_price
        self.currency = kwargs.get('currency', 'USD')
        self.name = kwargs.get('name', None)

    def __repr__(self):
        return u'<MarketListing: {0}, foil={1}, price={2}>'.format(self.name, self.foil, self.price)

# Sleeping Dogs doesn't work cause it has a tm so do unicode whatevs
def search(search_terms, set_name='IDK A SET'):
    url = 'http://steamcommunity.com/market/search/render/?query={0}+Trading+Card&start=0&count=50'.format(search_terms)

    req = requests.get(url)

    steam_html = req.json()['results_html']

    parsed = lxml.html.fragment_fromstring(steam_html, create_parent='div')

    cssed = parsed.xpath('//a[@class="market_listing_row_link"]')

    m = MarketSet(search_terms)

    for item in cssed:
        purchase_page = item.attrib['href']
        more = item.xpath('div/div/span')[0].text_content()

        # Item name
        itemnamediv = item.xpath('div/div/span[@class="market_listing_item_name"]')
        gamenamediv = list(item.xpath('div/div/span[@class="market_listing_game_name"]'))[0]

        match_these = ('{0} Foil Trading Card'.format(search_terms), '{0} Trading Card'.format(search_terms))
        if gamenamediv.text_content() not in match_these:
            continue

        # Make sure this item IS a trading card and not an emote or wallpaper
        for nameitem in itemnamediv:
            name_of_card = nameitem.text_content()

        # I dunno find the price as a quick check
        # Only works with USD
        match = re.findall('[\$](\d+(?:\.\d{1,2})?)', more)
        if match:
            itemprice = match[0]
        else:
            itemprice = None

        new_listing = MarketListing(
            name = name_of_card,
            purchase_url = purchase_page,
            price = match[0],
            currency = 'USD'
        )
        new_listing.foil = gamenamediv.text_content() == match_these[0]

        m.add(new_listing)

    print m

# optparse, get search query "deus ex trading card"
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='steam market thingy')
    parser.add_argument('-s', '--search', required=True, help='Search terms to use (will add "Trading Card" to the end)')
    parser.add_argument('-n', '--name', help='Name of this set (kinda pointless)')
    parser.add_argument('-m', '--monitor', action='store_true', help='Keep monitoring price until it gets below a certain price')
    opts = parser.parse_args()

    search(opts.search, opts.name)
