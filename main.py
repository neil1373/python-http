import numpy as np
import json
import os
import requests
from getpass import getpass
from urllib import parse
from enum import Enum
from datetime import datetime
from collections import namedtuple

# Initialization: Setup iChamp Headers
ichamp_headers = {
    'Host':'ichamp.sgp.dbs.com:60443',
    'Connection':'keep-alive',
    'Cache-Control':'max-age=0',
    'Upgrade-Insecure-Requests':'1',
    'Origin':'null',
    'Content-Type':'application/x-www-form-urlencoded',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
    'Sec-Fetch-Dest':'document',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site':'same-origin',
    'Sec-Fetch-Mode':'navigate',
    'Sec-Fetch-User':'?1',
    'Accept-Encoding':'gzip,deflate,br',
    'Accept-Language':'en-US,en;q=0.9',
    'RequestedCRURLParam':'%2Fichamp%2FiChange%3FAction%3DGOAHEADANDLOGIN',
}

# Step 1: Send login request to iChamp
def send_requests(user, pwd):
    login_info = {
        'username':user,
        'password':pwd,
        'Action':'GoAheadAndLogIn'
    }
    login_data = parse.urlencode(login_info)
    login_response = requests.post('https://ichamp.sgp.dbs.com:60443/ichamp/iChange', 
        headers = ichamp_headers, 
        data = login_data, 
        verify = False
    )
    # print(login_response.cookies)
    return login_response.cookies

# Step 2: Send request and get list of all tickets with JSON format
def get_tickets(user_cookies):
    query_info = {
        'processfield':'AllOpenIncidents'
    }
    query_data = parse.urlencode(query_info)
    query_response = requests.post('https://ichamp.sgp.dbs.com:60443/ichamp/iChange/incident/dashboard', 
        headers = ichamp_headers, 
        data = query_data, 
        cookies = user_cookies, 
        verify = False
    )
    # print(query_response)
    json_data = json.loads(query_response.text)
    issues = []
    for x in json_data['data']:
        x['raw_data'] = x.copy()
        x['resource'] = 'iChamp'
        issues.append(namedtuple("ichamp", x.keys())(*x.values()))
    # return json_data['data']
    return issues

# Step 3: Filter with ticket no., state(status), and key word
class IChampField(Enum):
    ticketNo = 'TicketNo'
    age = 'Age'
    create_time = 'create_time'
    ticketOwner = 'TicketOwner'
    queue = 'Queue'
    summary = 'Summary'
    state = 'State'
    minute = 'Minute'
    resource = 'resource'

class FilterType(Enum):
    equal = 'equal'
    contains = 'contains' 

def filter(ticket_list, key: IChampField, value, condition: FilterType):
    return {
        FilterType.contains : [x for x in ticket_list if value in x.raw_data[key.value]],
        FilterType.equal : [x for x in ticket_list if value == x.raw_data[key.value]]
        # FilterType.contains : [x for x in ticket_list if value in x.IChampField(value)],
        # FilterType.equal : [x for x in ticket_list if x.key.value == value]
    }.get(condition, [])

def main():
    print("Welcome to iChamp command line query system.")
    username = input("Please enter your DBS account ID:")
    print ("(Note: The screen won't show your password.)")
    password = getpass("Please enter your DBS account password:")
    print(datetime.now())
    user_cookies = send_requests(username, password)
    issue_list = get_tickets(user_cookies)
    # Save new file is not suggested
    '''
    ichamp_ticket_file = open('ichamp-tickets.json', 'w', encoding = "utf-8")
    ichamp_ticket_file.write(ichamp_tickets)
    ichamp_ticket_file.close()
    source_file = open('ichamp-tickets.json', encoding="utf-8")
    json_data = json.load(source_file)
    '''
    print(datetime.now())
    # Testing
    print(issue_list[0].resource)
    print(filter(issue_list, IChampField.ticketNo,'IN202008068800770',FilterType.equal)[0].resource) # Search with ticket no.

    print(filter(issue_list, IChampField.summary,'Could not login',FilterType.contains)) # Search Title(summary)

    print(len(filter(issue_list, IChampField.state, 'In Progress', FilterType.equal))) # Filter with State

if __name__ == '__main__':
    main()
