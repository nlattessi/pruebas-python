#!/bin/bash

for file in *.pdf; do pdftohtml -xml $file; done