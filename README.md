# Resumen

| Partido | Fuente | Párrafos | Resultado<sup>1</sup> | Páginas<sup>2</sup>
|:--------|:------:|--------:|:---------:|---------:|
| Actua | [PDF](http://reaccionayactua.com/wp-content/uploads/2019/04/Programa-Actu%CC%81a-Generales-19.pdf) | 369  | [HTML + EPUB + MD](#/actua.zip) | 23 |
| Ciudadanos | [HTML](https://www.ciudadanos-cs.org/programa-electoral) | 268  | [HTML + EPUB + MD](#/ciudadanos.zip) | 21 |
| PACMA | [HTML](https://pacma.es/elecciones-2019/compromisos) | 853  | [HTML + EPUB + MD](#/pacma.zip) | 45 |
| Podemos | [PDF](https://podemos.info/wp-content/uploads/2019/04/Podemos_programa_generales_28A.pdf) | 292  | [HTML + EPUB + MD](#/podemos.zip) | 33 |
| PP | [PDF](http://www.pp.es/sites/default/files/documentos/programa_electoral_2019_pp_0.pdf) | 693  | [HTML + EPUB + MD](#/pp.zip) | 42 |
| PSOE | [PDF](https://www.psoe.es/media-content/2019/04/PSOE-programa-electoral-elecciones-generales-28-de-abril-de-2019.pdf) | 1389  | [HTML + EPUB + MD](#/psoe.zip) | 91 |
| Vox | [PDF](https://www.voxespana.es/biblioteca/espana/2018m/gal_c2d72e181103013447.pdf) | 100  | [HTML + EPUB + MD](#/vox.zip) | 6 |

Notas:

* <sup>1</sup> ~~La contraseña del `zip` es `programaelectoral`~~ Actualmente no esta disponible para descargar.
* <sup>2</sup> Valor calculado del resultado de imprimir el `html` generado en formato `Din A4`, con fuente `Arial 12pt` y margen de `1cm`.
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
más chungo que he visto: El texto no era texto, si no imágenes de texto
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
cada dos por tres y a renunciar
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
<tr>
        <td>Actua</td>
        <td align="right">41</td>
        <td align="right">23</td>
        <td align="right">43 %</td>
        <td align="right">1501</td>
        <td align="right">57</td>
        <td align="right">96 %</td>
    </tr>
<tr>
        <td>Ciudadanos</td>
        <td align="right">26</td>
        <td align="right">21</td>
        <td align="right">19 %</td>
        <td align="right">1125</td>
        <td align="right">58</td>
        <td align="right">94 %</td>
    </tr>
<tr>
        <td>PACMA</td>
        <td align="right">92</td>
        <td align="right">45</td>
        <td align="right">51 %</td>
        <td align="right">877</td>
        <td align="right">80</td>
        <td align="right">90 %</td>
    </tr>
<tr>
        <td>Podemos</td>
        <td align="right">105</td>
        <td align="right">33</td>
        <td align="right">68 %</td>
        <td align="right">839</td>
        <td align="right">82</td>
        <td align="right">90 %</td>
    </tr>
<tr>
        <td>PP</td>
        <td align="right">102</td>
        <td align="right">42</td>
        <td align="right">58 %</td>
        <td align="right">5709</td>
        <td align="right">81</td>
        <td align="right">98 %</td>
    </tr>
<tr>
        <td>PSOE</td>
        <td align="right">152</td>
        <td align="right">91</td>
        <td align="right">40 %</td>
        <td align="right">615</td>
        <td align="right">161</td>
        <td align="right">73 %</td>
    </tr>
<tr>
        <td>Vox</td>
        <td align="right">25</td>
        <td align="right">6</td>
        <td align="right">76 %</td>
        <td align="right">183</td>
        <td align="right">23</td>
        <td align="right">87 %</td>
    </tr>
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

## Actua

![Actua](actua/analisis/2019%20-%20Generales%20-%20Actua.png)

* `14.13` ‰ public*:
    * `5.56` ‰ públicos
    * `2.91` ‰ pública
    * `2.78` ‰ públicas
    * `1.77` ‰ público
    * `0.13` ‰ publicación
* `9.24` ‰ social*:
    * `5.69` ‰ social
    * `2.65` ‰ sociales
    * `0.25` ‰ socialmente
* `8.29` ‰ polit*:
    * `3.54` ‰ política
    * `3.29` ‰ políticas
    * `0.51` ‰ político
    * `0.38` ‰ políticos
* `8.15` ‰ derech*:
    * `4.68` ‰ derechos
    * `1.77` ‰ derecho
    * `1.01` ‰ derecha
    * `0.13` ‰ derechas
* `6.52` ‰ model*:
    * `5.43` ‰ modelo
    * `0.63` ‰ modelos
* `6.25` ‰ econom*:
    * `1.90` ‰ económica
    * `1.39` ‰ económico
    * `1.01` ‰ economía
    * `0.76` ‰ económicas
    * `0.51` ‰ económicos
    * `0.13` ‰ económicamente
    * `0.13` ‰ economista
* `5.43` ‰ autonom*:
    * `1.77` ‰ autónomas
    * `1.26` ‰ autonomía
    * `0.38` ‰ autónomos
    * `0.38` ‰ autonómico
    * `0.38` ‰ autonómicas
    * `0.38` ‰ autonómica
    * `0.25` ‰ autonómicos
    * `0.25` ‰ autonomías
* `5.30` ‰ servici*:
    * `3.92` ‰ servicios
    * `1.01` ‰ servicio
* `5.30` ‰ sistem*:
    * `4.17` ‰ sistema
    * `0.63` ‰ sistemas
    * `0.13` ‰ sistémica
* `5.03` ‰ español*:
    * `3.79` ‰ españa
    * `0.38` ‰ española
    * `0.25` ‰ españolas
    * `0.13` ‰ españoles
    * `0.13` ‰ español

## Ciudadanos

![Ciudadanos](ciudadanos/analisis/2019%20-%20Generales%20-%20Ciudadanos.png)

* `17.63` ‰ español*:
    * `9.88` ‰ españa
    * `2.61` ‰ españoles
    * `1.92` ‰ español
    * `1.65` ‰ española
    * `0.41` ‰ españolas
* `12.49` ‰ public*:
    * `3.43` ‰ públicos
    * `3.02` ‰ públicas
    * `2.47` ‰ público
    * `2.06` ‰ pública
    * `0.14` ‰ publicarse
    * `0.14` ‰ publicaremos
    * `0.14` ‰ publicar
    * `0.14` ‰ publicando
    * `0.14` ‰ publicación
* `10.72` ‰ garantiz*:
    * `4.53` ‰ garantizar
    * `4.12` ‰ garantizaremos
    * `0.82` ‰ garantizando
    * `0.27` ‰ garantizará
    * `0.14` ‰ garantizarles
    * `0.14` ‰ garantizado
* `8.08` ‰ nacional*:
    * `6.45` ‰ nacional
    * `0.41` ‰ nacionales
    * `0.27` ‰ nacionalistas
    * `0.27` ‰ nacionalista
    * `0.14` ‰ nacionalidad
* `7.05` ‰ derech*:
    * `3.71` ‰ derecho
    * `2.88` ‰ derechos
* `6.90` ‰ impuls*:
    * `5.35` ‰ impulsaremos
    * `0.55` ‰ impulsando
    * `0.27` ‰ impulsar
    * `0.14` ‰ impulsará
    * `0.14` ‰ impulsada
* `6.32` ‰ mejor*:
    * `1.65` ‰ mejorar
    * `1.51` ‰ mejores
    * `1.51` ‰ mejoraremos
    * `0.96` ‰ mejora
    * `0.14` ‰ mejore
    * `0.14` ‰ mejorando
* `6.17` ‰ nuev*:
    * `1.92` ‰ nuevo
    * `1.51` ‰ nuevos
    * `1.51` ‰ nueva
    * `0.82` ‰ nuevas
* `5.88` ‰ trabaj*:
    * `2.47` ‰ trabajo
    * `1.51` ‰ trabajadores
    * `0.41` ‰ trabajador
    * `0.27` ‰ trabajar
    * `0.14` ‰ trabajos
    * `0.14` ‰ trabajen
    * `0.14` ‰ trabajaremos
    * `0.14` ‰ trabajando
    * `0.14` ‰ trabajadoras
    * `0.14` ‰ trabajadora
* `5.88` ‰ acab*:
    * `3.02` ‰ acabar
    * `2.47` ‰ acabaremos

## PACMA

![PACMA](pacma/analisis/2019%20-%20Generales%20-%20PACMA.png)

* `25.45` ‰ animal*:
    * `17.22` ‰ animales
    * `3.87` ‰ animal
    * `2.34` ‰ animalista
    * `0.07` ‰ animalistas
* `8.89` ‰ public*:
    * `2.00` ‰ pública
    * `1.87` ‰ público
    * `1.80` ‰ públicas
    * `1.74` ‰ públicos
    * `0.27` ‰ publicado
    * `0.13` ‰ publicar
    * `0.13` ‰ publicando
    * `0.13` ‰ publicación
    * `0.07` ‰ públicamente
    * `0.07` ‰ publicarán
* `8.46` ‰ person*:
    * `7.28` ‰ personas
    * `0.47` ‰ persona
    * `0.07` ‰ personan
* `6.22` ‰ educ*:
    * `3.27` ‰ educación
    * `1.07` ‰ educativo
    * `0.80` ‰ educativos
    * `0.27` ‰ educativas
    * `0.13` ‰ educativa
    * `0.13` ‰ educar
    * `0.07` ‰ educadores
* `6.14` ‰ desarroll*:
    * `3.87` ‰ desarrollo
    * `0.87` ‰ desarrollar
    * `0.47` ‰ desarrollen
    * `0.13` ‰ desarrollando
    * `0.13` ‰ desarrollan
    * `0.07` ‰ desarrollos
    * `0.07` ‰ desarrollados
    * `0.07` ‰ desarrolla
* `6.07` ‰ social*:
    * `3.74` ‰ social
    * `1.87` ‰ sociales
* `5.64` ‰ propon*:
    * `4.54` ‰ proponemos
    * `0.60` ‰ propone
    * `0.07` ‰ proponer
* `5.20` ‰ salud*:
    * `4.41` ‰ salud
    * `0.27` ‰ saludables
    * `0.13` ‰ saludable
* `5.06` ‰ polit*:
    * `2.34` ‰ políticas
    * `1.74` ‰ política
    * `0.53` ‰ políticos
    * `0.07` ‰ político
* `4.70` ‰ protección

## Podemos

![Podemos](podemos/analisis/2019%20-%20Generales%20-%20Podemos.png)

* `11.00` ‰ public*:
    * `3.04` ‰ público
    * `2.97` ‰ pública
    * `2.05` ‰ públicas
    * `1.70` ‰ públicos
    * `0.07` ‰ publicaremos
    * `0.07` ‰ publicar
    * `0.07` ‰ publicado
    * `0.07` ‰ publicación
* `9.60` ‰ derech*:
    * `5.65` ‰ derechos
    * `2.90` ‰ derecho
    * `0.14` ‰ derecha
    * `0.07` ‰ derechas
* `8.60` ‰ trabaj*:
    * `2.19` ‰ trabajo
    * `1.62` ‰ trabajadores
    * `1.41` ‰ trabajadoras
    * `0.57` ‰ trabajar
    * `0.49` ‰ trabajan
    * `0.42` ‰ trabajadora
    * `0.28` ‰ trabajará
    * `0.28` ‰ trabajador
    * `0.21` ‰ trabajaremos
    * `0.14` ‰ trabajos
    * `0.07` ‰ trabajamos
    * `0.07` ‰ trabajado
    * `0.07` ‰ trabaja
* `8.29` ‰ person*:
    * `6.64` ‰ personas
    * `0.92` ‰ persona
* `6.89` ‰ español*:
    * `4.10` ‰ españa
    * `0.92` ‰ española
    * `0.71` ‰ españolas
    * `0.42` ‰ españoles
    * `0.14` ‰ español
* `6.58` ‰ servici*:
    * `4.59` ‰ servicios
    * `1.41` ‰ servicio
* `5.96` ‰ establec*:
    * `1.70` ‰ estableceremos
    * `1.34` ‰ establecer
    * `0.71` ‰ establecerá
    * `0.49` ‰ establecerán
    * `0.28` ‰ establecimientos
    * `0.28` ‰ establecimiento
    * `0.21` ‰ establecido
    * `0.14` ‰ estableciendo
    * `0.14` ‰ establecida
    * `0.14` ‰ establece
* `5.89` ‰ pais*:
    * `4.45` ‰ país
    * `0.92` ‰ países
* `5.34` ‰ sistem*:
    * `4.24` ‰ sistema
    * `0.64` ‰ sistemas
* `5.19` ‰ social*:
    * `2.68` ‰ social
    * `1.91` ‰ sociales
    * `0.07` ‰ socialmente
    * `0.07` ‰ socialista

## PP

![PP](pp/analisis/2019%20-%20Generales%20-%20PP.png)

* `12.06` ‰ español*:
    * `6.21` ‰ españa
    * `2.27` ‰ españoles
    * `1.46` ‰ española
    * `0.88` ‰ español
    * `0.58` ‰ españolas
* `11.60` ‰ impuls*:
    * `6.94` ‰ impulsaremos
    * `1.24` ‰ impulsar
    * `1.24` ‰ impulsando
    * `0.88` ‰ impulso
    * `0.22` ‰ impulsarán
    * `0.15` ‰ impulsen
    * `0.07` ‰ impulse
    * `0.07` ‰ impulsará
    * `0.07` ‰ impulsan
    * `0.07` ‰ impulsado
* `8.43` ‰ desarroll*:
    * `4.68` ‰ desarrollo
    * `2.12` ‰ desarrollaremos
    * `0.22` ‰ desarrollar
    * `0.22` ‰ desarrollando
    * `0.15` ‰ desarrollen
    * `0.15` ‰ desarrolladas
    * `0.07` ‰ desarrollos
    * `0.07` ‰ desarrolle
    * `0.07` ‰ desarrollará
    * `0.07` ‰ desarrollarse
    * `0.07` ‰ desarrollan
    * `0.07` ‰ desarrolladores
* `8.27` ‰ public*:
    * `2.70` ‰ públicos
    * `1.68` ‰ público
    * `1.61` ‰ públicas
    * `1.53` ‰ pública
    * `0.07` ‰ públicamente
    * `0.07` ‰ publicando
    * `0.07` ‰ publicados
    * `0.07` ‰ publicación
* `7.81` ‰ promov*:
    * `5.55` ‰ promoveremos
    * `1.02` ‰ promover
    * `0.44` ‰ promoviendo
    * `0.22` ‰ promoverán
    * `0.15` ‰ promoverá
* `7.58` ‰ plan*:
    * `4.38` ‰ plan
    * `2.78` ‰ planes
* `7.42` ‰ nacional*:
    * `5.63` ‰ nacional
    * `1.10` ‰ nacionales
    * `0.15` ‰ nacionalidad
    * `0.07` ‰ nacionalismos
    * `0.07` ‰ nacionalismo
* `6.49` ‰ nuev*:
    * `2.56` ‰ nuevas
    * `1.83` ‰ nuevos
    * `0.95` ‰ nueva
    * `0.80` ‰ nuevo
* `6.18` ‰ segur*:
    * `5.19` ‰ seguridad
    * `0.22` ‰ seguras
    * `0.15` ‰ seguros
    * `0.15` ‰ seguro
    * `0.15` ‰ segura
* `6.11` ‰ autonom*:
    * `2.63` ‰ autónomas
    * `0.66` ‰ autonómicos
    * `0.58` ‰ autonómico
    * `0.51` ‰ autónomos
    * `0.44` ‰ autonómicas
    * `0.37` ‰ autonomía
    * `0.22` ‰ autónomo
    * `0.22` ‰ autonómica
    * `0.07` ‰ autónoma
    * `0.07` ‰ autonomías

## PSOE

![PSOE](psoe/analisis/2019%20-%20Generales%20-%20PSOE.png)

* `13.97` ‰ social*:
    * `5.80` ‰ social
    * `3.30` ‰ sociales
    * `2.31` ‰ socialista
    * `1.60` ‰ socialistas
    * `0.06` ‰ socialmente
* `10.58` ‰ español*:
    * `6.12` ‰ españa
    * `1.35` ‰ española
    * `1.03` ‰ españoles
    * `0.71` ‰ español
    * `0.67` ‰ españolas
    * `0.03` ‰ españas
* `7.67` ‰ derech*:
    * `4.55` ‰ derechos
    * `2.31` ‰ derecho
    * `0.22` ‰ derecha
    * `0.10` ‰ derechas
* `7.50` ‰ public*:
    * `1.89` ‰ pública
    * `1.76` ‰ público
    * `1.70` ‰ públicos
    * `1.54` ‰ públicas
    * `0.06` ‰ publicación
    * `0.03` ‰ públicamente
    * `0.03` ‰ publicando
* `7.36` ‰ polit*:
    * `3.14` ‰ políticas
    * `3.05` ‰ política
    * `0.38` ‰ políticos
    * `0.32` ‰ político
* `6.99` ‰ impuls*:
    * `2.21` ‰ impulsar
    * `1.73` ‰ impulsaremos
    * `1.03` ‰ impulso
    * `0.54` ‰ impulsando
    * `0.42` ‰ impulsado
    * `0.16` ‰ impulse
    * `0.16` ‰ impulsará
    * `0.13` ‰ impulsarán
    * `0.06` ‰ impulsadas
    * `0.03` ‰ impulsó
    * `0.03` ‰ impulsan
    * `0.03` ‰ impulsa
* `6.82` ‰ desarroll*:
    * `3.62` ‰ desarrollo
    * `1.38` ‰ desarrollar
    * `0.38` ‰ desarrollando
    * `0.35` ‰ desarrollaremos
    * `0.13` ‰ desarrollen
    * `0.10` ‰ desarrolle
    * `0.10` ‰ desarrollan
    * `0.06` ‰ desarrollos
    * `0.06` ‰ desarrollada
    * `0.03` ‰ desarrolló
    * `0.03` ‰ desarrollaran
    * `0.03` ‰ desarrollados
    * `0.03` ‰ desarrollado
    * `0.03` ‰ desarrolladas
    * `0.03` ‰ desarrolla
* `6.75` ‰ person*:
    * `5.93` ‰ personas
    * `0.38` ‰ persona
* `6.44` ‰ gobiern*:
    * `5.96` ‰ gobierno
    * `0.03` ‰ gobierne
    * `0.03` ‰ gobierna
* `6.20` ‰ sistem*:
    * `5.03` ‰ sistema
    * `0.71` ‰ sistemas
    * `0.03` ‰ sistémico
    * `0.03` ‰ sistémicas

## Vox

![Vox](vox/analisis/2019%20-%20Generales%20-%20Vox.png)

* `24.96` ‰ español*:
    * `8.85` ‰ españa
    * `4.43` ‰ españoles
    * `3.87` ‰ española
    * `3.87` ‰ español
    * `2.21` ‰ españolas
* `13.67` ‰ nacional*:
    * `8.85` ‰ nacional
    * `2.77` ‰ nacionalidad
    * `0.55` ‰ nacionalidades
    * `0.55` ‰ nacionales
* `11.29` ‰ public*:
    * `3.87` ‰ públicos
    * `2.77` ‰ público
    * `2.21` ‰ pública
    * `1.11` ‰ públicas
    * `0.55` ‰ publicación
* `8.91` ‰ famili*:
    * `3.87` ‰ familias
    * `2.21` ‰ familiar
    * `2.21` ‰ familia
* `7.13` ‰ inmigr*:
    * `2.77` ‰ inmigrantes
    * `2.77` ‰ inmigración
    * `1.11` ‰ inmigrante
* `7.13` ‰ empres*:
    * `3.87` ‰ empresa
    * `2.77` ‰ empresas
* `6.54` ‰ estado
* `5.94` ‰ autonom*:
    * `2.77` ‰ autonómicas
    * `0.55` ‰ autónomos
    * `0.55` ‰ autónoma
    * `0.55` ‰ autonómico
    * `0.55` ‰ autonómica
    * `0.55` ‰ autonomía
* `5.35` ‰ ilegal*:
    * `2.77` ‰ ilegales
    * `1.66` ‰ ilegal
    * `0.55` ‰ ilegalmente
* `5.35` ‰ reducción

## Conclusiones

No creo que realmente se pueda extraer conclusiones serias de estos gráficos
que no supiéramos todos ya.
