# a little file that activates the Thermometer  an reads it regularly
import re
# import matplotlib.pyplot as plt
import time
import shutil

print "Welcome to the Temperature-NSA. :-)"
print "Das Programm laeuft nun so vor sich hin."


def getCPUTemperature():
    tempFile = open("/sys/class/thermal/thermal_zone0/temp")
    cpu_temp = tempFile.read()
    tempFile.close()
    return float(cpu_temp) / 1000

# Return % of CPU used by user as a character string
"""def getCPUuse():
    CPU_use = os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip()
    CPU_use = str(CPU_use)
    return CPU_use

cpu_use = getCPUuse()
print cpu_use"""

# datum und Uhr zeit herausfinden
# Type gibt an, welche Infos man haben will
def getTimeDate(type):
    timedate = time.localtime()
    jahr, monat, tag = timedate[0:3]
    stunde, minute, sekunde = timedate[3:6]
    int_tag = timedate[6]
    wochentag = ""
    if int_tag == 0:
        wochentag = "Montag"
    if int_tag == 1:
        wochentag = "Dienstag"
    if int_tag == 2:
        wochentag = "Mittwoch"
    if int_tag == 3:
        wochentag = "Donnerstag"
    if int_tag == 4:
        wochentag = "Freitag"
    if int_tag == 5:
        wochentag = "Samstag"
    if int_tag == 6:
        wochentag = "Sonntag"

    if type == "wochentag":
        return wochentag
    if type == "tag":
        return tag
    if type == "monat":
        return monat
    if type == "jahr":
        return jahr
    if type == "stunde":
        return stunde
    if type == "minute":
        return minute
    if type == "sekunde":
        return sekunde
    if type == "alles":
        return wochentag, tag, monat, jahr, stunde, minute, sekunde


def checkOverhead():
    monat = getTimeDate("monat")
    monat = int(monat)

    # to fix that problem of a new started year (month can't be lower than 1)
    if monat > 2:
        monat -=  2
    elif monat <= 2:
        monat += 10

    list = open("/home/pi/Desktop/temperaturelist.txt", "r")
    list2 = open("/home/pi/Desktop/temperaturelist2.txt", "w")
    monat_text = ".%02i." % monat
    print monat_text
    for line in list:
        if monat_text not in line:
            list2.write(line)
    list.close()
    list2.close()
    shutil.move("/home/pi/Desktop/temperaturelist2.txt", "/home/pi/Desktop/temperaturelist.txt")


# variable for the duration measure of the program
start_time = time.time()

# this variable counts how often it hast to bei tried to open the document
interupts = 0

#the former temperature for comparison
former_temp = 0
former_monat = getTimeDate("monat")



while 1:


    # often this throws an exception, when the file is opened by the user
    while 1:
        try:
            w1_slave = open("/sys/bus/w1/devices/10-000802db50ea/w1_slave", "r")
            text = w1_slave.readlines()
            w1_slave.close()
            # merging text from list to string
            text = "".join(text)
            search = re.search("YES", text)
            is_okay = search.group()
        except:
            # if interupts == 0:
                # print "Das File1 konnte nicht durchsucht werden. Es wird erneut versucht."
            interupts += 1
            time.sleep(1)
            continue
        break

    temperature_list = []
    time_list = []

    # Only if the thermostat function correctly is_okay will be YES
    if is_okay == "YES":


        # search group often throws an exception, so we will try again
        # it throws the exception, when the BUS writes something in w1_slave
        while 1:
            try:
                search2 = re.search(r"t=\d{5}", text)
                temp = search2.group()
            except:
                # if interupts == 0:
                    # print "Das File2 konnte nicht durchsucht werden. Es wird erneut versucht."
                interupts += 1
                time.sleep(2)
                continue
            break

        # calculating the temp from the string file
        temp = temp[2:]
        temp = float(temp)
        temp = temp/1000
        temperature_list.append(temp)

        (wochentag, tag, monat, jahr, stunde, minute, sekunde) = getTimeDate("alles")

        """timedate = time.localtime()
        jahr, monat, tag = timedate[0:3]
        stunde, minute, sekunde = timedate[3:6]
        int_tag = timedate[6]
        wochentag = ""
        if int_tag == 0:
            wochentag = "Montag"
        if int_tag == 1:
            wochentag = "Dienstag"
        if int_tag == 2:
            wochentag = "Mittwoch"
        if int_tag == 3:
            wochentag = "Donnerstag"
        if int_tag == 4:
            wochentag = "Freitag"
        if int_tag == 5:
            wochentag = "Samstag"
        if int_tag == 6:
            wochentag = "Sonntag"""""


        try:
            temp_file = open("/home/pi/Desktop/temperaturelist.txt", "r")
            temp_file_text = temp_file.readlines()
            temp_file.close()
            # if not temp_file_text would be a list (?)
            temp_file_text = "".join(temp_file_text)


        except:
            print "temperaturelist.txt wird neu angelegt."
            temp_file_text = "Das ist eine chronologische Anzeige der Temperatur in Lucas' Zimmer.\nDahinter ist in Klammern die Temperatur der CPU in Grad Celsius.\n"
            temp_file = open("/home/pi/Desktop/temperaturelist.txt", "w")
            temp_file.write(temp_file_text)
            temp_file.close()
            time.sleep(2)

        cpu_temp = int(getCPUTemperature())

        # controll that the temperature has changed, so that the file won't be filled with redundant information
        temp_diff = temp - former_temp
        if (temp_diff > 0.5) or (temp_diff < -0.5):

            # print temp

            temp_file = open("/home/pi/Desktop/temperaturelist.txt", "w")
            new_line = "\n%s der %02i.%02i.%04i um %02i:%02i:%02i -> %4.1f Grad Celsius (CPU: %02i)" % (wochentag, tag, monat, jahr, stunde, minute, sekunde, temp, cpu_temp)

            # if there was a interupt it will be seen in the temperaturelist.txt
            if interupts > 5:
                interupt_time = interupts * 2
                interupt_message = "\nDas Programm wurde an dieser Stelle fuer %i Sekunden unterbrochen." % interupt_time
                temp_file.write(temp_file_text + interupt_message)
                interupts = 0
            elif interupts == 0:
                temp_file.write(temp_file_text + new_line)
            elif interupts <= 5:
                temp_file.write(temp_file_text + new_line)
                interupts = 0

            temp_file.close()
            former_temp = temp

        time_list.append(time.time())
        interupts = 0

        # delete the old information
        if (int(monat) - int(former_monat) == 2) or (int(monat) - int(former_monat) < 0):
            checkOverhead()
            former_monat = monat
        # the time to the next measurement
        # time.sleep(10)

        # plt.plot(time_list, temperature_list)
        # plt.show()
        # plt.close()

        # time measurement
        loop_time = time.time()
        deltaT = loop_time - start_time

        # print "Das Programm laeuft seit %i Sekunden." %deltaT

