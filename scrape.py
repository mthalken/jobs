import start_of_scrape
from start_of_scrape import find_jobs

desired_char = ['titles', 'companies', 'links', 'date_listed']

find_jobs('Indeed', 'data analyst', 'remote', desired_char)