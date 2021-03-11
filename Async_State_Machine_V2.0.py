import time
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil, os
import polling2
import asyncio
class MyHandler(FileSystemEventHandler):
    def on_created(self, event): #observes for the file in the source location - Triggers when new file is placed.
        Destination = 'C:\Python\Python38\Test_File_Handler_Destination'
        i=event.src_path[44:-4:] #To get the File Name
        poll_source(i,event.src_path) #Function call : Polling the intermediate status - Checking if the file is received to Source/not.
        with open("C:\Python\Python38\Test_File_Handler_Source\%s.txt"%i,"r") as fp:
            content = fp.read() # Reading the File
        with open('C:\Python\Python38\Test_File_Handler_Destination\All_File_Data.txt','a') as fw:
            fw.write('File Name: '+i+' Time: '+str(current_time()))
            fw.write('\n'+content) # Writing the data to another file named "All_File_Data" along with File Name and Time
        print("\nReading Data Completed\n")
        shutil.move(os.path.join('C:\Python\Python38\Test_File_Handler_Source', i+'.txt'), Destination) #Moving the file from Source to Destination
        poll_destination(i,Destination) #Function call : Polling the intermediate status - Checking whether the file is received to Destination/not.

def poll_source(filename,path):
    try:
        file_handle = polling2.poll(lambda: open('C:\Python\Python38\Test_File_Handler_Source\%s.txt'%filename), ignore_exceptions=(IOError,), timeout=3, step=0.1) #Check at source for 3 seconds
        if(file_handle):
            print("File Received to Source\n \n*Path : %s \n*File Name: %s \n*Time : %s\n" %(path,filename,current_time()))
    except FileNotFound:
        print("File Not Received to Source")

def poll_destination(filename,path):
    try:
        file_handle = polling2.poll(lambda: open('C:\Python\Python38\Test_File_Handler_Destination\%s.txt'%filename), ignore_exceptions=(IOError,), timeout=3, step=0.1) # Check at Destination for 3 seconds
        if(file_handle):
            print("File Moved to Destination\n \n*Path : %s \n*File Name: %s \n*Time : %s\n" %(path,filename,current_time()))
            asyncio.run(main()) # Upon successful verification of file at Destination - Trigger 3 Jobs Asynchronously
    except FileNotFound:
        print("File Not Received to Destination")
        
def current_time():
    return datetime.now().time()

async def Job1():
    await asyncio.sleep(1)
    print("Run Job1"+" Time: "+str(current_time()))

async def Job2():
    await asyncio.sleep(1)
    print("Run Job2"+" Time: "+str(current_time()))

async def Job3():
    await asyncio.sleep(1)
    print("Run Job3"+" Time: "+str(current_time()))


async def main():
    await asyncio.gather(
        asyncio.create_task(Job1()),
        asyncio.create_task(Job1()),
        asyncio.create_task(Job3()),
    )

event_handler = MyHandler() #Watch dog initialiser steps
observer = Observer()
observer.schedule(event_handler, path='C:\Python\Python38\Test_File_Handler_Source', recursive=False)
observer.start()
while True:
    try:
        pass
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
