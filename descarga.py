#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import subprocess
import bs4
import re
import argparse
from glob import glob
import sys
import yaml

from urllib.request import urlretrieve

dname=os.getcwd()

indices=[]
for c in glob("*/info.yml"):
    with open(c, 'r') as f:
        url = yaml.load(f).get("url", None)
        if url:
            d = c.split("/")[-2]
            indices.append((d,url))

for codigo, url in sorted(indices):
    print("Descargando %s: %s" % (codigo, url))
    pth = codigo+"/wks"
    os.makedirs(pth, exist_ok=True)
    book = "book"
    out = pth + "/" + book

    pdf = out + ".pdf"
    xml = out + ".xml"
    htm = out + ".html"

    if url.endswith(".pdf"):
        if not os.path.isfile(pdf):
            urlretrieve(url, filename=pdf)

        if not os.path.isfile(xml):
            os.chdir(pth)
            _pdf = book + ".pdf"
            subprocess.run(["pdftohtml", "-q", _pdf])
            subprocess.run(["sed", "s/<head>/<head><meta charset=\"UTF-8\">/", "-i", book+"s.html"])
            subprocess.run(["pdftohtml", "-q", "-xml", _pdf])
            subprocess.run(["pdftotext", "-q", _pdf])
            if glob("*.png"):
                subprocess.run("mogrify +repage -fuzz 600 -trim -resize 720> -format jpg -quality 75 *.png".split())
    else:
        if not os.path.isfile(htm):
            urlretrieve(url, filename=htm)

    os.chdir(dname)
