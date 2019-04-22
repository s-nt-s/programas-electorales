#!/usr/bin/python3
# -*- coding: utf-8 -*-
import nltk
import re
from util import get_arg, get_info, get_soup, set_info
from glob import glob
import os
import sys

from bunch import Bunch

import numpy as np
import matplotlib.pyplot as plt

from nltk import word_tokenize
from nltk.stem import SnowballStemmer

stemmer = SnowballStemmer('spanish')

cwd = os.getcwd()

re_puntuacion = r"[\.,;\)\(\[\]\-“”\"'–:…¿\?‘’«»—/]+"
re_corpus = re.compile(r"^"+re_puntuacion+"|"+re_puntuacion+"$")
re_number = re.compile(r"^[\d\.,/%\-ºª]+$")
re_sp = re.compile(r"\s+")

def mk_set(s):
    #s = s.replace(",", " ").replace("...", " ").replace("…", " ").lower()
    #s = re_sp.sub(" ", s)
    #s = set(s.split())
    #print (" ".join(sorted(s)))
    return set(s.strip().split())

# preposiciones + conjunciones + articulos + pronombres + adverbios
# + cosas varias
excluir = mk_set('''
a abajo acaso acá ahora ahí algo alguien alguna algunas alguno algunos allá allí ante antes apenas aquella aquellas aquello aquellos aquél aquí arriba así aunque ayer aún bajo bastante bien bueno cabe cerca claro como con conmigo conque consigo contigo contra cualesquiera cualquiera cuando cuanto cuidadosamente dado de debajo delante demasiada demasiadas demasiado demasiados demás desde detrás donde durante e el ella ellas ello ellos en encima enfrente entre esa esas escasa escasas escaso escasos ese eso esos esta estas este esto estos fin frecuentemente hacia hasta hoy igual inclusive jamás la las le lejos les lo los luego mal mas mañana me mediante mejor menos mientras misma mismas mismo mismos mucha muchas mucho muchos más mí mía mías mío míos nada nadie ni ninguna ningunas ninguno ningunos no nos nosotras nosotros nuestra nuestras nuestro nuestros nunca o obviamente ora os otra otras otro otros para peor pero pesar poca pocas poco pocos por porque probablemente pues puesto que quienesquiera quienquiera quizá se sea seguramente según si siempre sin sino siquiera so sobre suya suyas suyo suyos sí tal también tampoco tan tanta tantas tanto tantos te ti toda todas todo todos tras tuya tuyas tuyo tuyos tú u un una unas uno unos usted ustedes varias varios versus vos vosotras vosotros vuestra vuestras vuestro vuestros vía y ya yo él éste
cualquier
''')
promesa = mk_set('''
acabar ayudar cierre condicionar control deportación depuración derogación devolución difusión dotar establecerán exclusión exigencia exigir fortalecer ilegalización incorporación persecución prohibición rechazar reforma reformar reforzar revisión revocación supresión suprimir suspensión transformar
'''.lower())
no_promesa = mk_set('''
acabar ayudar cierre condicionar control deportación depuración derogación devolución difusión dotar establecerán exclusión exigencia exigir fortalecer ilegalización incorporación persecución prohibición rechazar reforma reformar reforzar revisión revocación supresión suprimir suspensión transformar
'''.lower())

promesa_stem = mk_set('''
garantiz impuls mejor acab desarroll propon proteccion establec promov apoy reduccion
actualiz aprovech complement compromet concienci
configur consider consolid constitu contribu
desatasc desbloqu descentraliz despenaliz despolitiz desprivatiz
dispondr flexibiliz fortalec
generaliz identific ilegaliz implement incentiv incorpor increment intensific introduc involucr mantendr moderniz multiplic normaliz
planific posibilit profesionaliz profundiz prohibicion promocion propondr reformul reintegr reorient restablec restring revision revolucion simplific supresion suspension transform
garantic armoniz optimiz paraliz penaliz prioriz
persecu persegu potenci
agiliz analiz avanz realiz rechaz reforz utiliz
depur derog reform revoc suprim cierr
''')

excluir2 = mk_set('''
parte partir partes partida publicidad plana ACTÚA ACTUAR
''')

def cd_mkdir(d):
    if not os.path.isdir(d):
        os.mkdir(d)
    os.chdir(d)

def get_stem(w):
    _w = stemmer.stem(w)
    '''
    if _w in promesa_stem:
        return "PROMESA"
    if w in promesa or (w.endswith("emos") and w not in no_promesa):
        if w in promesa:
            word_set.add(w)
            stems_set.add(_w)
        return "PROMESA"
    if w in ("autónomos", "autónomo", "autónomas"):
        return "autónomo"
    '''
    if _w == "españ":
        _w = "español"
    return _w

