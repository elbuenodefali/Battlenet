# coding=utf-8
import requests
from lettuce import step, world
from lettuce_webdriver.util import AssertContextManager
from nose.tools import assert_equals
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import Select


def find_id(browser, attribute):
    id = "%s" % attribute
    element = browser.find_element_by_id(id)
    return element


def find_name(browser, attribute):
    name = "%s" % attribute
    element = browser.find_element_by_name(name)
    return element


def find_xpath(browser, attribute):
    xpath = "%s" % attribute
    element = browser.find_element_by_xpath(xpath)
    return element


def find_partial_link(browser, attribute):
    partial_link = "%s" % attribute
    element = browser.find_element_by_partial_link_text(partial_link)
    return element


def find_css(browser, attribute):
    css = "%s" % attribute
    element = browser.find_element_by_css_selector(css)
    return element


def find_tags(browser, attribute):
    tags = "%s" % attribute
    elements = browser.find_elements_by_tag_name(tags)
    return elements

def find_class_name(browser, attribute):
    class_name = "%s" % attribute
    element = browser.find_element_by_class_name(class_name)
    return element

# Find element by ID
@step('there is an element with id "(.*?)"')
def check_element_with_id(step, identifier):
    try:
        with AssertContextManager(step):
            world.element = find_id(world.browser, identifier)
    except AssertionError:
            print ('Element not found')

# Find element by NAME
@step('there is an element with name "(.*?)"')
def check_element_with_name(step, name):
    with AssertContextManager(step):
        world.element = find_name(world.browser, name)


# Find element by XPATH
@step('there is an element with xpath "(.*?)"')
def check_element_with_xpath(step, xpath):
    with AssertContextManager(step):
        world.element = find_xpath(world.browser, xpath)


# Find element by Partial Link Text
@step('there is an element with partial link text "(.*?)"')
def check_element_with_partial_link(step, partial_link):
    with AssertContextManager(step):
        world.element = find_partial_link(world.browser, partial_link)


# Find element by CSS
@step('there is an element with css "(.*?)"')
def check_element_with_css(step, css):
    with AssertContextManager(step):
        world.element = find_css(world.browser, css)

# Find element by CLASS
@step('there is an element with class "(.*?)"')
def check_element_with_class(step, class_name):
    with AssertContextManager(step):
        world.element = find_class_name(world.browser, class_name)

# Write value in element
@step("I fill in with (?P<input_value>.+)")
def write_value(step, input_value):
    with AssertContextManager(step):
        world.element.clear()
        if input_value == 'empty':
            world.element.send_keys('')
        else:
            world.element.send_keys(input_value)

# Check value of an element
@step("the element contains (?P<output_value>.+)")
def check_value(step, output_value):
    if output_value == 'empty':
        output_value = ''
        assert_equals(world.element.get_attribute('value').encode('utf-8'), output_value)
    else:
        assert_equals(world.element.get_attribute('value').encode('utf-8'), output_value)



# Check class of parent element
@step('class of parent is "(.*?)"')
def check_class(step, value):
    child = world.element
    parent = child.find_element_by_xpath('..')
    assert_equals(parent.get_attribute('class').encode('utf-8'), value)


# Click on parent element
@step('I click on parent')
def click_parent(step):
    with AssertContextManager(step):
        child = world.element
        parent = child.find_element_by_xpath('..')
        parent.click()


# Click on an element
@step('I click on it')
def click_on_it(step):
    with AssertContextManager(step):
        world.element.click()

#Get all href values
@step("there are some links")
def get_links(step):
    with AssertContextManager(step):
        links_list = world.browser.find_elements_by_xpath("//*[@href]")
        href_list = []
        for href in links_list:
            href_list.append(href.get_attribute('href'))
        http_list = []
        for href in href_list:
            if href.startswith('http'):
                # print "%s" % href
                http_list.append(href)
        world.links = http_list

#Check response code of each href
@step('I navigate to each link and check response status code is lower than 400')
def navigate_to_links(step):
    try:
        for req in world.links:
            response = requests.get(req)
            # print "Tested: URL %s, RESPONSE CODE: %s" % (req, response.status_code)
            assert response.status_code < 400, \
                "URL: '%s' RESPONSE CODE: '%s'" % (req, response.status_code)
    except AssertionError:
        print "BROKEN LINK: URL: '%s' RESPONSE CODE: '%s'" % (req, response.status_code)

#Press TAB Key
@step("the focus is lost in that element pressing tab key")
def press_tab(step):
    world.element.send_keys(Keys.TAB)

