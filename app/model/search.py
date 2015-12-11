from models import *

class TrainSearch:
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