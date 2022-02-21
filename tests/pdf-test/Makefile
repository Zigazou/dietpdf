ALL: guide-auto-test.opt.pdf guide-auto-test.opt.pdf.qpdf-check guide-auto-test.opt.pdf.gs-check guide-auto-test.pdf.compare-gs guide-auto-test.pdf.compare-cairo test-de-horn.opt.pdf test-de-horn.opt.pdf.qpdf-check test-de-horn.opt.pdf.gs-check test-de-horn.pdf.compare-gs test-de-horn.pdf.compare-cairo je-fais-le-test.opt.pdf je-fais-le-test.opt.pdf.qpdf-check je-fais-le-test.opt.pdf.gs-check je-fais-le-test.pdf.compare-gs je-fais-le-test.pdf.compare-cairo xerox-versalink.opt.pdf xerox-versalink.opt.pdf.qpdf-check xerox-versalink.opt.pdf.gs-check xerox-versalink.pdf.compare-gs xerox-versalink.pdf.compare-cairo renault-arkana.opt.pdf renault-arkana.opt.pdf.qpdf-check renault-arkana.opt.pdf.gs-check renault-arkana.pdf.compare-gs renault-arkana.pdf.compare-cairo suzuki-swace.opt.pdf suzuki-swace.opt.pdf.qpdf-check suzuki-swace.opt.pdf.gs-check suzuki-swace.pdf.compare-gs suzuki-swace.pdf.compare-cairo boursorama-tarif.opt.pdf boursorama-tarif.opt.pdf.qpdf-check boursorama-tarif.opt.pdf.gs-check boursorama-tarif.pdf.compare-gs boursorama-tarif.pdf.compare-cairo ricoh-ucs.opt.pdf ricoh-ucs.opt.pdf.qpdf-check ricoh-ucs.opt.pdf.gs-check ricoh-ucs.pdf.compare-gs ricoh-ucs.pdf.compare-cairo royal-ours-blanc.opt.pdf royal-ours-blanc.opt.pdf.qpdf-check royal-ours-blanc.opt.pdf.gs-check royal-ours-blanc.pdf.compare-gs royal-ours-blanc.pdf.compare-cairo free-mobile-tarifs.opt.pdf free-mobile-tarifs.opt.pdf.qpdf-check free-mobile-tarifs.opt.pdf.gs-check free-mobile-tarifs.pdf.compare-gs free-mobile-tarifs.pdf.compare-cairo chirurgie-obesite.opt.pdf chirurgie-obesite.opt.pdf.qpdf-check chirurgie-obesite.opt.pdf.gs-check chirurgie-obesite.pdf.compare-gs chirurgie-obesite.pdf.compare-cairo initiation-latex.opt.pdf initiation-latex.opt.pdf.qpdf-check initiation-latex.opt.pdf.gs-check initiation-latex.pdf.compare-gs initiation-latex.pdf.compare-cairo math-into-latex.opt.pdf math-into-latex.opt.pdf.qpdf-check math-into-latex.opt.pdf.gs-check math-into-latex.pdf.compare-gs math-into-latex.pdf.compare-cairo

guide-auto-test.pdf:
	curl --silent "https://solidarites-sante.gouv.fr/IMG/pdf/guide_auto-test.pdf" -o "guide-auto-test.pdf"

guide-auto-test.opt.pdf: guide-auto-test.pdf
	dietpdf "guide-auto-test.pdf"

guide-auto-test.opt.pdf.qpdf-check: guide-auto-test.opt.pdf
	qpdf --suppress-recovery -check "guide-auto-test.opt.pdf" > "guide-auto-test.opt.pdf.qpdf-check"

guide-auto-test.opt.pdf.gs-check: guide-auto-test.opt.pdf
	gs -dNOPAUSE -dBATCH -sDEVICE=nullpage guide-auto-test.opt.pdf > guide-auto-test.opt.pdf.gs-check

