=======
dietpdf
=======


DietPDF aims at reducing PDF file size while not degrading quality nor losing
metadata.


Description
===========

DietPDF aims at reducing PDF file size while not degrading quality.

Here are some tricks used to achieve this goal:

- Use Zopfli instead of Zlib to get better compression ratio while being
  compatible with Zlib.
- Use JpegTran to optimize and remove unnecessary data from embedded JPEGs.
- Use of Run-Length Encoding to help Zopfli achieve better compression.
- Use Zopfli on embedded JPEGs, it helps sometimes
- Remove unnecessary spaces in the PDF
- Converts end of lines to spaces in Form Objects or Contents (this helps
  compression)

It also comes with `extractpdf` which extract all the streams contained in a
PDF file.

Notes
=====

This program is not ready for production!

It does not support cross-reference objects for the moment.

This project has been set up using PyScaffold 3.3.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.

Requirements
============

This is plain Python 3 using (quite) only standard libraries.

It uses the following external programs:

- `zopfli` (apt install zopfli)
- `jpegtran` (apt install libjpeg-turbo-progs)


Installation
============

In dietpdf directory:

    pip3 install .
    python3 setup.py install --home=~
