buildpdf:
	pdflatex initial.tex
	bibtex initial
	pdflatex initial.tex
	pdflatex initial.tex

deps:
	# There might be more dependencies, but this was the one I did not have installed by default
	sudo apt install texlive-bibtex-extra

clean:
	rm *.aux *.bcf *.pdf *.log *.bbl *.blg *.out *.run.xml *.synctex.gz

