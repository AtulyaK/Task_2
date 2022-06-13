# Task 2: 
#Use the GTFS files for (i) ACERail  (ii) CCJPA  (iii) SJJPA (GTFS-AMTRAK)
#Given the current time, time(), display the following:
#Completed Trips
#Ongoing Trips
#Upcoming Trips

#The plan is to first pull from the current time. 
#Then if start time is > than current put in future
#if start time< current time< end time then current trains
#if end time < current then past trains
#That is basically how to design it.

fileName = input("Input File Name: ")
import tabulate
import string
import datetime
import pytz
from datetime import datetime
from pytz import timezone
comArray = []
currArray = []
futArray = []
def findTimeSec(time):
  time = time.replace('"', "")
  timeS = time.split(':')
  timeSec = (int(timeS[0])*60)+int(timeS[1])
  return timeSec
# import the datetime to get the times of arrival and departure
date_format='%m_%d_%Y:%H_%M'
# reformats the information to date and time separated by space
date = datetime.now(tz=pytz.utc)
date = date.astimezone(timezone('US/Pacific'))
# sets the date time to PST
pstDateTime=date.strftime(date_format)
dateTime = pstDateTime.split(':')
time = dateTime[1].split('_')
# Splits the date time and time into relevant pieces to time is split by a colon
timeMin = (int(time[0])*60)+int(time[1])
# Converts time from hours and mintues to minutes
file = open(fileName,"r")
data = file.read()
# pulls the information from the stop times file 
trainArray = data.splitlines()
length = len(trainArray)
# This was copied from Task 1 because we need to separate the data to parse it
atIndex=0
dtIndex=0
# Sets Departure and Arrival time index to 0
data=trainArray[0].split(',')
# Splits train array into the right chunks to easily utilize data from relevant 
for i in data:
  if(i=='arrival_time'):
    atIndex=data.index(i)
  if(i=='departure_time'):
    dtIndex=data.index(i)
#   
sData = trainArray[1].split(',')
sData[atIndex] = sData[atIndex].replace('"', "")
tArr = (sData[atIndex].split(':'))
startTime = (int(tArr[0])*60)+int(tArr[1])
# sets variable startTime equal to the arrival times in minutes and finds the relevant times with sData
dData = trainArray[length-1].split(',')
dData[dtIndex] = dData[dtIndex].replace('"', "")
tDep = dData[dtIndex].split(':')
endTime = (int(tDep[0])*60)+int(tDep[1])
# Does the same as startTime except for departure times
tempStart = startTime
tempEnd = startTime
trains = []
for id in range(length-2):
  fData = (trainArray[id+1]).split(',')
  nData = (trainArray[id+2]).split(',')
  if(fData[0]==nData[0]):
    if((findTimeSec(fData[atIndex]))<tempStart):
      tempStart = findTimeSec(fData[atIndex])
    if((findTimeSec(nData[dtIndex]))>tempEnd):
      tempEnd = findTimeSec(nData[dtIndex])
  else:
    trains.append(fData[0]+","+str(tempStart)+","+str(tempEnd))
    tempStart = findTimeSec(nData[atIndex])
    tempEnd = findTimeSec(nData[dtIndex])
lastTrainData = trainArray[length-1].split(',')
lastID = lastTrainData[0]
trains.append(lastID+","+str(tempStart)+","+str(tempEnd))
for train in trains:
  tInfo = train.split(',')
  if((int(tInfo[1])< int(timeMin)) and (int(timeMin) < int(tInfo[2]))):
    currArray.append(tInfo[0])
  elif(int(tInfo[1])< int(timeMin)):
    comArray.append(tInfo[0])
  elif(int(tInfo[2])> int(timeMin)):
    futArray.append(tInfo[0])
print("Completed Trips: ")
print(comArray)
print("Current Trips: ")
print(currArray)
print("Future Trips: ")
print(futArray)