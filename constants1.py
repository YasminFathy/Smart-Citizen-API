__author__ = "Yasmin Fathy (Fathy.Yasmin@gmail.com)"

# constants
ACCESS_TOKEN = "Your Access Token to SmartCitizen"
API_URL = "https://api.smartcitizen.me/v0/me?access_token="
DEVICE_LAST_READINGS_ACCESS_URL = "https://api.smartcitizen.me/v0/devices/"
DEVICE_PREFIX = "sc-sics-sc-"
SENSOR_LST_DESCRIPTION = ["Digital Ambient Light Sensor", "Custom Circuit", "Humidity", "Temperature", "NO2", "CO",
						  "Electret microphone with envelope follower sound pressure sensor (noise)"]
SENSOR_LST_DESCRIPTION_SHORTNAMES =["light","battery", "humid", "temp", "NO2", "CO", "noise"]
SENSOR_LST_DESCRIPTION_SHORTNAMES_QK = ["Illuminance", "BatteryLevel", "Humidity","RoomTemperature",
										"ChemicalAgentAtmosphericConcentrationNO2","ChemicalAgentAtmosphericConcentrationCO", "Sound"]

SENSOR_LIST_UNITS=["Lux", "Percent", "Percent", "DegreeCelsius", "PPM", "PPM", "Decibel"]
RESOURCE_DICT = {"system":"smart-ics",
					"platform":"SC-ICS-02-18",
					 "mobile":"false",
					 "deployment":"unis-smart-campus",
					 "iot-type":"sensor",
					 "measurement":"automatic",
					 "lat":"51.2433445",
					 "lon":"-0.5932438",
					 "alt":"54",
					 "relativeAlt":"2",
					"qk":"NaN",
					"unit":"NaN",
					"deviceId":"NaN",
					"resourceId":"NaN"}

OBSERVATIONS_DICT = {"resourceId":"NaN",
					"timestamp":"NaN", # "updated_at"
					"dataValue":"NaN", # "raw_value"
					}
DEVICE_ID_DICT ={
	"3710": "sc-sics-sc-001",
	"3720": "sc-sics-sc-002",
	"3730": "sc-sics-sc-003",
	"3740": "sc-sics-sc-004",
	"3750": "sc-sics-sc-005",
	"3760": "sc-sics-sc-006",
	"3770": "sc-sics-sc-007",
	"3780": "sc-sics-sc-008",
	"3790": "sc-sics-sc-009",
	"3810": "sc-sics-sc-010",
	"3820": "sc-sics-sc-011",
	"3830": "sc-sics-sc-012"
}
TIME_INTERVAL = 5  # run after 5 seconds
MONGO_DB_ACCESS = "localhost:27017"
DB_COLLECTION_NAME = "SmartCitizen_sensors"
