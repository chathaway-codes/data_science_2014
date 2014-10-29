import csv

r = csv.reader(open('Farmers_Markets_in_New_York_State.csv','r'))
fw = open('Farmers_Markets_by_zipcode.csv','w')
counts = dict()

for line in r:
	zip = line[6]
	if zip == 'Zip': continue
	if zip in counts.keys(): counts[zip]+=1
	else: counts[zip] = 1
	
fw.write('Zip,Num_farmersmarkets\n')
for zip in sorted(counts.keys()):
	fw.write(zip+','+str(counts[zip])+'\n')