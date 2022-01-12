import undetected_chromedriver.v2 as uc
import pandas as pd
import sys
sys.path.append('../')

from time import sleep
from utils import random_sleep


class InteractiveBot():
    
    def __init__(self):
        self.driver = uc.Chrome()

    def _connect_and_clear(self):
        self.driver.get("https://m.apuestas.codere.es/deportes/index.htm#/NearestLocalPage")
        sleep(10)
        self.driver.maximize_window()
        random_sleep()
        self.driver.find_element_by_xpath('/html/body/ion-app/ion-alert/div/div[3]/button/span').click()
        random_sleep()
        zoom_element = self.driver.find_element_by_xpath('//*[@id="map"]/div/div/div[13]/div/div/div/button[2]')
        for _ in range(0,6):
            zoom_element.click()
            random_sleep()
        print('Sleeping for 100 seconds')
        sleep(100)

    def _extract_data(self):
        item_list = self.driver.find_elements_by_tag_name('ion-item')
        name_list = []
        location_list = []
        # Meter un TQDM
        for item in item_list:
            try:
                label = item.find_element_by_tag_name('ion-label')
                name  = label.find_element_by_tag_name('h2').text
                location = label.find_element_by_tag_name('p').text
                name_list.append(name)
                location_list.append(location)
            except Exception:
                print('No se pudo recuperar')
        
        pd.DataFrame.from_dict({
            'NOMBRE_LOCAL': name_list,
            'UBICACION': location_list
        }).to_csv('locales_codere.csv', index=False, encoding='utf-8')
                
    def run(self):
        self._connect_and_clear()
        self._extract_data()

if __name__ == '__main__':
    bot = InteractiveBot()
    bot.run()