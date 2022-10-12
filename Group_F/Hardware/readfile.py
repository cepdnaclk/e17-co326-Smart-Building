import csv
with open("..\\Data\\simulation_data\\Plant_2_Time_vs_DCPower_Data.csv", 'r') as file:
  csvreader = csv.reader(file)
  for row in csvreader:
    print(row[0])
