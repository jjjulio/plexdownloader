# !/usr/bin/env python3
import requests
import wget
import xml.etree.ElementTree as ET
import os
import webbrowser
import base64
import hashlib
import http.client
import json


class PlexMusicDownloader(object):
    plexUrl = 'http://trinity.usbx.me:11675'
    token = 'Typea5Ncd-aJ8yp8x1VV'
    downloadPath = '/home/julio/Music/'
    downloadPath = '/media/julio/M3/Artists/'

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

    def test(self):
        playlists = self.getPlaylists()
        for list in playlists:
            print(list.attrib)

    def showMenu(self):
        print("test")

    def getPlaylists(self):
        url = self.plexUrl + '/playlists?X-Plex-Token=' + self.token
        playlists = ET.fromstring(requests.get(url).text)
        return playlists

    def downloadPlaylist(self, idPlaylist):
        url = self.plexUrl + '/playlists/' + str(idPlaylist) + '/items?X-Plex-Token=' + self.token
        playlist = ET.fromstring(requests.get(url).text)
        total = len(playlist.findall('Track'))
        count = 1
        for track in playlist:
            # print(track.tag, track.attrib)
            title = track.attrib.get('title')
            album = track.attrib.get('parentTitle')
            artist = track.attrib.get('grandparentTitle')

            key = track[0][0].attrib.get('key')
            downloadUrl = self.plexUrl + key + '?X-Plex-Token=' + self.token
            # print(downloadUrl)
            container = track[0].attrib.get('container')
            ext = ".flac"
            if container == 'flac':
                ext = '.flac'
            else:
                if container == 'mp4':
                    ext = '.m4a'
                else:
                    if container == 'mp3':
                        ext = '.mp3'
            dir = self.downloadPath + artist.replace("/", "-").replace(":", " -").replace("\\", "-").replace(":",
                                                                                                             "-").replace(
                "*", "x").replace("?", "").replace("\"", "").replace("<", "").replace(">", "").replace("|", "").replace(
                "¿", "") + '/'
            path = self.downloadPath + artist.replace("/", "-").replace(":", " -").replace("\\", "-").replace(":",
                                                                                                              "-").replace(
                "*", "x").replace("?", "").replace("\"", "").replace("<", "").replace(">", "").replace("|", "").replace(
                "¿", "") + '/' + title.replace("/", "-").replace(":", " -").replace("\\", "-").replace(":",
                                                                                                       "-").replace("*",
                                                                                                                    "x").replace(
                "?", "").replace("\"", "").replace("<", "").replace(">", "").replace("|", "").replace("¿", "") + ext
            if not os.path.exists(path):
                print('Downloading --->[' + str(count) + '/' + str(total) + ']\t' + path)
                try:
                    os.makedirs(dir)
                except:
                    pass
                #print(downloadUrl)
                wget.download(downloadUrl, out=path)
            else:
                print('Skipping --->\t' + path + '\t already downloaded')
            count += 1
