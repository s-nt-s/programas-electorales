# -*- coding: utf-8 -*-
import re

re_punto = re.compile(r"^(\d+[\.\)])$")
re_sp = re.compile(r"\s+")
re_sp_strange = re.compile(r"[^\S ]")

min_top = 108 - 1
max_top = 1173


def is_titulo(c):
    tp = (c.attrs["height"], c.attrs["font"])
    if tp in ((22, 7), (23, 11), (23, 7)):
        return 1
    if tp in ((21, 8),):
        return 2
    if tp in ((21, 6),):
        return 3
    return -1


def clean(txt):
    txt = "".join(c for c in txt if c.isprintable())
    txt = re_sp_strange.sub("", txt)
    txt = re_sp.sub(" ", txt)
    return txt.strip()


def pre_convert(xml):
    return
    page = xml.find("page", attrs={"number": 29})
    text = page.find("text", attrs={"top": 599, "left": 177})
    text.attrs["top"] = 610


def convert(xml, fprint):
    for n in xml.findAll("page"):
        pag = n.attrs["number"]
        if pag < 3:
            continue
        txt = n.get_text().strip()
        childrens = [t for t in n.select(
            "> *") if "top" in t.attrs and t.attrs["top"] > min_top and t.attrs["top"] < max_top]
        childrens = [c for c in childrens if c.get_text().strip()]
        #childrens = sorted(childrens, key=lambda t: int(t.attrs["top"]/10))

        lastTop = None
        while childrens:
            c = childrens.pop(0)
            nivel = is_titulo(c)
            if nivel == 1:
                titulo = ""
                while childrens and is_titulo(c) == 1:
                    titulo = titulo + " " + c.get_text().strip()
                    lastTop = c.attrs["top"]
                    c = childrens.pop(0)
                titulo = clean(titulo)
                titulo = titulo.replace("V ", "V")
                fprint("\n# %s\n" % titulo)
                lastTop = None

            txt = clean(c.get_text().strip())
            if nivel > 1:
                fprint("\n%s %s\n" % ('#' * nivel, txt))
                lastTop = None
                continue

            if lastTop and (c.attrs["top"]-lastTop) > 21:
                fprint("")

            lastTop = c.attrs["top"]
            spl = txt.split()
            p1 = spl[0]
            if p1 == "•":
                fprint("*", end=" ")
                if len(spl) > 1:
                    fprint(" ".join(spl[1:]),)
                continue
            if re_punto.match(p1) and len(p1) < 5:
                p1 = "**"+p1+"**"
                fprint("\n"+p1, end=" ")
                if len(spl) > 1:
                    fprint(" ".join(spl[1:]))
            else:
                fprint(txt)


def post_convert(file_out):
    with open(file_out, "r") as f:
        md = f.read()
    md = re.sub(r"(### )?La\s+(### )?importancia\s+(### )?de\s+(### )?las\s+(### )?próximas\s+(### )?elecciones\s+(### )?europeas\.",
                "## La importancia de las próximas elecciones europeas.", md)
    md = re.sub(r"A C T Ú A p o r", "ACTÚA por", md)
    md = re.sub("\s+([\.,])", r"\1", md)
    md = re.sub(r"(m)\s+", r"\1", md, flags=re.IGNORECASE)
    md = md.replace("curriculumserán", "curriculum serán")
    words = set(w.strip().lower().replace(" ", "") for w in '''
administraciones
administración
administrativo
procedimientos
redistributiva
verdaderamente
administradas
construiremos
modernización
municipalismo
patrimoniales
transparencia
cumplimiento
introducción
modificación
nombramiento
regeneración
segmentación
compartidas
comunidades
criminaliza
democrática
federalismo
formaciones
información
inmigrantes
instrumento
solidaridad
tramitación
anualmente
democracia
documentos
económicas
energético
fiscalidad
organismos
permanente
proponemos
sostenible
transición
autónomas
económico
feminismo
formación
impunidad
servicios
avanzada
campañas
combatir
contrato
empresas
estambul
european
femenina
gobierno
igualdad
mediante
permisos
primeros
públicos
servicio
víctimas
calidad
cultura
elimine
hombres
impacto
impulso
mandato
mayoría
medidas
mujeres
racismo
sistema
tenemos
término
empleo
europa
hombre
modelo
mérito
método
online
social
spring
tiempo
ambos
hacia
justa
menos
mundo
nuevo
tramo
buen
como
para
unos
con
los
más
paz
una
al
de
el
no
un
    '''.strip().split("\n"))
    words = sorted(words, key=lambda x: (-len(x), x))
    #print ("\n".join(words))
    words = [" *".join(list(w)) for w in words]
    re_words = re.compile(r"\b(" + "|".join(words) + r")\b", re.IGNORECASE)
    _md = None
    while _md != md:
        _md = md
        md = re_words.sub(lambda x: x.group().replace(" ", ""), md)
    md = re.sub(r"‘\s+", "‘", md)
    md = re.sub(r"\s+’", "’", md)
    md = md.replace(" un a ", " una ")
    md = md.replace(" un o s ", " unos ")
    md = md.replace("Aplicar el nuevo marco global",
                    "* Aplicar el nuevo marco global")
    md = re.sub(r"\n\n\* ", r"\n* ", md, flags=re.MULTILINE)
    md = re.sub(r":\n\* ", r":\n\n* ", md, flags=re.MULTILINE)
    md = md.replace(" publico ", " público ")
    md = md.replace(" kmen ", " km en ")
    md = re.sub(r"“\s+", "“", md)
    md = re.sub(r"\s+”", "”", md)

    #md = re.sub(r"^(.{1,10})\n(.{1,10})", r"\1 \2", flags=re.MULTILINE)

    with open(file_out, "w") as f:
        f.write(md.strip())
