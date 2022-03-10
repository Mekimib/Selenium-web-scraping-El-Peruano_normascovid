# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 10:18:54 2022

@author: kiara
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 19:27:58 2021

@author: kiara
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# download chromedriver of your chrome version
driver = webdriver.Chrome(
    r"C:\Users\kiara\Downloads\chromedriver_win32\chromedriver")

driver.get('https://diariooficial.elperuano.pe/Normas/covid19#hide1')


#first click on "Filtrar por rango de fecha"
search = driver.find_element_by_id("chkfecha").click()


#Choose the date range you want to analyze
search = driver.find_element_by_id("fechaini")
search.send_keys(Keys.CONTROL + 'a', Keys.BACKSPACE)
search.send_keys('08/03/2020')
search.send_keys(Keys.ENTER)
search.send_keys(Keys.ENTER)


search = driver.find_element_by_id("fechafin")
search.send_keys(Keys.CONTROL + 'a', Keys.BACKSPACE)
search.send_keys('31/10/2020')
search.send_keys(Keys.ENTER)

#Click on "Buscar"
search = driver.find_element_by_id("btnFiltro").click()


time.sleep(400)

class_ele = driver.find_element_by_id("nleeLista")

pos = 0
df = pd.DataFrame(columns=['Numero', 'Institución', 'Nombre', 'Descripcion' , 'Fecha', 'link' ])

for ol in class_ele.find_elements_by_class_name('edicionesoficiales_articulos .ediciones_texto'):
    data = []
    h2 = ol.find_element_by_tag_name('h4').text
    div_2 = ol.find_element_by_tag_name('p').text
    div_3 = ol.find_element_by_tag_name('h5').text
    div_4 = ol.find_element_by_tag_name('p:nth-child(4)').text
    div_5 = ol.find_element_by_tag_name('p:nth-child(5)').text
    item = ol.find_element_by_css_selector('.ediciones_texto > h5 > a')
    link = item.get_attribute('href')
    data.append(div_2)
    data.append(h2)
    data.append(div_3)
    data.append(div_5)   
    data.append(div_4)
    data.append(link)
    df.loc[pos] = data
    pos += 1

print(df)


# save the dataframe in excel
df.to_excel(r'C:\Users\kiara\Dropbox\Freelance\Corona Net project\Peru\df_mar_oct_20.xlsx', index=False)

