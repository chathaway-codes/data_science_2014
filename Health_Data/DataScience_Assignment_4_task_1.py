#BMI Data from the Excel Sheet
import math
import xlrd
import xlsxwriter

def total_student_count(N_obese_over , pct_obese_over):
    return int((N_obese_over/pct_obese_over))
	
BMI_Data = xlrd.open_workbook('Student_Weight_Status_Category_Reporting_Results__Beginning_2010.xlsx')
sheet = BMI_Data.sheet_by_index(0)
zipValues = sheet.col_values(16,start_rowx=1, end_rowx=None)
current_zip = 0
zip_codes = {}
corrupted_values = []
blank_zip_codes = []
for i in range(0 , len(zipValues)):
    if zipValues[i] != current_zip:
	   current_zip = zipValues[i]
	   try:
	     zip = int(current_zip)
	   except ValueError:
	     blank_zip_codes.append(current_zip)
	     continue
	   zip_codes[zip] = []
	   zip_codes[zip].append(int(current_zip))
	   zip_codes[zip].append(0.0)
	   zip_codes[zip].append(0.0)
	   zip_codes[zip].append(0.0)
	   zip_codes[zip].append(0.0)
	   zip_codes[zip].append(0.0)
	   k = i
	   flag = 0
	   while zipValues[k] == current_zip:
	    try:
	   	  zip_codes[zip][1] = zip_codes[zip][1] + total_student_count(float(sheet.cell_value(k+1,9)) , float(sheet.cell_value(k+1,10)))
		  zip_codes[zip][2] = zip_codes[zip][2] + float(sheet.cell_value(k+1,7))
		  zip_codes[zip][4] = zip_codes[zip][4] + float(sheet.cell_value(k+1,5))
	    except ValueError:
		  flag = 1
	    k = k+1
	   if flag == 1:
	    corrupted_values.append(zip)
	    del zip_codes[zip]
	    continue
	   zip_codes[zip][3] = (zip_codes[zip][2]/zip_codes[zip][1])*100
	   zip_codes[zip][5] = (zip_codes[zip][4]/zip_codes[zip][1])*100
	   print zip_codes[zip]
	

excel_output = xlsxwriter.Workbook('BMI_Data.xlsx')
output_sheet = excel_output.add_worksheet()
column_headers = ['ZIP CODE' , 'NO. STUDENTS' , 'NO. OBESE' , '% OBESE' , 'NO. OVERWEIGHT' , '% OVERWEIGHT']
row = 0
col = 0
for item in column_headers:
   output_sheet.write(row,  col, item)
   col = col + 1

row = row + 1

for key , values in zip_codes.items():
   for j in range(0,6):
     output_sheet.write(row,  j, values[j])
   row = row + 1

row = 0
col = 0
output_sheet = excel_output.add_worksheet()
output_sheet.write(row , col , 'CORRUPTED ZIP CODES')
row = row + 1
for r in range(0 , len(corrupted_values)):
    output_sheet.write(row , col , corrupted_values[r])
    row = row + 1

row = 0
col = 0
output_sheet = excel_output.add_worksheet()
output_sheet.write(row , col , 'NO. BLANK ZIP CODES')
row = row + 1
output_sheet.write(row , col , len(blank_zip_codes))
   
	
excel_output.close()
    
		  
	   
       	   


   
  
