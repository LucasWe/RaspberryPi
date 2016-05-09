import paramiko
import sys
import re
import os


def getList():

    print "Die Informationen werden nun vom RaspberryPi geladen.\n"

    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('192.168.0.105', username='pi', password='raspberry')
    sftp = client.open_sftp()
    sftp.get("/home/pi/Desktop/temperaturelist.txt", "C:\Users\Lucas\PycharmProjects\Temperature_pie\Temperature.txt")
    sftp.close()
    client.close()



def getInput():
    print "Fuer die aktuelle Temperatur druecken sie [Enter]."
    print "Fuer die minimale und maximale Temperatur tippen Sie max."
    print "Fuer die gesamte Historie tippen sie 'all'."
    print "Um das Programm zu beenden tippen sie exit."
    while 1:
        inputt = raw_input("Ihre Eingabe bitte: ")
        if inputt == "exit":
            os.remove("C:\Users\Lucas\PycharmProjects\Temperature_pie\Temperature.txt")
            sys.exit(1)

        if (inputt != "max") and (inputt !="" ) and (re.search("\d\d.\d\d.\d\d\d\d", inputt) == None) and (inputt != "all" ):
            print "\nDie Eingabe war ungueltig. Bitte wiederholen."
            continue
        return inputt
        break


def listList():
    list = open("C:\Users\Lucas\PycharmProjects\Temperature_pie\Temperature.txt")
    listlist = []
    inti = 0
    for line in list:
        listlist.append(line)
        inti += 1
    list.close()
    return (listlist, inti)

def searchList(listlist, end):
    end2 = end - 1
    param = getInput()

    if param == "all":
        counter = 0
        print "\n\n"
        while counter < end:
            print listlist[counter]
            counter += 1
        print "\n"

    if param == "":
        search = re.search(" \d\d.\d ", listlist[end2])
        text = search.group()
        search = re.search("\d\d:\d\d:\d\d", listlist[end2])
        actual_time = search.group()
        search = re.search("\d\d.\d\d.\d\d\d\d", listlist[end2])
        actual_date = search.group()
        print "\nDie aktuelle Temperatur betraegt: %s Grad Celsius\n(gemessen am %s um %s).\n" % (text, actual_date, actual_time)

    if param == "max":
        minimum = 1000.0
        maximum = 0.0
        while end2 >= 4:
            if re.search(" \d\d.\d ", listlist[end2]):
                search = re.search(" \d\d.\d ", listlist[end2])
                end2 -= 1
                temp1 = search.group()
                if float(temp1) > maximum:
                    maximum = float(temp1)
                    suche = re.search("\d\d.\d\d.\d\d\d\d", listlist[end2])
                    maximumdate = suche.group()
                    suche = re.search("\d\d:\d\d:\d\d", listlist[end2])
                    maximumtime = suche.group()
                if float(temp1) < minimum:
                    minimum = float(temp1)
                    suche = re.search("\d\d.\d\d.\d\d\d\d", listlist[end2])
                    minimumdate = suche.group()
                    suche = re.search("\d\d:\d\d:\d\d", listlist[end2])
                    minimumtime = suche.group()
            end2 -= 1

        print "\nDie minimale Temperatur war: %2.1f Grad Celsius\n(am %s um %s)." % (minimum, minimumdate, minimumtime)
        print "Die maximale Temperatur war: %2.1f Grad Celsius\n(am %s um %s).\n" % (maximum, maximumdate, maximumtime)

    if re.search("\d\d.\d\d.\d\d\d\d", param):
        minimum = 1000.0
        maximum = 0.00005
        while end2 >= 4:
            if re.search(param, listlist[end2]) != None:
                search = re.search(" \d\d.\d ", listlist[end2])
                end2 -= 1
                temp1 = search.group()
                if float(temp1[1:]) > maximum:
                    maximum = float(temp1[1:])
                    suche = re.search("\d\d:\d\d:\d\d", listlist[end2])
                    maximumtime = suche.group()
                if float(temp1[1:]) < minimum:
                    minimum = float(temp1[1:])
                    suche = re.search("\d\d:\d\d:\d\d", listlist[end2])
                    minimumtime = suche.group()
            end2 -= 1
        if (maximum == 0.00005) or (minimum == 1000.0):
            print "\nDas angegebene Datum konnte nicht gefunden werden."
            print "Bitte nochmal versuchen.\n"
            return False

        print "\nDie minimale Temperatur am %s war: %2.1f Grad Celsius\n(um %s)." % (param, minimum, minimumtime)
        print "Die maximale Temperatur am %s war: %2.1f Grad Celsius\n(um %s).\n" % (param, maximum, maximumtime)


    return False


ready = False
getList()
listlist, end = listList()
while ready == False:
    ready = searchList(listlist, end)
os.remove("C:\Users\Lucas\PycharmProjects\Temperature_pie\Temperature.txt")