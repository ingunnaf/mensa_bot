from bs4 import BeautifulSoup
import requests
import pandas as pd
import tabula as tb
import textract as tx
from PyPDF2 import PdfReader
url = "https://www.stw.berlin/mensen/einrichtungen/technische-universität-berlin/mensa-tu-hardenbergstraße.html"

def getPDFurl(): 

  page = requests.get(
    url='https://proxy.scrapeops.io/v1/',
    params={
        'api_key': '904703d4-06e0-466f-a6cd-d030a70e39bd',
        'url': url, 
    },
  )

  soup = BeautifulSoup(page.content, 'html.parser')
  speiseplan = soup.find('div', id='speiseplan')
  file = speiseplan.find('a')
  file = 'https://www.stw.berlin' + file.attrs['href']
  return file

def downloadMenuPDF():
  file = getPDFurl()

  page2 = requests.get(
    url='https://proxy.scrapeops.io/v1/',
    params={
        'api_key': '904703d4-06e0-466f-a6cd-d030a70e39bd',
        'url': file, 
    },
  )

  pdf = open("menu.pdf", 'wb')
  pdf.write(page2.content)
  pdf.close()
  

#reader = PdfReader("menu.pdf")
#number_of_pages = len(reader.pages)
#page = reader.pages[1]
#text = page.extract_text()
#print(text)

## Now I have the pdf of the weekly plan for the food :-) 
## Now I can extract the info for one particular day from the pdf. 

# How do we do that ? And send it to a telegram bot ? 

