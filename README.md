### Simulator for Meter Data and Solar-PV data
A python script that allows you to generate synthetic smart meters data and Solar-PV generation data.

The script reads a CSV and cyclically follows the pattern of values to simulate a 24-hour running smart meter.
The simulated values are published onto RabbitMQ queues. The smart meter data as it arrives, is added to the PV generation data and the values are written to a csv with timestamp

### Table of Contents
1. [Requirements](#requirements)
2. [Running from source code](#method-1-running-from-source-code)
    1. [Run Producer](#method-1-running-from-source-code)
    2. [Run Listener](#to-run-listener-that-adds-pv-value-and-outputs-results-to-file)
3. [Run using docker-compose](#method-2-using-docker-containers-with-docker-compose-to-run-simulation)
4. [Viewing output csv files](#viewing-output-csv-files)
5. [Running Tests](#running-tests)
5. [Improvements](#improvements)

### Requirements 
- Method 1: To run script manually from source code
    - Python 3.7 or higher
    - RabbitMQ service
    - virtualenv (to create virtualenv)
- Method 2: To run using docker compose
    - docker (Tested on 2.3.0.4)
    - docker-compose (Tested on 1.26.2)
    

### Method 1: Running from source code
**Run Rroducer**
Setting up the source code gives more control and you can change input parameters
- Clone the repo and cd into "device_simulator" folder
    - `$> git clone git@github.com:SrikalaB/device_simulator.git`
    - `$> cd device_simulator`
- Install the virtualenv as per https://docs.python.org/3.7/library/venv.html and activate it.
    - Eg: `$> . venv/bin/activate`
- Install all required dependencies as follows
`$> pip3 install -r requirements.txt`
- Create the following environment variables with credentials to connect to RabbitMQ. Use the default password for testing in development environment
    -  `$> export USER=guest`
    -  `$> export PASSWORD=guest`
    -  `$> export BROKERS=127.0.0.1`

- Usage `$>python run_simulators.py --help`
    ```
    usage: run_simulators.py [-h] -p PROFILE
    
    optional arguments:
      -h, --help            show this help message and exit
      -p PROFILE, --profile PROFILE
                            Simulator Profile you want to run.[ Enter: LoadProfile
                            or PvProfile]
    ```
- Example: To run household meter simulation

    ``` 
    $> python run_simulators.py --profile LoadProfile
    If you wish to stop simulation at any point - Press ctrl+C
    
    Starting LoadProfile simulation for device with identifier meter123. Reading will start at current time UTC and will be published at 1 min intervals
    [SUCCESS] Published {"timestamp": "2020-11-18 17:30:00", "value": 5251.4, "device": "meter123", "unit": "W", "payload_type": "meter_data"} for LoadProfile with frequency 60 seconds
    [SUCCESS] Published {"timestamp": "2020-11-18 17:31:00", "value": 5253.07, "device": "meter123", "unit": "W", "payload_type": "meter_data"} for LoadProfile with frequency 60 seconds
            
    ```

As seen it assumes a frequency of 1 minute and publishes a message to RabbitMQ using user credentials. Leave the process running to let the simulation run.

#### To run listener that adds PV value and outputs results to file
**Run Listener**
- Open the repo code again in another terminal
    - `$>cd device_simulator`
    ```
    $> python listener.py
     [*] Waiting for messages. To exit press CTRL+C
    Received message {'timestamp': '2020-11-18 17:20:00', 'value': 5249.72, 'device': 'meter123', 'unit': 'W', 'payload_type': 'meter_data'}
    [SUCCESS] PvDataGenerationHandler called to handle message
    [SUCCESS] Completed writing row to file [datetime.datetime(2020, 11, 18, 17, 29), 5249.72, 1669.92, 3579.8, 'W']
    ```

### Method 2: Using docker containers with docker-compose to run simulation
Setting up using docker compose lets you run the simulation and view the output files quickly
- Clone the repo and cd into "device_simulator" folder
    - `$> git clone git@github.com:SrikalaB/device_simulator.git`
    - `$> cd device_simulator`
- Create the following environment variables with credentials to connect to RabbitMQ. Use the default password for testing in development environment
    -  `$> export USER=guest`
    -  `$> export PASSWORD=guest`
- Build containers and bring them up using docker compose
- `$> docker-compose up --build`
```.env
rabbitmq_1   |  completed with 3 plugins.
rabbitmq_1   | 2020-11-18 19:11:06.940 [info] <0.707.0> accepting AMQP connection <0.707.0> (172.19.0.3:47358 -> 172.19.0.2:5672)
rabbitmq_1   | 2020-11-18 19:11:06.947 [info] <0.707.0> connection <0.707.0> (172.19.0.3:47358 -> 172.19.0.2:5672): user 'guest' authenticated and granted access to vhost '/'
simulator_1  | [SUCCESS] Published {"timestamp": "2020-11-18 19:11:00", "value": 5945.61, "device": "meter123", "unit": "W", "payload_type": "meter_data"} for LoadProfile with frequency 60 seconds
rabbitmq_1   | 2020-11-18 19:11:07.034 [info] <0.722.0> accepting AMQP connection <0.722.0> (172.19.0.4:49412 -> 172.19.0.2:5672)
rabbitmq_1   | 2020-11-18 19:11:07.040 [info] <0.722.0> connection <0.722.0> (172.19.0.4:49412 -> 172.19.0.2:5672): user 'guest' authenticated and granted access to vhost '/'
listener_1   |  [*] Waiting for messages. To exit press CTRL+C
listener_1   | Received message {'timestamp': '2020-11-18 19:11:00', 'value': 5945.61, 'device': 'meter123', 'unit': 'W', 'payload_type': 'meter_data'}
listener_1   | [SUCCESS] PvDataGenerationHandler called to handle message
listener_1   | [SUCCESS] Completed writing row to file [datetime.datetime(2020, 11, 18, 19, 11), 5945.61, 874.37, 5071.24, 'W']

simulator_1  | [SUCCESS] Published {"timestamp": "2020-11-18 19:12:00", "value": 5951.88, "device": "meter123", "unit": "W", "payload_type": "meter_data"} for LoadProfile with frequency 60 seconds
listener_1   | Received message {'timestamp': '2020-11-18 19:12:00', 'value': 5951.88, 'device': 'meter123', 'unit': 'W', 'payload_type': 'meter_data'}
listener_1   | [SUCCESS] PvDataGenerationHandler called to handle message
listener_1   | [SUCCESS] Completed writing row to file [datetime.datetime(2020, 11, 18, 19, 12), 5951.88, 866.57, 5085.31, 'W']
```
Note: It may take a minute to establish connection with RabbitMQ.

####  Viewing output csv files
CSV format is as follows:
- Timestamp: Time in UTC at which the meter value and solar pv value were read from the device.
- Meter value: Power value of meter
- PV value: Power value of PV device
- Net load: Meter Value + (- PV value)
- Unit: Unit of power(W or kW) used for above 3 fields

To view the csv. From device_simulator folder
   ```.env
    $> cd ./messaging/output_files
    $> ls
       2020-11-17_meter_with_pv.csv 2020-11-18_meter_with_pv.csv
   ```
    

### Running Tests
The script comes with test cases that can be run using:

`python -m unittest test.test_simulator`

### Improvements
- Use Dataframes from python pandas to allow for resampling of source data for different time intervals.
- Add time zone capability to use simulator to produce values in different timezones.
- More test coverage

