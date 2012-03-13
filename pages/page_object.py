#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re
import urllib2

from urllib2 import HTTPError
from urlparse import urlparse
from BeautifulSoup import BeautifulSoup

from page import Page

from selenium.webdriver.common.by import By


class MySiteHomePage(Page):

    _some_locator = (By.ID, 'some_locator')
    _page_title = 'MySiteHomePage Page Title'
    _language_locator = (By.ID, 'language')
    _language_list_locator = (By.CSS_SELECTOR, '#language option')
    _404_page_locator = (By.ID, 'mozilla-404')
    _feed_link_locator = (By.CSS_SELECTOR, '#home-news-blog a')

    def __init__(self, testsetup, open_url=True):
        ''' Creates a new instance of the class and gets the page ready for testing '''
        Page.__init__(self, testsetup)
        if open_url:
            self.selenium.get(self.base_url)

    def go_to_home_page(self):
        self.selenium.get(self.base_url)

    def get_response_code(self, url):
        # check if response status 200
        try:
            urllib2.urlopen(url)
            result = 'The request returned an HTTP 200 response.'
        except HTTPError, e:
            response_code = e.code
            if response_code == 404:
                result = 'The request returned an HTTP 404 response.'
            elif response_code == 503:
                result = 'The request returned an HTTP 503 response.'
            else:
                result = 'The response code was %s' % response_code
        return result

    def validate_link(self, url):
        w3c_validator = 'http://validator.w3.org/'

        content = urllib2.urlopen(w3c_validator + 'check?uri=' + url)
        status = content.info().getheader('x-w3c-validator-status')

        if status != 'Valid':
            errors = content.info().getheader('x-w3c-validator-errors')
            warnings = content.info().getheader('x-w3c-validator-warnings')
            soup = BeautifulSoup(content)
            err_msg = soup.findAll('h2')
            self.validation_errors_log(err_msg, errors, warnings)

    @property
    def get_feed_link(self):
        return self.selenium.find_element(*self._feed_link_locator).get_attribute('href')

    def validate_feed(self, url):
        feed_validator = 'http://feedvalidator.org/'
        result = urllib2.urlopen(feed_validator + 'check.cgi?url=' + url).read()
        return re.search("This is a valid RSS feed", result)

    def is_robot_txt_present(self, url):
        u = urlparse(url)
        roboturl = "%s://%s/robots.txt" % (u.scheme, u.netloc)
        response = urllib2.urlopen(roboturl)
        if response.getcode() == 200:
            result = "A robots.txt file is present on the server"
        else:
            result = "No robots.txt file was found."
        return result

    def is_404_page_present(self, url):
        self.selenium.get(url)
        return self.is_element_visible(*self._404_page_locator)

    def get_all_links(self):
        return [element.get_attribute('href') for element in self.selenium.find_elements(By.TAG_NAME, "a")]

    @property
    def is_change_locale_visible(self):
        return self.is_element_visible(*self._language_locator)

    @property
    def locales_count(self):
        return len(self.selenium.find_elements(*self._language_list_locator))

    @property
    def locales(self):
        return [self.LocaleOption(self.testsetup, lang)
                for lang in self.selenium.find_elements(*self._language_list_locator)]

    class LocaleOption(Page):

        def __init__(self, testsetup, lang):
            Page.__init__(self, testsetup)
            self._root_element = lang

        def select(self):
            self._root_element.click()

        @property
        def value(self):
            return self._root_element.get_attribute('value')

    @property
    def header(self):
        return MySiteHomePage.HeaderRegion(self.testsetup)

    @property
    def footer(self):
        return MySiteHomePage.FooterRegion(self.testsetup)

    def sharelinks(self):
        return MySiteHomePage.ShareLinksRegion(self.testsetup)

    def get_favicon_link(self, url):
        _possible_fav_locator = ['link[rel=\'icon\']', 'link[rel=\'shortcut icon\']']

        for i in _possible_fav_locator:
            try:
                favicon = self.selenium.find_element(By.CSS_SELECTOR, i)
                return favicon.get_attribute('href')
            except:
                False

    def get_response_path(self, url, lang):
        headers = {
        'Accept-Language': lang,
        }
        data = None
        content = urllib2.Request(url, data, headers)
        response = urllib2.urlopen(content)
        path_url = response.geturl()
        return path_url

    class HeaderRegion(Page):

        _header_locator = (By.ID, 'branding')

        #Header Locators List
        _home_link_locator = (By.ID, 'bla bla')
        _signin_link_locator = (By.NAME, 'bla bla')
        _signout_link_locator = (By.CSS_SELECTOR, '#bla bla bla')
        _myaccount_link_locator = (By.XPATH, 'bla bla bla')

        _mozilla_logo_link_locator = (By.CSS_SELECTOR, '.mozilla')

        def click_home_logo(self):
            self.selenium.find_element(*self._home_link_locator).click()

        @property
        def is_mozilla_logo_visible(self):
            return self.is_element_visible(self._mozilla_logo_link_locator)

        def click_mozilla_logo(self):
            self.selenium.find_element(*self._mozilla_logo_link_locator).click()

        @property
        def logged_in(self):
            return self.is_element_visible(*self._signout_link_locator)

        @property
        def logged_out(self):
            return self.is_element_visible(*self._signin_link_locator)

        def click_signin(self):
            self.selenium.find_element(*self._signin_link_locator).click()

        def click_signout(self):
            self.selenium.find_element(*self._signout_link_locator).click()

    class FooterRegion(Page):

        _footer_locator = (By.ID, 'footer')
        #Footer Locators List
        _footer_link_locator = (By.CSS_SELECTOR, 'bla bla')

    class ShareLinksRegion(Page):

        _root_locator = (By.CSS_SELECTOR, '#share')
        _share_title = (By.CSS_SELECTOR, 'title')
        _twitter_twit_locator = (By.CSS_SELECTOR, '#twitter')
        _facebook_like_locator = (By.CSS_SELECTOR, '#facebook')

        @property
        def _root_element(self):
            return self.selenium.find_element(*self._root_locator)

        def click_share_on_facebook(self):
            self._root_element.find_element(*self._facebook_like_locator).click()

        def click_share_on_twitter(self):
            self._root_element.find_element(*self._twitter_twit_locator).click()

        @property
        def share_title_text(self):
            return self._root_element.find_element(*self._share_title).text
