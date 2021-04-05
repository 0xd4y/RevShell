# RevShell

Tool used for creating one-line reverse shell payloads.
* Supports url and base64 encoding
* Quick and easy way to generate a reverse shell payload
* User-friendly

```
usage: revshell.py [-h] [-i] [-p] [-s] [-t] [-e] [-c] [-f]

**** Outputs a reverse shell. ****

=== Default values ===

        1. ip = tun0 (otherwise eth0)
        2. port = 443
        3. rev_shell type = bash
        4. shell = /bin/sh

optional arguments:
  -h, --help        show this help message and exit
  -i , --ip         Specify the IP address you want to listen on.
  -p , --port       The port you want to listen on.
  -s , --shell      Which shell you want to use (e.g. /bin/bash, /bin/sh, etc.)
  -t , --rev-type   The kind of reverse shell you would like (e.g. perl, python, nc, etc.)
  -e , --encode     Specify encoding for the shell.
  -c, --clipboard   Copies into clipboard.
  -f, --force       Forces tool to accept argument.

=== Supported reverse shell types ===

        1. Ruby
        2. Python and Python3
        3. Netcat | nc
        4. Perl
        5. Bash
        6. PHP
        7. Powershell | ps

=== Supported encoding types ===

        1. base64 | b64   base64 encodes all characters.
        2. url          url-encodes special characters.
        3. url-all      url-encodes all characters.

Examples:

python3 revshell.py -i 10.13.3.7 -p 9001 -t nc -e url-all
python3 revshell.py -p 1337 -o reverse_shell.txt
python3 revshell.py -i tun0 -s /bin/bash -t ruby -e base64 -c

```
## Examples

![image](https://user-images.githubusercontent.com/77868212/113517220-371e9d00-9544-11eb-8c04-4db69dea636e.png)
===================================
![image](https://user-images.githubusercontent.com/77868212/113517269-806eec80-9544-11eb-8182-5fd4f18acaaa.png)
===================================
![image](https://user-images.githubusercontent.com/77868212/113517872-37b93280-9548-11eb-9625-43c74f1b44ec.png)
