from models import *

class TrainSearch:
    @staticmethod
    def find_closest(lat, lon):
        stops=  Stops.raw("SELECT stops.*, SQRT(POW(69.1 * (stop_lat - %s), 2) +POW(69.1 * (%s - stop_lon) * COS(stop_lat / 57.3), 2)) AS distance FROM stops inner join stop_times on (stop_times.stop_id = stops.stop_id)  \
        inner join trips on (trips.trip_id = stop_times.trip_id) inner join routes on (routes.route_id=trips.route_id) where routes.route_type=2 HAVING distance < 10 ORDER BY distance", lat, lon)
        for stop in stops:
            return model.to_dict(stop)
            break
        return None
    
    
    @staticmethod
    def find_route(start_text, end_text):
        start_id=None
        end_id=None
        stations = Stops.select().join(StopTimes, on=(StopTimes.stop_id == Stops.stop_id)).join(Trips, on=(Trips.trip_id == StopTimes.trip_id)).join(Routes, on=(Routes.route_id==Trips.route_id)).where(Routes.route_type==2).group_by(Stops)
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
            
        return "found!"