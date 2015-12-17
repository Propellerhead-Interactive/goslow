import urllib2, sys,datetime
from BeautifulSoup import BeautifulSoup
from peewee import SQL
sys.path.insert(0, 'app/model/')
from  models import Stops, Status, Routes, db




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
            route_stops = route_detail.split('-')
            route_start = route_stops[0]
            
            route_end = route_stops[-1]
            delay_of = c[1].split("of")[1].strip()
            current_status = c[2]
            current_detail = c[-1]
            
            route_beginning_stop = " ".join(route_start.strip().split(" ")[:-1])
            route_beginning_time = route_start.strip().split(" ")[-1]
            print "test1",route_beginning_time
           
           
            route_end_stop = " ".join(route_end.strip().split(" ")[:-1])
            route_end_time = route_end[-1]
            
            print "Status",status
            print "Route",route
            print "route start name", route_beginning_stop
            print "route end name", route_end_stop
            print "route start time====", route_beginning_time
            print "delay_of", delay_of
            print "detail", current_detail
            print "from", route_start
            print "to", route_end
            
            #route = Routes.select().where(Routes.route_long_name==route)
            #from_stop = Stops.select().where(Stops.stop_name == route_beginning_stop)
            #to_stop = Stops.select().where(Stops.stop_name == route_end_stop)
            
            s = Status.create(route=route, 
                fromStop = route_beginning_stop, 
                toStop=route_end_stop, 
                message=current_detail,
                delay_time=delay_of,
                train_time=route_beginning_time)
                
            s.save()
        
        r_id = 0
        # for route in TrainRoute.select().where(SQL("route_time > NOW() and route_name=%s ", route)).order_by(TrainRoute.route_time):
 #            print "Found route: " + route.route_name, route.route_time  # .raw() will return model insta
 #            #write_data(route, status)
 #            break;
       
crawl_status()



    


   
    

   