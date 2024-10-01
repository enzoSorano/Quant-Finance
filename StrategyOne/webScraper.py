# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 04:31:11 2024

@author: esorano
"""

from selenium import webdriver
from selenium.webdriver.common.by import By

'''
Description:
    A function that webscrapes magicformulainvesting.com for the tickers of
    all of the stocks that are undervalued
variables:
    path     = path to chromedriver(if you don't have chrome driver install them')
    email    = email you used to sign up for magicformulainvesting.com with
    password = password for magicformulainvesting.com
    tickers  = an empty list to store all of the ticker symbols scraped
'''
def getMagicFormulaStocks(path, email, password, tickers):
    
    service = webdriver.chrome.service.Service(path)
    service.start()
    
    url = "https://www.magicformulainvesting.com/Account/LogOn"
    
    driver = webdriver.Chrome(service=service)
    driver.get(url)
    driver.implicitly_wait(3)
    
    email_input = driver.find_element(By.ID, "Email")
    email_input.send_keys(email)
    
    password_input = driver.find_element(By.ID, "Password")
    password_input.send_keys(password)
    
    login_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][name='login']")
    login_button.click()
    
    # Wait for the radio button to be present and clickable, then select it
    radio_button = driver.find_element(By.CSS_SELECTOR, "input[type='radio'][value='false']")
    radio_button.click()
    
    get_stocks_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][name='stocks']")
    get_stocks_button.click()
    
    table = driver.find_element(By.ID, "tableform")
    
    # Extract text from each row and cell within tbody
    rows = table.find_elements(By.TAG_NAME, "tr")
    
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) > 1:
            second_td_text = cells[1].text
            tickers.append(second_td_text)