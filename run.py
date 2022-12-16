try:
    import undetected_chromedriver.v2 as uc
    import time
    import pandas as pd
    from selenium import webdriver
    from bs4 import BeautifulSoup as BS
    from selenium.common.exceptions import *
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import Select, WebDriverWait
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.support import expected_conditions as ec
    import itertools

except ImportError:
    import os
    os.system("pip install selenium undetected_chromedriver pandas beautifulsoup4")

class Chrome:
    def __init__(self):
        self.driver = uc.Chrome()
        self.get_page()
        
   
    def scroll_down_element(self, element, times):
        try:
            action = ActionChains(self.driver)
            action.move_to_element(element).perform()
            element.click() 
            for _ in range(times):
                element.send_keys(Keys.SPACE)
                time.sleep(0.1)
        except Exception as e:
            print( 'error scrolling down web element', e)
            
            
    def get_page(self):
        result = []
        try:
            self.driver.get("https://applipedia.paloaltonetworks.com/")
            time.sleep(30)
            table = WebDriverWait(self.driver,10).until(ec.presence_of_all_elements_located((By.XPATH,'//table')))
            # self.scroll_down_element(table[-1],10)
            body = WebDriverWait(self.driver,10).until(ec.presence_of_element_located((By.XPATH,'//body'))).get_attribute('innerHTML')
            self.driver.quit()
            content = BS(body,'html.parser')
            rows = content.select('#bodyScrollingTable>tr')
            
            for row in rows:
                try:
                    data = {
                        "Names":row.select_one('td:nth-child(1)>a').get_text(strip=True),
                        "Category":row.select_one('td:nth-child(2)').get_text(strip=True),
                        "Sub Category":row.select_one('td:nth-child(3)').get_text(strip=True),
                        "Rank":row.select_one('td:nth-child(4)>img')['title'],
                        "Technology":row.select_one('td:nth-child(5)').get_text(strip=True)
                    }
                except:
                    data = None
                # print(data)
                if data is not None:
                    result.append(data)
            print(result[-1])
           

        except Exception as e:
            print(e)
        
        pd.DataFrame(result).to_excel("result.xlsx",index=None)
        pd.DataFrame(result).to_csv("result.csv",index=None)
            
if __name__ == '__main__':
    Chrome()
