import urllib2, sys
from BeautifulSoup import BeautifulSoup
from peewee import SQL
sys.path.insert(0, 'app/model/')
#from  models import TrainRoute, Status


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
        if cells[1]!="On Time":
          
            cellsFUll = row.findAll("td")
            detail =  cellsFUll[1].span.ul.findChildren("li")[1].span.contents
            c = [x for x in detail if "Tag" not in str(type(x))  ]
           
            route_detail = c[0].strip()
            route_start = route_detail[0].split('-')
            print c[0]
            
            route_pieces = route_start.split(" ")
            
            route_start = (route_pieces)[0]
           
            delay_of = c[1]
            current_status = c[2]
            current_Detai = c[3]
            
            
            #<span>Union Station 11:13 - Oshawa GO 12:11<br>Delay of 05m:10s<br>Stopped</span>
           
            # late_cells = row.findAll("td.gridStatusWidthTwo > span.messageDisrp > ul.lastTrainD > li.odd > span")
 #            print "late cells",late_cells
 #
 #            data = second_li.find("span", text=True)
 #            print data
 #            #navigte to the reason
            
            
        print "SCAPE " + str(route) + " - "+  str(status)
        r_id = 0
        # for route in TrainRoute.select().where(SQL("route_time > NOW() and route_name=%s ", route)).order_by(TrainRoute.route_time):
 #            print "Found route: " + route.route_name, route.route_time  # .raw() will return model insta
 #            #write_data(route, status)
 #            break;
       

crawl_status()



    


   
    

   