import time
from splinter import Browser

class Refund:

    @staticmethod
    def make_refund(pc_number, email, travel_date, from_station, to_station, travel_time) :
      browser = Browser()
      browser.visit('https://serviceguarantee.gotransit.com/SitePages/FareGuarantee.aspx?render=min')
      browser.find_by_name('ctl00$m$WebPartClaimRequisition$ctl00$textboxPrestoCardInput').fill(pc_number)
      browser.execute_script("$('#contentStep1').hide(); $('#contentStep2').show()")
      browser.find_link_by_text(travel_date).click()

      time.sleep(1)

      browser.execute_script('$("#ctl00_m_WebPartClaimRequisition_ctl00_dropdownlistDeparture").show();');
      browser.select('ctl00$m$WebPartClaimRequisition$ctl00$dropdownlistDeparture', from_station)

      time.sleep(2)

      browser.execute_script('$("#ctl00_m_WebPartClaimRequisition_ctl00_dropdownlistArrival").show();');

      browser.select('ctl00$m$WebPartClaimRequisition$ctl00$dropdownlistArrival', to_station)

      time.sleep(1)

      browser.select('ctl00$m$WebPartClaimRequisition$ctl00$dropdownlistScheduledTime', travel_time)
      browser.find_by_name('ctl00$m$WebPartClaimRequisition$ctl00$buttonNextInTrip').first.click()

      time.sleep(1)

      browser.find_by_name('ctl00$m$WebPartClaimRequisition$ctl00$textboxEmail').fill(email)
      browser.find_by_name('ctl00$m$WebPartClaimRequisition$ctl00$textboxEmailConfirmation').fill(email)

      #browser.find_by_name('ctl00$m$WebPartClaimRequisition$ctl00$buttonSubmitClaim').first.click()

      #return browser.find_by_css('#detailsCard span');