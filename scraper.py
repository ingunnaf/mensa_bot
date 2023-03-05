from bs4 import BeautifulSoup
import requests
import pandas as pd
import tabula as tb
import textract as tx
from PyPDF2 import PdfReader
mensaURL = "https://www.stw.berlin/mensen/einrichtungen/technische-universität-berlin/mensa-tu-hardenbergstraße.html"

def getPDFurl(): 

  page = requests.get(
    url='https://proxy.scrapeops.io/v1/',
    params={
        'api_key': '904703d4-06e0-466f-a6cd-d030a70e39bd',
        'url': mensaURL, 
    },
  )

  soup = BeautifulSoup(page.content, 'html.parser')
  speiseplan = soup.find('div', id='speiseplan')
  menuURL = speiseplan.find('a')
  menuURL = 'https://www.stw.berlin' + menuURL.attrs['href']
  return menuURL

def downloadMenuPDF():
  menuURL = getPDFurl()

  page2 = requests.get(
    url='https://proxy.scrapeops.io/v1/',
    params={
        'api_key': '904703d4-06e0-466f-a6cd-d030a70e39bd',
        'url': menuURL, 
    },
  )

  pdf = open("menu.pdf", 'wb')
  pdf.write(page2.content)
  pdf.close()


