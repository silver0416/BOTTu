import os
import subprocess
import sys

# Check the Python version
result = subprocess.run(['python', '--version'], stdout=subprocess.PIPE)
python_version = result.stdout.decode().strip()
print('Python version:', python_version)

python_path = sys.executable
print('Python path:', python_path)

subprocess.run(['git', 'pull'])
subprocess.run([python_path, '-m', 'pip', 'install', '-r', 'requirements.txt'])


os.system('{} ./core/bot.py'.format(python_path))
