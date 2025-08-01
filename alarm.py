import machine
from mqtt import MQTT
from rtc import RTC
from configuration import Configuration
from buttons import Buttons
from display import Display
from scheduler import Scheduler
from util import singleton
from speaker import Speaker
from clock import Clock

@singleton
class Alarm:
    def __init__(self, scheduler: Scheduler, mqtt: MQTT):
        self.scheduler = scheduler
        self.configuration = Configuration().alarm_config
        self.mqtt = mqtt
        self.rtc = RTC()
        self.speaker = Speaker(scheduler)
        self.buttons = Buttons(scheduler)
        self.display = Display(scheduler)
        self.clock = Clock(scheduler)
        self.alarm_active=False
        self.alarm_matched=False
        self.beep_count=0
        self.max_beeps=50
        self.alarm_message=None
        
        self.show_alarm_icon()

        # add the cancel
        self.buttons.add_callback(2, self.cancel_alarm)
                        
        # we could be cleaver here, and calculate how long we need
        # to sleep for, but for now just run once a second
        self.scheduler.schedule("alarm_ticker", 1000, self.ticker_callback)

        mqtt.register_topic_callback(
            "alarm/enable", self.mqtt_callback)
        mqtt.register_topic_callback(
            "alarm/set", self.mqtt_callback)     
        mqtt.register_topic_callback(
            "alarm/message", self.mqtt_callback)                     

    def show_alarm_icon(self):
        if self.configuration.enabled:
            self.display.show_icon("AlarmOn")
        else:
            self.display.hide_icon("AlarmOn")
                
    async def ticker_callback(self):
        if self.configuration.enabled:
            now = self.rtc.get_time()
            hour, minute = self.parse_time(self.configuration.time)
            if now[3] == hour and now[4] == minute:                
                # check that we haven't already triggered the alarm
                if not self.alarm_matched:
                    print(f"alarm trigger at {hour}:{minute}")
                    self.alarm_matched=True
                    # trigger alarm
                    self.trigger_alarm()
            else:
                self.alarm_matched=False
        
    def trigger_alarm(self):

        if self.alarm_active==False:
            self.alarm_active=True

            # display the requested message
            if self.alarm_message:
                self.clock.show_message(self.alarm_message)

            # ok, now trigger the alarm
            self.scheduler.schedule("alarm_beep", 1000, self.beeper_callback)

    async def beeper_callback(self):
        self.speaker.beep(200)
        self.beep_count=self.beep_count+1
        if self.beep_count>self.max_beeps:
            await self.cancel_alarm()

    def parse_time(self, timevalue):

        # timevalue is in the form of "hh:mm"
        # split it into hour and minute
        # check that the message is correctly formatted
        # it needs to be number:number        
        hour=None
        minute=None
        if ":" in timevalue:                                            
            parts = timevalue.split(":")
            if len(parts) >= 2:
                hour = int(parts[0])
                minute = int(parts[1])

        return hour, minute


    async def cancel_alarm(self):
        print("cancel alarm")
        # remove the callbacks for the buttons
        #self.buttons.clear_callbacks()
        # and stop the alarm
        self.scheduler.remove("alarm_beep")

        self.alarm_active=False

    def mqtt_callback(self, topic, message):

        # convert message to string from bytes
        message = message.decode("utf-8")  
        topic= topic.decode("utf-8") 
        print(f"alarm mqtt called {topic} {message}")
        # see if its the enable/disable topic
        # check if it ends in "alarm/enabled"
        if topic.endswith("alarm/enable"):
            if message == "true" or message == "on":
                print("enable alarm")
                self.configuration.enabled = True
            else:
                print("disable alarm")
                self.configuration.enabled = False
              
            self.show_alarm_icon()            

        elif topic.endswith("alarm/set"):
            self.configuration.time = message
            
            print(f"set alarm to {self.configuration.time}")

        elif topic.endswith("alarm/message"):
            self.alarm_message=message
            print(f"set alarm message to {self.alarm_message}")
