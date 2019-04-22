#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import re

re_punto = re.compile(r"^(\d+\.)\s*$")
re_sp = re.compile(r"\s+")

min_top = 295 - 1
max_top = 807 + 1

def get_cap(pag, punto=None):
    if punto == 452:
        return "## Seguridad vial"
    if punto == 455:
        return "## Seguridad y emergencias"
    if punto is not None:
        return None

    if pag == 6:
        return "# Nuestro contrato con los españoles"
    if pag == 8:
        return "## Nuestros principios, la guía de nuestra acción política"
    if pag == 12:
        return "# 01. Comprometidos con el fortalecimiento de la Nación"
    if pag == 16:
        return "# 02. Una revolución fiscal para el crecimiento económico y la competitividad"
    if pag == 19:
        return "# 03. Por una economía moderna y avanzada"
    if pag == 22:
        return "## I+D+i"
    if pag == 25:
        return "## Autónomos"
    if pag == 26:
        return "## Empleo"
    if pag == 28:
        return "## Comercio"
    if pag == 29:
        return "## Turismo"
    if pag == 31:
        return "# 04. Por una educación de calidad y en libertad"
    if pag == 35:
        return "## Universidades"
    if pag == 36:
        return "## Deporte"
    if pag == 37:
        return "# 05. Más y mejor sociedad del bienestar"
    if pag == 39:
        return "## Sanidad"
    if pag == 43:
        return "## Consumo"
    if pag == 44:
        return "## Dependencia"
    if pag == 45:
        return "## Mayores"
    if pag == 46:
        return "## Pensiones"
    if pag == 47:
        return "# 06. Familia. Políticas sociales para la igualdad de oportunidades"
    if pag == 49:
        return "## Familia"
    if pag == 51:
        return "## Discapacidad"
    if pag == 53:
        return "## Servicios sociales"
    if pag == 54:
        return "## Igualdad"
    if pag == 55:
        return "## Violencia de género"
    if pag == 57:
        return "## Infancia y juventud"
    if pag == 58:
        return "## Animales de compañía"
    if pag == 59:
        return "# 07. Más oportunidades para las personas"
    if pag == 61:
        return "## Movilidad"
    if pag == 62:
        return "## Infraestructuras"
    if pag == 64:
        return "## Vivienda y urbanismo"
    if pag == 65:
        return "## Cultura"
    if pag == 67:
        return "# 08. Una España sostenible con futuro"
    if pag == 69:
        return "## Energía y cambio climático"
    if pag == 71:
        return "## Medio ambiente"
    if pag == 72:
        return "## Agricultura, ganadería y pesca"
    if pag == 75:
        return "## Agua"
    if pag == 76:
        return "## Medio rural"
    if pag == 78:
        return "# 09. Una Mejor Democracia"
    if pag == 80:
        return "## Justicia"
    if pag == 82:
        return "## Función pública"
    if pag == 84:
        return "## Transparencia y regeneración"
    if pag == 86:
        return "# 10. Retos globales de una Sociedad Abierta"
    if pag == 90:
        return "## Terrorismo"
    if pag == 91:
        return "## Inmigración"
    if pag == 92:
        return "## Lucha contra la ocupación de viviendas"
    if pag == 93:
        return "## Lucha contra el comercio ilegal"
    if pag == 94:
        return "## Lucha contra la explotación sexual"
    if pag == 94:
        return "## Seguridad vial"
    if pag == 94:
        return "## Seguridad y emergencias"
    if pag == 95:
        return "## Acción exterior"
    if pag == 96:
        return "## Unión Europea"
    if pag == 99:
        return "## Defensa"
    if pag == 100:
        return "## Cooperación"
    if pag == 101:
        return "## Emigración"
    return None

def get_text(childrens, top, left, bottom, right):
    txt = ""
    for  c in childrens:
        _top, _left = (c.attrs["top"], c.attrs["left"])
        if _top>=top and _top<=bottom and _left>=left and _left<=right:
            txt = txt + "\n" + c.decode_contents()
    return txt.strip()

def convert(xml, fprint):
    punto = 0
    for n in xml.findAll("page"):
        pag = n.attrs["number"]
        cap = get_cap(pag)
        if cap:
            fprint("\n%s\n" % cap)

        if pag < 6:
            continue
        txt = n.get_text().strip()
        if len(txt)<100:
            continue
        childrens = [t for t in n.select("> *") if "top" in t.attrs and t.get_text().strip()]

        if pag < 8:
            _min_top = 284 if pag == 6 else 150
            childrens = [t for t in childrens if t.attrs["top"]>_min_top and t.attrs["top"]<max_top]
            fprint("")
            for i, c in enumerate(childrens):
                prev = None if i==0 else childrens[i-1]
                if prev and (c.attrs["top"]-prev.attrs["top"])>29:
                    fprint("")
                fprint(c)
            continue
        if pag in (9, 10):
            txt = get_text(childrens, 187, 370, 402, 528)
            txt = re_sp.sub(" ", txt).strip()
            fprint("\n### %s\n" % txt)
            txt = get_text(childrens, 193, 766, 457, 999)
            fprint(txt)
            txt = get_text(childrens, 545, 232, 707, 484)
            txt = re_sp.sub(" ", txt).strip()
            fprint("\n### %s\n" % txt)
            txt = get_text(childrens, 550, 766, 776, 999)
            fprint(txt)
        if pag == 11:
            txt = get_text(childrens, 332, 284, 494, 528)
            txt = re_sp.sub(" ", txt).strip()
            fprint("\n### %s\n" % txt)
            txt = get_text(childrens, 338, 766, 585, 999)
            fprint(txt)
            txt = get_text(childrens, 693, 123, 726, 999)
            fprint("\n"+txt)

        if pag < 13:
            continue

        childrens = [t for t in childrens if t.attrs["top"]>min_top and t.attrs["top"]<max_top]

        pag1 = [c for c in childrens if c.attrs["left"]<640]
        pag2 = [c for c in childrens if c.attrs["left"]>640]

        for childrens in (pag1, pag2):
            childrens = sorted(childrens, key=lambda t: t.attrs["top"])

            for i, c in enumerate(childrens):
                prev = None if i==0 else childrens[i-1]
                txt = c.get_text().strip()
                m = re_punto.match(txt)
                if m:
                    punto = int(m.group(1)[:-1])
                    cap = get_cap(pag, punto)
                    if cap:
                        fprint("\n%s\n" % cap)
                    fprint("\n**%s**" % m.group(1), end=" ")
                elif txt == "•":
                    if prev and prev.get_text().strip().endswith(":"):
                        fprint("")
                    fprint("*", end=" ")
                else:
                    if prev and (c.attrs["top"]-prev.attrs["top"])>32:
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
    md = re.sub(r"^(45|198)\n\. ", r"**\1.** ", md, flags=re.MULTILINE)
    md = re.sub(r"^361\s+Implementaremos", "**361.** Implementaremos", md, flags=re.MULTILINE)
    md = re.sub("\s+([\.,])", r"\1", md)
    md = re.sub("(\s+)”", r"”\1", md)
    md = re.sub("“(\s+)", r"\1“", md)
    md = re.sub(r"^ +", r"", md, flags=re.MULTILINE)
    md = md.replace("I\nmplantaremos", "Implantaremos")

    with open(file_out, "w") as f:
        f.write(md.strip())
