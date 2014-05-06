import subprocess
import tempfile

from polished.backends import DjangoBackend


class ChinupDjangoBackend(DjangoBackend):
    TEMP_SCRIPT = None

    def __init__(self, *args, **kwargs):
        super(ChinupDjangoBackend, self).__init__(*args, **kwargs)
        script_data = open("generate_data.py", "r").read()

        self.TEMP_SCRIPT = tempfile.NamedTemporaryFile(delete=False)
        self.TEMP_SCRIPT.write(script_data)

    def prepare_page(self, *args, **kwargs):
        super(ChinupDjangoBackend, self).prepare_page(*args, **kwargs)

        print 'PREPARING PAGE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'

        try:
            #subprocess.call(["python", "manage.py", "shell", "<", self.SCRIPT])
            subprocess.check_call('python manage.py shell < %s' % self.TEMP_SCRIPT.name, shell=True)
        except Exception:
            pass
