cucumber.py, ACE via Python pickle unpacking. Written by
Oelin <me.oelin@gmail.com>.

```sh
cucumber.py [path]
```
   
This script exploits features of Python's popular serialisation library, pickle in such a way to cause the execution of arbitrary code by programs at run-time. Simply specify the path to a file containing Python source code. An exploitative pickle serialisation will then be written to stdout (ouput). If another Python program attempts to unpack this
serialisation, the original code given will be executed. Note that this script should only be used for demonstratory purposes. It is not a security hacking tool!
