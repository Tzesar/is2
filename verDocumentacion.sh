#!/bin/bash

# Mostrar la documentacion actual
chromium docs/_build/html/index.html &
if [ $? -z ]; then
    firefox docs/_build/html/index.html &
fi
