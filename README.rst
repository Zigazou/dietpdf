=======
DietPDF
=======


DietPDF aims at reducing PDF file size while not degrading quality nor losing
metadata.


Description
===========

DietPDF aims at reducing PDF file size while not degrading quality.

See the tricks_ page to learn more about how this can be achieved.

It also comes with `extractpdf` which extract all the streams contained in a
PDF file.

.. _tricks: TRICKS.rst

Notes
=====

This program is not ready for production!

This project has been set up using PyScaffold 3.3.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.

Requirements
============

This is plain Python 3 using (quite) only standard libraries.

It uses the following external programs:

- `zopfli` (apt install zopfli)
- `jpegtran` (apt install libjpeg-turbo-progs)
- `jpegoptim` (apt install jpegoptim)


Installation
============

In dietpdf directory:

    pip3 install .
    
    python3 setup.py install --home=~
