##Guide to run script

####Command to install all python dependencies:
`pip install -r requirements.txt`

####Command to run script:
`python car_details.py`

####Python version:
`python 3.9`

## How to use this utility
Required inputs in config.ini file:

>Section car_operation_details:
<br/>Available operations: 
<br/>`Read`: To get all car data.
<br/>`Update`: To update information of car by registration no.
<br/>`Delete`: To delete car record by registration no.
<br/>`Create`: To create car record with provided values in `car_details` section
> <br/>`Book`: To book car with provided values in `car_booking_details` section

>Section `car_booking_details`:
<br/>`customer_name`: Customer name
<br/>`uuid`: provide the uuid of car to book

>Section `car_details`:
<br/>`registration_no`: provide the registration number of car
<br/>`model`: provide the model number of car

## Python Dependencies

| Requirements | Version |
| ---- | ---- |
| configparser |5.0.2 |


####Log File path
`C:\Users\Administrator\Desktop\CarDetailsLogs`