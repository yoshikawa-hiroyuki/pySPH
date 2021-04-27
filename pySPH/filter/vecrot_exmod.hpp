/*
  SPH filter external module
 */
#ifndef _VECROT_EXMOD_HPP_
#define _VECROT_EXMOD_HPP_

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

namespace py = pybind11;


// calc_curl
//  calculate curl(rot) of vector sph data
//  @param x: vector sph
//  @param px, py, pz: pitch of grid
//  @return: curl vector of sph

template <typename T>
py::array_t<T> calc_curl(py::array_t<T> x, T px, T py, T pz) {
  const auto &info = x.request(); // struct{}
  const auto &shape = info.shape; // std::vector<ssize_t>
  py::array_t<T> y{shape};

  if ( shape.size() < 4 ||
       shape[0] < 2 || shape[1] < 2 || shape[2] < 2 || shape[3] < 3 )
    return y;

  T dvdx, dwdx, dudy, dwdy, dudz, dvdz;
  int i, j, k;
  for ( k = 0; k < shape[0]; k++ )
    for ( j = 0; j < shape[1]; j++ )
      for ( i = 0; i < shape[2]; i++ ) {
	if ( i == 0 ) {
	  dvdx = (*x.data(k, j, i+1, 1) - *x.data(k, j, i, 1)) / px;
	  dwdx = (*x.data(k, j, i+1, 2) - *x.data(k, j, i, 2)) / px;
	} else if ( i == shape[2] - 1 ) {
	  dvdx = (*x.data(k, j, i, 1) - *x.data(k, j, i-1, 1)) / px;
	  dwdx = (*x.data(k, j, i, 2) - *x.data(k, j, i-1, 2)) / px;
	} else {
	  dvdx = (*x.data(k, j, i+1, 1) - *x.data(k, j, i-1, 1)) / (px*2);
	  dwdx = (*x.data(k, j, i+1, 2) - *x.data(k, j, i-1, 2)) / (px*2);
	}
	if ( j == 0 ) {
	  dudy = (*x.data(k, j+1, i, 0) - *x.data(k, j, i, 0)) / py;
	  dwdy = (*x.data(k, j+1, i, 2) - *x.data(k, j, i, 2)) / py;
	} else if ( j == shape[1] - 1 ) {
	  dudy = (*x.data(k, j, i, 0) - *x.data(k, j-1, i, 0)) / py;
	  dwdy = (*x.data(k, j, i, 2) - *x.data(k, j-1, i, 2)) / py;
	} else {
	  dudy = (*x.data(k, j+1, i, 0) - *x.data(k, j-1, i, 0)) / (py*2);
	  dwdy = (*x.data(k, j+1, i, 2) - *x.data(k, j-1, i, 2)) / (py*2);
	}
	if ( k == 0 ) {
	  dudz = (*x.data(k+1, j, i, 0) - *x.data(k, j, i, 0)) / pz;
	  dvdz = (*x.data(k+1, j, i, 1) - *x.data(k, j, i, 1)) / pz;
	} else if ( k == shape[0] - 1 ) {
	  dudz = (*x.data(k, j, i, 0) - *x.data(k-1, j, i, 0)) / pz;
	  dvdz = (*x.data(k, j, i, 1) - *x.data(k-1, j, i, 1)) / pz;
	} else {
	  dudz = (*x.data(k+1, j, i, 0) - *x.data(k-1, j, i, 0)) / (pz*2);
	  dvdz = (*x.data(k+1, j, i, 1) - *x.data(k-1, j, i, 1)) / (pz*2);
	}

	*y.mutable_data(k, j, i, 0) = dwdy - dvdz;
	*y.mutable_data(k, j, i, 1) = dudz - dwdx;
	*y.mutable_data(k, j, i, 2) = dvdx - dudy;
      } // end of for(i)

  return y;
}

#endif //  _VECROT_EXMOD_HPP_
