import json

class Flight:
    def __init__(self, airline=None, flightId=None, landFrom=None, terminal=None, scheduledTime=None, updatedTime=None, status=None, trigger=None):
        pass

    def set_airline(self, val):
        self.airline = val

    def set_flightId(self, val):
        self.flightId = val

    def set_landFrom(self, val):
        self.landFrom = val

    def set_terminal(self, val):
        self.terminal = val

    def set_scheduledTime(self, val):
        self.scheduledTime = val

    def set_updatedTime(self, val):
        self.updatedTime = val

    def set_status(self, val):
        self.status = val

    def set_trigger(self, val):
        self.trigger = val

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)