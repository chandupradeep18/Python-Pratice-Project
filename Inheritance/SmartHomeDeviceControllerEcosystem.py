#04-07-2026
#Smart Home Device Controller Ecosystem
from datetime import datetime
from time import time
import re
class SmartDevice:
    total_devices=0
    def __init__(self,name:str,room:str,mac_address:str):
        if not self.is_valid_mac(mac_address):
            raise ValueError(f"Warning: Invalid MAC for {self._name}")
        self._name=name
        self._room=room
        self.__mac_address=mac_address
        self._is_online=True
        self._power_state=False
        SmartDevice.total_devices+=1
    
    def power(self):
        if not self._is_online:
            return f"[{self._name}] is offline and cannot be turned on.turned off."
        self._power_state= not self._power_state
        if self._power_state:
            return f"[{self._name}] turned ON."
        else:
            return f"[{self._name}] turned OFF."
    
    def get_status(self):
        state="ON" if self._power_state else "OFF"
        network = "Online" if self._is_online else "Offline"
        return f"{self._name} ({self._room}): Power={state}, Network={network}"
    
    @property
    def mac_address(self):
        return self.__mac_address
    
    @classmethod
    def get_total_device_count(cls):
        return f"Total smart devices on the network: {cls.total_devices}"
    
    @staticmethod
    def is_valid_mac(mac):
        pattern = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')
        return bool(pattern.match(mac))
    
    def _check_device(self):
        if not self._is_online:
            return False,'Device is Not Connected to Internet'
        if not self._power_state:
            return False,f"[{self._name}] is OFF. Turn it on first."
        return True,"Connected to Internet and Powered On"
        
class SmartLight(SmartDevice):
    def __init__(self, name, room, mac_address,max_brightness=100):
        super().__init__(name, room, mac_address)
        self.brightness=0
        self.color="White"
        self.max_brightness=max_brightness
    
    def set_brightness(self,level):
        success,message=self._check_device()
        if not success:
            return message
        if not 0<=level<=100:
            return f"Invalid brightness. Must be between 0 and {self.max_brightness}."
        self.brightness=level
        return f"[{self._name}] brightness set to {self.brightness}%."
    

    def set_color(self,value):
        """success,message=self._check_device()
        if not success:
            print(message)
            raise ValueError(message)"""
        self.color=value
        print(f"[{self._name}] color changed to {self.color}.")
    
    def get_status(self):
        base_status= super().get_status()
        return f"{base_status} | Brightness={self.brightness}%, Color={self.color}"

class SmartThermostat(SmartDevice):
    def __init__(self, name, room, mac_address):
        super().__init__(name, room, mac_address)
        self.current_temp=72.0
        self.target_temp=72.0
        self.mode="Off"
    
    def set_mode(self,mode):
        valid_modes = ["Heat", "Cool", "Eco"]
        success,message=self._check_device()
        if not success:
            return message
        if mode not in valid_modes:
            return f"Invalid mode. Choose from {valid_modes}."
        self.mode=mode
        return f"[{self._name}] mode set to {self.mode}."
    
    def set_temperature(self,temp):
        success,message=self._check_device()
        if not success:
            return message
        if 50.0 <=temp<=90.0:
            self.target_temp=float(temp)
            return f"[{self._name}] target temperature set to {self.target_temp}°F."
        return "Safety Limit: Temperature must be between 50°F and 90°F."   
    
    def get_status(self):
        base_status = super().get_status()
        return f"{base_status} | Mode={self.mode}, Temp={self.current_temp}°F -> Target={self.target_temp}°F"

class SmartCamera(SmartDevice):
    def __init__(self, name, room, mac_address,resolution="1080p",):
        super().__init__(name, room, mac_address)
        self.resolution=resolution
        self.is_recording = False
        self.motion_detection_active = False
    
    def toggle_motion_detection(self):
        success,message=self._check_device()
        if not success:
            return message
        self.motion_detection_active=not self.motion_detection_active
        status = "Armed" if self.motion_detection_active else "Disarmed"
        return f"[{self._name}] motion detection is now {status}."
    
    def trigger_motion(self):
        success,message=self._check_device()
        if not success:
            return message
        if not self.motion_detection_active:
            return f"[{self._name}] motion ignored (detection off)."
        self.is_recording = True
        return f"ALERT! Motion detected at [{self._name}]. Recording started at {self.resolution}."
    
    def get_status(self):
        base_status = super().get_status()
        motion = "Armed" if self.motion_detection_active else "Disarmed"
        rec = "Recording!" if self.is_recording else "Idle"
        return f"{base_status} | Motion={motion}, State={rec}"

