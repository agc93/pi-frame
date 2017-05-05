import subprocess


class ProcessDetails(object):
    """Container for process details
    """

    def __init__(self, processName):
        self.ProcessName = processName
    def GetPIDs(self):
        p = subprocess.Popen(['pidof', self.ProcessName], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out,err = p.communicate()
        #raise
        if out != None and out != "":
            out = out.rstrip('\n')
            l = out.split(' ')
            return l
        else:
            return None
    def GetProcess(self):
        p = subprocess.Popen(['pidof', self.ProcessName], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out,err = p.communicate()
        if out != None and out != "":
            out = out.rstrip('\n')
            l = out.strip(' ')
            return l
            s = subprocess.Popen(['ps', '-p', out], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            detail = s.stdout.readlines()
            if len(detail) != 1:
                status = detail[1].rsplit()
                return ProcessInfo(l, status[1], status[2], status[3])
class ProcessInfo(object):
    def __init__(self, pid, console, time, process):
        self.PID = pid
        self.Console = console
        self.Time = time
        self.Process = process
