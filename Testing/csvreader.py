import csv

temps = [(1, 'ds1855315', 25.58, 73.44),
         (2, 'ds1855315', 25.58, 73.44),
         (3, 'ds1855315', 25.58, 73.44)]

with open('log.csv','a+') as f:
    writer = csv.writer(f)
    writer.writerows(temps)

with open('log.csv','r', newline='\n') as f:
    reader = csv.reader(f)
    data = [tuple(row) for row in reader]

print(data)