#!/usr/bin/python3
# -*- coding: utf-8 -*-
import nltk
import re
from util import get_arg, get_info, get_soup, set_info, get_pages
from glob import glob
import os
import sys

from bunch import Bunch

import numpy as np
import matplotlib.pyplot as plt

from nltk import word_tokenize
from nltk.stem import SnowballStemmer

reload = len(sys.argv)>1 and sys.argv[1]=="--reload"

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

if reload:
    for y in sorted(glob("*/info.yml")):
        d = os.path.dirname(y)
        if d in ("psoe110",):
            continue
        print("Analizando %s" % d)
        os.chdir(cwd)
        os.chdir(d)

        data = get_info(autocomplete=True)
        soup = get_soup(data.output+".html")
        body = soup.find("body")
        body_txt = re.sub(r"  +", " ", body.get_text()).strip()
        body_slp = body_txt.split()

        data.pages = get_pages(data.output+".html")
        data.caracteres = len(body_txt)
        data.palabras = len(body_slp)
        data.parrafos = len(body.findAll(["p", "li"]))
        data.root = d
        filesize = data.get("filesize", {})
        for k in ("md", "html", "epub"):
            filesize[k]=os.path.getsize(data.output+'.'+k)
        for k in ("pdf", "html", "xml"):
            if "src_"+k in filesize:
                continue
            book = "wks/book."+k
            if os.path.isfile(book):
                filesize["src_"+k]=os.path.getsize(book)
            book = "wks/books."+k
            if os.path.isfile(book):
                filesize["src_"+k]=filesize.get(k, 0) + os.path.getsize(book)
        data.filesize = filesize

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
        l_corpus_stem = len(corpus_stem)
        l_corpus = len(corpus)
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
            words={w:(c*1000/l_corpus) for c,w in sorted(words, reverse=True)}
            c = (c*1000/l_corpus_stem)
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
        data.imagen = data.output+".png"
        set_info(data)

        y_pos = np.arange(len(objects))
        plt.rcdefaults()
        plt.barh(y_pos, performance, align='center', alpha=0.5)
        plt.yticks(y_pos, objects)#, rotation='30')
        plt.xlabel('‰ de uso')
        plt.ylabel('Raiz')
        plt.title("%s - %s - %s" % (data.year, data.partido, data.tipo))
        plt.tight_layout()

        plt.savefig(data.imagen)
        plt.clf()


def bar_compare(file, title, groups, ori, res, txt_res='HTML'):
    ind = np.arange(len(groups))
    width = 0.35

    plt.rcdefaults()
    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, ori, width, color='r')
    rects2 = ax.bar(ind + width, res, width, color='g')

    ax.set_title(title)
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(parts)

    ax.legend((rects1[0], rects2[0]), ('Original', txt_res))

    plt.tight_layout()
    plt.savefig(file)
    plt.clf()

os.chdir(cwd)

datas = [get_info(yml_file=i, autocomplete=False) for i in sorted(glob("*/analisis/info.yml"))]

if True or reload:
    parts = []
    pag_ori = []
    siz_ori = []
    pag_res = []
    siz_res = []

    for d in datas:
        p0 = d.get("src_pages", None) or d.pdf["Pages"]
        s0 = d.filesize.get("src_pdf", None) or d.filesize["src_html"]
        parts.append(d.partido)
        pag_ori.append(p0)
        siz_ori.append(s0/1024)
        pag_res.append(d.pages)
        siz_res.append(d.filesize["epub"]/1024)

    bar_compare("analisis/pag.png", "Páginas", parts, pag_ori, pag_res)
    bar_compare("analisis/size.png", "Tamaño en KB", parts, siz_ori, siz_res, txt_res='EPUB')

re_ltrim = re.compile(r" +$", re.MULTILINE)
def write(f, s, *args, trim=True):
    s = re_ltrim.sub("", s)
    if trim:
        s = s.strip()
    if len(args)>0:
        s = s.format(*args)
    f.write(s+"\n")


f=open("README.md", "w")

write(f,'''
# Resumen

| Partido | Fuente | Párrafos | Resultado<sup>1</sup> | Páginas<sup>2</sup>
|:--------|:------:|--------:|:---------:|---------:|
'''.strip())
for d in datas:
    formato = "PDF" if d.url.endswith(".pdf") else "HTML"
    write(f,'''
| {0} | [{1}]({2}) | {4}  | HTML + EPUB + MD | {3} |
    ''',
    d.partido, formato, d.url,
    d.pages,
    d.parrafos,
    int(d.riqueza_lexica*100),
    "#", d.root,
    "#" #d.output.replace(" ","%20")
    )
