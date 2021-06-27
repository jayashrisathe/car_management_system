import sys
from configparser import ConfigParser
import os
import logging
import json
import uuid

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(message)s',
    handlers=[
        logging.FileHandler(f"C:\\Users\\{os.getlogin()}\\Desktop\\CarDetailsLogs.log"),
        logging.StreamHandler()
    ]
)
CAR_RECORDS_FILE = "car_records.json"

class Car:
    def __init__(self):
        self.operation = "read"
        self.registration_no = ""
        self.model = ""
        self.brand = ""
        self.price = 0
        self.mileage = 0
        self.color = ""
        self.year = ""
        self.status = "available"
        self.uuid = ""
        self.customer_name = ""
        self.check_file_records()

    def check_file_records(self):
        """
        Function to add valid data in json file for the first time to avoid json errors.
        """
        try:
            with open(CAR_RECORDS_FILE) as f:
                json.load(f)
        except Exception:
            with open(CAR_RECORDS_FILE, 'w') as json_file:
                json.dump([], json_file)

    def get_config_parameters(self):
        """
        Function to get parameters from config file and set to the instance variables.
        """
        config = ConfigParser(allow_no_value=True)
        config.read("config.ini")
        if config.has_option("car_operation_details", "operation"):
            self.operation = config.get("car_operation_details", "operation")
        else:
            logging.debug("Please provide correct operation. (create/update/delete/read)")

        if config.has_option("car_details", "registration_no"):
            self.registration_no = config.get("car_details", "registration_no")
        else:
            logging.debug("Please provide registration no.")

        if config.has_option("car_details", "model"):
            self.model = config.get("car_details", "model")
        if config.has_option("car_details", "brand"):
            self.brand = config.get("car_details", "brand")
        if config.has_option("car_details", "price"):
            self.price = config.get("car_details", "price")
        if config.has_option("car_details", "mileage"):
            self.mileage = config.get("car_details", "mileage")
        if config.has_option("car_details", "color"):
            self.color = config.get("car_details", "color")
        if config.has_option("car_details", "year"):
            self.year = config.get("car_details", "year")
        if config.has_option("car_booking_details", "uuid"):
            self.uuid = config.get("car_booking_details", "uuid")
        if config.has_option("car_booking_details", "customer_name"):
            self.customer_name = config.get("car_booking_details", "customer_name")

    def get_operation_to_perform(self):
        """
        Function to call the correct method according operation provided by user.
        """
        if self.operation.lower() == "create":
            logging.debug(f"\n\nCreating record with given values\n\n")
            self.create_car_record()
        elif self.operation.lower() == "read":
            logging.debug(f"\n\nReading records\n\n")
            self.read_car_records()
        elif self.operation.lower() == "update":
            self.update_car_record()
        elif self.operation.lower() == "delete":
            logging.debug("Deleting the record with given values.")
            self.delete_car_record()
        elif self.operation.lower() == "book":
            self.car_booking()
        else:
            logging.warning("Please provide correct operation from: create, read, update, delete")

    def create_car_record(self):
        """
        Function to create the car record with provided car details from section: car_details
        """
        registration_nums = [data_dict["registration_no"] for data_dict in self.read_car_records()]
        if self.registration_no in registration_nums:
            logging.warning(f"\n\nRecord with given registration number: {self.registration_no} is already available!!\n\n")
            sys.exit()
        record_dict = {"registration_no": self.registration_no,
                       "status": self.status,
                       "model":self.model,
                       "brand": self.brand,
                       "price":self.price,
                       "mileage":self.mileage,
                       "color":self.color,
                       "year":self.year,
                       "uuid": str(uuid.uuid4())
                       }
        f = open(CAR_RECORDS_FILE)
        data = json.load(f)
        data.append(record_dict)
        data_to_write = json.dumps(data, indent=4)
        f.close()
        with open(CAR_RECORDS_FILE, "w") as file_obj:
            file_obj.write(data_to_write)

    def read_car_records(self):
        """
        Function to read all the car data and will print on console.
        """
        file_obj = open(CAR_RECORDS_FILE)
        data = json.load(file_obj)
        file_obj.close()
        logging.debug(f"Available car records: {data}")
        return data

    def update_car_record(self):
        """
        Function to update the car record by registration no.
        """
        logging.debug(f"\n\nUpdating record having registration no: {self.registration_no}\n\n")
        self.delete_car_record()
        self.create_car_record()

    def delete_car_record(self):
        """
        Function to delete the car record by registration no.
        """
        warning = True
        data = self.read_car_records()
        for index, data_dict in enumerate(data):
            if data_dict["registration_no"] == self.registration_no:
                warning = False
                data.pop(index)
                break
        if warning:
            logging.warning(f"\n\nRecord with given registration number: {self.registration_no} is not available!!\n\n")
            sys.exit()
        with open(CAR_RECORDS_FILE, "w") as outfile:
            outfile.write(json.dumps(data, indent=4))

    def car_booking(self):
        """
        Function to book the car record by provided uuid, only section: car_booking_details will be considered.
        """
        logging.debug(f"\n\nBooking the car having uuid: {self.uuid}\n\n")
        updated_data = []
        data = self.read_car_records()
        for data_dict in data:
            if data_dict["uuid"] == self.uuid:
                if not data_dict["status"] == "available":
                    logging.warning("\n\nSorry, cannot book this car as it is already booked.\n\n")
                data_dict["status"] = "booked"
                data_dict["customer_name"] = self.customer_name
            updated_data.append(data_dict)
        file = open(CAR_RECORDS_FILE, "w")
        json.dump(updated_data, file, indent=4)
        file.close()


if __name__ == "__main__":
    car_obj = Car()
    car_obj.get_config_parameters()
    car_obj.get_operation_to_perform()
