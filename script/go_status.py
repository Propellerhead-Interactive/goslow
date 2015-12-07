import urllib2
from BeautifulSoup import BeautifulSoup

import sys
sys.path.append( '../app/model/')
import models


def write_data(_name, _status):
    route = TrainRoute(name=_name)
    route.save()
    status = Status(route=route, status = _status)
    status.save()

def crawl_status():
    src='http://www.gotransit.com/publicroot/en/default.aspx'
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
        write_data(route, status)
     
def crawl_routes():
      
    
    
crawl_routes()
crawl_status()



    


   
    

   