write(f,"")
write(f,'''
Notas:

* <sup>1</sup> Se puede descargar de https://we.tl/t-CwCneKiaFF y la contraseña de los `zip` es `programaelectoral`.
* <sup>2</sup> Valor calculado del resultado de imprimir el `html` generado en formato `Din A4`, con fuente `Arial 12pt` y margen de `1cm`.
''')
write(f,'''

# ¿Por qué no usar PDF?

Hay muchos motivos para no usar `pdf` pero lo resumiría en que el `pdf`
esta pensado para que el usuario vea el `pdf` como quiere el autor, no
como quiere y necesita el usuario.

Si necesitas cambiar los margenes, el tipo de letra, o quitar las imágenes
decorativas será un infierno.

Quizá el programa hable de ecología, diversidad funcional, transparencia,
open data, licencias libres y flexibilidad, pero su propio formato no te deja remaquetarlo
para ahorrar papel cuando lo imprimas, tampoco te deja cambiarle el tipo
de letra para ayudarte con la compresión lectora si sufres algún tipo de
dislexia, en muchos casos usar un lector de texto para ciegos será imposible,
y mucho menos es libre, abierto, transparente o flexible.

# ¿Cómo se ha hecho la conversión?

Muy a grandes rasgos se han usado las herramientas de `poppler-utils` para
generar de cada `pdf` un `xml` y un `txt`, los cuales lee un script `python`
para conseguir recolocar y ensamblar el texto a la vez que detecta que es
un título, que es un párrafo y que es una lista, para finalmente generar un
fichero `Markdown` el cual se convierte a `epub` y `html` con `pandoc`.

En los casos que se podía usar como fuente un `html` en vez de un `pdf`
solo ha hecho falta arreglar los problemas de maquetación para generar
un `Markdown` que ya sirviera para el resto del proceso.

# Dificultad de conversión

La dificultad principal al convertir un `pdf` a texto plano, en concreto a un
lenguaje de marcado, es detectar el texto relevante (por ejemplo, no quieres copiar
los números de página), ensamblarlo correctamente
(pues en un `pdf` el texto no es "fluido"), incluso recolocarlo en no pocas ocasiones,
y a menudo corregir erratas que se producen en la transformación... pero veamos
en más detalle cada caso:

## Fácil

El programa más fácil de convertir ha sido sin duda **PACMA**. La razón es obvia,
existe una versión `html` bastante bien maquetada
([aunque el validador encuentra errores graves que le impiden completar el analisis `HTML`](https://validator.w3.org/check?charset=%28detect+automatically%29&doctype=Inline&group=1&uri=https://pacma.es/elecciones-2019/compromisos)
para nuestro proposito solo habia dos errores que realmente nos afectaban y eran de fácil solución)
y estaba cerca de cumplir las normas de Accesibilidad Web AA
([solo 8 problemas](https://www.tawdis.net/resumen?url=https%3A%2F%2Fpacma.es%2Felecciones-2019%2Fcompromisos&nivel=aa&crc=0)).

## Regular

El segundo programa más fácil en convertir fue el otro también disponible en `HTML`, el de **Ciudadanos**.
La diferencia con el predecesor es que estaba muy mal maquetado ([104 errores `HTML`](https://validator.w3.org/check?charset=%28detect+automatically%29&doctype=Inline&group=1&uri=https://www.ciudadanos-cs.org/programa-electoral))
y no cumple Accesibilidad Web AA ni de lejos ([68 problemas](https://www.tawdis.net/resumen?url=https%3A%2F%2Fwww.ciudadanos-cs.org%2Felecciones-2019&nivel=aa&crc=0)).

Aún así esto siempre será mejor que un `pdf`.

El caso de Ciudadanos llama la atención porque su programa de 2015 fue el `pdf`
más dificil que he visto: El texto no era texto, si no imágenes de texto
(hubo que usar `OCR` para intentar sacar algo), la indentación y los símbolos
que marcaban la jerarquía de los capítulos y listas era totalmente ambigua,
había partes repetidas en distintos capítulos, etc...

El porqué de este cambio lo atribuyo a la absorción de parte de **UPyD** por Ciudadanos,
ya que UPyD era uno de los pocos partidos que publicaba sistemáticamente su
programa en `HTML` y lo hacia de la misma manera (con múltiples problemas de maquetación
y accesibilidad).

## Difícil

Los programas de **Vox** y **Podemos** se encuentran en un nivel similar, y esperable, de dificultad.
Es decir, el propio de un `pdf` que al menos es lo suficientemente homogenio y simple
(básicamente son una lista de puntos con un solo nivel de indentación) como para
que no sea un infierno reensamblar el texto.

## Innecesariamente difíciles

Los tres que nos quedan son innecesariamente difíciles por distintas razones:

El de **Actua** esta mal generado (por los metadatos se ve que se ha hecho imprimiendo un `docx` a `pdf`)
de manera que al extraer el texto muchas palabras se dividen en varios
trozos (por ejemplo, `Póli tica So i a l`) y la posición y las coordenadas de los
bloques de texto están de tal manera que dificultaban la programación.

El del **PP** está lleno de fotos del líder posando que estorban,
empieza con páginas a una sola columna,
luego a dos columnas en un determinado formato, luego sigue a dos columnas pero en
otro formato y los márgenes no son estables, obligándote a readaptar el script
en cada movimiento y a renunciar
a detectar algunos contenidos (como los títulos, o algunas páginas en concreto)
de manera elegante y terminar hardcodeándolo.

El del **PSOE** aunque también es a dos columnas mantienen su formato
durante todo el documento, sin embargo, lo que es un caos es la indentación.
En ocasiones el uso de `-`, `*`, números y letras para listas se va alternando
sin quedar claro cuál es su jerarquía. A veces hay el típico aumento del
margen derecho que denota dicha jerarquía y otras veces no, a veces
parece que la lógica es "primero número, luego `-` y luego `*`" y otras veces
"primero número, luego `*` y luego `-`" u otra combinación posible.
De manera que al final renuncié a representar de manera semántica mediante un
buen lenguaje de marcado cualquier
tipo de jerarquía en las listas y simplemente muestro todo como un párrafo
detrás de otro.

## Resultado

Solo el de PACMA queda realmente bien ya que el de Ciudadanos pierde o recupera
estilos según se mire (no lo explico por no enrollarme, pero quien vea el código
y sepa de `html` lo entenderá) y los que estaban en `pdf` cada uno tiene sus problemas
no pudiéndose reproducir en ningún caso todos los estilos o formatos.

Sin embargo los textos están completos, que es lo que importa. Así que puedes
usar las versiones `epub`, `html` y `markdown` sin problemas y más cómodamente
que cualquiera de los originales.

''')

