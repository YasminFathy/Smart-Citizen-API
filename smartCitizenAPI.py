import requests
import constants
import threading
import os
import dateutil.parser
import datetime
from pymongo import MongoClient
__author__ = "Yasmin Fathy (Fathy.Yasmin@gmail.com)"


class smartCitizen(object):
	def __init__(self, url, access_token, drop_db=False):
		self.access_token = access_token
		self.response = self.get_response(url)
		# initialise mongodb access
		db_client = MongoClient(constants.MONGO_DB_ACCESS)

		# if drop_db, drop the existing db and create a new one
		if (drop_db):
			db_client.drop_database(db_client.Smart_Citizen_db)
			self.db_smartcitizen = db_client.Smart_Citizen_db
			self.db_smartcitizen_resourceregistry_collection = self.db_smartcitizen.ResourceRegistry
		else:
			self.db_smartcitizen = db_client.Smart_Citizen_db
			self.db_smartcitizen_resourceregistry_collection = self.db_smartcitizen.ResourceRegistry

	def get_response(self, url):
		try:
			if self.access_token is not None:
				response = requests.get(url+self.access_token)
				# check if the access is successfully
				if response.status_code == 200:
					#print("Response:")
					#for key, value in response.json().items():
					#	print([key, value])
					return response.json()
				else:
					print("Authentication Problem: Not 200 status code")
		except Exception as ex:
				print(ex)
				raise

	def get_devices_ids(self):
		try:
			if self.response is not None:
				ids_lst = []
				devices = self.response["devices"]
				for device in devices:
					ids_lst.append(device["id"])
					# sort all devices ascending
					ids_lst.sort()
				return ids_lst
		except Exception as ex:
				print(ex)
				raise

	def get_last_readings_sensors(self, devices_ids):
		try:
			for device_id in devices_ids:
				response = requests.get(constants.DEVICE_LAST_READINGS_ACCESS_URL+str(device_id))
				# check if data is retrieved successfully
				if response.status_code == 200:
					deviceID = constants.DEVICE_ID_DICT[str(device_id)]
					response_json = response.json()
					date_timestamp = response_json["last_reading_at"]
					if date_timestamp == None:
						date_timestamp = datetime.datetime.now().__str__()
					self._format_data(response_json["data"]["sensors"],date_timestamp,deviceID)
			# Run function continuously after 5 seconds
			threading.Timer(constants.TIME_INTERVAL, self.get_last_readings_sensors(devices_ids)).start()
		except Exception as ex:
			print(ex)
			raise

	# separate collections for each deviceID where the observations resourceID and timestamp will then be stored.
	def _write_observations_to_db(self, deviceID, observations):
		try:
			# e.g. deviceID = sc-si-sc-001
			if self.db_smartcitizen is not None:
				# get all collections from self.db_smartcitizen
				collection_names = self.db_smartcitizen.collection_names()
				# check if deviceID collection does not exist, create it
				if deviceID not in collection_names:
					deviceID_collection = self.db_smartcitizen[deviceID]
					deviceID_collection.insert(observations)
				# if deviceID collection exists, just add the observation
				else:
					self.db_smartcitizen[deviceID].insert(observations)
			else:
				print("There is a problem in connecting to db_smartcitizen")
		except Exception as ex:
				print(ex)
				raise

	# one collection for the resource registry - that is the properties that are generally static so
	# for example the resourceID, deviceID, location, platform etc.
	def _write_resource_to_db(self, resourceID, resourceStaticData):
		try:
			# e.g. resourceID =sc-sics-sc-001-temp
			if self.db_smartcitizen_resourceregistry_collection is not None:
				# check if resourceID does not exist, add it
				resource_id = self.db_smartcitizen_resourceregistry_collection.find({"resourceID": resourceID})
				if resource_id.count() == 0:
					self.db_smartcitizen_resourceregistry_collection.insert(resourceStaticData)
				else:
					print("Another resource is associated with the given resourceID")
			else:
				print("There is a problem in connecting to self.db_smartcitizen.ResourceRegistry")
		except Exception as ex:
				print(ex)
				raise

	def _format_data(self, json_reponse_sensors, time_stamp,device_id):
		try:
			dicts_resource = [] 		# resource = sc-sics-sc-001-temp
			dicts_observation = []  	    # device = sc-sics-sc-001
			ISO_time = time_stamp
			UTC_time = dateutil.parser.parse(ISO_time)
			last_reasing_timestamp = UTC_time.__str__()
			for resource in json_reponse_sensors:
				desc = resource['description']
				if desc in constants.SENSOR_LST_DESCRIPTION:
					idx = constants.SENSOR_LST_DESCRIPTION.index(desc)
					short_name = constants.SENSOR_LST_DESCRIPTION_SHORTNAMES[idx]
					# prepare the dict for this resource/observation
					dict_resource = constants.RESOURCE_DICT
					dict_observation = constants.OBSERVATIONS_DICT

					# insert into db_smartcitizen_resources_registery_collection
					resource_id=device_id+"-"+short_name
					dict_resource["deviceId"] = device_id
					dict_resource["resourceId"] = resource_id
					dict_resource["unit"] = constants.SENSOR_LIST_UNITS[idx]
					dict_resource["qk"] = constants.SENSOR_LST_DESCRIPTION_SHORTNAMES_QK[idx]
					self._write_resource_to_db(resource_id,dict(dict_resource))

					dict_observation["dataValue"] = resource['value']
					dict_observation["timestamp"] = last_reasing_timestamp
					dict_observation["resourceId"] = device_id+"-"+short_name

					self._write_observations_to_db(device_id,dict(dict_observation))

			if len(dicts_observation) == 0:
				dicts_observation.append(dict(constants.OBSERVATIONS_DICT))
			if len(dicts_resource) == 0:
				dicts_resource.append(dict(constants.RESOURCE_DICT))
			return dicts_resource, dicts_observation
		except Exception as ex:
			print(ex)
			raise

	# resource = sc-sics-sc-001-temp
	# device = sc-sics-sc-001
	def find_query(self, resource_Id, time_stamp):
		try:
			if self.db_smartcitizen is not None:
				deviceID = resource_Id.rsplit('-', 1)[0]
				deviceID_collection = self.db_smartcitizen[deviceID]
				cursor_device = deviceID_collection.find({"resourceId": resource_Id, "timestamp": time_stamp})
				cursor_resource = self.db_smartcitizen_resourceregistry_collection.find({"resourceId": resource_Id})
				return cursor_device, cursor_resource
		except Exception as ex:
				print(ex)
				raise

if __name__ == '__main__':
	smartcitizen_obj = smartCitizen(constants.API_URL,constants.ACCESS_TOKEN)
	# get list of devices' IDs associated with the current authorized user
	devices_ids = smartcitizen_obj.get_devices_ids()

	smartcitizen_obj.get_last_readings_sensors(devices_ids)
	# get data from mongodb by resourceID and timestamp
	cursor_device, cursor_resource = smartcitizen_obj.find_query("sc-sics-sc-001-light", "2016-10-05 18:54:47+00:00")

	print("There are %d query results" % cursor_device.count())
	print("Observations:")
	for ele in cursor_device:
		print(ele)
	print("Resource Information:")
	for ele in cursor_resource:
		print(ele)


