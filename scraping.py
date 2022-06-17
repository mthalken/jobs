import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import selenium
from selenium.webdriver.support.ui import WebDriverWait
import os
import urllib

def find_jobs(website, job_title, location, desired_char, filename = 'results.xls'):
    
    if website == 'Indeed':
        job_soup = load_indeed_jobs_div(job_title, location)
        jobs_list, num_listings = extracted_info_indeed(job_soup, desired_char)
        
    # add other job boards
    
    save_jobs(jobs_list, filename)
    
def save_jobs(jobs_list, filename):
    jobs = pd.DataFrame(jobs_list)
    jobs.to_excel(filename)
    
# create function to search indeed
def load_indeed_jobs_div(job_title, location):
    getVars = {'q': job_title, 'l': location, 'fromage': 'last', 'sort': 'date'}
    url = ('https://www.indeed.com/jobs?' + urllib.parse.urlencode(getVars))
    page = requests.get(url)
    soup = bs(page.content, 'html.parser')
    job_soup = soup.find(id = 'resultsCol')
    return job_soup

def extracted_info_indeed(job_soup, desired_char):
    job_elems = job_soup.find_all('td', class_='resultsContent')
    
    cols = []
    extracted_info = []

    if 'titles' in desired_char:
        titles = []
        cols.append('titles')
        for job_elem in job_elems:
            titles.append(job_title_indeed(job_elem))
        extracted_info.append(titles)

    if 'companies' in desired_char:
        companies = []
        cols.append('companies')
        for job_elem in job_elems:
            companies.append(company_indeed(job_elem))
        extracted_info.append(companies)

    if 'links' in desired_char:
        links = []
        cols.append('links')
        for job_elem in job_elems:
            links.append(link_indeed(job_elem))
        extracted_info.append(links)

    if 'date_listed' in desired_char:
        dates = []
        cols.append('date_listed')
        for job_elem in job_elems:
            dates.append(date_indeed(job_elem))
        extracted_info.append(dates)
        
    jobs_list = {}

    for j in range(len(cols)):
        jobs_list[cols[j]] = extracted_info[j]

    num_listings = len(extracted_info[0])
    
    return jobs_list, num_listings
#     print('{} new job postings retrieved. Stored in {}.'.format(num_listings, filename))
    
def job_title_indeed(job_elem):
    title_elem = job_elem.find('h2', title_='title')
    title = title_elem.text.strip()
    return title

def company_indeed(job_elem):
    company_elem = job_elem.find('span', class_='company')
    company = company_elem.text.strip()
    return company

def link_indeed(job_elem):
    link = job_elem.find('a')['href']
    link = 'www.indeed.com/' + link
    return link

def date_indeed(job_elem):
    date_elem = job_elem.find('span', class_='date')
    date = date_elem.text.strip()
    return date