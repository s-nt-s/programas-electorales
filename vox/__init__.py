# -*- coding: utf-8 -*-
import re

re_punto = re.compile(r"^(\d+\.) +")

min_top = 58 - 1
max_top = 599


def convert(xml, fprint):
    for n in xml.findAll("page"):
        pag = n.attrs["number"]
        if pag < 2:
            continue
        txt = n.get_text().strip()
        if len(txt) < 100:
            continue
        childrens = [t for t in n.select(
            "> *") if "top" in t.attrs and t.attrs["top"] > min_top and t.attrs["top"] < max_top]
        childrens = sorted(childrens, key=lambda t: int(t.attrs["top"]/10))
        c1 = childrens[0]
        b1 = c1.find("b")
        if b1 and b1.get_text().strip() == c1.get_text().strip():
            fprint("\n# %s" % childrens.pop(0).get_text().capitalize())

        for i, c in enumerate(childrens):
            txt = c.decode_contents().strip()
            if re_punto.search(txt):
                txt = re_punto.sub(r"\n**\1** ", txt)
            fprint(txt)


def post_convert(file_out):
    with open(file_out, "r") as f:
        md = f.read()
    md = md.replace("anualmente.Serán", "anualmente. Serán")
    md = md.replace("penitenciarios…etcétera", "penitenciarios… etcétera")
    md = re.sub(r"  +", " ", md)
    with open(file_out, "w") as f:
        f.write(md.strip())
