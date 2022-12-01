# -*- coding: utf-8 -*- 
'''
Created on 28 nov. 2022

@author: cluppi
'''
from datetime import datetime
from Logger import Logger
from os import path
from time import strftime
import requests
from pathlib import PurePath
from bs4 import BeautifulSoup
from pathlib import PurePath


class Scraper (object):

    def __init__ (self, logger):
        self.logger = logger

    def scraper(self):
        try:
            with open('../configuraciones/urls.txt', 'r') as fpIn:
                rutas = fpIn.readlines()
            rutas = [url.strip() for url in rutas]
        
            for url in rutas:
                file_name = PurePath(url).name
                file_path = path.join('.', file_name)
                text = ''

                try:
                    response = requests.get(url)
                    if response.ok:
                        text = response.text
                except requests.exceptions.ConnectionError as exc:
                    self.logger.error(f"Error: {exc}")
                
                with open(file_path, 'w') as fpOutput:
                    fpOutput.write(text)

                self.logger.info(f"Guardando datos en: {file_path}")
    
        except(OSError, IOError) as e:
            self.logger.error(f"Error al abrir el archivo {e}")

if __name__ == '__main__':
    logger = Logger("../log", "Scraper", dateFormat="%Y%m", timeFormat="")
    logger.info("-----------------------------------------------------------------------------------")    
    logger.info("Ejecutando Scraper: {}".format(strftime("%Y-%m-%d %H:%M:%S")))
    
    prueba = Scraper(logger)
    prueba.scraper()
    