guide-auto-test.pdf.compare-gs: guide-auto-test.pdf guide-auto-test.opt.pdf
	python3 generate-comparison-gs.py guide-auto-test.pdf guide-auto-test.opt.pdf > guide-auto-test.pdf.compare-gs

guide-auto-test.pdf.compare-cairo: guide-auto-test.pdf guide-auto-test.opt.pdf
	python3 generate-comparison-cairo.py guide-auto-test.pdf guide-auto-test.opt.pdf > guide-auto-test.pdf.compare-cairo

test-de-horn.pdf:
	curl --silent "https://www.has-sante.fr/upload/docs/application/pdf/2014-01/annexe_test_de_horn.pdf" -o "test-de-horn.pdf"

test-de-horn.opt.pdf: test-de-horn.pdf
	dietpdf "test-de-horn.pdf"

test-de-horn.opt.pdf.qpdf-check: test-de-horn.opt.pdf
	qpdf --suppress-recovery -check "test-de-horn.opt.pdf" > "test-de-horn.opt.pdf.qpdf-check"

test-de-horn.opt.pdf.gs-check: test-de-horn.opt.pdf
	gs -dNOPAUSE -dBATCH -sDEVICE=nullpage test-de-horn.opt.pdf > test-de-horn.opt.pdf.gs-check

test-de-horn.pdf.compare-gs: test-de-horn.pdf test-de-horn.opt.pdf
	python3 generate-comparison-gs.py test-de-horn.pdf test-de-horn.opt.pdf > test-de-horn.pdf.compare-gs

test-de-horn.pdf.compare-cairo: test-de-horn.pdf test-de-horn.opt.pdf
	python3 generate-comparison-cairo.py test-de-horn.pdf test-de-horn.opt.pdf > test-de-horn.pdf.compare-cairo

je-fais-le-test.pdf:
	curl --silent "https://handicap.gouv.fr/IMG/pdf/je_fais_le_test_pour_savoir_si_j_ai_la_covid-19.pdf" -o "je-fais-le-test.pdf"

je-fais-le-test.opt.pdf: je-fais-le-test.pdf
	dietpdf "je-fais-le-test.pdf"

je-fais-le-test.opt.pdf.qpdf-check: je-fais-le-test.opt.pdf
	qpdf --suppress-recovery -check "je-fais-le-test.opt.pdf" > "je-fais-le-test.opt.pdf.qpdf-check"

je-fais-le-test.opt.pdf.gs-check: je-fais-le-test.opt.pdf
	gs -dNOPAUSE -dBATCH -sDEVICE=nullpage je-fais-le-test.opt.pdf > je-fais-le-test.opt.pdf.gs-check

je-fais-le-test.pdf.compare-gs: je-fais-le-test.pdf je-fais-le-test.opt.pdf
	python3 generate-comparison-gs.py je-fais-le-test.pdf je-fais-le-test.opt.pdf > je-fais-le-test.pdf.compare-gs

je-fais-le-test.pdf.compare-cairo: je-fais-le-test.pdf je-fais-le-test.opt.pdf
	python3 generate-comparison-cairo.py je-fais-le-test.pdf je-fais-le-test.opt.pdf > je-fais-le-test.pdf.compare-cairo

xerox-versalink.pdf:
	curl --silent "https://www.xerox.fr/bureau/latest/VC6BR-01F.pdf" -o "xerox-versalink.pdf"

xerox-versalink.opt.pdf: xerox-versalink.pdf
	dietpdf "xerox-versalink.pdf"

xerox-versalink.opt.pdf.qpdf-check: xerox-versalink.opt.pdf
	qpdf --suppress-recovery -check "xerox-versalink.opt.pdf" > "xerox-versalink.opt.pdf.qpdf-check"

