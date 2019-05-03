#!/bin/bash
#find . -name "__init__.py" -exec ./genera.py {}  \;
for i in $(find . -name "__init__.py"); do
  p=$(dirname $i)
  list=($p/*.md)
  if [ ! -f "$p/_.md" ]; then
    cp "$list" "$p/_.md"
  fi
  ./genera.py "$p"
  cmp --silent "$p/_.md" "$list" || meld "$p/_.md" "$list"
done
