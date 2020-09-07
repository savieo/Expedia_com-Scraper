#!/usr/bin/env python
# -*- coding: utf-8 -*-
# from dragline.runner import main
# from dragline.parser import HtmlParser
# from dragline.http import Request, RequestError
# try:
#     from . import settings
#     from .items import *
# except:
#     import settings
#     from items import *
# import re
# import os
# import csv
# import json
# import datetime
# from dragline.shell import view
from dragline.runner import main
from dragline.parser import HtmlParser
from dragline.http import Request, RequestError
import settings
from items import *
import json
from exceptions import ValueError
import os
import csv
import re
import datetime

class Spider:
    def __init__(self, *args, **kwargs):
        self.name = "2363_Expedia_com"
        self.start = "https://www.expedia.com/"
        self.allowed_domains = []

    def parse(self, response):

        parser = HtmlParser(response)
        todaysdate = datetime.date.today()
        for days in range(0,60):
            startdate = (todaysdate+datetime.timedelta(days=days)).strftime('%-m/%-d/%Y')
            checkindate = (todaysdate+datetime.timedelta(days=days)).strftime('%Y/%m/%d')
            enddate = (todaysdate+datetime.timedelta(days=days+1)).strftime('%-m/%-d/%Y')
            # startdate= '8/29/2018'
            # enddate = '8/30/2018'
            inputdata = csv.DictReader(open(os.path.join(os.path.dirname(__file__),'hotel_input.csv')))
            roomdata = {}
            nonavailablelist = []
            for inp in inputdata:
                if inp["property"]: 
                    url = inp["link"]+"&chkin=%s&chkout=%s"%(startdate,enddate)      
                if inp["room_id"]:    
                    roomdata[inp["room_id"]]  = {"hotel_name":inp["hotel_name"],"ID":inp["ID"],"property_id":inp["property_id"],"checkindate":checkindate,"saved":False}
                if not inp["room_id"]:
                    nonavailablelist.append({"hotel_name":inp["hotel_name"],"ID":inp["ID"],"property_id":inp["property_id"],"checkindate":checkindate})     
                if inp["lastcheck"]:
                    yield  Request(url,callback=self.parse_booking_page,meta={"roomdata":roomdata,"nonavailablelist":nonavailablelist})       
                    roomdata = {}
                    nonavailablelist = []
                

    def parse_booking_page(self,response):
        if response.status == 503 or response.status == 403:
            self.logger.warning("Blocked page url is %s,length is %d"%(response.url,len(response.text)))
            raise RequestError("Request Blocked")

        if len(response.text) < 2000 or response.status != 200:
            self.logger.warning("bad output.. url is %s"%(response.url))
            raise RequestError("Invalid Response")

        try:
            json_text = re.findall("roomsAndRatePlans\s?=\s?({.*})",response.text)
        except:
            raise RequestError("No Json data found")

        jsondata = json.loads(json_text[0])
        roomtypes = jsondata['rooms']
        if "Branson-Hotels-All-American-Inn-And-Suites.h23829" in response.url:
            if len(roomtypes) > 3:
                self.logger.warning("more romm types "+str(len(roomtypes)))
        offersjsonmatch = re.findall("offersData\s?=\s?({.*})",response.text)
        offersjson = json.loads(offersjsonmatch[0])
        roomdata = response.meta["roomdata"]
        collectedroomtypes = []
        for rtype in roomtypes: 
            roomtypeid = roomtypes[rtype]["roomTypeCode"]
            if roomtypeid in roomdata:
                #collectedroomtypes.append(roomtypename)
                hotelname = roomdata[roomtypeid]["hotel_name"]
                ID = roomdata[roomtypeid]["ID"]
                propertyid = roomdata[roomtypeid]["property_id"]
                checkindate = roomdata[roomtypeid]["checkindate"] 
                if "offers" in offersjson:
                    price_dict ={}
                    for ddata in offersjson["offers"]:
                        if ddata["roomTypeCode"] == roomtypeid:
                            if "price" in ddata and ddata["price"]:
                                price = ddata["price"]["displayPrice"]
                                raw_price = ddata.get('price')
                                displayDepositAmount = raw_price.get('displayDepositAmount','') if raw_price else None

                                breakfast = ddata.get("amenities")
                                breakfast_for2 = breakfast.get('2194') if breakfast else None

                                if ddata["nonRefundableOutsideWindow"]:
                                    rate_type1 = "Non-Refundable"
                                elif 'refundable' in ddata and not ddata["refundable"]:    
                                    rate_type1 = "Non-Refundable"
                                elif not ddata["nonRefundableOutsideWindow"] and not 'refundable' in ddata:
                                    rate_type1 = "Non-Refundable"
                                else:
                                    rate_type1 = ""

                                rate_type2 = ""

                                if ddata["paymentChoiceAvailable"]:
                                    rate_type2 = "Reserve now, pay when you stay"                                
                                elif breakfast_for2:
                                    rate_type2 = "breakfast included for 2"
                                elif ddata["agencyReserveNowPayLater"]:
                                    rate_type2 = "Reserve now, ay later"

                                if ddata["showETPDepositChoice"]:
                                	rate_type2 = "Reserve with deposit"

                                rate_type = rate_type1 +', '+ rate_type2
                                rate_type = rate_type.strip(', ') if rate_type else None 
                                dict_value = {price:rate_type}
                                price_dict.update(dict_value)
                    for pric in price_dict:
                        hoteldata = {"ID":ID,
                                     "property_id":propertyid,
                                     "hotel_name":hotelname,
                                     "check_in_date":checkindate,
                                     "price":pric,
                                     "rate_type":price_dict[pric],
                                     "url":response.url,
                                     }

                        roomdata[roomtypeid]["saved"] = True
                        # yield Hoteldata(**hoteldata) 
                        Hoteldata(**hoteldata).save()

        for roomtypeid in roomdata:
            if not roomdata[roomtypeid]["saved"]:
                hotelname = roomdata[roomtypeid]["hotel_name"]
                ID = roomdata[roomtypeid]["ID"]
                propertyid = roomdata[roomtypeid]["property_id"]
                checkindate = roomdata[roomtypeid]["checkindate"]
                price = "na"
                rate_type = ""
                hoteldata = {"ID":ID,
                         "property_id":propertyid,
                         "hotel_name":hotelname,
                         "check_in_date":checkindate,
                         "price":price,
                         "rate_type":rate_type,
                         "url":response.url}
                # yield Hoteldata(**hoteldata) 
                Hoteldata(**hoteldata).save() 

        nonavailablelist = response.meta["nonavailablelist"]
        for nadata in nonavailablelist:
            hotelname = nadata["hotel_name"]
            ID = nadata["ID"]
            propertyid = nadata["property_id"]
            checkindate = nadata["checkindate"]
            price = "na"
            rate_type = ""
            hoteldata = {"ID":ID,
                         "property_id":propertyid,
                         "hotel_name":hotelname,
                         "check_in_date":checkindate,
                         "price":price,
                         "rate_type":rate_type,
                         "url":response.url}
            # yield Hoteldata(**hoteldata)
            Hoteldata(**hoteldata).save() 
    
    
if __name__ == '__main__':
    main(Spider, settings)
