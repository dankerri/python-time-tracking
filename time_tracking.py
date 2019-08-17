#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
import time
from PIL import Image
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.figsize'] = (18.0, 8.0) #figure窗口的大小


OR_LOG = './or_log.txt'
LOG = './output/log.txt'



# Helper Functions

# process data in or_log.txt
def getList(path):

    # ap_list[desc, min, percent] 
    ap_list = []
    last_start = '00:00'

    with open(path) as f:
        for line in f.readlines():
            
            record = []
            
            temp = line.split()
            if(temp[0] == '@' or ''):
                start = last_start
            else:
                start = temp[0]
            end = temp[1].strip() 
            desc = temp[2].strip() 

            # print("START: %s" % start)
            # print("END: %s" % end)
            # print("Des: %s" % desc)
            
            timeStart = datetime.strptime(start, '%H:%M')
            timeEnd = datetime.strptime(end, '%H:%M')
            amount = timeEnd -timeStart

            #  start calculating
            minute = int(amount.seconds / 60)
            # print("minute: %s" % minute)
            
            # hour = minute / 60
            # hour_minute = minute % 60
            # print("hour: %sh%sminute" % (hour, hour_minute) )
            
            fullDay = 24.0*60.0
            f_min = float(minute)
            percent = (f_min / fullDay) * 100
            percent = round(percent, 2)
            # print("percent: %s" %  percent)

            
            # print("==================")

            last_start = end
            record.extend([desc, minute, percent])
            ap_list.append(record)
        
        return ap_list
# print a list to console
def printRecord(theList): 

    for list in theList:
        desc = list[0].replace('.', ' ')
        minutes = list[1]
        percent = list[2]
        
        hour = int(minutes / 60)
        hour_minute = int(minutes % 60)  

        # \033[1;31m %s \033[0m
        # %s is the content

        print('\033[1;33m%s\033[0m' % desc)
        print('Percent:   \033[1;31m %s%% \033[0m                 \033[1;32m%smins\033[0m(\033[1;32m%sh%sm\033[0m) ' % (percent, minutes, hour, hour_minute))
        print('\n')
# helper function for sort list
def takeSecond(elem):
    return elem[1]
def minToHour(min): 
    hour = int(min / 60)
    hour_min = int(min % 60)

    if ( hour == 0):
        return str(hour_min) + 'm'
    return str(hour) + 'h' + str(hour_min) + 'm'

# functions
# ======================================
# Generate log.txt and Diagram

# show styled time tracking list on console in different way
def checkLog(or_log, order=-1): 
    theList =  getList(or_log)
    if(order == 1):
        theList.sort(reverse=True, key=takeSecond)

    printRecord(theList)

# draw bar diagram
def gennBar(or_log, save=False, order=False):
    theList =  getList(or_log)
    path = './output/Bar/'
    activity = []
    minutes = []

    if(order):
        theList.sort(reverse=True, key=takeSecond)
        path='./output/OrderedBar/'


    for list in theList:
        activity.append(list[0])
        minutes.append( int(list[1]) )

    plt.bar(range(len(activity)), minutes, width=0.35, tick_label=activity)
    plt.subplots_adjust(bottom=0.25)

    plt.xticks(rotation=-20)
    plt.xlabel("ACTIVITY", fontsize=20)  #设置X轴Y轴名称  
    plt.ylabel(u"花费时间")

    # minToHourList = []
    # for i in minutes:
    #     i = minToHour(i)
    #     minToHourList.append(i)

    for a,b in zip(range(len(activity)),minutes):
        text = minToHour(b)
        plt.text(a, b+0.05, text, ha='center', va= 'bottom',fontsize=10) 
    
    
    theDate = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    plt.title(theDate + u'时间使用情况')
    
    if(save): 
        plt.savefig(path + theDate + '.png')
        plt.close('all')
    else:
        plt.show()
        plt.close('all')

# draw pie diagram
def genPie(or_log, save=False):
    theList = getList(or_log)
    minutes = []
    activity = []

    for list in theList:
        activity.append(list[0] + ', ' + minToHour(list[1]) )
        minutes.append( int(list[1]) )

    plt.figure(figsize=(10, 10))
    plt.pie(minutes,labels=activity, autopct='%1.2f%%') #画饼图（数据，数据对应的标签，百分数保留两位小数点）
    plt.title("Pie chart")
    
    theDate = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    plt.title(theDate + u'时间使用情况')
    if(save): 
        plt.savefig('./output/Pie/' + theDate + '.png')
    else:
        plt.show()

