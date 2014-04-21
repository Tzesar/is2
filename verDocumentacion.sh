#!/bin/bash

# Mostrar la documentacion actual
firefox docs/_build/html/index.html &
if [ $? -ne 0 ]; then
    firefox docs/_build/html/index.html &
fi
