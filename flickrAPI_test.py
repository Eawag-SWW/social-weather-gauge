#
# download georeferenced photos from flickr.com
# with 'flood' tags
#
# Missing:
# - error handling!
# - unicode handling for umlaute, etc.
#
# September 28, 2012 -- Andreas Scheidegger
# =======================================================

import flickrapi
import flickrapi.shorturl
import urllib2                  # to download files

# -----------
# establish connection
# -----------
api_key = "84c43709db781dca1a88bf2feb04bc82"
ff = flickrapi.FlickrAPI(api_key)


# -----------
# get where-on-earth-ID of a place
# -----------

woeID_q = ff.places_find(query="copenhagen")
woeID_q[0].attrib
woeID = int(woeID_q[0][0].attrib['woeid']) # read the first woeid

# querry the XLM response
# print woeID_q[0].tag
# print woeID_q[0].attrib
# print woeID_q[0].attrib['total']

# print woeID_q[0][0].attrib
# print woeID_q[0][0].attrib['woeid']

# -----------
# search for pics
# -----------
# for more search options see here: http://www.flickr.com/services/api/flickr.photos.search.html
tags = "ueberschwemmung, Hochwasser, Flut, flood, flooding, flooded, deluge, inundation, oversvommelse, oversvommelser, oversvommet"
search_q = ff.photos_search(tags=tags, woe_id=woeID, accuracy=6)

# search in a circle instead of woeID, radios in [km]
# search_q = ff.photos_search(tags=tags,lat=46.767, lon=7.624, radius=30) # around Thun, CH

# print search_q[0].tag
# print search_q[0][0].attrib

# get number of results (limited to 50)
print search_q[0].attrib['total'] +  " Photos found"
n_pics = min(int(search_q[0].attrib['total']), 50)

# construct the urls of first 50 photos
pic_urls = []                   # empty list
for i in xrange(0, n_pics):
        # get photo infos
    photo_ID = search_q[0][i].attrib['id']
    farm_ID = search_q[0][i].attrib['farm']
    server_ID = search_q[0][i].attrib['server']
    secret = search_q[0][i].attrib['secret']

    print "------- "
    # print search_q[0][i].attrib['title'] # print title

    pic_url = "http://farm"+ farm_ID + ".static.flickr.com/" + server_ID + "/" + photo_ID + "_" + secret + "_b.jpg"
    pic_urls = pic_urls + [pic_url]  # add to list
    print pic_url

# -----------
# download files
# -----------

for i in xrange(0, len(pic_urls)):

    photo_file = urllib2.urlopen(pic_urls[i])

    output = open('downloads/photo_' + str(i) + '.jpg','wb')
    output.write(photo_file.read())
    output.close()

    print "Photo " + str(i+1) + " of " + str(len(pic_urls)) + " downloaded."

print "Done."
