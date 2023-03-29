"""
OPC UA Python Server with Simulated Data
Author: Manoel Costa
Date: 2023-03-29

Description:
This script creates an OPC UA server that simulates multiple equipment nodes
with tags for temperature, pressure, torque, humidity, light, voltage, and watts.
Each equipment node contains its own set of tags, and the values are continuously
updated with random simulated data.

Prerequisites:
- Python 3.6 or higher
- Install the "opcua" library using pip: pip install opcua

Instructions:
1. Make sure you have installed the required library.
2. Update the server endpoint, namespace, and other settings in the script, if necessary.
3. Run the script: python opcua_server.py
4. The server will start, and you can connect to it using an OPC UA client.
"""

# myopcua.py

# Required imports
import sys
import time
import random
from opcua import ua, Server

# Function to generate simulated data for each tag
def generate_simulated_data():
    return {
        "Temperature": random.uniform(20, 30),
        "Pressure": random.uniform(1000, 1050),
        "Torque": random.uniform(5, 30),
        "Humidity": random.uniform(40, 60),
        "Light": random.uniform(500, 1000),
        "Voltage": random.uniform(110, 240),
        "Watts": random.uniform(50, 500)
    }

# Function to create an equipment node under the parent_node with the given equipment_name
# and add tags for the equipment using the namespace_idx
def create_equipment_node(parent_node, equipment_name, namespace_idx):
    # Create an object node for the equipment
    equipment_node = parent_node.add_object(namespace_idx, equipment_name)
    tags = {}

    # Add variables for each tag to the equipment node
    for tag_name in generate_simulated_data().keys():
        tags[tag_name] = equipment_node.add_variable(namespace_idx, tag_name, 0)

    return tags

if __name__ == "__main__":
    # Initialize the OPC UA server
    server = Server()

    # Set up the server's endpoint
    server.set_endpoint("opc.tcp://127.0.0.1:4841/freeopcua/server/")

    # Set up the server's namespace
    uri = "http://examples.freeopcua.github.io"
    idx = server.register_namespace(uri)

    # Set up the object node
    objects = server.get_objects_node()
    simulated_data_node = objects.add_object(idx, "SimulatedData")

    # Create equipment nodes and their respective tags
    num_equipments = 5
    equipments = {}
    for i in range(num_equipments):
        equipment_name = f"Equipment_{i + 1}"
        equipments[equipment_name] = create_equipment_node(simulated_data_node, equipment_name, idx)

    # Start the server
    server.start()

    try:
        # Main loop to continuously update the variables with new simulated data
        while True:
            for equipment_name, tags in equipments.items():
                data = generate_simulated_data()
                for tag_name, value in data.items():
                    tags[tag_name].set_value(value)

            time.sleep(1)
    finally:
        # Close the server when exiting
        server.stop()
