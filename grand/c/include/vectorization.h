#ifndef grand_vectorization_h
#define grand_vectorization_h
#ifdef __cplusplus
extern "C" {
#endif

#include <stddef.h>


void turtle_ecef_from_geodetic_v(
    size_t n, const double * geodetic, double * ecef);

void turtle_ecef_to_geodetic_v(
    size_t n, const double * ecef, double * geodetic);


#ifdef __cplusplus
}
#endif
#endif
