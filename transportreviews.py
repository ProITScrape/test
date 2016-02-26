
import csv
import requests
import time
import json
from bs4 import *


##############################################################################################################            
f= csv.writer(open("Datajson.csv", "w"))
listReviwes=[]
##############################################################################################################            

url="http://transportreviews.com/Reviews/NewestReviews/1-31-2016-to-2-7-2016/All/ShowPaid/All/100PerPage/"

##############################################################################################################            

page=requests.post(url)
soup=BeautifulSoup(page.text,"html5lib")
##############################################################################################################            
Reviews=soup.findAll('div', {'id':"Subject"})
print len(Reviews)
for review in Reviews:
    reviewLink="http://transportreviews.com"+review.find('a').get('href')
    print reviewLink
    pageReview=requests.get(reviewLink)
    soup=BeautifulSoup(pageReview.text,"html5lib")
    tabledata=soup.find("table",{'width':"100%", 'cellspacing':"0",'cellpadding':"3", 'border':"0"})
    Trs=tabledata.findAll("tr")
    for tr in Trs:
        Tds=tr.findAll('td')
        i=0
        for td in Tds:
            if "Poster:" in td.get_text():
                Poster=Tds[i+1].get_text().strip()
            if "Date:" in td.get_text():
                 Date=Tds[i+1].get_text().strip()
            if "Reviewed:" in td.get_text():
                 Reviewed=Tds[i+1].get_text().strip()
                 CompanyLink="http://transportreviews.com"+Tds[i+1].find('a').get("href")
            if "Subject:" in td.get_text():
                 Subject=Tds[i+1].get_text().strip()
            if "Review:" in td.get_text():
                 Review=str(Tds[i+1].get_text()).split('Review Options')
                 Review=Review[0]
            i=i+1   
##############################################################################################################            
    data2=soup.find("td", {'width':"30%" ,'valign':"top"}) 
    Stars=data2.find('div', {'align':"center"}).findAll('img')  
    rating=0
    for star in Stars:
        if star.get('src')=="/images/img_star_large_a.gif" :
            rating=rating+1   
        if star.get('src')=="/images/img_star_large_b.gif" :
            rating=rating+0
##############################################################################################################            
    tables=data2.findAll('table')
    table1=tables[0]
    Trstable1=table1.findAll('tr')
    for tr in Trstable1:
        Tdstable1=tr.findAll('td')
        i=0
        for td in Tdstable1:
            if 'Quote or Order ID:' in td.get_text():
                QuoteOrderID=Tdstable1[i+1].get_text().strip()
            if 'Quote or Order Cost:' in td.get_text():
                QuoteOrderCost=Tdstable1[i+1].get_text().strip()  
            i=i+1    
##############################################################################################################            
    table2=tables[1]        
    Trstable2=table2.findAll('tr')
    for tr in Trstable2:
        Tdstable2=tr.findAll('td')
        i=0
        for td in Tdstable2:
            if 'Origin:' in td.get_text():
                Origin=Tdstable2[i+1].get_text().strip()
            if 'Pickup:' in td.get_text():
               Pickup=Tdstable2[i+1].get_text().strip()  
            if 'Time from first available' in td.get_text():
               TimeFirstAvailableDate=Tdstable2[i+1].get_text().strip() 
            if 'Destination:' in td.get_text():
               Destination=Tdstable2[i+1].get_text().strip() 
            if 'Delivery:' in td.get_text():
               Delivery=Tdstable2[i+1].get_text().strip() 
            if 'Total Time from pickup' in td.get_text():
               TotalTimePickupToDeliveryVehicle=Tdstable2[i+1].get_text().strip() 
            i=i+1 
##############################################################################################################            
    table3=tables[2]  
    Trstable3=table3.findAll('tr')
    for tr in Trstable3:
        Tdstable3=tr.findAll('td')
        i=0
        for td in Tdstable3:
            if "Truck/Carrier Type:" in td.get_text():
                TruckCarrierType=Tdstable3[i+1].get_text().strip()
            if "Dirty:" in td.get_text():
                Dirty=Tdstable3[i+1].get_text().strip()
            if "Items Stolen:" in td.get_text():
                ItemsStolen=Tdstable3[i+1].get_text().strip()
            if "Damaged:" in td.get_text():
                Damaged=Tdstable3[i+1].get_text().strip()
            i=i+1
##############################################################################################################            
    HonestyRating="" 
    nowlegeableRating="" 
    HoldTimesPromptness="" 
    OverallCustomerService=""         
    if len(tables)>3:        
        table4=tables[3]
        Trstable4=table4.findAll('tr')
        for tr in Trstable4:
            Tdstable4=tr.findAll('td')
            i=0
            for td in Tdstable4:
                if 'Honesty:' in td.get_text():
                    ratingClass=Tdstable4[i+1].find("div").get('class')
                    HonestyRating=int(filter(str.isdigit, str(ratingClass[0])))
                if 'Knowlegeable:' in td.get_text():
                    ratingClass=Tdstable4[i+1].find("div").get('class')
                    KnowlegeableRating=int(filter(str.isdigit, str(ratingClass[0])))
                if 'Hold Times/Promptness:' in td.get_text():
                    ratingClass=Tdstable4[i+1].find("div").get('class')
                    HoldTimesPromptness=int(filter(str.isdigit, str(ratingClass[0])))
                if 'Overall Customer Service:' in td.get_text():
                    ratingClass=Tdstable4[i+1].find("div").get('class')
                    OverallCustomerService =int(filter(str.isdigit, str(ratingClass[0])))
                        
                i=i+1        
##############################################################################################################            
                          
    items={
      "Poster":Poster,
      "Date":Date,
      "Reviewed":Reviewed,
      "Subject":Subject,
      "Review":Review,
      "companyReviewdLink":CompanyLink,
      "ratingValue":rating,
      "ratingsValues":[
        {
          "HonestyRating":HonestyRating,
          "KnowlegeableRating":KnowlegeableRating,
          "HoldTimesPromptness":HoldTimesPromptness,
          "OverallCustomerService":OverallCustomerService
         }
       ],
      "Origin" :Origin,
      "Pickup":Pickup,
      "QuoteOrderID":QuoteOrderID,
      "QuoteOrderCost":QuoteOrderCost,
      "TimeFirstAvailableDate":TimeFirstAvailableDate,
      "Destination":Destination,
      "Delivery":Delivery,
      "TotalTimePickupToDeliveryVehicle":TotalTimePickupToDeliveryVehicle,
      "TruckCarrierType":TruckCarrierType,
      "Dirty":Dirty,
      "ItemsStolen":ItemsStolen,
      "Damaged":Damaged,
      "reviewlink":reviewLink
     } 
    
    listReviwes.append(items)
##############################################################################################################            
   
with open('Datajson.csv', 'w') as outfile:
    json.dump(listReviwes , outfile)

        
