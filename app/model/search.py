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
    def find_route(start_id, end_id, departure_date):
       
        end_id = end_id or False

        #THIS FINDS THE ROUTE BY JOINING WHERE TWO STATIONS INTERSCT
       # st = StopTimes.select(StopTimes.departure_time).distinct().join(Trips).join(Routes).where(Routes.route_type==2, Trips.service_id.contains(datetime.datetime.today().strftime('%a')), StopTimes.stop==st_id).order_by(StopTimes.departure_time).asc()
        
        #ALL OF THE TRAINS FROM OR TO GIVEN A DAY of wEEK
        #   

        #dow = datetime.datetime.today().weekday()
        
        
        #from trips - day of week
        #from stops - 
        # sts = db.execute_sql("select trips.trip_id, s1.departure_time, s1.stop_id from_stop_id, s2.stop_id to_stop_id, \
#         s2.arrival_time, trips.direction_id from stop_times s1 inner join \
#         trips on (trips.trip_id = s1.trip_id) inner join stop_times s2 on \
#         (trips.trip_id = s2.trip_id) join routes on (routes.route_id=trips.route_id) where routes.route_type=3 AND s1.stop_id=%s and s2.stop_id=%s AND trips.trip_id \
#         LIKE %s group by s1.departure_time order by s1.departure_time" , (start_id, end_id, "%"+days[dow]+"%"))
#

        final_list = []

        if end_id:
            sts = db.execute_sql("SELECT DISTINCT trips.trip_id, s1.departure_time,s2.arrival_time, s1.stop_id from_stop_id, \
            s2.stop_id to_stop_id from stop_times s1 inner join trips on \
            trips.trip_id=s1.trip_id inner join routes on routes.route_id=trips.route_id \
            inner join stop_times s2 on  (trips.trip_id = s2.trip_id) \
            INNER JOIN calendar_dates ON (trips.service_id = calendar_dates.service_id) \
            WHERE s1.stop_id=%s AND s2.stop_id=%s AND calendar_dates.date_timestamp = %s AND routes.route_type=2 \
            AND  s1.departure_time<s2.departure_time GROUP BY departure_time", (start_id, end_id, departure_date))

            for st in sts:
                sched = ComposedSchedule(st[0],st[1],st[2],st[3],st[4])
                final_list.append(sched.__dict__) 
        else:
            sts = db.execute_sql("SELECT DISTINCT trips.trip_id, s1.departure_time \
                            FROM stop_times s1 \
                            INNER JOIN trips ON (trips.trip_id = s1.trip_id) \
                            INNER JOIN stop_times s2 ON (s2.trip_id = trips.trip_id) \
                            INNER JOIN routes ON (trips.route_id = routes.route_id) \
                            INNER JOIN calendar_dates ON (trips.service_id = calendar_dates.service_id) \
                            WHERE s1.stop_id=%s \
                            AND routes.route_type = 2 \
                            AND calendar_dates.date_timestamp = %s \
                            AND s1.departure_time < s2.departure_time \
                            GROUP BY s1.departure_time", (start_id, departure_date))

            for st in sts:
                final_list.append({'trip_id': st[0], 'departure_time': st[1]})
        
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
    def get_stops_from_line(from_station):
        arr_init = Routes.select(Stops.stop_id, Stops.stop_name, Routes.route_id).distinct().join(Trips).join(StopTimes).join(Stops).where(Routes.route_type ==2, Stops.stop_id == from_station)
        arr_init = arr_init.alias('b')
        arrst = Stops.select(Stops, Routes.route_id).join(StopTimes).join(Trips).join(Routes).join(arr_init, on=(arr_init.c.route_id == Routes.route_id)).group_by(Stops.stop_name)
        return arrst

    @staticmethod
    def get_stops_from_origin(from_station, departure_date, departure_time):
        #arr_init = StopTimes.select(Trips.block_id).distinct().join(Trips).where(StopTimes.stop_id == from_station, StopTimes.departure_time == departure_time, Trips.trip_id.contains(departure_date))
        #arr_init = arr_init.alias('b')
        #arrst = Trips.select(StopTimes.stop_id, Stops.stop_name).join(StopTimes).join(Stops).where(Trips.block_id == '21A', Trips.trip_id.contains(departure_date), StopTimes.stop_id != from_station).group_by(StopTimes)
        
        final_list = []
        sts = db.execute_sql("SELECT stop_times.stop_id, stops.stop_name FROM trips \
                                INNER JOIN stop_times ON (stop_times.trip_id = trips.trip_id) \
                                INNER JOIN stops ON (stop_times.stop_id = stops.stop_id) \
                                INNER JOIN calendar_dates ON (trips.service_id = calendar_dates.service_id) \
                                INNER JOIN (SELECT trips.block_id, stop_times.departure_time, trips.direction_id FROM stop_times \
                                    INNER JOIN trips ON (trips.trip_id = stop_times.trip_id) \
                                    INNER JOIN calendar_dates on (calendar_dates.service_id = trips.service_id) \
                                    WHERE stop_id=%s \
                                    AND stop_times.departure_time = %s \
                                    AND calendar_dates.date_timestamp = %s) as phil on (phil.block_id = trips.block_id) \
                                WHERE calendar_dates.date_timestamp = %s \
                                and trips.direction_id = phil.direction_id \
                                and stop_times.departure_time > phil.departure_time \
                                GROUP BY stop_times.stop_id", (from_station, departure_time, departure_date, departure_date))

        for st in sts:
                final_list.append({'stop_id': st[0], 'stop_name': st[1]})

        return final_list