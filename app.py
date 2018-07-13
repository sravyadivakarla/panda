#pip install Flask
#pip install flask-googlemaps
#pipenv install requests
#pip install -U googlemaps




from flask import Flask, render_template, request
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import googlemaps
import requests

app = Flask(__name__)

GoogleMaps(app, key="AIzaSyAlCwhKJ0C8n4eFM-ioPC5-MCFYy4P-TT8")
gmaps = googlemaps.Client(key='AIzaSyBSm6H8S7sZic1Hfcdmm_ywyU0Mn6KmDU4')


@app.route('/', methods = ['POST'])
def my_form_post():
	first = request.form['firstname']
	last = request.form['lastname']
	first = first.upper()
	last = last.upper()
	url = "https://openpaymentsdata.cms.gov/resource/daa6-m7ef.json?physician_first_name=" + first +"&physician_last_name="+ last

	data = requests.get(url).json()

	address = data[0]["recipient_primary_business_street_address_line1"]+"," + data[0]["recipient_primary_business_street_address_line2"] + "," + data[0]["recipient_city"] + "," + data[0]["recipient_state"] + " " + data[0]["recipient_zip_code"]

	print (address)

	#find coordinates:
	geocode_result = gmaps.geocode(address)
	latitude = geocode_result[0]['geometry']['location']['lat']
	longitude =  geocode_result[0]['geometry']['location']['lng']
	print (latitude)
	print (longitude)
	sndmap = Map(
                identifier="sndmap",
                lat= latitude,
                lng= longitude,
                markers={'http://maps.google.com/mapfiles/ms/icons/green-dot.png':[(latitude,longitude)]}
        )
	return render_template('example.html', sndmap=sndmap)



@app.route("/")
def mapview():
	sndmap = Map(
		identifier="sndmap",
		lat= 36.7783,
		lng= 119.4179,
		markers={'http://maps.google.com/mapfiles/ms/icons/green-dot.png':[(36.7783,119.4179)]}
	)
	return render_template('example.html', sndmap=sndmap)


if __name__ == "__main__":
    app.run(debug=True)
