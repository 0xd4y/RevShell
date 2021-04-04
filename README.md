# RevShell

This script is used for creating one-line reverse shells. 

```
usage: test.py [-h] [-i] [-p] [-s] [-t] [-e] [-r] [-c]
optional arguments:
  -h, --help        show this help message and exit
  1 #!/usr/bin/env python3
  -i , --ip         Specify the IP address you want to listen on.
  -p , --port       The port you want to listen on.
  -s , --shell      Which shell you want to use (e.g. /bin/bash, /bin/sh, etc.)
  -t , --rev-type   The kind of reverse shell you would like (e.g. perl, python, nc, etc.)
  -e , --encode     Specify encoding for the shell.
  -r, --raw         Prints out shell without a newline.
  -c, --clipboard   Copies into clipboard.

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
python3 revshell.py -p 1337
```
