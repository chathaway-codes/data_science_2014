import csv
import math
import xlsxwriter

#Loading the .csv file
f = open('Student_Weight_Status_Category_Reporting_Results__Beginning_2010.csv');
Data = csv.reader(f)

#helper function
def total_student_count(N_obese_over , pct_obese_over):
    if pct_obese_over == 0:
	  return 0
    return round((N_obese_over/pct_obese_over))

#helper function which handles division by zero
def division(N , M):
    if M == 0:
	  return 0
    return N/M

#Dictionary to store zip code data
zip_codes = {}
current_zip = 0

#counter to count the number of rows in the .csv file with blank zip codes
blank_zips = 0

#looping over the rows
for col in Data:
   if col[16] == '':                 #if a zip code is blank continue
      blank_zips = blank_zips + 1
      continue
   if col[0] == 'LOCATION CODE':     #ignore the first row with the headers
      continue
   for j in range(1 , 11):           #set blank slots as zero values
      if col[j] == '':
         col[j] = 0.0
   current_zip = col[16]       
   if col[16] not in zip_codes.keys():  #if the zip code has not been added to the dictionary
      zip_codes[current_zip] = []
      zip_codes[current_zip].append(current_zip)
      if col[10] != 0.0:
        zip_codes[current_zip].append(total_student_count(float(col[9]) , float(col[10][:-1])/100))
      if col[10] == 0.0:
	    zip_codes[current_zip].append(total_student_count(float(col[9]) , col[10])*100)
      zip_codes[current_zip].append(float(col[7]))
      zip_codes[current_zip].append(division(float(zip_codes[current_zip][2]) , float(zip_codes[current_zip][1]))*100)
      zip_codes[current_zip].append(float(col[5]))
      zip_codes[current_zip].append(division(float(zip_codes[current_zip][4]) , float(zip_codes[current_zip][1]))*100)
      zip_codes[current_zip].append(1)
   else:                               #if the zip code has been added to the dictionary
    if col[10] != 0.0:
      zip_codes[current_zip][1] = zip_codes[current_zip][1] + (total_student_count(float(col[9]) , float(col[10][:-1])/100))
    if col[10] == 0.0:
	  zip_codes[current_zip][1] = zip_codes[current_zip][1] + (total_student_count(float(col[9]) , col[10])*100)
    zip_codes[current_zip][2] = zip_codes[current_zip][2] + float(col[7])
    zip_codes[current_zip][4] = zip_codes[current_zip][4] + float(col[5])
    zip_codes[current_zip][3] = division(float(zip_codes[current_zip][2]) , float(zip_codes[current_zip][1]))*100
    zip_codes[current_zip][5] = division(float(zip_codes[current_zip][4]) , float(zip_codes[current_zip][1]))*100
    zip_codes[current_zip][6] = zip_codes[current_zip][6] + 1


#sorting the keys
keylist = zip_codes.keys()
keylist.sort()

#calculating the total number of rows in the .csv file with valid (non-blank) zip codes
total = 0
for key in keylist:
    print zip_codes[key]
    total = total + zip_codes[key][6]

#creating an Excel file for the output
excel_output = xlsxwriter.Workbook('BMI_Data.xlsx')
output_sheet = excel_output.add_worksheet()
column_headers = ['ZIP CODE' , 'NO. STUDENTS' , 'NO. OBESE' , '% OBESE' , 'NO. OVERWEIGHT' , '% OVERWEIGHT' , 'NO OF ROWS']
row = 0
col = 0
for item in column_headers:
   output_sheet.write(row,  col, item)
   col = col + 1

row = row + 1

for key in keylist:
   for j in range(0,7):
     output_sheet.write(row,  j, zip_codes[key][j])
   row = row + 1

#new sheet with additional data   

output_sheet = excel_output.add_worksheet()
output_sheet.write(0 , 0 , 'VALID ROWS')
output_sheet.write(1 , 0 , total)
output_sheet.write(0 , 1 , 'BLANK ZIP CODE ROWS')
output_sheet.write(1 , 1 , blank_zips)
output_sheet.write(0 , 2 , 'TOTAL')
output_sheet.write(1 , 2 , total + blank_zips)
output_sheet.write(0 , 3 , 'VALID ZIPS')
output_sheet.write(1 , 3 , len(zip_codes))

excel_output.close()
