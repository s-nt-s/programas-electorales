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
decorativas sera un infierno.

Quizá el programa hable de ecología, diversidad funcional, transparencia,
open data, licencias libres y flexibilidad, pero su propio formato no te deja remaquetarlo
para ahorrar papel cuando lo imprimas, tampoco te deja cambiarle el tipo
de letra para ayudarte con la compresión lectora si sufres algún tipo de
dislexia, en muchos casos usar un lector de texto para ciegos sera imposible,
y mucho menos es libre, abierto, transparente o flexible.

# ¿Cómo se ha hecho la conversión?

Muy a grandes rasgos se han usado las herramientas de `poppler-utils` para
generar de cada `pdf` un `xml` y un `txt`, los cuales lee un script `python`
para conseguir recolocar y ensamblar el texto a la vez que detecta que es
un título, que es un párrafo y que es una lista, para finalmente generar un
fichero `Markdown` el cual se convierte a `epub` y `html` con `pandoc`.

En los casos que se podía usar como fuente un `html` en vez de un `pdf`
solo ha hecho falta la arreglar los problemas de maquetación para generar
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
Es decir, el propio de un `pdf` que al menos es lo suficientemente homogeneizo y simple
(básicamente son una lista de puntos con un solo nivel de indentación) como para
que no sea un infierno reensamblar el texto.

## Innecesariamente difíciles

Los tres que nos quedan son innecesariamente difíciles por distintas razones:

El de **Actua** esta mal generado (por los metadatos se ve que se ha hecho imprimiendo un `docx` a `pdf`)
de manera que al extraer el texto muchas palabras se dividen en varios
trozos (por ejemplo, `Póli tica So i a l`) y la posición y las coordenadas de los
bloques de texto están de tal manera que dificultaban la programación.

El del **PP** esta lleno de fotos del líder posando que estorban,
empieza con paginas a una sola columna,
luego a dos columnas en un determinado formato, luego sigue a dos columnas pero en
otro formato y los margenes no son estables, obligándote a readaptar el script
cada dos por tres y a renunciar
a detectar algunos contenidos (como los títulos, o algunas páginas en concreto)
de manera elegante y terminar hardcodeandolo.

El del **PSOE** aunque también es a dos columnas mantienen su formato
durante todo el documento, sin embargo, lo que es un caos es la indentación.
En ocasiones el uso de `-`, `*`, números y letras para listas se va alternando
sin quedar claro cual es su jerarquía. A veces hay el típico aumento del
margen derecho que denota dicha jerarquía y otras veces no, a veces
parece que la lógica es "primero número, luego `-` y luego `*`" y otras veces
"primero número, luego `*` y luego `-`" u otra combinación posible.
De manera que al final renuncie a representar de manera semántica mediante un
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
(y por lo tanto no llevara `*`).

Bajo los gráficos se encuentra el desglose de palabras pertenecientes a una raíz.

## Actua

![Actua](actua/analisis/2019%20-%20Generales%20-%20Actua.png)

* `104x` public*:
    * `44x` públicos
    * `23x` pública
    * `22x` públicas
    * `14x` público
    * ` 1x` publicación
* `68x` social*:
    * `45x` social
    * `21x` sociales
    * ` 2x` socialmente
* `61x` polit*:
    * `28x` política
    * `26x` políticas
    * ` 4x` político
    * ` 3x` políticos
* `60x` derech*:
    * `37x` derechos
    * `14x` derecho
    * ` 8x` derecha
    * ` 1x` derechas
* `48x` model*:
    * `43x` modelo
    * ` 5x` modelos
* `46x` econom*:
    * `15x` económica
    * `11x` económico
    * ` 8x` economía
    * ` 6x` económicas
    * ` 4x` económicos
    * ` 1x` económicamente
    * ` 1x` economista
* `40x` autonom*:
    * `14x` autónomas
    * `10x` autonomía
    * ` 3x` autónomos
    * ` 3x` autonómico
    * ` 3x` autonómicas
    * ` 3x` autonómica
    * ` 2x` autonómicos
    * ` 2x` autonomías
