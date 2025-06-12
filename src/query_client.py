import random
import time

import requests


def get_node_carbon_emission(node_ip, node_port, docker_ip):
    """Get carbon emission data from a node"""
    try:
        response = requests.get(f"http://{docker_ip}:{node_port}/get_carbon_emission", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                return data.get("carbon_emission", {}).get("current_emission_rate", float('inf'))
    except Exception as e:
        print(f"Failed to get carbon emission from {node_ip}:{node_port}: {e}")
    return float('inf')


def select_nodes_by_carbon_footprint(nodes, quorum_size, docker_ip):
    """Select nodes with lowest carbon emissions for query"""
    node_emissions = []
    
    for node in nodes:
        emission_rate = get_node_carbon_emission(node["ip"], node["port"], docker_ip)
        node_emissions.append((node, emission_rate))
    
    # Sort by carbon emission (lowest first)
    node_emissions.sort(key=lambda x: x[1])
    
    # Select nodes with lowest emissions up to quorum size
    selected_nodes = [node for node, _ in node_emissions[:quorum_size]]
    
    return selected_nodes


def query(nodes, quorum_size, target_ip, target_port, docker_ip, use_carbon_optimization=True):
    """Query nodes with optional carbon emission optimization"""
    total_messages = 0
    
    if use_carbon_optimization:
        # Select nodes based on carbon emissions
        selected_nodes = select_nodes_by_carbon_footprint(nodes, quorum_size, docker_ip)
    else:
        # Use random selection (original behavior)
        selected_nodes = random.sample(nodes, min(quorum_size, len(nodes)))
    
    # Query the selected nodes
    query_results = []
    for node in selected_nodes:
        try:
            response = requests.get(
                f"http://{docker_ip}:{node['port']}/query_node?target_ip={target_ip}&target_port={target_port}",
                timeout=10
            )
            total_messages += 1
            
            if response.status_code == 200:
                query_results.append(response.json())
            
        except Exception as e:
            print(f"Query failed for node {node['ip']}:{node['port']}: {e}")
    
    # Return consensus result if available
    if len(query_results) >= (quorum_size // 2) + 1:
        return total_messages, query_results[0]  # Simple consensus
    else:
        raise Exception("Failed to achieve quorum for query")
