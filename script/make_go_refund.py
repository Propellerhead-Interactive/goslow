import time
import datetime
from splinter import Browser
#browser = Browser('phantomjs')
browser = Browser('firefox')

browser.visit('https://serviceguarantee.gotransit.com/SitePages/FareGuarantee.aspx?render=min')
print browser.title

browser.find_by_name('ctl00$m$WebPartClaimRequisition$ctl00$textboxPrestoCardInput').fill('12341234123412345')
browser.execute_script("$('#contentStep1').hide(); $('#contentStep2').show()")
days = browser.find_by_css('#ctl00_m_WebPartClaimRequisition_ctl00_calendarTravelDate tr:not(:first-child) td a')

for d in days:
	print d['title']

browser.find_link_by_text('14').click()

print "=============="
time.sleep(1)

browser.execute_script('$("#ctl00_m_WebPartClaimRequisition_ctl00_dropdownlistDeparture").show();');
departures = browser.find_by_css('#ctl00_m_WebPartClaimRequisition_ctl00_dropdownlistDeparture option')

for e in departures:
	print e.text

browser.select('ctl00$m$WebPartClaimRequisition$ctl00$dropdownlistDeparture', 'AC')

print "=============="
time.sleep(2)

browser.execute_script('$("#ctl00_m_WebPartClaimRequisition_ctl00_dropdownlistArrival").show();');

arrivals = browser.find_by_css('#ctl00_m_WebPartClaimRequisition_ctl00_dropdownlistArrival option')

for a in arrivals:
	print a.text

browser.select('ctl00$m$WebPartClaimRequisition$ctl00$dropdownlistArrival', 'UN')

print "=============="
time.sleep(1)

times = browser.find_by_css('#ctl00_m_WebPartClaimRequisition_ctl00_dropdownlistScheduledTime option')

for t in times:
	print t.text

browser.select('ctl00$m$WebPartClaimRequisition$ctl00$dropdownlistScheduledTime', 206)
browser.find_by_name('ctl00$m$WebPartClaimRequisition$ctl00$buttonNextInTrip').first.click()

time.sleep(1)
'''
browser.find_by_name('ctl00$m$WebPartClaimRequisition$ctl00$buttonSubmitClaim').first.click()

confirmation = browser.find_by_css('#detailsCard span');

for c in confirmation:
	print c.text
'''