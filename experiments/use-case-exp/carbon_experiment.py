import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import requests
import time
import random
import csv
from config import settings
import utils

def set_diverse_carbon_emission_rates(edge_servers):
    """Set different carbon emission rates for edge servers to simulate diverse energy sources"""
    emission_rates = [0.2, 0.3, 0.5, 0.7, 0.9, 1.2]  # kg CO2 per kWh
    
    for i, server in enumerate(edge_servers):
        rate = emission_rates[i % len(emission_rates)]
        try:
            response = requests.post(
                f"http://{server['ip']}:{server['port']}/set_carbon_emission_rate",
                json={"carbon_emission_rate": rate},
                timeout=5
            )
            if response.status_code == 200:
                print(f"Set carbon emission rate {rate} for server {server['ip']}:{server['port']}")
            server['carbon_rate'] = rate
        except Exception as e:
            print(f"Failed to set carbon rate for {server['ip']}:{server['port']}: {e}")
            server['carbon_rate'] = 0.5  # default

def simulate_variable_loads(edge_servers):
    """Simulate variable loads on different servers"""
    for server in edge_servers:
        load_factor = random.uniform(0.5, 2.0)  # Random load between 50% and 200%
        try:
            response = requests.post(
                f"http://{server['ip']}:{server['port']}/set_load_factor",
                json={"load_factor": load_factor},
                timeout=5
            )
            if response.status_code == 200:
                print(f"Set load factor {load_factor:.2f} for server {server['ip']}:{server['port']}")
        except Exception as e:
            print(f"Failed to set load factor for {server['ip']}:{server['port']}: {e}")

def collect_carbon_emission_data(edge_servers):
    """Collect carbon emission data from all servers"""
    emission_data = []
    
    for server in edge_servers:
        try:
            response = requests.get(
                f"http://{server['ip']}:{server['port']}/get_carbon_emission",
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    emission_info = data.get("carbon_emission", {})
                    emission_data.append({
                        'server_id': f"{server['ip']}:{server['port']}",
                        'current_emission_rate': emission_info.get('current_emission_rate', 0),
                        'total_emission': emission_info.get('total_emission', 0),
                        'power_consumption': emission_info.get('power_consumption_watts', 0),
                        'carbon_rate': data.get('carbon_emission_rate', 0),
                        'load_factor': data.get('load_factor', 1.0),
                        'timestamp': time.time()
                    })
        except Exception as e:
            print(f"Failed to collect data from {server['ip']}:{server['port']}: {e}")
    
    return emission_data

def run_carbon_experiment():
    """Run the carbon emission experiment"""
    print("Starting carbon emission experiment...")
    
    # Load edge servers
    edge_servers = utils.load_csv_dataset_as_dict('data/edge_servers.csv')
    
    # Start all nodes with diverse carbon emission rates
    set_diverse_carbon_emission_rates(edge_servers)
    utils.start_all_nodes(edge_servers)
    
    # Wait for nodes to stabilize
    time.sleep(30)
    
    results = []
    experiment_duration = 300  # 5 minutes
    collection_interval = 30  # Collect data every 30 seconds
    
    start_time = time.time()
    iteration = 0
    
    while (time.time() - start_time) < experiment_duration:
        print(f"Iteration {iteration}: Collecting carbon emission data...")
        
        # Simulate variable loads
        if iteration % 3 == 0:  # Change loads every 3 iterations
            simulate_variable_loads(edge_servers)
        
        # Collect emission data
        emission_data = collect_carbon_emission_data(edge_servers)
        
        # Add iteration info to each record
        for record in emission_data:
            record['iteration'] = iteration
            record['experiment_time'] = time.time() - start_time
        
        results.extend(emission_data)
        
        print(f"Collected data from {len(emission_data)} servers")
        
        iteration += 1
        time.sleep(collection_interval)
    
    # Save results to CSV
    if results:
        fieldnames = results[0].keys()
        with open('data/carbon_emission_results.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        
        print(f"Experiment completed. Results saved to carbon_emission_results.csv")
        print(f"Total data points collected: {len(results)}")
        
        # Calculate and print summary statistics
        total_emissions = sum(r['total_emission'] for r in results)
        avg_power = sum(r['power_consumption'] for r in results) / len(results)
        
        print(f"Total carbon emissions: {total_emissions:.4f} kg CO2")
        print(f"Average power consumption: {avg_power:.2f} watts")
    else:
        print("No data collected during experiment")

if __name__ == "__main__":
    run_carbon_experiment()
