build:
	pdflatex -interaction=nonstopmode paper.tex
	bibtex paper
	pdflatex paper.tex
	pdflatex paper.tex

open:
	xdg-open paper.pdf 2>/dev/null >/dev/null &

deps:
	# There might be more dependencies, but these were the ones I did not have installed by default
	sudo apt install texlive-bibtex-extra
	sudo apt-get install --no-install-recommends texlive-latex-extra

clean:
	rm *.aux *.bcf *.pdf *.log *.bbl *.blg *.out *.run.xml *.synctex.gz || :

edit:
	sensible-editor paper.tex

once:
	bibtex paper
	pdflatex -interaction=nonstopmode paper.tex

buildOnChange:
	while :; do inotifywait paper.tex; make once; done

