from lettuce import before, world, after
from selenium import webdriver
import lettuce_webdriver.webdriver
import requests

@before.all
def setup_browser():
    path = 'C:/Users/RaFa/Downloads/chromedriver_win32/chromedriver.exe'
    world.browser = webdriver.Chrome(path)
    world.browser.implicitly_wait(10)
    world.browser.get('https://eu.battle.net/account/creation/tos.html')

@after.all
def close_browser(total):
    world.browser.quit()
