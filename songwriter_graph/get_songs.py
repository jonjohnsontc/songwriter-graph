from time import sleep

from splinter import Browser, driver
from selenium.common.exceptions import (
    ElementNotInteractableException,
    ElementClickInterceptedException,
    NoSuchElementException,
)


def get_songs(browse):
    """
    Retrieves all song results for a given artist, and saves them as 
    one or multiple html files.
    """
    result = browse.html
    n = len(browse.url) - 1 - browse.url[::-1].index("/")
    fn = browse.url[n + 1 :].replace("%20", " ")
    with open("../data/ascap_songs/{}.html".format(fn), "wb") as f:
        f.write(result.encode("utf-8"))
    i = 2
    while len(browse.find_by_tag('a[id="pageNumber{}"]'.format(i))) != 0:
        try:
            browse.find_by_tag('a[id="pageNumber{}"]'.format(i))[0].click()
        except ElementClickInterceptedException:
            browse.find_by_tag('a[class="close-cookie-banner"]').click()
            browse.find_by_tag('a[id="pageNumber{}"]'.format(i))[0].click()
        sleep(5)
        if (
            len(
                browse.find_by_tag(
                    'button[class="btn btn--blue [ card__expand--all ]"]'
                )
            )
            != 0
        ):
            expand_results = browse.find_by_tag(
                'button[class="btn btn--blue [ card__expand--all ]"]'
            )
            expand_results.click()
        with open("../data/ascap_songs/{}_{}.html".format(fn, i), "wb") as f:
            f.write(browse.html.encode("utf-8"))
        i += 1


def sort_thru_pages(browse, artist):
    """
    Searches ASCAP's ACE database for artist, retreives the 
    subsequent results and stores them as an html file.
    """
    if len(browse.find_by_xpath('//*[@id="btn--agree"]')) == 1:

        # For the Terms and Conditions page. It's likely that there will always be
        # a T&C page, since a different browser instance is started for each search

        agree_btn = browse.find_by_xpath('//*[@id="btn--agree"]')
        agree_btn.click()
        sleep(3)
    else:
        sleep(3)
    ar = browse.find_by_tag('a[class="nav_action"]')
    if len(ar) >= 25:
        print("> 25 results for {}, will search manually".format(artist))
        return
    for i in range(len(ar)):
        sleep(3)
        artist_results = browse.find_by_tag('a[class="nav_action"]')

        # I have to re-instantiate the `find_by_tag` method, because
        # the object becomes stale after loading a new page

        artist_results[i].click()
        sleep(2)
        if (
            len(
                browse.find_by_tag(
                    'button[class="btn btn--blue [ card__expand--all ]"]'
                )
            )
            != 0
        ):
            sleep(2)
            expand = browse.driver.find_element_by_tag_name(
                'button[class="btn btn--blue [ card__expand--all ]"]'
            )
            browse.driver.execute_script(
                "arguments[0].scrollIntoView(true);", expand
            )

            # I've been running into numerous erros trying to scroll
            # to the `expand` tag via the above `.find_by_tag` method,
            # hence using Selenium's `driver` to find it instead

            try:
                expand.click()
                get_songs(browse)
                go_back = browse.find_by_tag('a[id="back-button"]')
                go_back.click()
            except ElementNotInteractableException:

                # Specifically for when there is a zero results page

                print(
                    "exception, possibly zero results: {}".format(browse.url)
                )
                go_back = browse.find_by_tag('a[id="back-button"]')
                sleep(1)
                go_back.click()
            except ElementClickInterceptedException:

                # Will like to look further into this, the scrolling
                # script above is not working for everything

                print(
                    "exception, cannot scroll into view: {}".format(browse.url)
                )
                go_back = browse.find_by_tag('a[id="back-button"]')
                sleep(1)
                go_back.click()
        else:
            get_songs(browse)
            go_back = browse.find_by_tag('a[id="back-button"]')
            go_back.click()


def result_scraper(artist):
    """
    Searches ASCAP's ACE database for artist, retreives the 
    subsequent results and stores them as an html file.
    """
    d = 2
    browse = Browser()
    browse.visit("https://www.ascap.com/ace")
    performer = browse.find_by_xpath('//*[@id="search__input--two"]')
    performer.click()
    performer.fill(artist)
    search = browse.find_by_xpath('//*[@id="startSearch"]')
    search.click()
    sleep(2)
    sort_thru_pages(browse, artist)
    browse.quit()
    print("finished pulling " + artist)


def quick_search(lst):
    """
    From a list of artists, iteratively searches ASCAP for the EXACT
    name, and retreives song results via 'get_songs'.
    """
    for n in lst:
        browse = Browser(headless=True)
        browse.visit(
            "https://www.ascap.com/ace#ace/performer/{}".format(
                n.replace(" ", "%20")
            )
        )
        sleep(5)
        if (
            len(
                browse.find_by_tag(
                    'button[class="btn btn--blue [ card__expand--all ]"]'
                )
            )
            != 0
        ):
            try:
                expand = browse.find_by_tag(
                    'button[class="btn btn--blue [ card__expand--all ]"]'
                )
                expand.click()
                get_songs(browse)
                print("Success {}".format(n))
                browse.quit()
            except:
                print("Error, could not get {}".format(n))
                browse.quit()

        else:
            get_songs(browse)
            print("Success {}".format(n))
            browse.quit()
