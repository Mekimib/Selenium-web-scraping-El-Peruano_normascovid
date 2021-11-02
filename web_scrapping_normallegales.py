# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 19:27:58 2021

@author: kiara
"""

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re 
import pandas as pd
import urllib.request


driver = webdriver.Chrome(
    r"C:\Users\kiara\Downloads\chromedriver_win32 (2)\chromedriver")
driver_sub = webdriver.Chrome( r"C:\Users\kiara\Downloads\chromedriver_win32 (2)\chromedriver")

driver.get('https://diariooficial.elperuano.pe/Normas?_ga=2.118140352.876794275.1634819782-2095561376.1634227953')
driver_sub.get('https://diariooficial.elperuano.pe/Normas?_ga=2.118140352.876794275.1634819782-2095561376.1634227953')
search = driver_sub.find_element_by_name("cddesde")
search.send_keys(Keys.CONTROL + 'a', Keys.BACKSPACE)
search.send_keys('28/07/2021')
search.send_keys(Keys.ENTER)
search.send_keys(Keys.ENTER)


search = driver.find_element_by_name("cddesde")
search.send_keys(Keys.CONTROL + 'a', Keys.BACKSPACE)
search.send_keys('28/07/2021')
search.send_keys(Keys.ENTER)
search.send_keys(Keys.ENTER)

time.sleep(400)

class_ele = driver.find_element_by_id("NormasEPPortal")

pos = 0
df = pd.DataFrame(columns=['Fecha', 'Institución', 'Nombre', 'Descripcion','Designacion' ])

for ol in class_ele.find_elements_by_class_name('edicionesoficiales_articulos .ediciones_texto'):
    data = []
    h2 = ol.find_element_by_tag_name('h4').text
    div_2 = ol.find_element_by_tag_name('p').text
    div_3 = ol.find_element_by_tag_name('h5').text
    div_4 = ol.find_element_by_tag_name('p:nth-child(4)').text
    #Get in the link of each box and come back to continue screaping
    item = ol.find_element_by_css_selector('.ediciones_texto > h5 > a')
    link = item.get_attribute('href') 
    driver_sub.get(link)
    html = driver_sub.page_source
    soup=BeautifulSoup(html,'html.parser')
    #Get only the words after Desginar if exists. 
    pattern=re.compile(r'Designar[\.| ]')
    no_of_words=6
    h3='0'
    for elem in soup(text=pattern):
        str=elem.parent.text
        list=str.split(' ')
        list_indices=[i for i,x in enumerate(list) if re.match(pattern,x.strip()+' ')]# +' ' to conform with our pattern
        for index in list_indices:
            start=index-no_of_words
            end=index+no_of_words+1
            if start<0:
                start=0
                data = []
                h3= (' '.join(list[start:end]).strip())     
    #come back and continue scrapping the followed boxes
    driver_sub.execute_script('window.history.go(-1)')        
    data.append(div_2)
    data.append(h2)
    data.append(div_3)
    data.append(div_4)
    data.append(h3)
    df.loc[pos] = data
    pos += 1

print(df)


# save the dataframe in excel
df.to_excel(r'C:\Users\kiara\Dropbox\MPP\Third Semester\4_Text as Data\r practice\normas_legales\df.xlsx', index=False)


#To do list
# change date variable to a date format and split edicion extraordinario in another variable
# mutate a designacion dummy
#mutate a renuncia dummy
# mutate a gabinete variable with the name of the prime minister
# if it is posible, define a gender variable
#improve designacion variable with the name of the designated person with extract
