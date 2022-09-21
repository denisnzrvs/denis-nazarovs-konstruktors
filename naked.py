import requests
import json
import datetime
import time
import yaml

from datetime import datetime
from configparser import ConfigParser

# Explains what the programm does
print('Asteroid processing service')

# Initiating and reading config values
print('Loading configuration from file')

# NASA API configuration values

try:
		config = ConfigParser()
		config.read('config.ini')

		nasa_api_key = config.get('nasa', 'api_key')
		nasa_api_url = config.get('nasa', 'api_url')
	
except:
	logger.exception('')
print('DONE')

# Getting todays date, formatting it and printing message with date of request
dt = datetime.now()
request_date = str(dt.year) + "-" + str(dt.month).zfill(2) + "-" + str(dt.day).zfill(2)  
print("Generated today's date: " + str(request_date))

# Prints URL that the request is sent to, saves the request into varaiable 'r'
print("Request url: " + str(nasa_api_url + "rest/v1/feed?start_date=" + request_date + "&end_date=" + request_date + "&api_key=" + nasa_api_key))
r = requests.get(nasa_api_url + "rest/v1/feed?start_date=" + request_date + "&end_date=" + request_date + "&api_key=" + nasa_api_key)

# Prints info about recieved response from API
print("Response status code: " + str(r.status_code))
print("Response headers: " + str(r.headers))
print("Response content: " + str(r.text))

