import os
import subprocess
import sys
import shutil


python_path = sys.executable
print('Python path:', python_path)

subprocess.run(['git', '-c', 'diff.mnemonicprefix=false', '-c', 'core.quotepath=false', '--no-optional-locks', 'pull', 'origin', 'main'])
subprocess.run([python_path, '-m', 'pip', 'install', '-r', 'requirements.txt'])

# check if the operating system is linux,if it is,then check if FFMPEG and gifski are installed
if os.name == 'posix':
    # check if FFMPEG is installed
    if not shutil.which('ffmpeg'):
        print('FFMPEG is not installed, please install it first!')
        exit()
    # check if gifski is installed
    if not shutil.which('gifski'):
        print('gifski is not installed, please install it first!')
        exit()



os.system('{} ./core/bot.py'.format(python_path))
