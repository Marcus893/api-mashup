from geocode import getGeocodeLocation
import json
import httplib2

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = "NU2XZADRIKFHO11J3PERWFN4K1CIMUL1C112BHG5OQNSV4JO"
foursquare_client_secret = "H0ZVMFQX4YIMMREGQLYZHUOM4K3DK4F0WXO4URFO2HPOM11Q"


def findARestaurant(mealType,location):
	#1. Use getGeocodeLocation to get the latitude and longitude coordinates of the location string.
    geo = getGeocodeLocation(location)
    latitude = geo[0]
    longitude = geo[1]
	
	#2.  Use foursquare API to find a nearby restaurant with the latitude, longitude, and mealType strings.
	#HINT: format for url will be something like https://api.foursquare.com/v2/venues/search?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&v=20130815&ll=40.7,-74&query=sushi
    url = ("https://api.foursquare.com/v2/venues/search?client_id=%s&client_secret=%s&v=20130815&ll=%d,%d&query=%s" % (foursquare_client_id, foursquare_client_secret, latitude, longitude, mealType))

	#3. Grab the first restaurant
    h = httplib2.Http() 
    result = json.loads(h.request(url,'GET')[1])
    if result['response']['venues']:
        restaurant = result['response']['venues'][0]
        venue_id = restaurant['id']
        restaurant_name = restaurant['name']
        restaurant_address = restaurant['location']['formattedAddress']
        address = ""
        for i in restaurant_address:
            address += i + " "
        restaurant_address = address 
	#4. Get a  300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture
        url = ('https://api.foursquare.com/v2/venues/%s/photos?client_id=%s&v=20150603&client_secret=%s' % ((venue_id,foursquare_client_id,foursquare_client_secret)))
        result = json.loads(h.request(url, 'GET')[1])
	#5. Grab the first image
        if result['response']['photos']['items']:
            firstpic = result['response']['photos']['items'][0]
            prefix = firstpic['prefix']
            suffix = firstpic['suffix']
            imageURL = prefix + "300x300" + suffix 
	#6. If no image is available, insert default a image url
        else:
            imageURL = "http://pixabay.com/get/8926af5eb597ca51ca4c/1433440765/cheeseburger-34314_1280.png?direct"
	#7. Return a dictionary containing the restaurant name, address, and image url
        restaurantInfo = {'name': restaurant_name, 'address': restaurant_address, 'image': imageURL}
        print "Restaurant Name: %s" % restaurantInfo['name']
        print "Restaurant Address: %s" % restaurantInfo['address']
        print "Image: %s \n" % restaurantInfo['image']	
        return restaurantInfo 
    else:
        print "No Restaurant Found for %s" % location 
        return "No restaurant found"
        
if __name__ == '__main__':
	findARestaurant("Pizza", "Tokyo, Japan")
	findARestaurant("Tacos", "Jakarta, Indonesia")
	findARestaurant("Tapas", "Maputo, Mozambique")
	findARestaurant("Falafel", "Cairo, Egypt")
	findARestaurant("Spaghetti", "New Delhi, India")
	findARestaurant("Cappuccino", "Geneva, Switzerland")
	findARestaurant("Sushi", "Los Angeles, California")
	findARestaurant("Steak", "La Paz, Bolivia")
	findARestaurant("Gyros", "Sydney, Australia")