from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.environ.get('API_KEY')

mensaURL = "https://www.stw.berlin/mensen/einrichtungen/technische-universität-berlin/mensa-tu-hardenbergstraße.html"

def getPDFurl(): 

  page = requests.get(
    url='https://proxy.scrapeops.io/v1/',
    params={
        'api_key': API_KEY,
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
        'api_key': API_KEY,
        'url': menuURL, 
    },
  )

  pdf = open("menu.pdf", 'wb')
  pdf.write(page2.content)
  pdf.close()


