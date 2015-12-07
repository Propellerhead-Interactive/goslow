import urllib2
from BeautifulSoup import BeautifulSoup

import sys
sys.path.append( '../app/model/')
import models

src='http://www.gotransit.com/publicroot/en/default.aspx'

def write_data(_name):
    route = TrainRoute(name=_name)
    route.save()

def crawl():
    page = urllib2.urlopen(src)
    soup = BeautifulSoup(page)
    crawl_list = []
    table = soup.findAll('table',  )
    
    table = soup.find("table", { "class" : "gridStatusTrain" })
    tb = table.find("tbody")
    rows = tb.findAll("tr")

    for row in rows:
        cells = row.findAll("td", text=True)
        route = cells[0]
        status = cells[1]
        print str(route) + " - "+  str(status)
        write_data(route)
        
    
crawl()


    


   
    

   