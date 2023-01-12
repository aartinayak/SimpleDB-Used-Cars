from typing import final
import boto.sdb
import pandas as pd
import random

AWS_REGION = 'us-east-1'
ACCESS_KEY_ID = 'AKIAVLOQ2XROMXGOYF4L'
ACCESS_KEY = 'lBOO9aYvkXYFz2yrNugjaGkWCPx443kfQMa0jPcj'
QUERY_FORMAT = "{}"
DOMAIN_NAME = "Used_Cars_APP"
FILTER_LOGIC_PATTERN = "{} = \'{}\' "

FORM_SUCCESS_MESSAGE = "Listed successfully. Your Listing ID is {}"
FORM_FAILURE_MESSAGE = "Listing failed..{}"

NO_SQL_QUERY = {"CAR_LISTING": "SELECT * from Used_Cars_APP ", "LISTING_ID": "select listing_id from Used_Cars_APP"}
HTML_NAME_MAPPING_TO_COL_NAME = {"vin": "itemName", "Body Type": "body_type", 'City': 'city',
                                 "model_name": "model_name", "Engine_type": "engine_type",
                                 "Color": "exterior_color", "listing_id": "listing_id","Transmission":"transmission",
                                 "Fuel Type":"fuel_type","Maximum seating":"maximum_seating"}


def validate_owner_count(owner_data):
    if len(owner_data) < 4 and owner_data.isnumeric():
        return True, ""
    else:
        return False, "Please enter valid owner count"

def validate_power(power_data):
    if power_data is not None:
        return True, ""
    else:
        return False, "Please enter valid Power of the car"

def validate_price(price_data):
    if price_data is not None:
        return True, ""
    else:
        return False, "Please enter valid Price of the car"

def validate_torque(torque_data):
    if torque_data is not None:
        return True, ""
    else:
        return False, "Please enter valid Torque"

def validate_transmission(transmission_data):
    if transmission_data is not None and transmission_data.isalpha():
        return True, ""
    else:
        return False, "Please enter valid Transmission"

def validate_year(year_data):
    if year_data is not None and len(year_data) == 4 and year_data.isnumeric():
        return True, ""
    else:
        return False, "Please enter valid Year of the car"

def validate_vin(vin_data):
    if len(vin_data) == 17 and vin_data.isalnum():
        return True, ""
    else:
        return False, "Please enter valid VIN"

def validate_body_type(body_type_data):
    
    if body_type_data is not None and body_type_data.isalnum():
        return True, ""
    else:
        return False, "Please enter valid Body Type"

def validate_city(city_data):
    
    if city_data is not None and city_data.isalpha():
        return True, ""
    else:
        return False, "Please enter valid city"

def validate_zip(zip_data):
    
    if len(zip_data) == 5 and zip_data.isnumeric():
        return True, ""
    else:
        return False, "Please enter valid zip"

def validate_color(color_data):
    
    if color_data is not None and color_data.isalpha():
        return True, ""
    else:
        return False, "Please enter valid color"

def validate_fuel_tank_volume(fuel_tank_data):
    
    if fuel_tank_data.isalnum():
        return True, ""
    else:
        return False, "Please enter valid fuel tank"

def listing_date(list_data):
    
    if list_data is not None:
        return True, ""
    else:
        return False, "Please enter valid date"

def maximum_seating(seating_data):
    
    if seating_data is not None and seating_data.isnumeric() and int(seating_data) >1 and int(seating_data) < 20:
        return True, ""
    else:
        return False, "Please enter valid maximum seating"

def validate_milage(milage_data):
    
    if milage_data.isnumeric():
        return True, ""
    else:
        return False, "Please enter valid mileage"


VALIDATION_FUNCTION_MAPPING = {
    'vin' : validate_vin,
    "body_type": validate_body_type,
    "city": validate_city,
    "dealer_zip": validate_zip,
    "engine_type": None,
    "exterior_color": validate_color,
    "fueltank_volume": validate_fuel_tank_volume,
    "listing_date": listing_date,
    "maximum_seating": maximum_seating,
    "mileage": validate_milage,
    "model_name": None,
    "owner_count": validate_owner_count,
    "transmission": validate_transmission,
    "power": validate_power,
    "torque": validate_torque,
    "year": validate_year
}

def get_data_from_db(conn, query):
    """
    Function to ge the dya
    :param conn:
    :param query:
    :return:
    """
    dom = conn.get_domain('Used_Cars_APP')
    data_iterator = dom.select(query)
    return data_iterator

def construct_insert_query(form_data):
    data_keys = {}
    for key in form_data:
        if key != 'vin':
            data_keys[key] = form_data.get(key)

       
    random_listing_id = generate_listing_id()
    data_keys['listing_id'] = random_listing_id
    return {form_data['vin']: data_keys}


def generate_listing_id():
    conn = get_connection()
    current_list_id = list(get_data_from_db(conn, NO_SQL_QUERY["LISTING_ID"]))
    return make_it_truly_random(current_list_id)

def make_it_truly_random(current_list_id):
    random_listing_id = random.randint(111111111, 999999999)
    if random_listing_id in current_list_id:
        make_it_truly_random(current_list_id)
    return random_listing_id

def validate_form_submitted_data(form_data):
    for key in form_data:
        if key in VALIDATION_FUNCTION_MAPPING:
            validation_function = VALIDATION_FUNCTION_MAPPING.get(key)
            if callable(validation_function):
                check, message = validation_function(form_data[key])
                if not check:
                    return FORM_FAILURE_MESSAGE.format(message)
                    
    query = construct_insert_query(form_data)
    put_data_into_db(None,query)
    return FORM_SUCCESS_MESSAGE.format(query[form_data['vin']].get('listing_id'))

def get_filtered_cars_details(filter_dictionary):
    conn = get_connection()
    query = NO_SQL_QUERY.get("CAR_LISTING")
    where_logic = "where "
    for key in filter_dictionary:
        current_filter = FILTER_LOGIC_PATTERN.format(HTML_NAME_MAPPING_TO_COL_NAME[key], filter_dictionary.get(key))
        if where_logic == "where ":
            where_logic = where_logic + current_filter
        else:
            where_logic = where_logic + "and " + current_filter
    if where_logic != "where ":
        formatted_query = query + where_logic
    else:
        formatted_query = query
    data_iterator = get_data_from_db(conn, formatted_query)
    return list(data_iterator)

def get_connection():
    conn = boto.sdb.connect_to_region(AWS_REGION, aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=ACCESS_KEY)
    return conn

def put_data_into_db(conn=None, js1=""):
    if conn is None:
        conn = get_connection()
    dom = conn.get_domain(DOMAIN_NAME)
    dom.batch_put_attributes(js1)