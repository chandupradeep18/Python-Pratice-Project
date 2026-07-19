#14-07-2026
import time
from datetime import datetime

#decorator
"""
def making_time(method):
    def enhanced():
        start=time.time()
        method()
        end=time.time()
        print(end-start,'Seconds')
    return enhanced

@making_time
def brew_tea():
    print("Prepairing Tea")
    time.sleep(2)
    print("Tea is Ready")

brew_tea()"""
#decorator with Parameters and return value
def making_time_proccess(drink_method):
    def modify(**kwargs):
        print("Starting at ",datetime.now())
        start=time.time()
        result=drink_method(**kwargs)
        end=time.time()
        print("Ending at ",datetime.now())
        print(end-start,'Seconds to Make ',kwargs.get('type',""))
        return result
    return modify

@making_time_proccess
def Refreshing_drink(type:str,sleep_time:int):
    print('Prepairing a Refreshing Drink ',type)
    time.sleep(sleep_time)
    print('Your Refreshing Drink is Ready to Serve')
    return 'Your Refreshing Drink is Ready to Serve'
print(Refreshing_drink(type='Cold Black Coffece',sleep_time=5))

@making_time_proccess
def Make_cake():
    print('Prepairing a Cake')
    time.sleep(2)
    print('Your Cake is Ready to Serve')
    return datetime.now()
print(Make_cake())

