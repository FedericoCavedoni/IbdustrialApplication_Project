from communication_API import CommunicationAPI

class ThreadReceiver(CommunicationAPI):
    """ Class implemented by PC """
    def __init__(self):
        super().__init__(
            json_handler = self.receive_timeseries,
            threshold_reached_handler = None,
            port = 5556)


    def receive_timeseries(self, json_data : dict):
        """ { } """
        print("Ricevuto: " + str(json_data))

thread_receiver = ThreadReceiver()
thread_receiver.run()