# if the valid response recieved successfully, it is processed
if r.status_code == 200:

	# Converts the response text into JSON format
	json_data = json.loads(r.text)

	# Arrays to store safe and dangerous asteroids
	ast_safe = []
	ast_hazardous = []

	# Stores the asteroid count (if it exists in the reponse) and prints it
	if 'element_count' in json_data:
		ast_count = int(json_data['element_count'])
		print("Asteroid count today: " + str(ast_count))

		# If there are near-earth objects for the date of request (today), they get processed one by one
		if ast_count > 0:
			for val in json_data['near_earth_objects'][request_date]:
				# Checks if the object is a potentially hazardous asteroid, and if needed data about it is included. Stores asteroid's name and URL, performs diameter checks
				if 'name' and 'nasa_jpl_url' and 'estimated_diameter' and 'is_potentially_hazardous_asteroid' and 'close_approach_data' in val:
					tmp_ast_name = val['name']
					tmp_ast_nasa_jpl_url = val['nasa_jpl_url']
					# Checks if diameter data is given in kilometers
					if 'kilometers' in val['estimated_diameter']:
						# If estimated diameter minimum and maximum values are given, they are rouded and stored for the asteroid
						if 'estimated_diameter_min' and 'estimated_diameter_max' in val['estimated_diameter']['kilometers']:
							tmp_ast_diam_min = round(val['estimated_diameter']['kilometers']['estimated_diameter_min'], 3)
							tmp_ast_diam_max = round(val['estimated_diameter']['kilometers']['estimated_diameter_max'], 3)
						else:
						# If there is no minumum and maxumum diameter data (in kilometers), corresponding variables are set to -2
							tmp_ast_diam_min = -2
							tmp_ast_diam_max = -2
					else:
						# If there is no diameter data (in kilometers), corresponding variables are set to -1
						tmp_ast_diam_min = -1
						tmp_ast_diam_max = -1

					# If a potentially hazardous asteroid is found, the variable indicates that it is hazardous
					tmp_ast_hazardous = val['is_potentially_hazardous_asteroid']

					# If  close approach data for the asteroid is not empty, date and time of approach is stored in multiple formats
					if len(val['close_approach_data']) > 0:
						if 'epoch_date_close_approach' and 'relative_velocity' and 'miss_distance' in val['close_approach_data'][0]:
							tmp_ast_close_appr_ts = int(val['close_approach_data'][0]['epoch_date_close_approach']/1000)
							tmp_ast_close_appr_dt_utc = datetime.utcfromtimestamp(tmp_ast_close_appr_ts).strftime('%Y-%m-%d %H:%M:%S')
							tmp_ast_close_appr_dt = datetime.fromtimestamp(tmp_ast_close_appr_ts).strftime('%Y-%m-%d %H:%M:%S')

							# If relative velocity data available, it gets stored
							if 'kilometers_per_hour' in val['close_approach_data'][0]['relative_velocity']:
								tmp_ast_speed = int(float(val['close_approach_data'][0]['relative_velocity']['kilometers_per_hour']))
							else:
								# If not available, variable set to -1
								tmp_ast_speed = -1 

							# If miss distance data available, it gets rounded and stored
							if 'kilometers' in val['close_approach_data'][0]['miss_distance']:
								tmp_ast_miss_dist = round(float(val['close_approach_data'][0]['miss_distance']['kilometers']), 3)
							else:
								# If not available, variable set to -1
								tmp_ast_miss_dist = -1
						# If close approach UNIX TS, speed and miss distance data is not available, corresponding values are set, allowing to interprete what data is missing.
						else:
							tmp_ast_close_appr_ts = -1
							tmp_ast_close_appr_dt_utc = "1969-12-31 23:59:59"
							tmp_ast_close_appr_dt = "1969-12-31 23:59:59"
					
					# If no close approach data at all is available, a message is printed, timestamps and other variables are set, allowing to interprete what data is missing. 
					else:
						print("No close approach data in message")
						tmp_ast_close_appr_ts = 0
						tmp_ast_close_appr_dt_utc = "1970-01-01 00:00:00"
						tmp_ast_close_appr_dt = "1970-01-01 00:00:00"
						tmp_ast_speed = -1
						tmp_ast_miss_dist = -1

					# Overview of the asteroid info is printed.
					print("------------------------------------------------------- >>")
					print("Asteroid name: " + str(tmp_ast_name) + " | INFO: " + str(tmp_ast_nasa_jpl_url) + " | Diameter: " + str(tmp_ast_diam_min) + " - " + str(tmp_ast_diam_max) + " km | Hazardous: " + str(tmp_ast_hazardous))
					print("Close approach TS: " + str(tmp_ast_close_appr_ts) + " | Date/time UTC TZ: " + str(tmp_ast_close_appr_dt_utc) + " | Local TZ: " + str(tmp_ast_close_appr_dt))
					print("Speed: " + str(tmp_ast_speed) + " km/h" + " | MISS distance: " + str(tmp_ast_miss_dist) + " km")
					
					# Adding asteroid data to the corresponding array
					if tmp_ast_hazardous == True:
						ast_hazardous.append([tmp_ast_name, tmp_ast_nasa_jpl_url, tmp_ast_diam_min, tmp_ast_diam_max, tmp_ast_close_appr_ts, tmp_ast_close_appr_dt_utc, tmp_ast_close_appr_dt, tmp_ast_speed, tmp_ast_miss_dist])
					else:
						ast_safe.append([tmp_ast_name, tmp_ast_nasa_jpl_url, tmp_ast_diam_min, tmp_ast_diam_max, tmp_ast_close_appr_ts, tmp_ast_close_appr_dt_utc, tmp_ast_close_appr_dt, tmp_ast_speed, tmp_ast_miss_dist])

		# If there are no near-earth objects for today (ast_count == 0), a message is printed
		else:
			print("No asteroids are going to hit earth today")

	# Amount of hazardous and safe asteroids are printed
	print("Hazardous asteorids: " + str(len(ast_hazardous)) + " | Safe asteroids: " + str(len(ast_safe)))

	# If there are hazardous asteroids in the array, it gets processed
	if len(ast_hazardous) > 0:

		# The array of hazardous asteroids is sorted by the timestamp of the closest approach
		ast_hazardous.sort(key = lambda x: x[4], reverse=False)

		#Prints summary of possible asteroid impacts today
		print("Today's possible apocalypse (asteroid impact on earth) times:")
		# Cycles through every hazardous asteroid and prints the local date and time of close approach, name and URL of the asteroid
		for asteroid in ast_hazardous:
			print(str(asteroid[6]) + " " + str(asteroid[0]) + " " + " | more info: " + str(asteroid[1]))

		# Sorts hazarous asteroids by the miss distance
		ast_hazardous.sort(key = lambda x: x[8], reverse=False)
		# Print name and miss distance of the closest hazardous asteroid, as well as its url
		print("Closest passing distance is for: " + str(ast_hazardous[0][0]) + " at: " + str(int(ast_hazardous[0][8])) + " km | more info: " + str(ast_hazardous[0][1]))
	# If the hazardous asteroids array is empty, message is printed
	else:
		print("No asteroids close passing earth today")

# If API response code is not 200 (request not successful), a message is printed with the response code and response text.

else:
	print("Unable to get response from API. Response code: " + str(r.status_code) + " | content: " + str(r.text))