xerox-versalink.opt.pdf.gs-check: xerox-versalink.opt.pdf
	gs -dNOPAUSE -dBATCH -sDEVICE=nullpage xerox-versalink.opt.pdf > xerox-versalink.opt.pdf.gs-check

xerox-versalink.pdf.compare-gs: xerox-versalink.pdf xerox-versalink.opt.pdf
	python3 generate-comparison-gs.py xerox-versalink.pdf xerox-versalink.opt.pdf > xerox-versalink.pdf.compare-gs

xerox-versalink.pdf.compare-cairo: xerox-versalink.pdf xerox-versalink.opt.pdf
	python3 generate-comparison-cairo.py xerox-versalink.pdf xerox-versalink.opt.pdf > xerox-versalink.pdf.compare-cairo

renault-arkana.pdf:
	curl --silent "https://cdn.group.renault.com/ren/fr/product-plans/arkana/brochure/Brochure_Arkana.pdf.asset.pdf/4f5f9fafe1.pdf" -o "renault-arkana.pdf"

renault-arkana.opt.pdf: renault-arkana.pdf
	dietpdf "renault-arkana.pdf"

renault-arkana.opt.pdf.qpdf-check: renault-arkana.opt.pdf
	qpdf --suppress-recovery -check "renault-arkana.opt.pdf" > "renault-arkana.opt.pdf.qpdf-check"

renault-arkana.opt.pdf.gs-check: renault-arkana.opt.pdf
	gs -dNOPAUSE -dBATCH -sDEVICE=nullpage renault-arkana.opt.pdf > renault-arkana.opt.pdf.gs-check

renault-arkana.pdf.compare-gs: renault-arkana.pdf renault-arkana.opt.pdf
	python3 generate-comparison-gs.py renault-arkana.pdf renault-arkana.opt.pdf > renault-arkana.pdf.compare-gs

renault-arkana.pdf.compare-cairo: renault-arkana.pdf renault-arkana.opt.pdf
	python3 generate-comparison-cairo.py renault-arkana.pdf renault-arkana.opt.pdf > renault-arkana.pdf.compare-cairo

suzuki-swace.pdf:
	curl --silent "https://www.suzuki.fr/uploads/brochures/modele/brochure-swace-hybride.pdf" -o "suzuki-swace.pdf"

suzuki-swace.opt.pdf: suzuki-swace.pdf
	dietpdf "suzuki-swace.pdf"

suzuki-swace.opt.pdf.qpdf-check: suzuki-swace.opt.pdf
	qpdf --suppress-recovery -check "suzuki-swace.opt.pdf" > "suzuki-swace.opt.pdf.qpdf-check"

suzuki-swace.opt.pdf.gs-check: suzuki-swace.opt.pdf
	gs -dNOPAUSE -dBATCH -sDEVICE=nullpage suzuki-swace.opt.pdf > suzuki-swace.opt.pdf.gs-check

suzuki-swace.pdf.compare-gs: suzuki-swace.pdf suzuki-swace.opt.pdf
	python3 generate-comparison-gs.py suzuki-swace.pdf suzuki-swace.opt.pdf > suzuki-swace.pdf.compare-gs

suzuki-swace.pdf.compare-cairo: suzuki-swace.pdf suzuki-swace.opt.pdf
	python3 generate-comparison-cairo.py suzuki-swace.pdf suzuki-swace.opt.pdf > suzuki-swace.pdf.compare-cairo

boursorama-tarif.pdf:
	curl --silent "https://www.boursorama.com/pub/brochure_tarifaire/boursorama_bt.pdf" -o "boursorama-tarif.pdf"

boursorama-tarif.opt.pdf: boursorama-tarif.pdf
	dietpdf "boursorama-tarif.pdf"

boursorama-tarif.opt.pdf.qpdf-check: boursorama-tarif.opt.pdf
	qpdf --suppress-recovery -check "boursorama-tarif.opt.pdf" > "boursorama-tarif.opt.pdf.qpdf-check"

