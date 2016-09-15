
"""
Copyright (C) 2016 by Wapack Labs Corporation
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""



import os
import urllib
import urllib2
import socket
from urllib import urlopen, quote
import json
import sys
import csv


#add your API key here
my_api_key = ''


#sample search terms..
#search for domains, emails, urls or IP addresses. For wildcards use '%', example - '%@mydomain.com'

search_terms = ['yandex.ru','mail.ru']

"""
#uncomment this section to read from file

input_file = "your_input_file.txt"
search_terms = []

with open(input_file) as infile:
    for line in infile:
        _next = line.lower().strip()
        search_terms.append(_next)
"""


def query_cyberwatch_api(url,search):
    try:
        response_str = urlopen(url)
        response_str = response_str.read().decode('utf-8')
        response = json.loads(response_str)
        return response
    except:
        print '[!]exception '+search+'.. check your query'
    


for search in search_terms:

    print '[+] searching on '+search+' ...'

    url = 'https://api.wapacklabs.com/cyberwatch/search?api_key='+my_api_key+'&term='+search
    response = query_cyberwatch_api(url,search)

    for r in response:
        dic = response[r]
        if type(dic) == dict:
            print '[+]hits for the following data sources..'
            for d in dic:
                print ' [-]'+d                
                for items in dic[d]:
                    if items == 'total':
                        print '   [-]'+str(dic[d][items])+' total hits'
                    if items == 'last_page':
                        print '   [-]'+str(dic[d][items])+ ' total pages of results'

            print '[+]writing results to CSV files..' 
            for d in dic:

                all_pages = dic[d]['last_page']
                next_url = dic[d]['next_page_url']
                data = dic[d]['data']
                #print 'all pages '+str(all_pages)
                    
                csv_file_name = search+'_'+d+'.csv'
                with open(csv_file_name, 'wb') as csvfile:
                    indicatorwriter = csv.writer(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)    
                    columns = []
                    print '     [-] writing all results to '+csv_file_name
                    print '     [-] getting column names.. '
                    for results in data[:1]:
                        for r in results:
                            columns.append(r)
                    indicatorwriter.writerow(columns)
                    print '             [-] processing page 1'
                    for results in data:
                        temp = []
                        for r in results:
                            temp.append(results[r])
                        try:
                            indicatorwriter.writerow(temp)
                        except:
                            pass
                    counter = 2
                    try:
                        while next_url.startswith('http'):
                            
                            response = query_cyberwatch_api(next_url,search)
                            for r in response:
                                dic2 = response[r]
                                if type(dic2) == dict:
                                    for d in dic2:
                                        print '             [-] processing page '+str(counter)
                                        counter += 1
                                        next_url = dic2[d]['next_page_url']
                                        data = data = dic2[d]['data']
                                        
                                        for results in data:
                                            temp = []
                                            for r in results:
                                                temp.append(results[r])
                                            #print temp
                                            try:
                                                indicatorwriter.writerow(temp)
                                            except:
                                                pass
                    except:
                        pass



                    



                    

        

                        


            





