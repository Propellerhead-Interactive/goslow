import urllib2
import json
from BeautifulSoup import BeautifulSoup




def get_routes():
    routes = [151, 153, 155, 157, 159, 161, 203, 205, 207, 209, 279, 281, 285, 412, 414, 432, 434, 436, 442, 465, 479, 481, 483, 491, 493, 495, 718, 719, 720, 721, 722, 723, 725, 801, 803, 805, 807, 809, 829, 831, 833, 835, 858, 860, 862, 864, 866, 917, 918, 919, 920, 921, 922, 923, 924]
    src='http://gmcprod.metrolinx.com/pins//details/'
    for x in routes:
        newsrc=src + str(x)
        page = urllib2.urlopen(newsrc)
        #if len(page)>100:
        a = (str(BeautifulSoup(page)))
        
        if len(a) > 50:
            route = json.loads(a)
            route_id = route["trip"]["id"]
            route_name = route["trip"]["name"]
            route_time = route["trip"]["time"]
        
            print route_id, route_name, route_time
        
get_routes()
        
    
    