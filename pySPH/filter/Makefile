# Makefile for filter_exmod (SPH filter external module)
#
G=-O3
CXX=c++
CXXFLAGS=$(G) -Wall -std=c++14 -fPIC \
	`python3 -m pybind11 --includes`
LDFLAGS=-shared

ifeq ("$(shell uname)", "Darwin")
LDFLAGS+=-undefined dynamic_lookup
endif

MODULE=filter_exmod`python3-config --extension-suffix`

all: $(MODULE)

$(MODULE) : filter_exmod.o
	$(CXX) $(CXXFLAGS) $< -o $(MODULE) $(LDFLAGS)

clean:
	rm -rf *.o *.so __pycache__

filter_exmod.o : filter_exmod.cpp vecrot_exmod.hpp
