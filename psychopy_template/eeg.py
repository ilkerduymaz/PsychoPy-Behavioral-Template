import serial


class EEG:
    def __init__(self, port="COM5", send_triggers=True):
        self.port = port
        self.send_triggers = send_triggers

        if self.send_triggers:
            self.initPort()

    def initPort(self):
        try:
            self.p_port = serial.Serial(self.port)
        except serial.SerialException:
            self.p_port = None
            Warning("No parallel port found")

    def sendTrigger(self, win, trigger: int):
        if self.send_triggers and trigger is not None:
            win.callOnFlip(self.p_port.write, bytes([int(trigger)]))
        else:
            print(f"trigger: {trigger}")
