#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
import re
from urlparse import urlparse

from pages.page_object import MySiteHomePage
from unittestzero import Assert

xfail = pytest.mark.xfail


class TestTemplate():

    ################################################################
    # GENERAL TEST LIST OF MAIN FUNCTIONALITY FOR MARKETING PRODUCTS
    ################################################################
#    def test_that_we_do_something_to_find_a_bug(self, mozwebqa):
#        pass
#
#    def test_header(self, mozwebqa):
#        pass
#
#    def test_footer(self, mozwebqa):
#        pass
#
    def test_locale(self, mozwebqa):
        main_page = MySiteHomePage(mozwebqa)
        if main_page.is_change_locale_visible:
            for i in range(main_page.locales_count):
                main_page.locales[i].select()
                selected = main_page.locales[i].value
                regex = re.search('((.*-)(.*))', selected)
                try:
                    selected = regex.group(2) + regex.group(3).upper()
                except:
                    print ""
                Assert.contains(selected, main_page.get_url_current_page())
        else:
            print "There is no language selector on the page"

    def test_response_200(self, mozwebqa):
        main_page = MySiteHomePage(mozwebqa)
        for url in main_page.get_all_links():
            # Ignoring js links
            if '#' or 'javascript' in url:
                continue
            response = main_page.get_response_code(url)
            Assert.equal(response, 'The request returned an HTTP 200 response.', 'in url: %s' % url)

    def test_response_404(self, mozwebqa):
        main_page = MySiteHomePage(mozwebqa)
        garbage_path = ['/76976cd1a3cbadaf77533a', '/garbage123213', '/blablabla']
        for path in garbage_path:
            url = main_page.base_url + path
            response = main_page.get_response_code(url)
            Assert.equal(response, 'The request returned an HTTP 404 response.', 'in url: %s' % url)
            Assert.true(main_page.is_404_page_present(url))

    def test_validate_links(self, mozwebqa):
        main_page = MySiteHomePage(mozwebqa)
        main_page.validate_link(main_page.base_url)

    def test_validate_feeds(self, mozwebqa):
        main_page = MySiteHomePage(mozwebqa)
        #feed_link = main_page.get_feed_link
        feed_link = 'http://blog.mozilla.com/feed/'
        validate_result = main_page.validate_feed(feed_link)
        Assert.not_none(validate_result)

    def test_favicon_exist(self, mozwebqa):
        main_page = MySiteHomePage(mozwebqa)
        link = main_page.get_favicon_link(main_page.base_url)
        if link:
            match = re.search('favicon.(ico|png|gif)', link)
            if match:
                Assert.contains('favicon', link)
            response = main_page.get_response_code(link)
        elif link == None:
            u = urlparse(main_page.base_url)
            link = "%s://%s/favicon.ico" % (u.scheme, u.netloc)
            response = main_page.get_response_code(link)
        else:
            link = '%sfavicon.ico' % main_page.base_url
            response = main_page.get_response_code(link)
        Assert.equal(response, 'The request returned an HTTP 200 response.', 'in url: %s' % link)

    @xfail(reason="not everywhere we have robots :( ")
    def test_robot_txt_present_on_site(self, mozwebqa):
        main_page = MySiteHomePage(mozwebqa)
        result = main_page.is_robot_txt_present(main_page.base_url)
        Assert.equal(result, "A robots.txt file is present on the server")
        #TODO: Could be added comparing with proper robots.txt file

    def test_request_ends_with_slash(self, mozwebqa):
        # BaseUrl Should be added without language in path for proper tests of locale (e.g. http://mozilla.org/firefox)
        lang = ['en-US', 'de']
        main_page = MySiteHomePage(mozwebqa, False)
        url_path = urlparse(main_page.base_url)
        for i in lang:
            response_path = main_page.get_response_path(main_page.base_url, i)
            url_path_re = urlparse(response_path)
            if (url_path.path == '' and url_path_re.path == '/'):
                Assert.true(response_path.endswith('/'))
            else:
                Assert.contains("/%s/" % i, response_path)

#    def test_login(self, mozwebqa):
#        pass
#
#    def test_logout(self, mozwebqa):
#        pass
#
#    def test_create_account(self, mozwebqa):
#        pass
#
#    def test_input_forms_security(self, mozwebqa):
#        pass
#
#    def test_pagination(self, mozwebqa):
#        pass