write(f,'''
# Páginas y tamaño

<table>
<thead>
<tr>
    <th rowspan="2">Partido</th>
    <th colspan="3" align="center">Páginas</th>
    <th colspan="3" align="center">Tamaño (KB)</th>
</tr>
    <tr>
        <th>Original<sup>1</sup></th>
        <th>HTML</th>
        <th>Ahorro</th>
        <th>Original<sup>2</sup></th>
        <th>EPUB</th>
        <th>Ahorro</th>
    </tr>
</thead>
<tbody>
''')
for d in datas:
    p0 = d.get("src_pages", None) or d.pdf["Pages"]
    s0 = d.filesize.get("src_pdf", None) or d.filesize["src_html"]
    write(f,'''
    <tr>
        <td>{0}</td>
        <td align="right">{1}</td>
        <td align="right">{2}</td>
        <td align="right">{3} %</td>
        <td align="right">{4}</td>
        <td align="right">{5}</td>
        <td align="right">{6} %</td>
    </tr>
    ''',
    d.partido,
    p0,
    d.pages,
    int((p0-d.pages)*100/p0),
    int(s0/1024),
    int(d.filesize["epub"]/1024),
    int((s0-d.filesize["epub"])*100/s0)
    )
write(f,'''
</tbody>
</table>

Notas:

* <sup>1</sup> Para Ciudadanos el valor es lo que resultaría de imprimir su página web.
Para el resto es el número de páginas de sus `pdf` (esto incluye a PACMA porque también tenían una [versión `pdf`](https://pacma.es/elecciones-2019/files/pacma-compromisos-elecciones-generales-2019.pdf)).
* <sup>2</sup> Para Ciudadanos el valor es lo que resultaría de descargar su página web, incluido `css`, `javascript` e imágenes.
Para el resto es el número tamaño de su `pdf`.

## ¿En qué se van tantas páginas?

![Páginas](/analisis/pag.png)

Lo más común es que se rellenen páginas con grandes margenes y un tamaño de letra
amplio (si, justo como en el cole), lo cual, aunque no me gusta,
es hasta cierto punto normal porque mucha
gente encuentra la lectura más cómoda así. Este es el caso de la mayoría, con
la excepción del **PP**, que usando un tipo de letra relativamente pequeño
en comparación con los otros derrocha espacio con múltiples fotos del líder
posando y otras con pinta de `powerpoint` de una presentación corporativa.

## ¿En qué se van tantos KB?

![Tamaño](/analisis/size.png)

Aquí se ve muy bien lo dicho anteriormente sobre el **PP**, mientras que en los
demás la reducción de peso es la normal, en el PP se dispara al prescindir de
los elementos decorativos o de exhibición del líder.

# Palabras más usadas

Tras eliminar algunas preposiciones, conjunciones, artículos, pronombres, adverbios
y otras palabras poco relevantes pero muy usadas en nuestro idioma, se buscan
las raíces de palabras más usadas (representadas con la raíz más un `*`) y se
escogen las 10 más usadas. Si da la casualidad de que alguna de esas raíces
solo corresponde a una palabra, indico directamente la palabra en vez de la raíz
(y por lo tanto no llevará `*`).

Bajo los gráficos se encuentra el desglose de palabras pertenecientes a una raíz.

**¡OJO!** Que los porcentajes son en ‰ (tanto por mil), no en % (tanto por ciento).

''')
write(f,"")
for d in datas:
    write(f,"## {0}", d.partido)
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
        write(f,"* `{0:.2f}` ‰ {1}", c, s)
        if len(words)>1:
            for w, c in words.items():
                write(f,"    * `{0:2.2f}` ‰ {1}", c, w, trim=False)
    write(f,"")
write(f,'''
## Conclusiones

No creo que realmente se pueda extraer conclusiones serias de estos gráficos
que no supiéramos todos ya.
''')

f.close()
