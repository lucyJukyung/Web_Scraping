import requests
from bs4 import BeautifulSoup

URL = f"https://stackoverflow.com/jobs?q=python&sort=i"

def get_last_page():
  result = requests.get(URL)
  soup = BeautifulSoup(result.text, 'html.parser')
  pages = soup.find("div", {"class": "s-pagination"}).find_all('a')
  last_page = pages[-2].get_text(strip = True)
  return int(last_page) #change it to int because 'range' in extract_jobs does not take str value

def extract_job(html):
  title = html.find("h2", {"class":"fs-body3"}).string
  company, location = html.find("h3", {"class":"fc-black-700"}).find_all("span", recursive=False) #recursive=False = do not go in deep. 
  company = company.get_text(strip=True) 
  location = location.get_text(strip=True)
  job_id = html['data-jobid']

  return {'Title': title, "Company": company, "Location":location, "Apply_Link": f"https://stackoverflow.com/jobs/{job_id}"}
  

def extract_jobs(last_page):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping SO: Page: {page}")
    result = requests.get(f"{URL}&pg={page+1}") # +1 bc it starts from 0 without it. 
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("div", {"class":"-job"})
    for result in results:
      job = extract_job(result)
      jobs.append(job)
  
  return jobs  
  # print(result.status_code)

def get_jobs():
  last_page = get_last_page()
  jobs = extract_jobs(last_page)
  
  return jobs