PROJECT=paper

all:
	pdflatex $(PROJECT)
	biber $(PROJECT)
	pdflatex $(PROJECT)
	pdflatex $(PROJECT)

clean:
	rm $(PROJECT).aux
	rm $(PROJECT).bbl
	rm $(PROJECT).blg
	rm $(PROJECT).out

distclean: clean
	rm $(PROJECT).pdf
