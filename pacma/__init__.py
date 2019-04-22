#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import re

heads = ["h%s" % i for i in range(1,7)]
re_sp = re.compile(r"\s+")
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
    article = xml.find("article")
    article.find("div").unwrap()
    for p in article.select("ul > p") + article.select("ol > p"):
        p.name = "li"
    hs=[]
    for ih in heads:
        ih = article.findAll(ih)
        if len(ih)>0:
            hs.append(ih)
    for i, h in enumerate(hs):
        for n in h:
            n.name=("h%s" % (i+1))
            if "id" in n.attrs:
                del n.attrs["id"]
            if n.string.upper() == n.string:
                num, txt = n.string.strip().split(None, 1)
                n.string = num + " " + txt.capitalize()

def convert(xml, fprint):
    article = xml.find("article")
    fprint("")
    for n in article.select("> *"):
        tag = n.name
        if tag in heads:
            l = int(tag[1])
            txt = re_sp.sub(" ", n.get_text()).strip()
            fprint("%s %s\n" % ('#'*l, txt))
        elif tag=="p":
            fprint(n)
            fprint("")
        elif tag in ("ol", "ul") and is_lista_simple(n):
            num = 0 if tag == "ol" else None
            for li in n.select("> li"):
                if num is not None:
                    fprint("%s." % index[num], end=" ")
                    num = num + 1
                else:
                    fprint("*", end=" ")
                fprint(li)
            fprint("")
        else:
            fprint(str(n)+'\n')
