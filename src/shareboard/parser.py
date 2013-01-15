import subprocess


class ShellParser(object):
    def __init__(self, command):
        self.command = command

    def parse(self, data):
        p = subprocess.Popen(self.command, shell=True,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE)
        stdout, stderr = p.communicate(data)
        return stdout
