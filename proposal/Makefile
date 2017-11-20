build:
	pdflatex -interaction=nonstopmode initial.tex
	bibtex initial
	pdflatex initial.tex
	pdflatex initial.tex

open: build
	xdg-open initial.pdf 2>/dev/null >/dev/null &

deps:
	# There might be more dependencies, but this was the one I did not have installed by default
	sudo apt install texlive-bibtex-extra

clean:
	rm *.aux *.bcf *.pdf *.log *.bbl *.blg *.out *.run.xml *.synctex.gz || :

edit:
	sensible-editor initial.tex

once:
	bibtex initial
	pdflatex -interaction=nonstopmode initial.tex

buildOnChange:
	while :; do inotifywait initial.tex; make once; done