boursorama-tarif.opt.pdf.gs-check: boursorama-tarif.opt.pdf
	gs -dNOPAUSE -dBATCH -sDEVICE=nullpage boursorama-tarif.opt.pdf > boursorama-tarif.opt.pdf.gs-check

boursorama-tarif.pdf.compare-gs: boursorama-tarif.pdf boursorama-tarif.opt.pdf
	python3 generate-comparison-gs.py boursorama-tarif.pdf boursorama-tarif.opt.pdf > boursorama-tarif.pdf.compare-gs

boursorama-tarif.pdf.compare-cairo: boursorama-tarif.pdf boursorama-tarif.opt.pdf
	python3 generate-comparison-cairo.py boursorama-tarif.pdf boursorama-tarif.opt.pdf > boursorama-tarif.pdf.compare-cairo

ricoh-ucs.pdf:
	curl --silent "https://www.amparis.fr/files/2018-03/20171220-044259-ricoh-ucs-advanced-brochure-final-french-nov-17-hr.pdf" -o "ricoh-ucs.pdf"

ricoh-ucs.opt.pdf: ricoh-ucs.pdf
	dietpdf "ricoh-ucs.pdf"

ricoh-ucs.opt.pdf.qpdf-check: ricoh-ucs.opt.pdf
	qpdf --suppress-recovery -check "ricoh-ucs.opt.pdf" > "ricoh-ucs.opt.pdf.qpdf-check"

ricoh-ucs.opt.pdf.gs-check: ricoh-ucs.opt.pdf
	gs -dNOPAUSE -dBATCH -sDEVICE=nullpage ricoh-ucs.opt.pdf > ricoh-ucs.opt.pdf.gs-check

ricoh-ucs.pdf.compare-gs: ricoh-ucs.pdf ricoh-ucs.opt.pdf
	python3 generate-comparison-gs.py ricoh-ucs.pdf ricoh-ucs.opt.pdf > ricoh-ucs.pdf.compare-gs

ricoh-ucs.pdf.compare-cairo: ricoh-ucs.pdf ricoh-ucs.opt.pdf
	python3 generate-comparison-cairo.py ricoh-ucs.pdf ricoh-ucs.opt.pdf > ricoh-ucs.pdf.compare-cairo

royal-ours-blanc.pdf:
	curl --silent "https://www.hotelroyaloursblanc.com/_files/_media/1/Photos/Seminaires/Brochure%20Groupes%20%20Sminaires%20-%20%20Royal%20Ours%20Blanc%20.pdf" -o "royal-ours-blanc.pdf"

royal-ours-blanc.opt.pdf: royal-ours-blanc.pdf
	dietpdf "royal-ours-blanc.pdf"

royal-ours-blanc.opt.pdf.qpdf-check: royal-ours-blanc.opt.pdf
	qpdf --suppress-recovery -check "royal-ours-blanc.opt.pdf" > "royal-ours-blanc.opt.pdf.qpdf-check"

royal-ours-blanc.opt.pdf.gs-check: royal-ours-blanc.opt.pdf
	gs -dNOPAUSE -dBATCH -sDEVICE=nullpage royal-ours-blanc.opt.pdf > royal-ours-blanc.opt.pdf.gs-check

royal-ours-blanc.pdf.compare-gs: royal-ours-blanc.pdf royal-ours-blanc.opt.pdf
	python3 generate-comparison-gs.py royal-ours-blanc.pdf royal-ours-blanc.opt.pdf > royal-ours-blanc.pdf.compare-gs

royal-ours-blanc.pdf.compare-cairo: royal-ours-blanc.pdf royal-ours-blanc.opt.pdf
	python3 generate-comparison-cairo.py royal-ours-blanc.pdf royal-ours-blanc.opt.pdf > royal-ours-blanc.pdf.compare-cairo

free-mobile-tarifs.pdf:
	curl --silent "https://mobile.free.fr/docs/bt/tarifs.pdf" -o "free-mobile-tarifs.pdf"