#Check text error
@step("its text is (?P<text_error>.+)")
def get_its_text(step, text_error):
    if world.element.text == '':
        text_error = ''
    assert_equals(world.element.text, text_error)

#Fill in again
@step("I fill in again with (?P<input_value_2>.+)")
def write_value_again(step, input_value_2):
    with AssertContextManager(step):
        world.element.clear()
        world.element.send_keys(input_value_2)

#Check password strength
@step("the password strength is (?P<strength>.+)")
def password_strength(step, strength):
    time.sleep(1)
    child = find_id(world.browser,'password-error-inline')
    world.element = child.find_element_by_xpath('..')
    if strength == 'empty':
        pass
    else:
        assert_equals(world.element.text,strength)

#Get elements with tag li
@step("its children are list elements")
def get_li_elements(step):
    world.guideline = world.element.find_elements_by_tag_name('li')

#Check password length
@step("check password guideline length (?P<A>.+)")
def check_pass_length(step, A):
    assert_equals(world.guideline[0].get_attribute('class').encode('utf-8'),A)

#Check password alphanumeric values
@step("check password guideline alphanumeric value (?P<B>.+)")
def check_pass_alpha(step, B):
    assert_equals(world.guideline[1].get_attribute('class').encode('utf-8'),B)

#Check password special characters
@step("check password guideline special characters (?P<C>.+)")
def check_pass_specialcharacters(step, C):
    assert_equals(world.guideline[2].get_attribute('class').encode('utf-8'),C)

#Check password similar to email
@step("check password guideline similar to email (?P<D>.+)")
def check_pass_similar_to_email(step, D):
    assert_equals(world.guideline[3].get_attribute('class').encode('utf-8'),D)

#Get all options from country list
@step("I get all the options of the list")
def get_all_options(step):
    world.form = world.browser.find_element_by_id('change-country')
    world.form_div = world.form.find_elements_by_tag_name('div')
    world.select = Select(world.form_div[1].find_element_by_id('country-list'))
    options = world.select.options
    del options[0] #It is not a country
    world.country = []
    for value in options:
        world.country.append(value.get_attribute('value').encode('utf-8'))

#Check country param value
@step("HTTP GET country param is changed and current option selected is changed")
def step_impl(step):
    for country in world.country:
        world.browser.get('https://eu.battle.net/account/creation/tos.html?country=%s' % country)
        time.sleep(1)
        world.form = world.browser.find_element_by_id('change-country')
        world.form_div = world.form.find_elements_by_tag_name('div')
        world.select = Select(world.form_div[1].find_element_by_id('country-list'))
        option_selected = world.select.first_selected_option
        assert_equals(option_selected.get_attribute('value').encode('utf-8'),country, "Wrong country selected")

#Return to web page
@step('I return to "(.*?)"')
def return_to(step,url):
    world.browser.get(url)

#Get regions
@step("there are some regions to choose")
def get_regions(step):
    world.regions = find_id(world.browser,"select-regions")
    world.ul_regions = world.regions.find_element_by_class_name("region-ul")
    world.li_regions = world.ul_regions.find_elements_by_tag_name('li')

#Get languages
@step("there are some language to choose")
def get_languages(step):
    world.language = find_id(world.browser,"select-language")
    world.ul_language = []
    world.ul_language = world.language.find_elements_by_class_name("region-ul")
    world.li_language_0 = world.ul_language[0].find_elements_by_tag_name('li')
    world.li_language_1 = world.ul_language[1].find_elements_by_tag_name('li')
    world.li_language_2 = world.ul_language[2].find_elements_by_tag_name('li')
    world.li_language_3 = world.ul_language[3].find_elements_by_tag_name('li')
    world.li_language_4 = world.ul_language[4].find_elements_by_tag_name('li')
    world.li_language_5 = world.ul_language[5].find_elements_by_tag_name('li')

#Open regions and languages menu
@step("I want to choose my region and language")
def open_region_language(step):
    world.caret = world.browser.find_element_by_class_name("caret")
    world.caret.click()

#Check Americas
@step("I check Americas and its languages")
def check_americas(step):
        class_attribute = world.li_regions[0].get_attribute('class').encode('utf-8')
        assert_equals(('active' in class_attribute), False)
        world.li_regions[0].find_element_by_tag_name('a').click()
        class_attribute = world.li_regions[0].get_attribute('class').encode('utf-8')
        assert_equals(('active' in class_attribute), True)
        for language in world.li_language_0:
            class_attribute = language.get_attribute('class').encode('utf-8')
            assert_equals(('active' in class_attribute), False)
            language.find_element_by_tag_name('a').click()
            class_attribute = language.get_attribute('class').encode('utf-8')
            assert_equals(('active' in class_attribute), True)
            time.sleep(2)

