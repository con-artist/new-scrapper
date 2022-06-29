import datetime
import location_news_website
import sendLogs
import extractNewsLocations
import sys


args = sys.argv
# path = args[1]
path = "C:/Users/Rajat/Desktop/aggregatr/"
todays_date = datetime.datetime.now().strftime("%d-%m-%y")
# print todays_date
# locations = os.listdir("locations_EPs/")
EPs = ["delhi_EPs", "jaipur_EPs", "bangalore_EPs", "mumbai_EPs"]
locations = [ep[:-4] for ep in EPs]
# print "first"
log_filename = location_news_website.main(todays_date, locations, path)
# print "scraping done"
extractNewsLocations.runNER(locations, path)
# print "NER done"
# sendLogs.send(log_filename, todays_date, path)
# print "mail sent"