free-mobile-tarifs.opt.pdf: free-mobile-tarifs.pdf
	dietpdf "free-mobile-tarifs.pdf"

free-mobile-tarifs.opt.pdf.qpdf-check: free-mobile-tarifs.opt.pdf
	qpdf --suppress-recovery -check "free-mobile-tarifs.opt.pdf" > "free-mobile-tarifs.opt.pdf.qpdf-check"

free-mobile-tarifs.opt.pdf.gs-check: free-mobile-tarifs.opt.pdf
	gs -dNOPAUSE -dBATCH -sDEVICE=nullpage free-mobile-tarifs.opt.pdf > free-mobile-tarifs.opt.pdf.gs-check

free-mobile-tarifs.pdf.compare-gs: free-mobile-tarifs.pdf free-mobile-tarifs.opt.pdf
	python3 generate-comparison-gs.py free-mobile-tarifs.pdf free-mobile-tarifs.opt.pdf > free-mobile-tarifs.pdf.compare-gs

free-mobile-tarifs.pdf.compare-cairo: free-mobile-tarifs.pdf free-mobile-tarifs.opt.pdf
	python3 generate-comparison-cairo.py free-mobile-tarifs.pdf free-mobile-tarifs.opt.pdf > free-mobile-tarifs.pdf.compare-cairo

chirurgie-obesite.pdf:
	curl --silent "https://www.has-sante.fr/upload/docs/application/pdf/2009-09/brochure_obesite_patient_220909.pdf" -o "chirurgie-obesite.pdf"

chirurgie-obesite.opt.pdf: chirurgie-obesite.pdf
	dietpdf "chirurgie-obesite.pdf"

chirurgie-obesite.opt.pdf.qpdf-check: chirurgie-obesite.opt.pdf
	qpdf --suppress-recovery -check "chirurgie-obesite.opt.pdf" > "chirurgie-obesite.opt.pdf.qpdf-check"

chirurgie-obesite.opt.pdf.gs-check: chirurgie-obesite.opt.pdf
	gs -dNOPAUSE -dBATCH -sDEVICE=nullpage chirurgie-obesite.opt.pdf > chirurgie-obesite.opt.pdf.gs-check

chirurgie-obesite.pdf.compare-gs: chirurgie-obesite.pdf chirurgie-obesite.opt.pdf
	python3 generate-comparison-gs.py chirurgie-obesite.pdf chirurgie-obesite.opt.pdf > chirurgie-obesite.pdf.compare-gs

chirurgie-obesite.pdf.compare-cairo: chirurgie-obesite.pdf chirurgie-obesite.opt.pdf
	python3 generate-comparison-cairo.py chirurgie-obesite.pdf chirurgie-obesite.opt.pdf > chirurgie-obesite.pdf.compare-cairo

initiation-latex.pdf:
	curl --silent "https://mirrors.ibiblio.org/CTAN/info/guide-latex-fr/guide-latex-fr.pdf" -o "initiation-latex.pdf"

initiation-latex.opt.pdf: initiation-latex.pdf
	dietpdf "initiation-latex.pdf"

initiation-latex.opt.pdf.qpdf-check: initiation-latex.opt.pdf
	qpdf --suppress-recovery -check "initiation-latex.opt.pdf" > "initiation-latex.opt.pdf.qpdf-check"

initiation-latex.opt.pdf.gs-check: initiation-latex.opt.pdf
	gs -dNOPAUSE -dBATCH -sDEVICE=nullpage initiation-latex.opt.pdf > initiation-latex.opt.pdf.gs-check

initiation-latex.pdf.compare-gs: initiation-latex.pdf initiation-latex.opt.pdf
	python3 generate-comparison-gs.py initiation-latex.pdf initiation-latex.opt.pdf > initiation-latex.pdf.compare-gs

