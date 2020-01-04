import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = "https://au.indeed.com/jobs?q=python&l=Kew+VIC&limit=50&radius=50"

def extract_indeed_pages():
  result = requests.get (URL)

  soup = BeautifulSoup(result.text, "html.parser")

  pagination = soup.find("div", {"class":"pagination"})

  links = pagination.find_all("a")
  pages = []

  for link in links[:-1]: 
    pages.append(int(link.string))

  max_page = (pages[-1])
  return max_page

def extract_job(html):
  title = html.find("div", {"class": "title"}).find("a")["title"]
  company = html.find("span", {"class": "company"})
  location = html.find("span", {"class": "location"}).string
  job_id = html["data-jk"]

  if company is not None:
    c_anchor = company.find("a")
    if c_anchor is not None:
      company = c_anchor.string
    else:
      company = company.string
    company = company.strip() #strip("F") will remove 'F' from the first letter, strip() removes redundant spaces  
 
  # else:
  #   print("No company")

  return {
    'title': title, 
    'company': company, 
    'location': location, 
    'link': f"https://au.indeed.com/viewjob?jk={job_id}"}

def extract_indeed_jobs(last_page):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping Indeed: Page: {page}")
    result = requests.get(f"{URL}&start={page*LIMIT}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("div", {"class":"jobsearch-SerpJobCard"})
    for result in results:
      job = extract_job(result)
      jobs.append(job)
    #print(result.status_code)
  return jobs
    
def get_jobs():
  last_page = extract_indeed_pages()
  jobs = extract_indeed_jobs(last_page)
  return jobs