#!/usr/bin/python3
# -*- coding: utf-8 -*-
import bs4
import sys
import re
from subprocess import run
import argparse
import os
from util import get_info, set_info, get_function, get_soup, clean_tags, to_md, get_arg
import pyminizip
from glob import glob

arg = get_arg('Genera un epub de un programa electoral')

re_rtrim = re.compile(r" +$", re.MULTILINE)
re_ltrim = re.compile(r"^\s*\n+")

yml = get_info(autocomplete=True)

isLastLineBlank = False
def fprint(txt, *args, re_clean=None, **kargs):
    global isLastLineBlank
    if isinstance(txt, bs4.Tag):
        txt = to_md(txt)
    if re_clean is not None:
        txt = re_clean.sub("", txt)
    txt = re_rtrim.sub("", txt)
    if isLastLineBlank:
        txt = re_ltrim.sub("", txt)
        if len(txt)==0:
            return
    #print(txt, *args, **kargs)
    if kargs.get("file", sys.stdout) == sys.stdout:
        kargs["file"] = out
        print(txt, *args, **kargs)
    isLastLineBlank = len(txt.split("\n")[-1])==0

out = open(yml.output+".md", "w")

def print_meta(yml, fprint):
    fprint('''
---
title: '{0} - {1} - {2}'
author: '{1}'
description: 'Programa electoral del partido político {1} para las elecciones {2} de {0} en España'
lang: es-ES
date: {3}
subject: ['Política', 'Programa electoral', '{1}', 'Elecciones {2}']
URL: "{4}"
---
    '''.strip().format(
        yml.year,
        yml.partido,
        yml.tipo,
        yml.fecha,
        yml.url,
        )
    )

def end_convert(file_out):
    with open(file_out, "r") as f:
        md = f.read()
    md = clean_tags(md)
    md = clean_tags(md, extra=True)
    with open(file_out, "w") as f:
        f.write(md.strip())

module = __import__(arg.target)
convert = getattr(module, "convert")
pre_convert = get_function(module, "pre_convert")
post_convert = get_function(module, "post_convert")
print_meta = get_function(module, "print_meta", default=print_meta)

xml = get_soup("wks/book.xml", "xml", save="wks/parsed.xml") or get_soup("wks/book.html", save="wks/parsed.html")

print_meta(yml, fprint)
pre_convert(xml)
convert(xml, fprint)
out.close()
end_convert(yml.output+".md")
post_convert(yml.output+".md")
print("")

run(["pandoc", "--standalone", "-t", "html5", "-o", yml.output+".html", yml.output+".md"])
soup = get_soup(yml.output+".html")
soup.find("header").extract()
for n in soup.findAll(["div", "p"]):
    if len(n.select("*"))==0 and len(n.get_text().strip())==0:
        n.extract()
with open(yml.output+".html", "w") as f:
    f.write(str(soup))
run(["miepub", "--chapter-level", "1", "--css", "../epub.css", "--txt-cover", yml.txt_cover, yml.output+".md"])

pyminizip.compress_multiple([yml.output+'.'+i for i in ("md", "html", "epub")], [], yml.output+".zip", "programaelectoral", 9)
