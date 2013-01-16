# vim: set fileencoding=utf-8 :
import subprocess


class ShellParser(object):
    def __init__(self, command):
        self.command = command

    def parse(self, text, cwd=None, encoding='utf-8'):
        p = subprocess.Popen(self.command, shell=True, cwd=cwd,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE)
        # the text should be encoded to use in Shell
        stdout, stderr = p.communicate(text.encode(encoding))
        # the text should be decoded to use in Python
        return unicode(stdout, encoding)
