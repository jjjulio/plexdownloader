# This is a sample Python script.
from PlexMusicDownloader import *
from PlexDownloader import *


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #PMD = PlexMusicDownloader()
    #PMD.downloadPlaylist(192005)
    #PMD.test()
    PD = plexDownloader()
    PD.login()
    #PD.getSections()
    #PD.getSerie()
    PD.downloadSerie('http://95.217.203.29:42428/web/index.html#!/server/782f9fbca6be116e6bfa72cee03099c1cfe01304/details?key=%2Flibrary%2Fmetadata%2F1252014&context=library%3Acontent.library~25~2')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