* `39x` servici*:
    * `31x` servicios
    * ` 8x` servicio
* `39x` sistem*:
    * `33x` sistema
    * ` 5x` sistemas
    * ` 1x` sistémica
* `37x` español*:
    * `30x` españa
    * ` 3x` española
    * ` 2x` españolas
    * ` 1x` españoles
    * ` 1x` español

## Ciudadanos

![Ciudadanos](ciudadanos/analisis/2019%20-%20Generales%20-%20Ciudadanos.png)

* `120x` español*:
    * `72x` españa
    * `19x` españoles
    * `14x` español
    * `12x` española
    * ` 3x` españolas
* `85x` public*:
    * `25x` públicos
    * `22x` públicas
    * `18x` público
    * `15x` pública
    * ` 1x` publicarse
    * ` 1x` publicaremos
    * ` 1x` publicar
    * ` 1x` publicando
    * ` 1x` publicación
* `73x` garantiz*:
    * `33x` garantizar
    * `30x` garantizaremos
    * ` 6x` garantizando
    * ` 2x` garantizará
    * ` 1x` garantizarles
    * ` 1x` garantizado
* `55x` nacional*:
    * `47x` nacional
    * ` 3x` nacionales
    * ` 2x` nacionalistas
    * ` 2x` nacionalista
    * ` 1x` nacionalidad
* `48x` derech*:
    * `27x` derecho
    * `21x` derechos
* `47x` impuls*:
    * `39x` impulsaremos
    * ` 4x` impulsando
    * ` 2x` impulsar
    * ` 1x` impulsará
    * ` 1x` impulsada
* `43x` mejor*:
    * `12x` mejorar
    * `11x` mejores
    * `11x` mejoraremos
    * ` 7x` mejora
    * ` 1x` mejore
    * ` 1x` mejorando
* `42x` nuev*:
    * `14x` nuevo
    * `11x` nuevos
    * `11x` nueva
    * ` 6x` nuevas
* `40x` trabaj*:
    * `18x` trabajo
    * `11x` trabajadores
    * ` 3x` trabajador
    * ` 2x` trabajar
    * ` 1x` trabajos
    * ` 1x` trabajen
    * ` 1x` trabajaremos
    * ` 1x` trabajando
    * ` 1x` trabajadoras
    * ` 1x` trabajadora
* `40x` acab*:
    * `22x` acabar
    * `18x` acabaremos

## PACMA

![PACMA](pacma/analisis/2019%20-%20Generales%20-%20PACMA.png)

* `352x` animal*:
    * `258x` animales
    * `58x` animal
    * `35x` animalista
    * ` 1x` animalistas
* `123x` public*:
    * `30x` pública
    * `28x` público
    * `27x` públicas
    * `26x` públicos
    * ` 4x` publicado
    * ` 2x` publicar
    * ` 2x` publicando
    * ` 2x` publicación
    * ` 1x` públicamente
    * ` 1x` publicarán
* `117x` person*:
    * `109x` personas
    * ` 7x` persona
    * ` 1x` personan
* `86x` educ*:
    * `49x` educación
    * `16x` educativo
    * `12x` educativos
    * ` 4x` educativas
    * ` 2x` educativa
    * ` 2x` educar
    * ` 1x` educadores
* `85x` desarroll*:
    * `58x` desarrollo
    * `13x` desarrollar
    * ` 7x` desarrollen
    * ` 2x` desarrollando
    * ` 2x` desarrollan
    * ` 1x` desarrollos
    * ` 1x` desarrollados
    * ` 1x` desarrolla
* `84x` social*:
    * `56x` social
    * `28x` sociales
* `78x` propon*:
    * `68x` proponemos
    * ` 9x` propone
    * ` 1x` proponer
* `72x` salud*:
    * `66x` salud
    * ` 4x` saludables
    * ` 2x` saludable
