import argparse
import io
import os
import re
import sys

import bs4
import pdfkit
import yaml
from bunch import Bunch
from markdownify import markdownify
from PyPDF2 import PdfFileReader

re_sp = re.compile(r"\s+")


def get_pages(html):
    options = {
        'page-size': 'A4',
        'margin-top': '10mm',
        'margin-right': '10mm',
        'margin-bottom': '10mm',
        'margin-left': '10mm',
        'zoom': 1
    }
    if html.startswith("http"):
        pdf = pdfkit.from_url(html, False, options=options)
    else:
        pdf = pdfkit.from_file(html, False, options=options)
    with io.BytesIO(pdf) as fp:
        pdf = PdfFileReader(fp)
        return pdf.getNumPages()


class CustomDumper(yaml.Dumper):
    def represent_dict_preserve_order(self, data):
        return self.represent_dict(data.items())


CustomDumper.add_representer(dict, CustomDumper.represent_dict_preserve_order)


def get_info(yml_file="info.yml", autocomplete=False):
    with open(yml_file, 'r') as f:
        yml = Bunch(yaml.load(f))
        if autocomplete:
            if "txt_cover" not in yml:
                yml.txt_cover = "Programa %s %s %s" % (
                    yml.partido, yml.tipo, yml.year)
            if "output" not in yml:
                yml.output = "%s - %s - %s" % (yml.year, yml.tipo, yml.partido)
    return yml


def set_info(yml, yml_file="info.yml"):
    with open(yml_file, 'w') as f:
        yml = dict(yml)
        yaml.dump(dict(yml), f, default_flow_style=False,
                  Dumper=CustomDumper, allow_unicode=True)


def get_function(module, name, default=None):
    try:
        return getattr(module, name)
    except:
        if default is not None:
            return default
        return lambda *args, **kargs: None


def clean_tags(txt, extra=False):
    for tag in ("em", "strong", "b", "i"):
        txt = re.sub(r"</"+tag+r">(\s*)<"+tag+r">", r"\1", txt)
        txt = re.sub(r"<"+tag+r">(\s*)</"+tag+r">", r"\1", txt)
        txt = re.sub("<"+tag+r">(\s+)", r"\1<"+tag+">", txt)
        txt = re.sub(r"(\s+)</"+tag+">", "</"+tag+r">\1", txt)
        if extra:
            txt = re.sub(r"(,)</"+tag+">", "</"+tag+r">\1", txt)
    return txt


def get_soup(source, tp="lxml", save=None):
    if not os.path.isfile(source):
        return None
    with open(source, "r") as f:
        txt = f.read()
        txt = clean_tags(txt)
        soup = bs4.BeautifulSoup(txt, tp)
    if tp == "xml":
        for n in soup.select("*"):
            if n.name == "text" and len(n.select("*")) == 0 and len(n.get_text().strip()) == 0:
                n.extract()
                continue
            for a in ("top", "left", "right", "number", "font", "height"):
                if a in n.attrs:
                    n.attrs[a] = int(n.attrs[a])
    for n in soup.findAll(["text", "div", "p", "h1", "h2", "h3", "h4", "h5", "h6"]):
        if len(n.select("> *")) == 0 and len(n.get_text().strip()) == 0:
            n.extract()
    for n in soup.findAll(["i", "em", "b", "strong", "span"]):
        if len(n.select("> *")) == 0 and len(n.get_text().strip()) == 0:
            n.unwrap()
    if save is not None:
        with open(save, "w") as f:
            f.write(str(soup))
    return soup


def to_md(n):
    txt = n.decode_contents()
    txt = re_sp.sub(" ", txt).strip()
    txt = markdownify(txt)
    return txt


def get_arg(description):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("target", help="Carpeta de trabajo")
    arg = parser.parse_args()

    yml_file = "info.yml"
    mpy = "__init__.py"
    if arg.target.endswith("/"+yml_file) or arg.target.endswith("/"+mpy):
        arg.target = os.path.dirname(arg.target)

    if not os.path.isdir(arg.target):
        sys.exit("%s no es un directorio" % arg.target)

    os.chdir(arg.target)
    if arg.target.endswith("/"):
        arg.target = arg.target[:-1]
    if arg.target.startswith("./"):
        arg.target = arg.target[2:]

    if not os.path.isfile(yml_file):
        sys.exit("no existe el fichero %s" % yml_file)
    if not os.path.isfile(mpy):
        sys.exit("no existe el fichero %s" % mpy)

    return arg
