"""Constants and reference values for astrodynamics and space systems."""

import math

# --- Physical and Astronomical Constants (SI) ---
EARTH_RADIUS_M = 6_378_137.0  # WGS84 semi-major axis (equatorial radius) [m]
EARTH_RADIUS_KM = 6_378.137
EARTH_POLAR_RADIUS_M = 6_356_752.3142  # WGS84 polar semi-minor axis [m]
EARTH_FLATTENING = 1.0 / 298.257223563

EARTH_MU = 3.986004418e14  # Standard gravitational parameter G*M [m^3/s^2]
EARTH_MU_KM = 398600.4418  # [km^3/s^2]

EARTH_J2 = 1.08262668e-3  # Second zonal harmonic (oblateness)
EARTH_J3 = -2.53265648e-6
EARTH_J4 = -1.61962159e-6

EARTH_ROTATION_RATE_RAD_S = 7.2921159e-5  # Earth rotation rate [rad/s]
EARTH_SOLAR_DAY_S = 86400.0  # Solar day [s]
EARTH_SIDEREAL_DAY_S = 86164.0905  # Sidereal day [s]

SPEED_OF_LIGHT = 299_792_458.0  # [m/s]
PLANCK_CONSTANT = 6.62607015e-34  # [J*s]
BOLTZMANN_CONSTANT = 1.380649e-23  # [J/K]

STANDARD_GRAVITY = 9.80665  # [m/s^2] (used for Isp -> exhaust velocity: ve = Isp * g0)
SOLAR_CONSTANT_W_M2 = 1361.0  # Total solar irradiance at 1 AU [W/m^2]
SOLAR_RADIATION_PRESSURE_N_M2 = SOLAR_CONSTANT_W_M2 / SPEED_OF_LIGHT  # ~4.54e-6 N/m^2

# --- Sun sync helpers ---
SUN_MEAN_MOTION_RAD_S = 2.0 * math.pi / (365.242199 * 86400.0)  # ~1.99106e-7 rad/s (~0.9856 deg/day)
