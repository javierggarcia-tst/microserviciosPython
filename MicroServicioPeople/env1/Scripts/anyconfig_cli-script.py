#!C:\Users\leith\source\repos\FlaskApi\FlaskApi\env1\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'anyconfig==0.9.8','console_scripts','anyconfig_cli'
__requires__ = 'anyconfig==0.9.8'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('anyconfig==0.9.8', 'console_scripts', 'anyconfig_cli')()
    )
