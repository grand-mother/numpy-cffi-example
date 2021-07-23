#include "turtle.h"
#include "vectorization.h"


/* Vectorization of the geodetic to ECEF conversion */
void turtle_ecef_from_geodetic_v(
    size_t n, const double * geodetic, double * ecef)
{
        const double * g = geodetic;
        double * c = ecef;
        size_t i;
        for (i = 0; i < n; i++, c+=3, g+=3) {
                turtle_ecef_from_geodetic(g[0], g[1], g[2], c);
        }
}


/* Vectorization of the ECEF to geodetic conversion */
void turtle_ecef_to_geodetic_v(
    size_t n, const double * ecef, double * geodetic)
{
        double * g = geodetic;
        const double * c = ecef;
        size_t i;
        for (i = 0; i < n; i++, c+=3, g+=3) {
                turtle_ecef_to_geodetic(c, g, g + 1, g + 2);
        }
}