initiation-latex.pdf.compare-cairo: initiation-latex.pdf initiation-latex.opt.pdf
	python3 generate-comparison-cairo.py initiation-latex.pdf initiation-latex.opt.pdf > initiation-latex.pdf.compare-cairo

math-into-latex.pdf:
	curl --silent "https://tex.loria.fr/general/mil.pdf" -o "math-into-latex.pdf"

math-into-latex.opt.pdf: math-into-latex.pdf
	dietpdf "math-into-latex.pdf"

math-into-latex.opt.pdf.qpdf-check: math-into-latex.opt.pdf
	qpdf --suppress-recovery -check "math-into-latex.opt.pdf" > "math-into-latex.opt.pdf.qpdf-check"

math-into-latex.opt.pdf.gs-check: math-into-latex.opt.pdf
	gs -dNOPAUSE -dBATCH -sDEVICE=nullpage math-into-latex.opt.pdf > math-into-latex.opt.pdf.gs-check

math-into-latex.pdf.compare-gs: math-into-latex.pdf math-into-latex.opt.pdf
	python3 generate-comparison-gs.py math-into-latex.pdf math-into-latex.opt.pdf > math-into-latex.pdf.compare-gs

math-into-latex.pdf.compare-cairo: math-into-latex.pdf math-into-latex.opt.pdf
	python3 generate-comparison-cairo.py math-into-latex.pdf math-into-latex.opt.pdf > math-into-latex.pdf.compare-cairo

clean:
	rm -f -- guide-auto-test.opt.pdf guide-auto-test.opt.pdf.qpdf-check guide-auto-test.opt.pdf.gs-check guide-auto-test.pdf.compare-gs guide-auto-test.pdf.compare-cairo
	rm -f -- test-de-horn.opt.pdf test-de-horn.opt.pdf.qpdf-check test-de-horn.opt.pdf.gs-check test-de-horn.pdf.compare-gs test-de-horn.pdf.compare-cairo
	rm -f -- je-fais-le-test.opt.pdf je-fais-le-test.opt.pdf.qpdf-check je-fais-le-test.opt.pdf.gs-check je-fais-le-test.pdf.compare-gs je-fais-le-test.pdf.compare-cairo
	rm -f -- xerox-versalink.opt.pdf xerox-versalink.opt.pdf.qpdf-check xerox-versalink.opt.pdf.gs-check xerox-versalink.pdf.compare-gs xerox-versalink.pdf.compare-cairo
	rm -f -- renault-arkana.opt.pdf renault-arkana.opt.pdf.qpdf-check renault-arkana.opt.pdf.gs-check renault-arkana.pdf.compare-gs renault-arkana.pdf.compare-cairo
	rm -f -- suzuki-swace.opt.pdf suzuki-swace.opt.pdf.qpdf-check suzuki-swace.opt.pdf.gs-check suzuki-swace.pdf.compare-gs suzuki-swace.pdf.compare-cairo
	rm -f -- boursorama-tarif.opt.pdf boursorama-tarif.opt.pdf.qpdf-check boursorama-tarif.opt.pdf.gs-check boursorama-tarif.pdf.compare-gs boursorama-tarif.pdf.compare-cairo
	rm -f -- ricoh-ucs.opt.pdf ricoh-ucs.opt.pdf.qpdf-check ricoh-ucs.opt.pdf.gs-check ricoh-ucs.pdf.compare-gs ricoh-ucs.pdf.compare-cairo
	rm -f -- royal-ours-blanc.opt.pdf royal-ours-blanc.opt.pdf.qpdf-check royal-ours-blanc.opt.pdf.gs-check royal-ours-blanc.pdf.compare-gs royal-ours-blanc.pdf.compare-cairo
	rm -f -- free-mobile-tarifs.opt.pdf free-mobile-tarifs.opt.pdf.qpdf-check free-mobile-tarifs.opt.pdf.gs-check free-mobile-tarifs.pdf.compare-gs free-mobile-tarifs.pdf.compare-cairo
	rm -f -- chirurgie-obesite.opt.pdf chirurgie-obesite.opt.pdf.qpdf-check chirurgie-obesite.opt.pdf.gs-check chirurgie-obesite.pdf.compare-gs chirurgie-obesite.pdf.compare-cairo
	rm -f -- initiation-latex.opt.pdf initiation-latex.opt.pdf.qpdf-check initiation-latex.opt.pdf.gs-check initiation-latex.pdf.compare-gs initiation-latex.pdf.compare-cairo
	rm -f -- math-into-latex.opt.pdf math-into-latex.opt.pdf.qpdf-check math-into-latex.opt.pdf.gs-check math-into-latex.pdf.compare-gs math-into-latex.pdf.compare-cairo