* `70x` polit*:
    * `35x` políticas
    * `26x` política
    * ` 8x` políticos
    * ` 1x` político
* `65x` protección

## Podemos

![Podemos](podemos/analisis/2019%20-%20Generales%20-%20Podemos.png)

* `142x` public*:
    * `43x` público
    * `42x` pública
    * `29x` públicas
    * `24x` públicos
    * ` 1x` publicaremos
    * ` 1x` publicar
    * ` 1x` publicado
    * ` 1x` publicación
* `124x` derech*:
    * `80x` derechos
    * `41x` derecho
    * ` 2x` derecha
    * ` 1x` derechas
* `111x` trabaj*:
    * `31x` trabajo
    * `23x` trabajadores
    * `20x` trabajadoras
    * ` 8x` trabajar
    * ` 7x` trabajan
    * ` 6x` trabajadora
    * ` 4x` trabajará
    * ` 4x` trabajador
    * ` 3x` trabajaremos
    * ` 2x` trabajos
    * ` 1x` trabajamos
    * ` 1x` trabajado
    * ` 1x` trabaja
* `107x` person*:
    * `94x` personas
    * `13x` persona
* `89x` español*:
    * `58x` españa
    * `13x` española
    * `10x` españolas
    * ` 6x` españoles
    * ` 2x` español
* `85x` servici*:
    * `65x` servicios
    * `20x` servicio
* `77x` establec*:
    * `24x` estableceremos
    * `19x` establecer
    * `10x` establecerá
    * ` 7x` establecerán
    * ` 4x` establecimientos
    * ` 4x` establecimiento
    * ` 3x` establecido
    * ` 2x` estableciendo
    * ` 2x` establecida
    * ` 2x` establece
* `76x` pais*:
    * `63x` país
    * `13x` países
* `69x` sistem*:
    * `60x` sistema
    * ` 9x` sistemas
* `67x` social*:
    * `38x` social
    * `27x` sociales
    * ` 1x` socialmente
    * ` 1x` socialista

## PP

![PP](pp/analisis/2019%20-%20Generales%20-%20PP.png)

* `156x` español*:
    * `85x` españa
    * `31x` españoles
    * `20x` española
    * `12x` español
    * ` 8x` españolas
* `150x` impuls*:
    * `95x` impulsaremos
    * `17x` impulsar
    * `17x` impulsando
    * `12x` impulso
    * ` 3x` impulsarán
    * ` 2x` impulsen
    * ` 1x` impulse
    * ` 1x` impulsará
    * ` 1x` impulsan
    * ` 1x` impulsado
* `109x` desarroll*:
    * `64x` desarrollo
    * `29x` desarrollaremos
    * ` 3x` desarrollar
    * ` 3x` desarrollando
    * ` 2x` desarrollen
    * ` 2x` desarrolladas
    * ` 1x` desarrollos
    * ` 1x` desarrolle
    * ` 1x` desarrollará
    * ` 1x` desarrollarse
    * ` 1x` desarrollan
    * ` 1x` desarrolladores
* `107x` public*:
    * `37x` públicos
    * `23x` público
    * `22x` públicas
    * `21x` pública
    * ` 1x` públicamente
    * ` 1x` publicando
    * ` 1x` publicados
    * ` 1x` publicación
* `101x` promov*:
    * `76x` promoveremos
    * `14x` promover
    * ` 6x` promoviendo
    * ` 3x` promoverán
    * ` 2x` promoverá
* `98x` plan*:
    * `60x` plan
    * `38x` planes
* `96x` nacional*:
    * `77x` nacional
    * `15x` nacionales
    * ` 2x` nacionalidad
    * ` 1x` nacionalismos
    * ` 1x` nacionalismo
* `84x` nuev*:
    * `35x` nuevas
    * `25x` nuevos
    * `13x` nueva
    * `11x` nuevo
* `80x` segur*:
    * `71x` seguridad
    * ` 3x` seguras
    * ` 2x` seguros
    * ` 2x` seguro
    * ` 2x` segura
