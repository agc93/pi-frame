import subprocess


class ProcessDetails(object):
    """Container for process details
    """

    def __init__(self, process_name):
        self.ProcessName = process_name

    def get_PIDs(self):
        try:
            out = subprocess.check_output(['pidof', self.ProcessName], stderr=subprocess.PIPE, universal_newlines=True)
        except subprocess.CalledProcessError as err:
            out = err.output
        # raise
        if out != None and out != "":
            out = out.rstrip('\n')
            l = out.split(' ')
            return l
        else:
            return None

    def get_process(self):
        try:
            out = subprocess.check_output(['pidof', self.ProcessName], stderr=subprocess.PIPE, universal_newlines=True)
        except subprocess.CalledProcessError as err:
            out = err.output
        if out is not None and out != "":
            out = out.rstrip('\n')
            l = out.strip(' ')
            #return l
            try:
                s = subprocess.check_output(['ps', '-p', out], stderr=subprocess.PIPE, universal_newlines=True)
            except subprocess.CalledProcessError as err:
                s = err.output
            detail = s.split('\n')
            if len(detail) != 1:
                status = detail[1].rsplit()
                return ProcessInfo(l, status[1], status[2], status[3])


class ProcessInfo(object):
    def __init__(self, pid, console, time, process):
        self.PID = pid
        self.Console = console
        self.Time = time
        self.Process = process
