import configparser
from colorama import init, Fore
import os
import subprocess
import sys
import re
import json




class ThothTerminal:

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        init()

        self.name = self.config['Emulator']['username']
        self.start_dir = self.config['Directory']['start_dir']
        self.quit_command = self.config['Commands']['quit_command']

        self.exp = re.compile("cd .")

        with open('pallete.json') as f:
            data = f.read()

        self.color_codes = json.loads(data)

    def start(self):

        try:
            os.chdir(self.start_dir)
            color = self.color_codes.get(self.config['Emulator']['fore_color'])
            errorColor = self.color_codes.get(self.config['Emulator']['error_color'])
            if color != None and errorColor != None:
                print(color + self.config['Emulator']['start_line'])
                while True:
                    current_dir = os.getcwd()
                    input_text = f"{self.name} in *{current_dir}* ∴ "
                    inp = input(input_text)
                    match = bool(re.match(self.exp, inp))
                    if inp.lower() == self.quit_command:
                        sys.exit()
                    elif match == True:
                        split_inp = inp.split(" ")
                        final_inp = " ".join(split_inp[1:])
                        try:
                            os.chdir(final_inp)
                        except FileNotFoundError:
                            err = "thothemu: cd: {}: No such file or directory".format(final_inp)
                            print(self.error_color + err)
                            print(self.error_color + color)
                    else:
                        subprocess.run(inp, shell=True)
            else:
                print(Fore.RED + 'Invalid color code. Quitting.')
                sys.exit()
        except KeyboardInterrupt:
            print(Fore.RED + 'Quitting.')
            sys.exit()

newTerminal = ThothTerminal()
newTerminal.start()
