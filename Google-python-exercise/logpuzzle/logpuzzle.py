#/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""
def myfn(lisel):
  #return lisel[-8:-4] THIS CAN BE USED WITH ANIMAL_CODE_GOOGLE.COM BUT NOT WITH PLACE
  #key = re.search(r'\w-(\w+)')
  key = re.search(r'-(\w+)-(\w+)\.\w+', lisel)
  if key:
    return key.group(2)
  else:
    return lisel 

def read_urls(filename):
  """Returns a list of the puzzle urls from the given log file,
  extracting the hostname from the filename itself.
  Screens out duplicate urls and returns the urls sorted into
  increasing order."""
  # +++your code here+++
  host = re.search(r'_(\w+.\w+.com)', filename)
  hostname = host.group(1)
  print hostname
  f = open(filename)
  s = f.read()
  f.close()
  lis = []
  match = re.findall(r'("GET .*) HTTP', s)
  for i in match:
    if 'puzzle' in i:
      j = 'http://' + hostname + i[5:]
      lis.append(j)
  lis = sorted(lis, key=myfn) 
  p = []
  for i in lis:  
    if not i in p:
      p.append(i)
  return p    
  #sys.exit(0)
def writef(img_urls, dest_dir):
  f = file(os.path.join(dest_dir, 'index.html'), 'w')
  f.write('<html><body>\n')
  j = 0
  for i in img_urls:
    image = 'img' + str(j)
    j+=1
    urllib.urlretrieve(i, os.path.join(dest_dir, image))
    f.write('<img src = "%s">' %image   )
    
    f.write('</body></html>')
    f.close()
  return


def download_images(img_urls, dest_dir):
  """Given the urls already in the correct order, downloads
  each image into the given directory.
  Gives the images local filenames img0, img1, and so on.
  Creates an index.html in the directory
  with an img tag to show each local image file.
  Creates the directory if necessary.
  """
  # +++your code here+++
  #path= os.path
  #print path
  #l = os.listdir#('/home/gokul/mypy/google-python-exercises/logpuzzle')
  #for i in l:
  if os.path.exists(dest_dir):
    print 'Directory %s already exist, do you want to merge?(0/1)' %dest_dir
    k = input()
    if k == 0:
      sys.exit(0)
    else:
      f = file(os.path.join(dest_dir, 'index.html'), 'w')
      f.write('<html><body>\n')
      j = 0
      for i in img_urls:
        image = 'img' + str(j)
        j+=1
        urllib.urlretrieve(i, os.path.join(dest_dir, image))
	f.write('<img src = "%s">' %image   )
	 
      f.write('</body></html>')
      f.close()

    #else:
    # writef(img_urls, dest_dir)
  else:
    os.makedirs(dest_dir)
    #writef(img_urls, dest_dir)
    f = file(os.path.join(dest_dir, 'index.html'), 'w')
    f.write('<html><body>\n')
    j = 0
    for i in img_urls:
      image = 'img' + str(j)
      j+=1
      urllib.urlretrieve(i, os.path.join(dest_dir, image))
      f.write('<img src = "%s">' %image   )
      
    f.write('</body></html>')
    f.close()

  #os.system('mkdir mydir')
  #os.system('cd mydir')
    
def main():
  args = sys.argv[1:]

  if not args:
    print 'usage: [--todir dir] logfile '
    sys.exit(1)

  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  img_urls = read_urls(args[0])
  for i in img_urls:
    print i
  if todir:
    download_images(img_urls, todir)
  else:
    print '\n'.join(img_urls)

if __name__ == '__main__':
  main()