clean-all:
	rm -f -- guide-auto-test.pdf guide-auto-test.opt.pdf guide-auto-test.opt.pdf.qpdf-check guide-auto-test.opt.pdf.gs-check guide-auto-test.pdf.compare-gs
	rm -f -- test-de-horn.pdf test-de-horn.opt.pdf test-de-horn.opt.pdf.qpdf-check test-de-horn.opt.pdf.gs-check test-de-horn.pdf.compare-gs
	rm -f -- je-fais-le-test.pdf je-fais-le-test.opt.pdf je-fais-le-test.opt.pdf.qpdf-check je-fais-le-test.opt.pdf.gs-check je-fais-le-test.pdf.compare-gs
	rm -f -- xerox-versalink.pdf xerox-versalink.opt.pdf xerox-versalink.opt.pdf.qpdf-check xerox-versalink.opt.pdf.gs-check xerox-versalink.pdf.compare-gs
	rm -f -- renault-arkana.pdf renault-arkana.opt.pdf renault-arkana.opt.pdf.qpdf-check renault-arkana.opt.pdf.gs-check renault-arkana.pdf.compare-gs
	rm -f -- suzuki-swace.pdf suzuki-swace.opt.pdf suzuki-swace.opt.pdf.qpdf-check suzuki-swace.opt.pdf.gs-check suzuki-swace.pdf.compare-gs
	rm -f -- boursorama-tarif.pdf boursorama-tarif.opt.pdf boursorama-tarif.opt.pdf.qpdf-check boursorama-tarif.opt.pdf.gs-check boursorama-tarif.pdf.compare-gs
	rm -f -- ricoh-ucs.pdf ricoh-ucs.opt.pdf ricoh-ucs.opt.pdf.qpdf-check ricoh-ucs.opt.pdf.gs-check ricoh-ucs.pdf.compare-gs
	rm -f -- royal-ours-blanc.pdf royal-ours-blanc.opt.pdf royal-ours-blanc.opt.pdf.qpdf-check royal-ours-blanc.opt.pdf.gs-check royal-ours-blanc.pdf.compare-gs
	rm -f -- free-mobile-tarifs.pdf free-mobile-tarifs.opt.pdf free-mobile-tarifs.opt.pdf.qpdf-check free-mobile-tarifs.opt.pdf.gs-check free-mobile-tarifs.pdf.compare-gs
	rm -f -- chirurgie-obesite.pdf chirurgie-obesite.opt.pdf chirurgie-obesite.opt.pdf.qpdf-check chirurgie-obesite.opt.pdf.gs-check chirurgie-obesite.pdf.compare-gs
	rm -f -- initiation-latex.pdf initiation-latex.opt.pdf initiation-latex.opt.pdf.qpdf-check initiation-latex.opt.pdf.gs-check initiation-latex.pdf.compare-gs
	rm -f -- math-into-latex.pdf math-into-latex.opt.pdf math-into-latex.opt.pdf.qpdf-check math-into-latex.opt.pdf.gs-check math-into-latex.pdf.compare-gs

