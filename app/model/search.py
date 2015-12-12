from models import *
from playhouse.shortcuts import *

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
    def find_route(start_text, end_text):
        start_id=None
        end_id=None
        stations = self.get_stops()
        for s in stations:
            print s.stop_name
            if start_text.lower().strip()==s.stop_name.lower().strip():
                start_id = s.stop_id
        if start_id is None:
            return "Could not find from station " + start_text
        for s2 in stations:
            if end_text.lower().strip()==s2.stop_name.lower().strip():
                end_id = s2.stop_id
        if end_id is None:
            return "Could not find to station: " + end_text
    
       # st = StopTimes.select(StopTimes.departure_time).distinct().join(Trips).join(Routes).where(Routes.route_type==2, Trips.service_id.contains(datetime.datetime.today().strftime('%a')), StopTimes.stop==st_id).order_by(StopTimes.departure_time).asc()
        #THIS FINDS THE ROUTE BY JOINING WHERE TWO STATIONS INTERSCT
        
        sql = 'select DISTINCT t1.route_id, t1.stop_id,  t2.stop_id from (select route_id, \
         stop_id, trip_headsign from stop_times inner join trips on stop_times.trip_id = trips.trip_id \
         where stop_id="%s") t1,\
         (select route_id,  stop_id,trip_headsign from stop_times inner join trips on stop_times.trip_id =trips.trip_id \
         where stop_id="%s") t2 where t1.trip_headsign=t2.trip_headsign ;'
#   
        return "found!"

    @staticmethod
    def get_stops():
        return Stops.select(Stops.stop_name, Routes.route_id, Stops.stop_id).join(StopTimes).join(Trips).join(Routes).where(Routes.route_type == 2).group_by(Stops)

    @staticmethod
    def get_stops_from_origin(from_station):
        arr_init = Routes.select(Stops.stop_id, Stops.stop_name, Routes.route_id).distinct().join(Trips).join(StopTimes).join(Stops).where(Routes.route_type ==2, Stops.stop_name == from_station)
        arr_init = arr_init.alias('b')
        arrst = Stops.select(Stops, Routes.route_id).join(StopTimes).join(Trips).join(Routes).join(arr_init, on=(arr_init.c.route_id == Routes.route_id)).group_by(Stops.stop_name)
        return arrst