class SmartLock(SmartDevice):
    def __init__(self, name, room, mac_address,pin):
        super().__init__(name, room, mac_address)
        self.__pin=pin
        self.is_locked=True
        self._power_state = True
    
    def unlock(self,pin):
        success,message=self._check_device()
        if not success:
            return message
        if pin==self.__pin:
            self.is_locked=False
            return f"[{self._name}] Unlocked successfully."
        return f"[{self._name}] ALERT: Incorrect PIN. Lock remains engaged."
    
    def lock(self):
        success,message=self._check_device()
        if not success:
            return message
        self.is_locked=True
        return f"[{self._name}] Locked securely."
    
    def get_status(self):
        base_status = super().get_status()
        lock_state = "LOCKED" if self.is_locked else "UNLOCKED"
        return f"{base_status} | State={lock_state}"

class SmartHomeHub:
    def __init__(self,name):
        self.home_name=name
        self.devices={}
    
    def add_device(self,device:SmartDevice):
        mac=device.mac_address
        if mac in self.devices:
            print(f"Error: Device with MAC {mac} is already registered.")
        else:
            self.devices[mac]=device
            print(f"Successfully paired: {device._name} to {self.home_name} Hub.")
    
    def display_all_devices(self):
        for device in self.devices.values():
            print(device.get_status())
        print("-----------------------------------")
    
    def run_routine(self,routine_name):
        if routine_name=="Goodnight":
            for device in self.devices.values():
                if isinstance(device,SmartLight):
                    print(device.set_brightness(5))
                    device.set_color="light Green"
                if isinstance(device,SmartLock):
                    print(device.lock())
                if isinstance(device,SmartThermostat):
                    print(device.set_mode("Cool"))
                    print(device.set_temperature(68.0))
                if isinstance(device,SmartCamera):
                    print(device.power())
                    print(device.toggle_motion_detection())
                    print(device.trigger_motion())
        elif routine_name == "Morning":
            # Turn on bedroom/kitchen lights, set temp, disarm cameras
            for device in self.devices.values():
                if isinstance(device, SmartLight) and device._room in ["Bedroom", "Kitchen"]:
                    print(device.set_brightness(90))
                    device.set_color="white"
                elif isinstance(device, SmartThermostat):
                    print(device.set_mode("Heat"))
                    print(device.set_temperature(72.0))
                elif isinstance(device, SmartCamera):
                    print(device.toggle_motion_detection())
        else:
            print(f"Routine '{routine_name}' not found.")

if __name__ == "__main__":
    # 1. Check Class Method
    print(SmartDevice.get_total_device_count())

    # 2. Instantiate Devices
    living_room_light = SmartLight("Main Chandelier", "Living Room", "00:1A:2B:3C:4D:5E")
    bedroom_light = SmartLight("Bedside Lamp", "Bedroom", "00:1A:2B:3C:4D:5F")
    hallway_thermostat = SmartThermostat("Nest Thermostat", "Hallway", "00:1A:2B:3C:4D:60")
    front_door_cam = SmartCamera("Porch Cam", "Outside", "00:1A:2B:3C:4D:61", "4K")
    front_door_lock = SmartLock("Main Deadbolt", "Outside", "00:1A:2B:3C:4D:62", "1234")

    # 3. Check Class Method Again (Should be 5 now)
    print(SmartDevice.get_total_device_count())

    # 4. Initialize Hub and Add Devices
    hub = SmartHomeHub("My Smart Villa")
    hub.add_device(living_room_light)
    hub.add_device(bedroom_light)
    hub.add_device(hallway_thermostat)
    hub.add_device(front_door_cam)
    hub.add_device(front_door_lock)

    # 5. Play with Individual Device Methods (Variables, Logic, Validation)
    print("\n--- Manual Device Testing ---")
    print(living_room_light.power())
    print(living_room_light.set_brightness(150)) # Should fail (validation)
    print(living_room_light.set_brightness(75))  # Should pass
    print(living_room_light.set_color("#FF5733"))
    
    print(front_door_lock.unlock("9999")) # Should fail (encapsulation / private variable check)
    print(front_door_lock.unlock("1234")) # Should pass

    # 6. View Status
    hub.display_all_devices()

    # 7. Execute Hub Routines (The heavy business logic looping through inherited classes)
    hub.run_routine("Goodnight")
    
    # 8. Trigger an event
    print("\n--- Simulating Real World Event ---")
    print(front_door_cam.trigger_motion())
    
    # 9. Final Status Check
    hub.display_all_devices()