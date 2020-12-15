#
# Makefile
# dlilien, 2020-12-15 18:00
#

all: input_data.so vx.txt

clean:
	rm -f *.so vx.txt true_beta.txt *.png

%.so: %.f90
		elmerf90 -o $@ $<

vx.txt: extract_vx.py rectangle/inversion_input_t0001.vtu
	python extract_vx.py

rectangle/inversion_input_t0001.vtu: true_input.sif rectangle/mesh.nodes
	ElmerSolver true_input.sif

rectangle/mesh.nodes: rectangle.grd
	ElmerGrid 1 2 rectangle.grd
