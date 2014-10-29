retail.csv:
csv file downloaded from https://health.data.ny.gov/Health/Food-Service-Establishment-Last-Inspection/cnih-y5dw filtered with only facility and zipcode showing and sorted by ascending zipcodes

outretail.csv:
Zipcodes and the number of facilities in them

retail.py
python 2.7 .py file which takes in a retail.csv file and creates an outretail.csv files. It ignores non integer values for zipcodes which may have been placed by mistake and deletes digits from the zipcode until there are 5.