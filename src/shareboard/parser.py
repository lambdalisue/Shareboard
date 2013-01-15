# vim: set fileencoding=utf-8 :
import subprocess


class ShellParser(object):
    def __init__(self, command):
        self.command = command

    def parse(self, data):
        p = subprocess.Popen(self.command, shell=True,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE)
        stdout, stderr = p.communicate(data.encode('utf-8'))
        return unicode(stdout, 'utf-8')
