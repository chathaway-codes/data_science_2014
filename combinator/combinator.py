import csv
import sys

def main(argv):
  # Open each file
  data = []
  headers = ["zip_code"]
  for f_name in argv:
    with open(f_name, 'r') as csv_file:
      w = csv.reader(csv_file)
      headers_t = next(w, None)
      data_temp = {"file_name": f_name, "headers": headers_t, "data": []}

      for row in w:
        data_temp["data"] += [row]

      data += [data_temp]
  # With all data verify that everything has a ZIP code called "zip_code"
  for d in data:
    if "zip_code" not in d["headers"]:
      raise Exception("Error: no \"zip_code\" in header of %s" % d["file_name"])

  # Combine the data
  combined_data = {}
  for d in data:
    zip_code_index = d["headers"].index("zip_code")
    original_header_count = len(headers)
    headers += d["headers"][:zip_code_index] + d["headers"][zip_code_index+1:]
    added_headers = len(headers) - original_header_count
    updated_zip_codes = []
    for e in d["data"]:
      if e[zip_code_index] not in combined_data:
        # Fill in missing data values with nothing
        combined_data[e[zip_code_index]] = [""]*(original_header_count-1)
      combined_data[e[zip_code_index]] += e[:zip_code_index] + e[zip_code_index+1:]
      updated_zip_codes += [e[zip_code_index]]

    # Add empty spots for things
    for key, value in combined_data.iteritems():
      if key not in updated_zip_codes:
        value += [""]*added_headers

  # Spit back out the data
  csvwriter = csv.writer(sys.stdout, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
  # Write header
  csvwriter.writerow(headers)
  output_data = []
  for key, value in combined_data.iteritems():
    row = [key] + value
    output_data += [row]

  output_data = sorted(output_data, key=lambda a: a[0])
  for row in output_data:
    csvwriter.writerow(row)


if __name__ == "__main__":
  main(sys.argv[1:])
