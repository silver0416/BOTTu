import os
import subprocess
import sys


python_path = sys.executable
print('Python path:', python_path)

subprocess.run(['git', 'pull'])
subprocess.run([python_path, '-m', 'pip', 'install', '-r', 'requirements.txt'])


os.system('{} ./core/bot.py'.format(python_path))
