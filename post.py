#!/usr/bin/env python3

import twata
import sys

def usage():
    print("Usage: %s <message> " % sys.argv[0])
    sys.exit()

def main():

    if len(sys.argv) != 2:
        usage()

    t = twata.Twata()
    #print("sending message:", sys.argv[1])
    #t.send_image(t.mk_image(sys.argv[1]))

    print("sending message:%s" % twata.lorem)
    t.send_image(t.mk_image(twata.lorem))

if __name__ == "__main__":
    main()
