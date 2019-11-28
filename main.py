from requests import get, post
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import pdfkit

def simple_get(url):
    """
    poskusi dobiti vsebino na url-ju z HTTP GET requestom
    Če je vsebina urlja HTML ali XML, vrnemo text, drugeče None
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
           and content_type is not None 
           and content_type.find('html') > -1)


def log_error(e):
    '''
    Vedno je dobra ideja error log. 
    Ta funkcija samo sprinta napako.
    '''
    print(e)

def ih_web_scrap():
    
    webLink = "https://wiki.razor.si/index.php?title=Special:AllPages"
    
    raw_html = simple_get(webLink)
    soup = BeautifulSoup(raw_html, 'html.parser')
    
    for ultag in soup.find_all('ul', {'class': 'mw-allpages-chunk'}):
        for litag in ultag.find_all('li'):
            #print(litag.text) 
            #print(litag.a.get('href'))
            article_name = litag.text
            article_url = litag.a.get('href')
            make_pdf(article_name, article_url)

def replace_special_character(stringR):
    newstring = stringR.lower()
    newstring = newstring.replace("č", "c")
    newstring = newstring.replace("š", "s")
    newstring = newstring.replace("ž", "z")
    return newstring

def make_pdf(article_name, article_url):
    #article_url is in the format '/index.php?title=Word'
    print(article_name)
    article_name = replace_special_character(article_name)
    print(article_name)
    
    pdfkit.from_url(f"https://wiki.razor.si{article_url}", f"data/{article_name}.pdf")

#make_pdf("index.php?title=Apache2")

ih_web_scrap()



