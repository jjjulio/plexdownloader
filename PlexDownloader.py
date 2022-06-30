import requests
import wget
import xml.etree.ElementTree as ET
import os
import webbrowser
import base64
import hashlib
import http.client
import json
import re

class plexDownloader(object):
    token = 'Typea5Ncd-aJ8yp8x1VV'
    downloadPath = "/home/julio/series/"
    serverUrl = "https://5699.krylabz.xyz/"


    def login(self):
        if os.path.isfile("./plex_token.json"):
            with open('plex_token.json') as json_file:
                data = json.load(json_file)
                print(data)
                self.token = data['user']['authentication_token']
            print("Token Loaded: " + self.token)
            return
        username = input('Username: ')
        password = input('Password: ')
        client_name = input('Client Name: ')
        client_version = input('Client Version: ')
        client_id = hashlib.sha512('{} {}'.format(client_name, client_version).encode()).hexdigest()
        base64string = base64.b64encode('{}:{}'.format(username, password).encode())
        headers = {'Authorization': 'Basic {}'.format(base64string.decode('ascii')),
                   'X-Plex-Client-Identifier': client_id,
                   'X-Plex-Product': client_name,
                   'X-Plex-Version': client_version}

        conn = http.client.HTTPSConnection('plex.tv')
        conn.request('POST', '/users/sign_in.json', '', headers)
        response = conn.getresponse()
        print(response.status, response.reason)
        data = json.loads(response.read().decode())
        print('Auth-Token: {}'.format(data['user']['authentication_token']))
        conn.close()
        with open('plex_token.json', 'w') as outfile:
            json.dump(data, outfile)
        self.token = data['user']['authentication_token']

    def getSections(self):
        print("+---------------------------------------------------------+\nSections available:\n")
        list = requests.get(self.serverUrl + "library/sections" + "?X-Plex-Token=" + self.token).text
        sections = []
        count = 0
        for section in list.split('\n'):
            if "key" in section:
                sections.append(re.sub(r'agent.*', '', re.sub(r'.*key','key',section)))
                print(sections[count])
                count += 1
        viewdetails = ""
        while viewdetails != 'y' and viewdetails != 'n':
            viewdetails = input('do You want to get items on section? (y/n): ')
        if viewdetails == 'y':

            selected = False
            while not selected:
                key = input('Select one of keys values above (ex key="27" imput 27): ')
                for section in sections:
                    value = "key=\"" + key + "\""
                    if value in section:
                        selected = True
                        print("Section selected: " + key)
                        self.getItems(section)
                        break

    def getItems(self, section):
        print(section)
        if 'type="show"' in section:
            key = re.sub(r'\".*', '', re.sub(r'.*key=\"', '', section))
            list = requests.get(self.serverUrl + "library/sections/" + key + "/all?X-Plex-Token=" + self.token).text
            print(list)

            count = 0
            items = []
            for item in list.split('\n'):
                if "key" in item:
                    items.append(re.sub(r'.*key', 'key', item))
                    print(str(count) + " - " + re.sub(r'\".*', '', re.sub(r'.*title=\"', '', items[count])))
                    print(items[count])
                    count += 1
        if 'type="movie"' in section:
            key = re.sub(r'\".*', '', re.sub(r'.*key=\"', '', section))
            list = requests.get(self.serverUrl + "library/sections/" + key + "/all?X-Plex-Token=" + self.token).text
            print(list)
            count = 0
            items = []
            for item in list.split('\n'):
                if "Part id" in item:
                    items.append(re.sub(r'.*key', 'key', item))
                    print(str(count) + " - " + re.sub(r'.*\ file=\"', '', items[count]))
                    print(items[count])
                    count += 1


    def getSerie(self):
        list = requests.get(self.serverUrl + "library/metadata/1252014/allLeaves?X-Plex-Token=" + self.token).text
        files = []
        for item in list.split('\n'):
            if "Part id" in item:
                files.append(item)
                print(item)

    def downloadSerie(self, url):
        id = re.sub(r'&.*', '', re.sub(r'.*metadata%2F', '', url))
        list = requests.get(self.serverUrl + "library/metadata/" + id + "/allLeaves?X-Plex-Token=" + self.token).text
        files = []
        for item in list.split('\n'):
            if "Part id" in item:
                files.append(item)
                print(item)

    def getSeries(self):
        print(requests.get(self.serverUrl + "?X-Plex-Token=" + self.token).text)


    def getServers(self):
        print(requests.get(self.serverUrl + "servers" + "?X-Plex-Token=" + self.token).text)