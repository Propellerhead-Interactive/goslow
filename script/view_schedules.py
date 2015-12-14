import time
import datetime
import sys
sys.path.append( 'app/model/')
from models import db, Routes, Stops, StopTimes, Trips

db.connect()

#Get Starting Stations
#select s.stop_name from routes r inner join trips t on (r.route_id = t.route_id) inner join stop_times st on (st.trip_id = t.trip_id) inner join stops s on (s.stop_id = st.stop_id) where r.route_type=2 group by s.stop_name;

init = Stops.select(Stops.stop_name, Routes.route_id, Stops.stop_id).join(StopTimes).join(Trips).join(Routes)
init = init.alias('a')

depst = init.where(Routes.route_type == 2).group_by(Stops.stop_name)

for s in depst:
	print s.stop_name

print '============='
starting_from = raw_input("Please type in your origin station from the list above: ")
print '============='
#Get Arriving Stations based on above

arr_init = Routes.select(Stops.stop_id, Stops.stop_name, Routes.route_id).distinct().join(Trips).join(StopTimes).join(Stops).where(Routes.route_type ==2, Stops.stop_name == starting_from)
arr_init = arr_init.alias('b')
arrst = init.join(arr_init, on=(arr_init.c.route_id == Routes.route_id)).group_by(Stops.stop_name)

st_id = ""

print 'Thanks! Here are the stations you can go to from', starting_from
print '============='

for t in arrst:
	if t.stop_name.lower() == starting_from.lower():
		st_id = t.stop_id
	else :
		print t.stop_name

print '============='
ending_at = raw_input("Please type in your destination station from the list above: ")
print '============='


st = StopTimes.select(StopTimes.departure_time).distinct().join(Trips).join(Routes).where(Routes.route_type==2, Trips.service_id.contains(datetime.datetime.today().strftime('%a')), StopTimes.stop==st_id).order_by(StopTimes.departure_time).asc()

for s in st:
	print s.departure_time
