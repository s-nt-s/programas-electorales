#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import re

heads = ["h%s" % i for i in range(1,7)]
re_sp = re.compile(r"\s+")
re_punto = re.compile(r"^\d+\.\s+")
index = "abcdefghijkl"

def is_lista_simple(n):
    for li in n.select("> *"):
        if li.name != "li":
            return False
        for s in li.select("*"):
            if s.name != "strong":
                return False
    return True

def pre_convert(xml):
    for h in xml.select("li > h4"):
        h.unwrap()

def convert(xml, fprint):
    count = 0
    for p in xml.select("div.propuestas > div.propuesta"):
        txt = p.select("div.titulo")[0].get_text().strip()
        fprint("\n# %s\n" % txt)
        content = p.select("div.content > div.content > div")[0]
        for n in content.select("> *"):
            if n.name == "h3":
                txt = re_sp.sub(" ", n.get_text()).strip()
                fprint("\n## %s\n" % txt)
            elif n.name == "ol":
                for li in n.select("> *"):
                    if li.name == "li":
                        count = count + 1
                        fprint("\n**%s.**" % count, end=" ")
                        fprint(li, re_clean=re_punto)
                        fprint("")
                    elif li.name == "ul":
                        for i in li.select("> li"):
                            fprint("*", end=" ")
                            fprint(i)
            elif n.name == "ul":
                for i in n.select("> li"):
                    fprint("*", end=" ")
                    fprint(i)
            elif n.name == "li":
                count = count + 1
                fprint("\n**%s.**" % count, end=" ")
                fprint(n, re_clean=re_punto)
                fprint("")

def post_convert(file_out):
    with open(file_out, "r") as f:
        md = f.read()
    md = md.replace("discriminación,en", "discriminación, en")
    md = md.replace("despoblación.Fomentaremos", "despoblación. Fomentaremos")
    with open(file_out, "w") as f:
        f.write(md.strip())
