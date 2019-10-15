#!/usr/bin/env python2
"""
Logpuzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Google's Python Class
http://code.google.com/edu/languages/google-python-class/

Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg
HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US;
rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"

"""

import os
import re
import sys
import urllib
import argparse


def sort_for(n):
    return sorted(n, n.rsplit("-", 2)[-1])


def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""

    domain = "http://{}".format(filename.split("_")[1])
    # regex: had help from Alec Stephens.  Tricky dicky stuff right there
    reg_ex = re.findall(r'GET (\/.*?\.jpg)', open(filename).read())

    urls = []

    for picture in reg_ex:
        urls.append("{}{}".format(domain, picture))
    # retrieved from StackOverflow(https://stackoverflow.com/questions/
    # 29677994/python-help-sorting-after-hyphen)
    return sorted(urls, key=lambda x: x.rsplit("-", 2)[-1])


def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """
    # with help from Zach Kline
    index_of_images = 0
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    files = file(os.path.join(dest_dir, 'index.html'), 'w')
    files.write("<html> \n    <body>\n")
    for image in img_urls:
        names = "img{}".format(index_of_images)
        index_of_images += 1
        print ("Retrieving {}".format(names))
        # provided by Zach Kline
        urllib.urlretrieve(image, os.path.join(dest_dir, names))
        files.write("<img src={}>".format(names))
    files.write("\n    </body> \n</html>")


def create_parser():
    """Create an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir', help='for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')
    return parser


def main(args):
    """Parse args, scan for urls, get images from urls"""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
