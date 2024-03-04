import subprocess
import os
import datetime


class USBDevnode():
    def __init__(self, port, hwversion = "3B+"):
        self.hwversion = self.autodetectHardwareVersion() #hwversion
        self.log_id = "USB"
        self.port = port
        self.debug("USBDevNode: Autodetected HW version [%s]" % self.hwversion)

    def autodetectHardwareVersion(self):
        hardwareVersion = self.getRaspberryPiModel()
        if "Raspberry Pi 3 Model B Plus Rev 1.3" in hardwareVersion:
            return "3B+"
        else:
            return "3B"
    def debug(self,message):
        dt = self.getDateTime()
        print("[%s] %s | %s" % (self.log_id, dt, message))
        with open ("/debug_mn.txt", "a") as myfile:
                myfile.write("[%s] %s | %s\n" % (self.log_id, dt, message))

    def getDateTime(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def getPort(self):
        return self.port

    def getHardwareVersion(self):
        return self.hwversion
    
    def getRaspberryPiModel(self):
        model = "UNKNOWN"  # too old, newer OS versions do have this procfile
        with open("/proc/device-tree/model") as myfile:
            model = myfile.read().strip()
        return model


    def scanPath(self, path):
        try:
            self.debug("Scanning path %s" % path)
            files = os.listdir(path)
            for file in files:
                if file.strip() == "tty":
                    #self.log("GPS ???")
                    #self.log("listing [%stty]" % path)
                    files2 = os.listdir("%stty" % path)
                    for file2 in files2:
                        #self.log("trying [%s]" % file2)
                        if file2[:3] == "tty":
                            return "/dev/%s" % file2
                if file[:3] == "tty":
                    fullpath = "%s%s" % (path, file[:3])
                    return "/dev/%s" % file
        except:
            return None

    def getDevnode(self):
        hwversion = self.hwversion
        port = self.port

        if (port == "GPS"):
            path = "/sys/devices/platform/soc/3f980000.usb/usb1/1-1/1-1.1/1-1.1.3/1-1.1.3.4/1-1.1.3.4:1.0/tty/"
            path = "/sys/devices/platform/soc/3f980000.usb/usb1/1-1/1-1.2/1-1.2:1.0/tty/"

        if (port == 2):
            if hwversion == "3B+":  #RPi3B+
                path = "/sys/devices/platform/soc/3f980000.usb/usb1/1-1/1-1.1/1-1.1.%d/1-1.1.%d:1.0/" % (port, port)
            else:
                path = "/sys/devices/platform/soc/3f980000.usb/usb1/1-1/1-1.%d/1-1.%d:1.0/" % (port, port)

        if (port == 3):
            if hwversion == "3B+":  #RPi3B+
                path = "/sys/devices/platform/soc/3f980000.usb/usb1/1-1/1-1.1/1-1.1.%d/1-1.1.%d:1.0/" % (port, port)
            else:
                path = "/sys/devices/platform/soc/3f980000.usb/usb1/1-1/1-1.%d/1-1.%d:1.0/" % (port, port)

        if (port == 4):
            if hwversion == "3B+":  #RPi3B+
                port = 3
                path = "/sys/devices/platform/soc/3f980000.usb/usb1/1-1/1-1.%d/1-1.%d:1.0" % (port, port)
            else:
                path = "/sys/devices/platform/soc/3f980000.usb/usb1/1-1/1-1.%d/1-1.%d:1.0/" % (port, port)

        if (port == 5):
            if hwversion == "3B+":  #RPi3B+
                port = 2
                path = "/sys/devices/platform/soc/3f980000.usb/usb1/1-1/1-1.%d/1-1.%d:1.0" % (port, port)
            else:
                path = "/sys/devices/platform/soc/3f980000.usb/usb1/1-1/1-1.%d/1-1.%d:1.0/" % (port, port)

        devnode = self.scanPath(path)
        if devnode is None:
            path = "%s/tty" % path
            devnode = self.scanPath(path)
        self.debug("scanPath returned [%s]" % devnode)
        return devnode
