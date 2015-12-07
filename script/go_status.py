import urllib2, sys
from BeautifulSoup import BeautifulSoup
from peewee import SQL
sys.path.insert(0, 'app/model/')
from  models import TrainRoute, Status


def write_data(route, _status):
   
    status = Status(route=route, message = _status)
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
        print "SCAPE " + str(route) + " - "+  str(status)
        r_id = 0
        for route in TrainRoute.select().where(SQL("route_time > NOW() and route_name=%s ", route)).order_by(TrainRoute.route_time):
            print "Found route: " + route.route_name, route.route_time  # .raw() will return model insta
            write_data(route, status)
            break;
       

crawl_status()



    


   
    

   