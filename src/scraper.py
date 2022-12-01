# -*- coding: utf-8 -*- 
'''
Created on 28 nov. 2022

@author: cluppi
'''

from datetime import datetime
from pickle import TRUE
from Logger import Logger
from os import path
from time import strftime
import requests
from pathlib import PurePath
from bs4 import BeautifulSoup
from pathlib import PurePath
import pandas as pd
from pandas import ExcelWriter

class Scraper (object):

    def __init__ (self, logger):
        self.logger = logger

    def scraper(self):
        monto = 0
        promedioDolar = 0
        promedioEuro = 0
        promedioReal = 0
        promedioFinalDolar = 0
        promedioFinalEuro = 0
        promedioFinalReal = 0
        montoFinalDolar = 0
        montoFinalEuro = 0
        montoFinalReal = 0
        tipoMonedaDolar = []
        tipoMonedaEuro = []
        tipoMonedaReal = []
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
                        text = BeautifulSoup(response.text,"html.parser")
                        entradas = text.find_all('div', {'class': 'tab-pane fade in active', 'id': 'billetes'})
                        #print(f"Entradas: {entradas}")

                        for i, entrada in enumerate(entradas):
                            fechaCotizacion = entrada.find('th', {'class': 'fechaCot'}).getText()
                            #print(fechaCotizacion)
                            
                            compra = entrada.find('tr').getText()
                            venta = entrada.find('th').getText()
                            #venta = entrada.find('td', {'class': 'tit'}).getText()
                            #print(compra)
                            #print(venta)
                            #tipoMoneda = entrada.find_all('td', {'class': 'tit'})
                            #print(tipoMoneda)
                            valores = entrada.find_all('td')
                            
                            for valor in valores:
                            #valores = valores[i]
                                #print(f"Valor: {valor}")
                                if 'Dolar U.S.A' in valor:
                                    moneda = 'Dolar U.S.A'
                                elif 'Euro' in valor:
                                    moneda = 'Euro'
                                elif 'Real *' in valor:
                                    moneda = 'Real'
                                #print(f"Moneda: {moneda}")
                                if moneda == 'Dolar U.S.A' and 'Dolar U.S.A' not in valor:
                                    
                                    monto = str(valor).split("<td>")
                                    monto = str(monto).split("</td>")
                                    montoFinal = monto[0].split("['', '")
                                    montoFinalDolar = montoFinal[1].replace(",",".")

                                    tipoMonedaDolar.append(montoFinalDolar)
                                    #print(tipoMoneda)
                                    promedioDolar = promedioDolar + float(montoFinalDolar)
                                    #print(f"Promedio Dolar: {promedioDolar}")
                                    promedioFinalDolar = promedioDolar/2
                                    #print(promedioFinalDolar)
                                    #if promedioDolar == 0:
                                    #    promedioDolar = promedioDolar + float(montoFinalDolar)
                                    #else:
                                    #    print(f"Promedio Dolar: {promedioDolar}")
                                    #    promedioFinalDolar = promedioDolar/2
                                    #    #print(promedioFinalDolar)
                                elif moneda == 'Euro' and 'Euro' not in valor:
                                    monto = str(valor).split("<td>")
                                    monto = str(monto).split("</td>")
                                    montoFinal = monto[0].split("['', '")
                                    montoFinalEuro = montoFinal[1].replace(",",".")

                                    tipoMonedaEuro.append(montoFinalEuro)
                                    #print(tipoMoneda)
                                    promedioEuro = promedioEuro + float(montoFinalEuro)
                                    promedioFinalEuro = promedioEuro/2

                                    #if promedioEuro == 0:
                                    #    
                                    #else:
                                    #    print(f"Promedio Euro: {promedioEuro}")
                                    #    
                                    #    #print(promedioFinalEuro)
                                elif moneda == 'Real' and 'Real *' not in valor:
                                    monto = str(valor).split("<td>")
                                    monto = str(monto).split("</td>")
                                    montoFinal = monto[0].split("['', '")
                                    #print(montoFinal)
                                    montoFinalReal = montoFinal[1].replace(",",".")
                                    
                                    tipoMonedaReal.append(montoFinalReal)
                                    #print(tipoMoneda)
                                    promedioReal = promedioReal + float(montoFinalReal)
                                    promedioFinalReal = promedioReal/2

                                    #if promedioReal == 0:
                                    #    promedioReal = promedioReal + float(montoFinalReal)
                                    #else:
                                    #    print(f"Promedio Real: {promedioReal}")
                                    #    promedioFinalReal = promedioReal/2
                                    #    #print(promedioFinalReal)
                            #print(f"Tipos Monedas: {tipoMonedaDolar} - {tipoMonedaEuro} - {tipoMonedaReal}")
                            #print(f"Promedios: {promedioFinalDolar} - {promedioFinalEuro} - {promedioFinalReal}")
                            #fechaCotizacion = fechaCotizacion.split()
                            df = pd.DataFrame(columns=['Día',fechaCotizacion,'a','b'])
                            
                            nuevaFila = pd.DataFrame(columns=['Moneda','Compra','Venta','Promedio'])
                            print(type(nuevaFila))
                            #df.loc[len(nuevaFila)] = nuevaFila
                            #df = df.loc[~df.index.duplicated(keep='first')]
                            #df = df.append(nuevaFila, ignore_index=True)
                            #df = pd.concat([df,nuevaFila], axis=0)
                            print(len(nuevaFila))
                            df.loc[len(df.index)] = nuevaFila
                            #print(df)
                            

                            writer = ExcelWriter('ejemplo.xlsx')
                            df.to_excel(writer, 'Hoja de datos', index=False)
                            writer.save()
                            #print (f"%d - %s  |  %s  |  %s" % (i + 1, fechaCotizacion, compra, venta))

                except requests.exceptions.ConnectionError as exc:
                    self.logger.error(f"Error: {exc}")
                
                #with open('salida.csv', 'w') as fpOutput:
                    #print(f"Valores {valores}")
                    #for i in valores:
                        #print(i)
                        #self.logger.info(f"Guardando datos en: {file_path}")

                
        except(OSError, IOError) as e:
            self.logger.error(f"Error al abrir el archivo {e}")

if __name__ == '__main__':
    logger = Logger("../log", "Scraper", dateFormat="%Y%m", timeFormat="")
    logger.info("-----------------------------------------------------------------------------------")    
    logger.info("Ejecutando Scraper: {}".format(strftime("%Y-%m-%d %H:%M:%S")))
    
    prueba = Scraper(logger)
    prueba.scraper()
    