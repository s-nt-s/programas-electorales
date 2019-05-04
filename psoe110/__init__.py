# -*- coding: utf-8 -*-
import re

import bs4

re_punto = re.compile(r"^<b>(\d+\.) *</b> *")
re_sp = re.compile(r"\s+")


def mktag(inner):
    div = bs4.BeautifulSoup("<unwrapme>"+inner+"\n</unwrapme>", 'lxml')
    return div.find("unwrapme")


def get_cap(page):
    if page == 6:
        return "La España del conocimiento"
    if page == 14:
        return "La España competititva y de las oportunidades"
    if page == 24:
        return "La España del bienestar"
    if page == 30:
        return "La España feminista"
    if page == 34:
        return "La España de la transición ecológica"
    if page == 38:
        return "La España de los nuevos derechos y libertades"
    if page == 44:
        return "Una España europea abierta al mundo"
    return None


min_top = 104 - 1
max_top = 846
sub = None


def print_meta(yml, fprint):
    fprint('''
---
title: '{0} - {1} - {2} (resumen)'
author: '{1}'
description: 'Resumen del programa electoral del partido político {1} para las elecciones {2} de {0} en España'
lang: es-ES
date: {3}
subject: ['Política', 'Programa electoral resumido', '{1}', 'Elecciones {2}']
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


def convert(xml, fprint):
    for n in xml.findAll("page"):
        pag = n.attrs["number"]
        cap = get_cap(pag)
        if cap:
            fprint("\n# %s" % cap)
        if pag < 6:
            continue
        txt = n.get_text().strip()
        if len(txt) < 100:
            flag = True
            continue
        childrens = [t for t in n.select(
            "> *") if "top" in t.attrs and t.attrs["top"] > min_top and t.attrs["top"] < max_top]
        childrens = sorted(childrens, key=lambda t: int(t.attrs["top"]/10))

        while childrens:
            c = childrens.pop(0)
            txt = c.get_text().strip()
            if len(txt) == 0:
                continue

            b1 = c.find("b")
            if b1 and txt.startswith("/ ") and txt == b1.get_text().strip():
                txt = "%s %s %s" % (txt[1:], childrens.pop(
                    0).get_text(), childrens.pop(0).get_text())
                txt = re_sp.sub(" ", txt).strip()
                txt = txt.replace(" TRABA JAR ", " TRABAJAR ")
                txt = txt.capitalize().replace("españa", "España")
                fprint("\n## %s" % txt)
                continue
            txt = c.decode_contents().strip()
            if re_punto.search(txt):
                txt = re_punto.sub(r"\n**\1**", txt)
                fprint(txt, end=" ")
            else:
                fprint(txt)


def post_convert(file_out):
    re_words = re.compile(r"\b([^\d\W]+-[^\d\W]+)\b")
    full_word = set()
    with open("wks/book.txt", "r") as f:
        full_word = set(re_words.findall(f.read()))

    with open(file_out, "r") as f:
        md = f.read()

    md = re.sub(r"  +", " ", md)
    md = re.sub(r"</b>(\s+)<b>", r"\1", md)
    md = re.sub(r"</i>(\s+)<i>", r"\1", md)

    re_words = re.compile(r"\b([^\d\W]+-\n[^\d\W]+)\b")
    words = set()
    for i in re_words.findall(md):
        if i not in full_word:
            words.add(i)
    for w in words:
        md = re.sub(r"\b"+w+r"\b", w.replace("-\n", "")+"\n", md)
    md = re.sub(r" *\n *([:,\.])", r"\1\n", md)
    md = re.sub(r"\s+\.", ".", md)
    md = re.sub(r"^ ", "", md, flags=re.MULTILINE)

    with open(file_out, "w") as f:
        f.write(md.strip())
