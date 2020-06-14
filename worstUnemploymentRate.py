import pandas as pd
import os
import requests
from smartystreets_python_sdk import StaticCredentials, exceptions, ClientBuilder
from smartystreets_python_sdk.us_zipcode import Lookup as ZIPCodeLookup


def getZipCode(cityName, stateName):
    auth_id = "64c1b167-5f64-f1ab-0898-5a13c92e2359"
    auth_token = "WfTDEo4wyzYEaOeoe3FV"

    # We recommend storing your secret keys in environment variables instead---it's safer!
    # auth_id = os.environ['SMARTY_AUTH_ID']
    # auth_token = os.environ['SMARTY_AUTH_TOKEN']

    credentials = StaticCredentials(auth_id, auth_token)

    client = ClientBuilder(credentials).build_us_zipcode_api_client()

    # Documentation for input fields can be found at:
    # https://smartystreet.com/docs/us-zipcode-api#input-fields

    lookup = ZIPCodeLookup()
    lookup.input_id = "dfc33cb6-829e-4fea-aa1b-b6d6580f0817"  # Optional ID from your system
    lookup.city = cityName
    lookup.state = stateName

    try:
        client.send_lookup(lookup)
    except exceptions.SmartyException as err:
        print(err)
        return

    result = lookup.result
    zipcodes = result.zipcodes
    cities = result.cities

    # for zipcode in zipcodes:
    #     print("\nZIP Code: " + zipcode.zipcode)

    return zipcodes


cityofHighestUnemployment = ""
directory = os.fsencode(r'C:/Users/rahul/Projects/covid19hackathon2020/datasets/localAreaUnemployement/Data/')
for dir in os.listdir(directory):
    maxRate = 0.0
    dirStr = directory + dir
    for file in os.listdir( dirStr):
        filename = os.fsdecode(file)
        fullfilename =  dirStr + os.fsencode("/") + file
        fullfilename =  os.fsdecode(fullfilename)
        data = pd.read_excel(fullfilename, skiprows=11, header=None, names=["Year", "Period", "laborforce", "employment", "unemployment", "unemploymentrate"])
        df = pd.DataFrame(data)
        row = df[['unemploymentrate']].idxmax()
        try:
            maxUnemploymentRate = df.iloc[row]['unemploymentrate'].values[0]
        except:
            continue
        cityData = pd.read_excel(fullfilename, header=None)
        df2 = pd.DataFrame(cityData)
        if(filename.endswith(".xlsx")):
            if(maxRate < maxUnemploymentRate):
                maxRate = maxUnemploymentRate
                cityName = df2.iloc[5].values[1]
                cityofHighestUnemployment = "" + cityName

    cityofHighestUnemployment = cityofHighestUnemployment.split(",")[0]
    stateName = str(os.fsdecode(dir))
    try:
        zipCode = getZipCode(cityName=cityofHighestUnemployment, stateName=stateName)[0].zipcode
    except:
        print("Skipping state " + stateName + " as we cant find zipcode based on city " + cityName)
        continue
    print("State: " + stateName , "ZipCode:" + zipCode , "Unemployent Rate: " + str(maxRate), "City:" + cityofHighestUnemployment)