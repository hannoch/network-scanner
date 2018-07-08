#!/usr/bin/env python
# coding=utf-8

import gevent
from gevent import monkey
monkey.patch_all()
from gevent import Greenlet
from gevent.queue import Queue

import os
import requests
import socket
import pythonwhois
import sys
import re
import time
import optparse
from urllib.parse import urlparse
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


sys.setrecursionlimit(10000)
tasks = Queue()


class web_eye(Greenlet):

    def __init__(self, url):
        Greenlet.__init__(self)
        self.target = url
        print(self.target)
        self.cms_list = set()

    def run(self):
        try:
            response = requests.get(self.target, timeout=15, verify=False)
            self.headers = response.headers
            self.content = response.content.decode("utf-8")

            gevent.spawn(self.read_config).join()
            gevent.joinall([
                gevent.spawn(self.get_whois, '1'),
                gevent.spawn(self.discern, '2'),
                gevent.spawn(self.discern, '3'),
                gevent.spawn(self.discern, '4'),
                gevent.spawn(self.discern, '5'),
                gevent.spawn(self.discern, '6'),
                gevent.spawn(self.discern, '7'),
                gevent.spawn(self.discern, '8'),
                gevent.spawn(self.discern, '9'),
                gevent.spawn(self.discern, '10'),
                gevent.spawn(self.discern, '11'),
            ])
        except Exception as e:
            print (e)
            return

    def read_config(self):
        mark_list = []
        config_file = open('config.txt', 'r')
        for mark in config_file:
            # remove comment, group, blank line
            if re.match(r"\[.*?\]|^;", mark) or not mark.split():
                continue
            name, location, key, value = mark.strip().split("|", 3)
            mark_list.append([name, location, key, value])
        config_file.close()
        for mark_info in mark_list:
            tasks.put_nowait(mark_info)

    def discern(self, number):
        while not tasks.empty():
            mark_info = tasks.get()
            name, discern_type, key, reg = mark_info
            
            if discern_type == 'headers':
                self.discern_from_header(name, discern_type, key, reg)
            elif discern_type == 'index':
                self.discern_from_index(name, discern_type, key, reg)
            elif discern_type == "url":
                self.discern_from_url(name, discern_type, key, reg)
            else:
                pass
            gevent.sleep(0)

    def discern_from_header(self, name, discern_type, key, reg):
        if "Server" in self.headers:
            self.cms_list.add("Server:"+self.headers["Server"])
        if "X-Powered-By" in self.headers:
            self.cms_list.add("X-Powered-By:"+self.headers["X-Powered-By"])
        if key in self.headers and (re.search(reg, self.headers[key], re.I)):
            self.cms_list.add(name)
        else:
            pass

    def discern_from_index(self, name, discern_type, key, reg):
        if re.search(reg, self.content, re.I):
            self.cms_list.add(name)
        else:
            pass

    def discern_from_url(self, name, discern_type, key, reg):
        try:
            result = requests.get(self.target + key, timeout=15, verify=False)
            # time.sleep(0.5)
            if re.search(reg, result.content, re.I):
                self.cms_list.add(name)
            else:
                pass
        except Exception as e:
            # print (e)
            pass

    def get_whois(self,name):
        try:
            domain = urlparse(self.target).netloc
        
            # if domain is ip,stop querying domain.
            result1 = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",domain)
            if result1:
                return
            # remove port
            result2 = re.search(r"\:\d{1,5}$",domain)
            if result2:
                domain = domain.split(":")[0]
                
            # get domain's ip
            try:
                ip = socket.gethostbyname(domain)
                self.cms_list.add("IP:"+ip)
            except Exception as e:
                # print e
                pass

            if re.match(r"^www\.",domain):
                domain = domain.strip("www.") 
            who = pythonwhois.get_whois(domain)

            # get whois
            if who["contacts"]["registrant"]["name"] is not None:
                self.cms_list.add("Domain_User:"+who["contacts"]["registrant"]["name"].encode("utf8"))
            if who["contacts"]["registrant"]["email"] is not None:
                self.cms_list.add("Domain_Email:"+who["contacts"]["registrant"]["email"].encode("utf8"))
            if who["contacts"]["registrant"]["phone"] is not None:
                self.cms_list.add("Domain_Phone:"+who["contacts"]["registrant"]["phone"].encode("utf8"))
            if who["registrar"] is not None:
                self.cms_list.add("Domain_Registrar:"+who["registrar"][0].encode("utf8"))
            if who["nameservers"] is not None:
                name_servers=[]
                for i in who["nameservers"]:
                    name_servers.append(i.encode('UTF8'))
                self.cms_list.add("Domai_name_servers:"+str(name_servers).encode("utf8"))
        except Exception as e:
            # print e
            pass

'''
def main():
    url = 'http://192.168.74.135'
    if url:
        res = web_eye(url)
        res.run()
        cms = list(res.cms_list)
        print (cms)
    else:
        sys.exit(0)

if __name__ == '__main__':
    main()
'''
