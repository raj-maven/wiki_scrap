# from __future__ import unicode_literals

import cgi
import re
from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.response import FileResponse
from pyramid.view import view_config

from bs4 import BeautifulSoup
import urllib
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# Home view, available at http://127.0.0.1:6543
@view_config(route_name='home', renderer='templates/index.jinja2')
def home(request):
    return {'project': 'wiki_scrap'}

# result view
@view_config(route_name='result', renderer="templates/result.jinja2")
def result(request):
    if request.method == "POST":
        data = []
        error = ""
        url = request.POST['url']
        sub = ".wikipedia.org/wiki"

        # Get response status code of enterd url
        status_code = urllib.urlopen(url).getcode()

        # check status code and string content of url
        if (status_code == 200) & (sub in url):
            # Open the url and get its html content
            r = urllib.urlopen(url).read()
            soup = BeautifulSoup(r)
            try:
            	# find table of content in form soup html
                toc = soup.find(id="toc")

                # find numbers, text, and anchors value form table of content element
                tocnumbers = toc.find_all("span", class_="tocnumber")
                toctexts = toc.find_all("span", class_="toctext")
                anchors = toc.find_all('a')
                
                # pass data to store in a list 
                for i in range(len(tocnumbers)):
                    data.append({'number': tocnumbers[i].text,
                                'text': toctexts[i].text,
                                 'url': anchors[i]["href"]})
            except:
                error = "No 'Table of Content' in wikipedia Page"
        else:
            error = "Not a valid  wikipedia url"
        
        # write the screped data into csv file and save it
        with open('data.csv', 'w') as csvfile:
            fieldnames = ['#', 'Title', 'url']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for val in data:
                writer.writerow({'#': val['number'], 'Title': val['text'],
                                'url': url+val['url']})

    	return dict(data=data, error=error, url=url)
    else:
    	return dict(error="Please enter the Url first.")


# For downloading csv file 
@view_config(route_name='download')
def download(request):
    response = FileResponse('data.csv')
    response.headers['Content-Disposition'] = ("attachment; filename=Data.csv")
    return response