* `79x` autonom*:
    * `36x` autónomas
    * ` 9x` autonómicos
    * ` 8x` autonómico
    * ` 7x` autónomos
    * ` 6x` autonómicas
    * ` 5x` autonomía
    * ` 3x` autónomo
    * ` 3x` autonómica
    * ` 1x` autónoma
    * ` 1x` autonomías

## PSOE

![PSOE](psoe/analisis/2019%20-%20Generales%20-%20PSOE.png)

* `408x` social*:
    * `181x` social
    * `103x` sociales
    * `72x` socialista
    * `50x` socialistas
    * ` 2x` socialmente
* `309x` español*:
    * `191x` españa
    * `42x` española
    * `32x` españoles
    * `22x` español
    * `21x` españolas
    * ` 1x` españas
* `224x` derech*:
    * `142x` derechos
    * `72x` derecho
    * ` 7x` derecha
    * ` 3x` derechas
* `219x` public*:
    * `59x` pública
    * `55x` público
    * `53x` públicos
    * `48x` públicas
    * ` 2x` publicación
    * ` 1x` públicamente
    * ` 1x` publicando
* `215x` polit*:
    * `98x` políticas
    * `95x` política
    * `12x` políticos
    * `10x` político
* `204x` impuls*:
    * `69x` impulsar
    * `54x` impulsaremos
    * `32x` impulso
    * `17x` impulsando
    * `13x` impulsado
    * ` 5x` impulse
    * ` 5x` impulsará
    * ` 4x` impulsarán
    * ` 2x` impulsadas
    * ` 1x` impulsó
    * ` 1x` impulsan
    * ` 1x` impulsa
* `199x` desarroll*:
    * `113x` desarrollo
    * `43x` desarrollar
    * `12x` desarrollando
    * `11x` desarrollaremos
    * ` 4x` desarrollen
    * ` 3x` desarrolle
    * ` 3x` desarrollan
    * ` 2x` desarrollos
    * ` 2x` desarrollada
    * ` 1x` desarrolló
    * ` 1x` desarrollaran
    * ` 1x` desarrollados
    * ` 1x` desarrollado
    * ` 1x` desarrolladas
    * ` 1x` desarrolla
* `197x` person*:
    * `185x` personas
    * `12x` persona
* `188x` gobiern*:
    * `186x` gobierno
    * ` 1x` gobierne
    * ` 1x` gobierna
* `181x` sistem*:
    * `157x` sistema
    * `22x` sistemas
    * ` 1x` sistémico
    * ` 1x` sistémicas

## Vox

![Vox](vox/analisis/2019%20-%20Generales%20-%20Vox.png)

* `42x` español*:
    * `16x` españa
    * ` 8x` españoles
    * ` 7x` española
    * ` 7x` español
    * ` 4x` españolas
* `23x` nacional*:
    * `16x` nacional
    * ` 5x` nacionalidad
    * ` 1x` nacionalidades
    * ` 1x` nacionales
* `19x` public*:
    * ` 7x` públicos
    * ` 5x` público
    * ` 4x` pública
    * ` 2x` públicas
    * ` 1x` publicación
* `15x` famili*:
    * ` 7x` familias
    * ` 4x` familiar
    * ` 4x` familia
* `12x` inmigr*:
    * ` 5x` inmigrantes
    * ` 5x` inmigración
    * ` 2x` inmigrante
* `12x` empres*:
    * ` 7x` empresa
    * ` 5x` empresas
* `11x` estado
* `10x` autonom*:
    * ` 5x` autonómicas
    * ` 1x` autónomos
    * ` 1x` autónoma
    * ` 1x` autonómico
    * ` 1x` autonómica
    * ` 1x` autonomía
* `9x` ilegal*:
    * ` 5x` ilegales
    * ` 3x` ilegal
    * ` 1x` ilegalmente
* `9x` reducción

## Conclusiones

No creo que realmente se pueda extraer conclusiones serias de estos gráficos
que no supiéramos todos ya.