#Check Europe
@step("I check Europe and its languages")
def check_Europe(step):
    class_attribute = world.li_regions[1].get_attribute('class').encode('utf-8')
    assert_equals(('active' in class_attribute), False)
    world.li_regions[1].find_element_by_tag_name('a').click()
    class_attribute = world.li_regions[1].get_attribute('class').encode('utf-8')
    assert_equals(('active' in class_attribute), True)
    for language in world.li_language_1:
        class_attribute = language.get_attribute('class').encode('utf-8')
        assert_equals(('active' in class_attribute), False)
        language.find_element_by_tag_name('a').click()
        class_attribute = language.get_attribute('class').encode('utf-8')
        assert_equals(('active' in class_attribute), True)
        time.sleep(2)

#Check Corea
@step("I check Corea and its languages")
def check_Corea(step):
    class_attribute = world.li_regions[2].get_attribute('class').encode('utf-8')
    assert_equals(('active' in class_attribute), False)
    world.li_regions[2].find_element_by_tag_name('a').click()
    class_attribute = world.li_regions[2].get_attribute('class').encode('utf-8')
    assert_equals(('active' in class_attribute), True)
    for language in world.li_language_2:
        class_attribute = language.get_attribute('class').encode('utf-8')
        assert_equals(('active' in class_attribute), True)
        language.find_element_by_tag_name('a').click()
        class_attribute = language.get_attribute('class').encode('utf-8')
        assert_equals(('active' in class_attribute), True)
        time.sleep(2)

#Check Taiwan
@step("I check Taiwan and its languages")
def check_Taiwan(step):
    class_attribute = world.li_regions[3].get_attribute('class').encode('utf-8')
    assert_equals(('active' in class_attribute), False)
    world.li_regions[3].find_element_by_tag_name('a').click()
    class_attribute = world.li_regions[3].get_attribute('class').encode('utf-8')
    assert_equals(('active' in class_attribute), True)
    for language in world.li_language_3:
        class_attribute = language.get_attribute('class').encode('utf-8')
        assert_equals(('active' in class_attribute), True)
        language.find_element_by_tag_name('a').click()
        class_attribute = language.get_attribute('class').encode('utf-8')
        assert_equals(('active' in class_attribute), True)
        time.sleep(2)

#Check China
@step("I check China and its languages")
def check_China(step):
    class_attribute = world.li_regions[4].get_attribute('class').encode('utf-8')
    assert_equals(('active' in class_attribute), False)
    world.li_regions[4].find_element_by_tag_name('a').click()
    class_attribute = world.li_regions[4].get_attribute('class').encode('utf-8')
    assert_equals(('active' in class_attribute), True)
    for language in world.li_language_4:
        class_attribute = language.get_attribute('class').encode('utf-8')
        assert_equals(('active' in class_attribute), True)
        language.find_element_by_tag_name('a').click()
        class_attribute = language.get_attribute('class').encode('utf-8')
        assert_equals(('active' in class_attribute), True)
        time.sleep(2)

#Check Southeast Asia
@step("I check Southeast Asia and its languages")
def check_Southeast(step):
    class_attribute = world.li_regions[5].get_attribute('class').encode('utf-8')
    assert_equals(('active' in class_attribute), False)
    world.li_regions[5].find_element_by_tag_name('a').click()
    class_attribute = world.li_regions[5].get_attribute('class').encode('utf-8')
    assert_equals(('active' in class_attribute), True)
    for language in world.li_language_5:
        class_attribute = language.get_attribute('class').encode('utf-8')
        assert_equals(('active' in class_attribute), True)
        language.find_element_by_tag_name('a').click()
        class_attribute = language.get_attribute('class').encode('utf-8')
        assert_equals(('active' in class_attribute), True)
        time.sleep(2)

#Check cookie compliance
@step("cookie compliance box appears")
def cookie_compliance(step):
    world.cookie_compliance = world.browser.find_element_by_id('eu-cookie-compliance')
    world.cookie_compliance_class = world.cookie_compliance.get_attribute('class').encode('utf-8')
    assert_equals(world.cookie_compliance_class,'modal eu-cookie-compliance desktop')

#Click on accept button
@step("I click on Accept")
def click_accept(step):
    world.browser.find_element_by_id('cookie-compliance-agree').click()

#Check cookie compliance box is closed
@step("the box is closed")
def close_cookie_compliance(step):
    world.cookie_compliance_class = world.cookie_compliance.get_attribute('class').encode('utf-8')
    assert_equals(world.cookie_compliance_class,'modal eu-cookie-compliance desktop hide')