def genLog(or_log, log) : 
    theList = getList(or_log)
    # print(theList)
    with open(log, 'a') as f: 

        f.write(time.strftime('%Y-%m-%d',time.localtime(time.time())))
        f.write('\n')

        for record in theList:
            f.write( record[0] )
            f.write( str(', ') )
            f.write( str(record[1]) )
            f.write( str(', ') )
            f.write( str(record[2]) ) 
            
            f.write('\n')
        f.write('\n')

        # printRecord(theList)
        genBar(OR_LOG, True)
        genPie(OR_LOG, True)
        print("\033[1;32mGenerated log.txt and the Diagram !  \033[0m\n")

def genBar(or_log, save=False):

    path='./output/Bar/'
    theDate = time.strftime('%Y-%m-%d',time.localtime(time.time()))

    theList =  getList(or_log)
    activity = []
    minutes = []

    s_theList = getList(or_log)
    s_theList.sort(reverse=True, key=takeSecond)
    s_activity = []
    s_minutes = []

    # p_activity = []


    for list in theList:
        activity.append(list[0])
        minutes.append( int(list[1]) )
    for list in s_theList:
        s_activity.append(list[0])
        s_minutes.append( int(list[1]) )
    # for list in theList:
        # p_activity.append(list[0]+', '+minToHour(list[1]))


    # Start drawing
    plt.figure(1)
    plt.subplots_adjust(hspace=0.9)
    plt.title(theDate)


    # Bar
    plt.subplot(211)
    plt.bar(range(len(activity)), minutes, width=0.35, tick_label=activity)
    # plt.subplots_adjust(bottom=0.25)
    plt.xticks(rotation=-20)
    # plt.xlabel("ACTIVITY", fontsize=20)  #设置X轴Y轴名称  
    plt.ylabel(u"花费时间")
    # set text of each bar.
    for a,b in zip(range(len(activity)),minutes):
        text = minToHour(b)
        plt.text(a, b+0.05, text, ha='center', va= 'bottom',fontsize=10) 
    # plt.title(theDate + u'时间使用柱状图')

    plt.subplot(212)
    plt.bar(range(len(s_activity)), s_minutes, width=0.35, tick_label=s_activity)
    # plt.subplots_adjust(bottom=0.25)
    plt.xticks(rotation=-20)
    # plt.xlabel("ACTIVITY", fontsize=20)  #设置X轴Y轴名称  
    plt.ylabel(u"花费时间")
    # set text of each bar.
    for a,b in zip(range(len(s_activity)),s_minutes):
        text = minToHour(b)
        plt.text(a, b+0.05, text, ha='center', va= 'bottom',fontsize=10) 
    # plt.title(theDate + u'时间使用柱状图')
    
    if(save): 
        plt.savefig(path + theDate + '.png')
        plt.close('all')
    else:
        plt.show()
        plt.close('all')


# entry of programm
# ========================================
def main():
    flag = 1
    list_from_log = getList(OR_LOG)

    while(flag > 0): 
        print("---------------\033[1;31m TIME TRACKING \033[0m----------------")
        print("1. Checkout Time Tracking Of Today.")
        print("2. Show Bar.")
        print("3. Show Pie.")
        print("0. Generate Time Tracking Log and Diagram.")
        print("q. Exit.")
        print("--------------------------------------------")
        operation = input("\033[1;33m choose operation:  \033[0m")
        ex = 'q'

        print('\n')
        if ( operation == str(1) ): 
            checkLog(OR_LOG)
        elif ( operation == str(11) ):
            checkLog(OR_LOG, 1)
        elif ( operation == str(2) ):
            genBar(OR_LOG)
        elif ( operation == str(3) ):
            genPie(OR_LOG)
        elif ( operation == str(0) ): 
            genLog(OR_LOG, LOG)
        elif ( str(operation) == ex ):
            print("\033[1;33m Exit. \033[0m")
            flag = -1

        else:
            print("\033[1;33m Please Choose the Vaild Operation. \033[0m")
            print("\n\n")
main()