datas = []
for y in sorted(glob("*/info.yml")):
    d = os.path.dirname(y)
    if d in ("psoe110",):
        continue
    print("Analizando %s" % d)
    os.chdir(cwd)
    os.chdir(d)

    data = get_info(autocomplete=True)
    data.out_name = data.output[:-2]
    file_html = data.out_name+"html"
    soup = get_soup(file_html)
    body = soup.find("body")
    body_txt = re.sub(r"  +", " ", body.get_text()).strip()
    body_slp = body_txt.split()

    data.caracteres = len(body_txt)
    data.palabras = len(body_slp)
    data.parrafos = len(body.findAll(["p", "li"]))
    data.root = d

    corpus = []
    stems = {}
    for w in body_slp:
        w = re_corpus.sub("", w)
        if len(w)>3 and w.lower() not in excluir and not re_number.match(w):
            corpus.append(w)
    for i, w in enumerate(corpus):
        _w = w.lower()
        if w.upper() != w and _w != w:
            w = _w
            corpus[i]=w

    data.riqueza_lexica = len(set(corpus)) / len(corpus)
    #data.corpus = sorted(set(corpus), key=lambda x: (-len(x), x))

    corpus_stem = []
    for w in corpus:
        if w in excluir2:
            continue
        _w = get_stem(w)
        if len(_w)<4:
            continue
        corpus_stem.append(_w)
        st = stems.get(_w, set())
        st.add(w)
        stems[_w]=st


    objects = []
    performance = []
    slices = []
    freq_stem = nltk.FreqDist(corpus_stem)
    freq_corpus = {w:c for w,c in nltk.FreqDist(corpus).most_common()}
    data.freq={}
    for s, c in freq_stem.most_common(10):
        words=[]
        prct=[]
        for w in stems[s]:
            f = freq_corpus[w]
            words.append((f,w))
            prct.append(f)
        words={w:c for c,w in sorted(words, reverse=True)}
        data.freq[s]={
            "count": c,
            "words": words
        }
        if len(words)==1:
            s=list(words.keys())[0]
        else:
            s=s+"*"
        objects.append(s)
        performance.append(c)
        slices.append(sorted(prct))

    cd_mkdir("analisis")
    data.imagen = data.out_name+"png"
    set_info(data)

    y_pos = np.arange(len(objects))
    plt.rcdefaults()
    plt.barh(y_pos, performance, align='center', alpha=0.5)
    plt.yticks(y_pos, objects)#, rotation='30')
    plt.xlabel('Uso')
    plt.ylabel('Raiz')
    plt.title("%s - %s - %s" % (data.year, data.partido, data.tipo))
    plt.tight_layout()

    plt.savefig(data.imagen)
    plt.clf()

    datas.append(data)

os.chdir(cwd)
re_ltrim = re.compile(r" +$", re.MULTILINE)
def write(f, s, *args, trim=True):
    s = re_ltrim.sub("", s)
    if trim:
        s = s.strip()
    if len(args)>0:
        s = s.format(*args)
    f.write(s+"\n")

with open("analisis.md", "w") as f:
    write(f,'''
# Resumen

| Partido | Fuente | Páginas<sup>1</sup> | Párrafos | Resultado<sup>2</sup> |
|:--------|:------:|--------:|---------:|:---------:|
    '''.strip())
    for d in datas:
        formato = "PDF" if d.url.endswith(".pdf") else "HTML"
        pages = int(d.caracteres/3000)+1
        pdf_pages = d.get("pdf", {}).get("Pages", None)
        if pdf_pages is not None:
            pages = "<small>%s-%s=</small> %s" % (pdf_pages, pdf_pages-pages, pages)
        write(f,'''
| {0} | [{1}]({2}) | {3} | {4}  | [HTML + EPUB + MD]({6}/{7}zip) |
        ''',
        d.partido, formato, d.url,
        pages,
        d.parrafos,
        int(d.riqueza_lexica*100),
        d.root, data.out_name.replace(" ","%20")
        )
    write(f,"")
    write(f,'''
Notas:

* <sup>1</sup> Suponiendo unos 3000 caracteres por página. En el caso de los `pdf` aparece también una resta que representa el número de páginas del `pdf` original y el número de `páginas` ahorradas gracias a la reconversión, es decir, el espacio que se desaprovechaba por culpa de la maquetación del `pdf` y/o él uso de imagenes irrelevantes.
* <sup>2</sup> La contraseña del `zip` es `programaelectoral`
* Para el conteo de palabras en los gráficos de más abajo se han excluido algunas preposiciones, conjunciones, artículos, pronombres y adverbios
    ''')
    write(f,"")
    for d in datas:
        write(f,"# {0}", d.partido)
        write(f,"")
        write(f,'''
![{0}]({1}/analisis/{2})
        ''',d.partido, d.root, d.imagen.replace(" ","%20"))
        write(f,"")
        for s, vl in d.freq.items():
            c = vl["count"]
            words = vl["words"]
            if len(words)==1:
                s = list(words.keys())[0]
            else:
                s = s + "*:"
            write(f,"* `{0}x` {1}", c, s)
            if len(words)>1:
                for w, c in words.items():
                    write(f,"    * `{0:2}x` {1}", c, w, trim=False)
        write(f,"")