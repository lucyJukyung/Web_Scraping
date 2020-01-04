import csv

def save_to_file(jobs):
  file = open("jobs.csv", mode="w")
  writer = csv.writer(file)
  writer.writerow(["title", "company", "location", "link"])
  for job in jobs:
    writer.writerow(list(job.values())) #.values() getting only values without 'title', 'location'... so on. but this is dict-values so need to change them to 'list' value
  return 