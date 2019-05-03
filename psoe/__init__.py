#!/usr/bin/python3
# -*- coding: utf-8 -*-
import bs4
import sys
import re
from subprocess import run

re_punto = re.compile(r"^\s*(\d+\.)+\s*$")
re_letra = re.compile(r"^\s*([a-z]|\d+)\)\s*$")
re_sp = re.compile(r"\s+")

def clean_tags(txt):
    for tag in ("em", "strong", "b", "i"):
        txt = re.sub("<"+tag+r">(\s+)", r"\1<"+tag+">", txt)
        txt = re.sub(r"(\s+)</"+tag+">", "</"+tag+r">\1", txt)
        txt = re.sub(r"</"+tag+r">(\s+)<"+tag+r">", r" ", txt)
        txt = re.sub(r"<"+tag+r">(\s*)</"+tag+r">", r"\1", txt)
        txt = re.sub(r"</"+tag+r"><"+tag+r">", "", txt)
    return txt

def get_inner(n):
    txt = n.decode_contents()
    #txt = clea_tags(txt)
    txt = re_sp.sub(" ", txt).strip()
    return txt

min_top = 65 - 1 #111 - 1
max_top = 846

def convert(xml, fprint):
    lastTop = None
    osdBlock = False
    prmGuion = True
    for n in xml.findAll("page"):
        pag = n.attrs["number"]
        if pag<7 or pag>148:
            continue

        childrens = [t for t in n.select("> *") if "top" in t.attrs and t.attrs["top"]>min_top and t.attrs["top"]<max_top]

        pag1 = [c for c in childrens if c.attrs["left"]<656]
        pag2 = [c for c in childrens if c.attrs["left"]>656]

        for childrens in (pag1, pag2):
            childrens = sorted(childrens, key=lambda t: int(t.attrs["top"]/10))
            txt = ""
            for c in childrens:
                txt = txt + " " + c.get_text().strip()
            txt = txt.strip()
            if len(txt)>0 and len(txt)<300 and txt.upper() == txt:
                txt = txt.capitalize().replace("españa", "España")
                if txt.startswith("/ "):
                    fprint("\n## %s\n" % txt[2:].capitalize())
                else:
                    fprint("\n# %s\n" % txt)
                continue

            while childrens:
                c = childrens.pop(0)
                txt = c.get_text().strip()
                if len(txt)==0:
                    continue
                b1 = c.find("b")
                if b1 and txt.startswith("/ ") and txt == b1.get_text().strip():
                    sub = txt[1:]
                    while len(childrens)>0:
                        c_next = childrens[0]
                        txt = c_next.get_text().strip()
                        b1 = c_next.find("b")
                        if b1 and txt == b1.get_text().strip():
                            sub = sub + " " + childrens.pop(0).get_text()
                        else:
                            break
                    sub = re_sp.sub(" ", sub).strip()
                    sub = sub.capitalize().replace("españa", "España")
                    fprint("\n## %s\n" % sub)
                    lastTop = None
                    continue
                if lastTop is not None and (c.attrs["top"]-lastTop)>47:
                    fprint("")
                lastTop = c.attrs["top"]
                isLetra = re_letra.match(txt)
                if isLetra:
                    letra = isLetra.group(1)
                    fprint("\n**%s)**" % letra, end=" ")
                    continue
                txt = get_inner(c)
                if re_punto.match(txt):
                    fprint("\n**%s**" % txt, end=" ")
                elif txt.startswith("-"):
                    fprint("\n**\\-**", end=" ")
                    if txt!="-":
                        fprint(txt[1:].strip())
                elif c.get_text().strip() == "•":
                    fprint("\n**\\***", end=" ")
                else:
                    fprint(txt)
    fprint('''
## Todos los países, en la asamblea general de naciones se comprometieron (2015) a alcanzar los siguientes objetivos de desarrollo sostenible (ods):

**ODS 1** Erradicar la pobreza extrema, en todas sus dimensiones

**ODS 2** Erradicar el hambre y promover prácticas agrícolas sostenibles y resilientes

**ODS 3** Garantizar salud y bienestar para todos los ciudadanos,
independientemente de su país de origen o de procedencia

**ODS 4** Garantizar una educación inclusiva, equitativa y de calidad

**ODS 5** Empoderar a todas las mujeres y lograr la igualdad de género

**ODS 6** Garantizar el acceso al agua potable y al saneamiento, para toda la población

**ODS 7** Asegurar el acceso a energía limpia, asequible y segura

**ODS 8** Prosperidad económica inclusiva, con empleo digno
y protección social para todos y todas

**ODS 9** Fomentar la innovación, la industrialización inclusiva
y las infraestructuras resilientes

**ODS 10** Reducir las desigualdades entre personas, garantizando la
igualdad de oportunidades, con indepencia de origen, lugar de residencia, orientación sexual

**ODS 11** Promover ciudades inclusivas, seguras, resilientes y sostenibles

**ODS 12** Garantizar modalidades sostenibles de consumo y producción

**ODS 13** Combatir el cambio climático y sus efectos, mediante acciones de mitigación y de adaptación.

**ODS 14** Preservar y restaurar los océanos , los mares y los recursos marinos,
mediante la reducción de la contaminación y la conservación de los ecosistemas marinos

**ODS 15** Preservar y restaurar los ecosistemas terrestres, garantizando su protección y uso sostenible

**ODS 16** Promover la paz, la justicia y las instituciones eficaces,
combatienedo toda forma de violencia y de corrupción y estableciendo mecanismos
de rendición de cuentas

**ODS 17** Generar alianzas para alcanzar el cumplimiento de la agenda 2030,
movilizando recursos humanos y económicos
    '''.rstrip())

def post_convert(file_out):
    with open(file_out, "r") as f:
        md = f.read()
    md = md.replace("2.52\n.", "**2.52.**")
    md = md.replace("<b>• ", "**\\*** <b>")
    md = re.sub(r"(\*\*\\\*\*\* <b>[^<\.]+</b>$)", r"\1\n", md, flags=re.MULTILINE)
    md = md.replace("\n\n\n", "\n\n")
    md = md.replace("<b>Para superar estas carencias", "\n<b>Para superar estas carencias")
    md = re.sub(r"\s+\*\*2018\.\*\*\n", " 2018.\n\n", md)
    md = md.replace("<b>(1)</b>", "(Desde la educación y la formación profesional, objeto de propuestas en el punto 2 de este Programa electoral)")
    #md = re.sub(r"<b>\d+\)</b>\n", r"\1)", md)
    with open(file_out, "w") as f:
        f.write(md.strip())
