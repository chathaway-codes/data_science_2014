import csv
import collections
zips = collections.defaultdict(int)

with open('outretail.csv', 'wb') as outcsv:   
    with open('retail.csv', 'rb') as incsv:
        writer = csv.writer(outcsv)
        reader = csv.reader(incsv)
        for row in reader:
            if (row[1].isdigit()): #takes care non integer zip codes like spaces, nothing, or mistakenly put data
                number_string = str(row[1])
                zips[number_string[:5]]+=1 #takes care of lines with zip codes bigger than 5
        z = collections.OrderedDict(sorted(zips.items(), key=lambda t: t[0]))
        for key,value in z.iteritems():
           writer.writerow([key, value])

                    

