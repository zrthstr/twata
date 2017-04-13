#!/usr/bin/env python3

import twata

def main():
    t = twata.Twata()
    t.get_files()
    t.read_image()

if __name__ == "__main__":
    main()
