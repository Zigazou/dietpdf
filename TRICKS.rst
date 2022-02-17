==============================================
Tricks used by DietPDF to reduce PDF file size
==============================================


As PDF hax a complex format, it requires many tricks to reduce sizes.

DietPDF works at a very low-level.

Optimization of compression
===========================

DietPDF will:

* use Zopfli to achieve better compression than with Zlib

* try to use RLE before Zopfli to see if it helps compression

* try to use PNG predictors whenever appropriate to help compression

* keep original version of the stream if it cannot give better results

* remove ASCII85Decode encoding scheme.

Optimization of content streams
===============================

PDF content streams are source codes generally written in a human readable way.

DietPDF will:

* remove unnecessary spaces (for example before or after delimiters)

* rewrite float numbers:

  * reduce precision (rounded by 2) but ensure to never give 0 while the
    original number is not zero

  * converts `digits.0` to `digits`

  * converts `0.digits` to `.digits`

* replace line returns with space (this helps compression)

* remove comments

* replace hexadecimal strings with standard strings

* replace escaped parts in standard strings

Optimization of objects
=======================

DietPDF will:

* remove unnecessary spaces (for example befoire or after delimiters)
  
* group together contents objects of the same page (this helps compression)

Optimization of JPEG images
===========================

DietPDF will:

* use `jpegtran` and `jpegoptim` to optimize JPEG embedded in PDFs

* strip any unnecessary information contained in JPEG files
  
* try to use RLE and Zopfli compression on JPEG, it sometimes helps

Optimization of objects without stream
======================================

Since PDF 1.5, objects without stream may be placed in an object stream. This
allows compression to be applied to data which are not allowed to be compressed.

DietPDF will:

* put every object without stream inside a unique object stream compressed by
  Zopfli.

Optimization of cross-reference table
=====================================

Since PDF 1.5, cross-reference tables may be placed in cross-reference streams.
This allows to compress the cross-reference table.

DietPDF will:

* put all references in a unique cross-reference stream.

Optimization of PDF file structure
==================================

PDF file format natively supports updates.

DietPDF will:

* keep only the latest version of any object in the optimized file

* delinearize PDF
