from flask import Flask, request, jsonify
import requests

class CommunicationAPI():
    """
    CommunicationAPI is a web-server designed for handling and routing
    different types of incoming data such as JSON and files.
    The single systems can extend this class and use it as API to communicate
    with other systems according to the pre-defined standard.
    """
    def __init__(self, json_handler=None, threshold_reached_handler = None, port=5555):
        self.app = Flask(__name__, template_folder=None, static_folder=None)
        self.setup_routes()
        self.port = port
        self.json_handler = json_handler
        self.threshold_reached_handler = threshold_reached_handler

    def setup_routes(self):
        """ Defines routes for the Flask application """

        @self.app.route('/receive_sample_result', methods=['POST'])
        def receive_sample_result():
            """ Handles the incoming JSON messages"""
            if self.json_handler:
                json_data = request.json
                self.json_handler(json_data)
                return jsonify({'message': 'json received', "success": True}), 200
            else:
                return jsonify({'message': 'json handler not defined', "success": False}), 501
            
        @self.app.route('/threshold_reached', method=["GET"])
        def receive_threshold_reached():
            if self.threshold_reached_handler:
                self.threshold_reached_handler()
                return jsonify({'message': 'comando ricevuto'}), 200

    def send_sample(self, target_ip, target_port, json_data):
        """ Sends a JSON to the specified system """
        try:
            requests.post(
                f"http://{target_ip}:{target_port}/receive_sample", json=json_data, timeout=30)
        except requests.RequestException as e:
            print(f"[CommunicationAPI] Send JSON failed: {e}")

    def run(self):
        """ runs the service"""
        self.app.run(host="0.0.0.0", port=self.port)
