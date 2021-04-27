/*
  SPH filter external module
 */
#include <pybind11/pybind11.h>

#include "vecrot_exmod.hpp"


PYBIND11_MODULE(filter_exmod, m)
{
    m.doc() = "SPH filter external C++ module";

    m.def("calc_curl", &calc_curl<float>, "");
    m.def("calc_curl", &calc_curl<double>, "");
}
