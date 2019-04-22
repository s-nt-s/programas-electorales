#!/usr/bin/python3
# -*- coding: utf-8 -*-
import bs4
import sys
import re

re_punto = re.compile(r"^\d+\.$")

def mktag(inner):
    div = bs4.BeautifulSoup("<unwrapme>"+inner+"\n</unwrapme>", 'lxml')
    return div.find("unwrapme")

def pre_convert(xml):
    for n in xml.findAll("text", text="2", attrs={"font":11, "width": 6}):
        n.string=""
        n.append(mktag("<sub>2</sub>"))
        n.find("unwrapme").unwrap()
        n.attrs["top"]=n.attrs["top"]-13
    for n in xml.findAll("text", text="xxi"):
        n.attrs["top"] = n.attrs["top"] - 5

min_top = 148 - 1
max_top = 1203

def convert(xml, fprint):
    flag=True
    for n in xml.findAll("page"):
        pag = n.attrs["number"]
        if pag<5:
            continue
        txt = n.get_text().strip()
        if len(txt)<100:
            flag=True
            continue
        childrens = [t for t in n.select("> *") if "top" in t.attrs and t.attrs["top"]>min_top and t.attrs["top"]<max_top]
        childrens = sorted(childrens, key=lambda t: int(t.attrs["top"]/10))
        if flag:
            fprint("\n# %s\n" % childrens.pop(0).get_text())
        flag=False
        for i, c in enumerate(childrens):
            txt = c.decode_contents().strip()
            if re_punto.match(txt):
                txt = "**"+txt+"**"
                fprint("\n"+txt, end=" ")
            else:
                top = c.attrs["top"]
                if i>0:
                    last_top = childrens[i-1].attrs["top"]
                    if (top-last_top)>21:
                        txt = "\n"+txt
                fprint(txt)

def post_convert(file_out):
    re_words = re.compile(r"\b([^\d\W]+-[^\d\W]+)\b")
    full_word = set()
    with open("wks/book.txt", "r") as f:
        full_word = set(re_words.findall(f.read()))

    with open(file_out, "r") as f:
        md = f.read()

    re_words = re.compile(r"\b([^\d\W]+-\n[^\d\W]+)\b")
    words = set()
    for i in re_words.findall(md):
        if i not in full_word:
            words.add(i)
    for w in words:
        md = re.sub(r"\b"+w+r"\b", w.replace("-\n","")+"\n", md)
    md = re.sub(r"(\d+)\s+%", r"\1%", md)
    md = md.replace("CO\n<sub>2</sub>", "CO<sub>2</sub>")
    md = re.sub(r" *\n *([:,\.])", r"\1\n", md)
    md = re.sub(r"\s+\.", ".", md)
    md = re.sub(r"^ ", "", md, flags=re.MULTILINE)
    md = re.sub(r"([05])\s+(000)\b", r"\1.\2", md)

    with open(file_out, "w") as f:
        f.write(md.strip())
