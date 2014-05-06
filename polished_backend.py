import subprocess
import tempfile

from polished.backends import DjangoBackend


class ChinupDjangoBackend(DjangoBackend):
    SCRIPT_PATH = ''

    def __init__(self, *args, **kwargs):
        super(ChinupDjangoBackend, self).__init__(*args, **kwargs)
        script_data = open("generate_data.py", "r").read()

        f = tempfile.NamedTemporaryFile()
        f.write(script_data)

        self.SCRIPT = f.name

    def prepare_page(self, *args, **kwargs):
        super(ChinupDjangoBackend, self).prepare_page(*args, **kwargs)

        print 'PREPARING PAGE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'

        subprocess.call(["python", "manage.py", "shell", "<", self.SCRIPT])
        #subprocess.check_call('python manage.py shell < %s' % self.SCRIPT, shell=True)
