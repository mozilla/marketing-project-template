#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException


class Page(object):
    '''
    Base class for all Pages
    '''

    def __init__(self, testsetup):
        '''
        Constructor
        '''
        self.testsetup = testsetup
        self.base_url = testsetup.base_url
        self.selenium = testsetup.selenium
        self.timeout = testsetup.timeout

    @property
    def is_the_current_page(self):
        page_title = self.selenium.title

        if not page_title == self._page_title:
            print "Expected page title: %s" % self._page_title
            print "Actual page title: %s" % page_title
            raise Exception("Expected page title does not match actual page title.")
        else:
            return True

    def is_element_visible(self, *locator):
        try:
            return self.selenium.find_element(*locator).is_displayed()
        except NoSuchElementException, ElementNotVisibleException:
            return False

    def is_element_present(self, *locator):
        self.selenium.implicitly_wait(0)
        try:
            self.selenium.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
        finally:
            # set back to where you once belonged
            self.selenium.implicitly_wait(self.testsetup.default_implicit_wait)

    def get_url_current_page(self):
        return(self.selenium.current_url)

    def get_page_title(self):
        return self.selenium.title

    def refresh(self):
        self.selenium.refresh()

    def return_to_previous_page(self):
        self.selenium.back()

    def validation_errors_log(self, err_msg, errors, warnings):
        logfile = 'results/validate_errors.html'
        logfile_dirname = os.path.dirname(logfile)
        if logfile_dirname and not os.path.exists(logfile_dirname):
            os.makedirs(logfile_dirname)
        logfile = open(logfile, 'w')
        logfile.write('<html><head><title>HTML Validation Report</title><style>')
        logfile.write('\nbody {font-family: Helvetica, Arial, sans-serif; font-size: 12px}')
        logfile.write('\nh2 {font-size: 16px; color: red}')
        logfile.write('\ntable {border: 1px solid #e6e6e6; color: #999; font-size: 12px; border-collapse: collapse}')
        logfile.write('\n.error, .failed, .invalid, {color: red}')
        logfile.write('\n</style></head><body>')
        logfile.write('\n<h1>Summary</h1>')
        logfile.write(str(err_msg[0]))
        logfile.write('\n<h1>Results</h2>')
        logfile.write('<table class="header"><tr><th>Result:</th>')
        logfile.write('<td colspan="2" class="failed"> %s Errors, %s warning(s)' % (errors, warnings))
        logfile.write('</td></tr><tr><th><label title="Address of Page to Validate" for="uri">Address</label>:</th>')
        logfile.write('<td colspan="2">')
        logfile.write('<input type="text" id="uri" name="uri" value="%s" size="50" /></td></tr>' % self.base_url)
        logfile.write('\n</table></body></html>')
        logfile.close()
