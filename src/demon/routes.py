from flask import request, jsonify
from .node import Node

def setup_carbon_routes(app):
    @app.route('/set_carbon_emission_rate', methods=['POST'])
    def set_carbon_emission_rate():
        """Set the carbon emission rate for this node"""
        try:
            data = request.get_json()
            rate = data.get('carbon_emission_rate', 0.5)
            node = Node.instance()
            node.set_carbon_emission_rate(rate)
            return jsonify({"status": "success", "carbon_emission_rate": rate})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    @app.route('/set_load_factor', methods=['POST'])
    def set_load_factor():
        """Set the load factor for this node"""
        try:
            data = request.get_json()
            factor = data.get('load_factor', 1.0)
            node = Node.instance()
            node.set_load_factor(factor)
            return jsonify({"status": "success", "load_factor": factor})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    @app.route('/get_carbon_emission', methods=['GET'])
    def get_carbon_emission():
        """Get current carbon emission data for this node"""
        try:
            node = Node.instance()
            emission_data = node.calculate_carbon_emission()
            return jsonify({
                "status": "success",
                "carbon_emission": emission_data,
                "carbon_emission_rate": node.carbon_emission_rate,
                "load_factor": node.load_factor
            })
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
