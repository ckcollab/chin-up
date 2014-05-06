import subprocess

from polished.backends import DjangoBackend


class ChinupDjangoBackend(DjangoBackend):
    SCRIPT = ''

    def __init__(self, *args, **kwargs):
        super(ChinupDjangoBackend, self).__init__(*args, **kwargs)
        self.SCRIPT = open("generate_data.py", "r").read()

        print 'WILL EXECUTE %s' % self.SCRIPT

    def prepare_page(self, *args, **kwargs):
        super(ChinupDjangoBackend, self).prepare_page(*args, **kwargs)

        print 'PREPARING PAGE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'

        subprocess.call(["python", "manage.py", "shell", "<", self.SCRIPT])
