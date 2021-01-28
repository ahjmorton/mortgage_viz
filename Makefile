.DEFAULT := diagram
BUILDDIR := build

diagram: builddir
	python3 mortgage_viz.py | dot -Tpng -o ${BUILDDIR}/mortgage_viz.png
        
builddir:
	mkdir -p ./${BUILDDIR}

clean:
	rm -rF ./${BUILDDIR}

watch: diagram
	fswatch -0 ./mortgage_viz.py | xargs -0 -n1 -I {} make diagram

preview: diagram
	open ${BUILDDIR}/mortgage_viz.png
