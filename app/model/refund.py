import time
from splinter import Browser

class Refund:

    @staticmethod
    def make_refund(pc_number, email, travel_date, from_station, to_station, travel_time) :
      #browser = Browser()
      browser = Browser('phantomjs')
      browser.visit('https://secure.gotransit.com/en/serviceguarantee/eligibility.aspx')

      print "Selecting date ..."
      datepicker = browser.execute_script("$('#ui-datepicker-div').find('a.ui-state-default').filter(function(i){return $(this).text() === '"+travel_date+"';}).click();")
      time.sleep(1)
      print "Selecting departure station ..."
      browser.execute_script("$('#departureStationDropDownList input').click();")
      browser.execute_script("$('#ui-id-1 li').filter(function(){ return $(this).text() == $('#departureStationDropDownList select option').filter(function(){return $(this).val() === '"+from_station+"'}).text(); }).click();");
      time.sleep(1)
      print "Selecting arrival station ..."
      browser.execute_script("$('#parentArrivalStations input').click();")
      browser.execute_script("$('#ui-id-2 li').filter(function(){ return $(this).text() == $('#parentArrivalStations select option').filter(function(){return $(this).val() === '"+to_station+"'}).text(); }).click();");
      time.sleep(1)
      print "Selecting departure time ..."
      browser.execute_script("$('#parentScheduledTime input').click();")
      browser.execute_script("$('#ui-id-3 li').filter(function(){ return $(this).text() == $('#parentScheduledTime select option').filter(function(){return $(this).text() === '"+travel_time+"'}).text(); }).click();");
      time.sleep(1)
      print "Checking if trip qualifies ..."
      browser.find_by_name('ctl00$ContentPlaceHolder1$btnQualifyTrip').first.click()

      time.sleep(2)

      if len(browser.find_link_by_text('Service Guarantee')) == 4:
            print "TRIP QUALIFIES ... continuing ..."
            print "Appending querystring to URL for ease ..."
            browser.execute_script("var _href=$('#disclaimerText').find('a').attr('href'); $('#disclaimerText').find('a').attr('href', _href + '&render=min')")
            print "Proceeding to complete claim ... "
            browser.find_by_id('disclaimerText').find_by_tag('a').first.click()
            time.sleep(4)

            print "Click next to dismiss first screen ... "
            browser.find_by_id('ctl00_m_WebPartClaimRequisition_ctl00_buttonNextInTrip').first.click()
            print "Click next to dismiss first screen ... DONE"
            time.sleep(1)
            print "Check privacy policy box ... "
            browser.check('ctl00$m$WebPartClaimRequisition$ctl00$checkBoxPrivacyStatement')
            print "Entering PRESTO card number ... "
            browser.find_by_name('ctl00$m$WebPartClaimRequisition$ctl00$textboxPrestoCardInput').fill(pc_number)
            print "Bypass CAPTCHA ..."
            browser.execute_script("$('#contentStep2').hide(); $('#contentStep3').show()")
            print "Entering Email ..."
            browser.find_by_name('ctl00$m$WebPartClaimRequisition$ctl00$textboxEmail').fill(email)
            print "Entering Email again ..."
            browser.find_by_name('ctl00$m$WebPartClaimRequisition$ctl00$textboxEmailConfirmation').fill(email)
            print "Submitting claim ..."
#            #browser.find_by_name('ctl00$m$WebPartClaimRequisition$ctl00$buttonSubmitClaim').first.click()

      else:
            print "TRIP DOES NOT QUALIFY. END."
            return browser.find_by_id('disclaimerText').find_by_tag('span').first.value;