import urllib
import os
import hashlib

# non-absolute path is used for html generation, so changing this only would be unwise
cachedir = os.getcwd() + "/cache/"

if not os.path.exists(cachedir):
    os.makedirs(cachedir)


def loadToCache(imgurl):
    if imgurl == "NotFound":
        return "../resources/notfound.png"
    extension = imgurl.split(".")[-1].split("?")[0]
    url_hash = hashlib.md5(imgurl.encode("utf-8")).hexdigest()
    cacheFile = cachedir + url_hash + "." + extension

    if not os.path.isfile(cacheFile):
        try:
            urllib.request.urlretrieve(imgurl, cacheFile)
        except Exception: # pylint: disable=broad-except
            return "../resources/notfound.png"

    return "../cache/" + url_hash + "." + extension
