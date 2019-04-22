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
from util import get_info, set_info

from urllib.request import urlretrieve

re_float = re.compile(r"^\d+\.\d+$")
dname=os.getcwd()

indices=[]
for c in glob("*/info.yml"):
    indices.append((c, os.path.dirname(c), get_info(c, autocomplete=False)))

for path_info, codigo, info in sorted(indices):
    print("Descargando %s: %s" % (codigo, info.url))
    pth = codigo+"/wks"
    os.makedirs(pth, exist_ok=True)
    book = "book"
    out = pth + "/" + book

    pdf = out + ".pdf"
    xml = out + ".xml"
    htm = out + ".html"
    flag = False

    if info.url.endswith(".pdf"):
        if not os.path.isfile(pdf):
            urlretrieve(info.url, filename=pdf)

        flag = True
        pdfinfo = subprocess.check_output(["pdfinfo", pdf])
        pdfinfo = pdfinfo.decode(sys.stdout.encoding)
        info.pdf = {}
        for l in pdfinfo.split("\n"):
            l = l.strip()
            if len(l):
                k, v = l.split(":", 1)
                k = k.strip()
                v = v.strip()
                if len(v)==0 or v=='none':
                    v = None
                elif v.isdigit():
                    v = int(v)
                elif re_float.match(v):
                    v = float(v)
                elif v == 'no':
                    v = False
                elif v == 'yes':
                    v = True
                info.pdf[k]=v

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

    if flag:
        os.chdir(dname)
    set_info(info, yml_file=path_info)
