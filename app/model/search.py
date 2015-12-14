from models import *
from playhouse.shortcuts import *
import datetime

class TrainSearch:

    @staticmethod
    def find_closest(lat, lon):
        stops =  Stops.raw("SELECT stops.*, SQRT(POW(69.1 * (stop_lat - %s), 2) +POW(69.1 * (%s - stop_lon) * COS(stop_lat / 57.3), 2)) AS distance FROM stops inner join stop_times on (stop_times.stop_id = stops.stop_id)  \
        inner join trips on (trips.trip_id = stop_times.trip_id) inner join routes on (routes.route_id=trips.route_id) where routes.route_type=2 HAVING distance < 10 ORDER BY distance", lat, lon)
        for stop in stops:
            return model_to_dict(stop)
            break
        return None
    
    
    @staticmethod
    def find_route(start_id, end_id, dow=0):
       
        
        try:
            dow = int(dow)
        except ValueError:
            print "error converting int"
            return  "Third Arg must be an integer"
        #THIS FINDS THE ROUTE BY JOINING WHERE TWO STATIONS INTERSCT
       # st = StopTimes.select(StopTimes.departure_time).distinct().join(Trips).join(Routes).where(Routes.route_type==2, Trips.service_id.contains(datetime.datetime.today().strftime('%a')), StopTimes.stop==st_id).order_by(StopTimes.departure_time).asc()
        
        #ALL OF THE TRAINS FROM OR TO GIVEN A DAY of wEEK
        #   
       
        days =  [ 
              'Mon', 
              'Tue', 
              'Wed', 
              'Thu',  
              'Fri', 
              'Sat',
              'Sun']
        #dow = datetime.datetime.today().weekday()
        
        
        #from trips - day of week
        #from stops - 
        # sts = db.execute_sql("select trips.trip_id, s1.departure_time, s1.stop_id from_stop_id, s2.stop_id to_stop_id, \
#         s2.arrival_time, trips.direction_id from stop_times s1 inner join \
#         trips on (trips.trip_id = s1.trip_id) inner join stop_times s2 on \
#         (trips.trip_id = s2.trip_id) join routes on (routes.route_id=trips.route_id) where routes.route_type=3 AND s1.stop_id=%s and s2.stop_id=%s AND trips.trip_id \
#         LIKE %s group by s1.departure_time order by s1.departure_time" , (start_id, end_id, "%"+days[dow]+"%"))
#
        sts = db.execute_sql("SELECT DISTINCT trips.trip_id, s1.departure_time,s2.arrival_time, s1.stop_id from_stop_id, \
        s2.stop_id to_stop_id from stop_times s1 inner join trips on \
        trips.trip_id=s1.trip_id inner join routes on routes.route_id=trips.route_id \
        inner join stop_times s2 on  (trips.trip_id = s2.trip_id) WHERE \
        s1.stop_id=%s AND s2.stop_id=%s AND trips.trip_id LIKE %s AND routes.route_type=2 \
        AND  s1.departure_time<s2.departure_time GROUP BY departure_time", (start_id, end_id, "%"+days[dow]+"%"))
        
        final_list = []
        
        for st in sts:
            print st[0]
            sched = ComposedSchedule(st[0],st[1],st[2],st[3],st[4])
            final_list.append(sched.__dict__) 
        return final_list
        
    @staticmethod
    def find_trip(_id):
        trips = []
        times = StopTimes.select().join(Stops).where(StopTimes.trip==_id).order_by(StopTimes.stop_sequence)
        for t in times:
            trips.append(model_to_dict(t))
        return trips

    @staticmethod
    def get_stops():
        return Stops.select(Stops.stop_name, Routes.route_id, Stops.stop_id, Stops.stop_lat, Stops.stop_lon).join(StopTimes).join(Trips).join(Routes).where(Routes.route_type == 2).group_by(Stops)

    @staticmethod
    def get_stops_from_origin(from_station):
        arr_init = Routes.select(Stops.stop_id, Stops.stop_name, Routes.route_id).distinct().join(Trips).join(StopTimes).join(Stops).where(Routes.route_type ==2, Stops.stop_id == from_station)
        arr_init = arr_init.alias('b')
        arrst = Stops.select(Stops, Routes.route_id).join(StopTimes).join(Trips).join(Routes).join(arr_init, on=(arr_init.c.route_id == Routes.route_id)).group_by(Stops.stop_name)
        return arrst