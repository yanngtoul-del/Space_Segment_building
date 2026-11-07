"""Numerical and analytical orbit propagation with J2 perturbation, eclipses, and ground tracks."""

import math
from dataclasses import dataclass
import numpy as np
from scipy.integrate import solve_ivp
from ssb.core.constants import (
    EARTH_RADIUS_M,
    EARTH_RADIUS_KM,
    EARTH_MU,
    EARTH_J2,
    EARTH_ROTATION_RATE_RAD_S,
    SUN_MEAN_MOTION_RAD_S,
)
from ssb.core.orbit import OrbitDefinition


@dataclass
class OrbitStatePoint:
    time_s: float
    position_eci_km: tuple[float, float, float]
    velocity_eci_km_s: tuple[float, float, float]
    latitude_deg: float
    longitude_deg: float
    altitude_km: float
    in_eclipse: bool


@dataclass
class OrbitSimulationSummary:
    duration_days: float
    orbit_period_minutes: float
    eclipse_duration_avg_minutes: float
    eclipse_fraction_pct: float
    sunlit_fraction_pct: float
    beta_angle_deg: float
    ground_track: list[OrbitStatePoint]


class OrbitPropagator:
    """Propagates orbits including Earth J2 oblateness and calculates ground traces & eclipses."""

    @staticmethod
    def _j2_derivatives(t: float, y: np.ndarray) -> np.ndarray:
        """State derivative in ECI frame: y = [x, y, z, vx, vy, vz] in SI units [m, m/s]."""
        r_vec = y[:3]
        v_vec = y[3:]

        r = np.linalg.norm(r_vec)
        r2 = r * r
        r3 = r2 * r
        z = r_vec[2]
        z2 = z * z

        # Two-body gravitational acceleration
        a_grav = - (EARTH_MU / r3) * r_vec

        # J2 perturbation acceleration
        # a_j2_x = - 3/2 * J2 * mu * R_E^2 / r^5 * x * (1 - 5 * z^2 / r^2)
        # a_j2_y = - 3/2 * J2 * mu * R_E^2 / r^5 * y * (1 - 5 * z^2 / r^2)
        # a_j2_z = - 3/2 * J2 * mu * R_E^2 / r^5 * z * (3 - 5 * z^2 / r^2)
        factor = - 1.5 * EARTH_J2 * EARTH_MU * (EARTH_RADIUS_M**2) / (r**5)
        z_ratio = z2 / r2

        a_j2 = np.zeros(3)
        a_j2[0] = factor * r_vec[0] * (1.0 - 5.0 * z_ratio)
        a_j2[1] = factor * r_vec[1] * (1.0 - 5.0 * z_ratio)
        a_j2[2] = factor * r_vec[2] * (3.0 - 5.0 * z_ratio)

        a_total = a_grav + a_j2
        return np.concatenate([v_vec, a_total])

    @staticmethod
    def kepler_to_eci(orbit: OrbitDefinition) -> tuple[np.ndarray, np.ndarray]:
        """Convert Keplerian orbital elements to ECI position [m] and velocity [m/s]."""
        a_m = orbit.semi_major_axis_km * 1000.0
        e = orbit.eccentricity
        i = math.radians(orbit.inclination_deg)
        raan = math.radians(orbit.raan_deg)
        arg_p = math.radians(orbit.arg_perigee_deg)
        nu = math.radians(orbit.true_anomaly_deg)

        # In orbital plane (perifocal frame PQW)
        p_m = a_m * (1.0 - e**2)
        r_mag = p_m / (1.0 + e * math.cos(nu))

        r_pqw = np.array([r_mag * math.cos(nu), r_mag * math.sin(nu), 0.0])
        h = math.sqrt(EARTH_MU * p_m)
        v_pqw = np.array([- (EARTH_MU / h) * math.sin(nu), (EARTH_MU / h) * (e + math.cos(nu)), 0.0])

        # Rotation matrix from PQW to ECI: R = Rz(-raan) * Rx(-i) * Rz(-arg_p)
        cos_o, sin_o = math.cos(raan), math.sin(raan)
        cos_i, sin_i = math.cos(i), math.sin(i)
        cos_w, sin_w = math.cos(arg_p), math.sin(arg_p)

        px = cos_o * cos_w - sin_o * sin_w * cos_i
        py = sin_o * cos_w + cos_o * sin_w * cos_i
        pz = sin_w * sin_i

        qx = -cos_o * sin_w - sin_o * cos_w * cos_i
        qy = -sin_o * sin_w + cos_o * cos_w * cos_i
        qz = cos_w * sin_i

        wx = sin_o * sin_i
        wy = -cos_o * sin_i
        wz = cos_i

        rot_mat = np.array([[px, qx, wx], [py, qy, wy], [pz, qz, wz]])
        r_eci = rot_mat @ r_pqw
        v_eci = rot_mat @ v_pqw

        return r_eci, v_eci

    @classmethod
    def get_sun_vector_eci(cls, t_s: float, day_of_year: float = 80.0) -> np.ndarray:
        """Approximate Sun direction unit vector in ECI for a given epoch."""
        # Mean ecliptic longitude of the Sun:
        # Equinox at ~day 80
        sun_long_rad = ((day_of_year - 80.0) / 365.25) * 2.0 * math.pi + (t_s * SUN_MEAN_MOTION_RAD_S)
        obliquity_rad = math.radians(23.44)

        x_sun = math.cos(sun_long_rad)
        y_sun = math.sin(sun_long_rad) * math.cos(obliquity_rad)
        z_sun = math.sin(sun_long_rad) * math.sin(obliquity_rad)
        sun_vec = np.array([x_sun, y_sun, z_sun])
        return sun_vec / np.linalg.norm(sun_vec)

    @classmethod
    def check_eclipse(cls, r_eci_m: np.ndarray, sun_vec_eci: np.ndarray) -> bool:
        """Cylindrical Earth shadow model for eclipse check."""
        # Distance projected along anti-Sun direction:
        s_dot_r = np.dot(sun_vec_eci, r_eci_m)
        if s_dot_r >= 0.0:
            # Satellite is on sunlit hemisphere
            return False

        # Distance perpendicular to sun-earth line:
        perp_dist = np.linalg.norm(r_eci_m - s_dot_r * sun_vec_eci)
        return bool(perp_dist < EARTH_RADIUS_M)

    @classmethod
    def eci_to_lat_lon(cls, r_eci_m: np.ndarray, t_s: float) -> tuple[float, float, float]:
        """Convert ECI position vector to geodetic latitude, longitude [deg] and altitude [km]."""
        # Earth rotation angle (assuming Greenwich sidereal time = 0 at t=0)
        theta = (t_s * EARTH_ROTATION_RATE_RAD_S) % (2.0 * math.pi)

        # Rotate to ECEF around Z-axis
        cos_t = math.cos(theta)
        sin_t = math.sin(theta)
        x_ecef = cos_t * r_eci_m[0] + sin_t * r_eci_m[1]
        y_ecef = -sin_t * r_eci_m[0] + cos_t * r_eci_m[1]
        z_ecef = r_eci_m[2]

        r_xy = math.sqrt(x_ecef**2 + y_ecef**2)
        lat_rad = math.atan2(z_ecef, r_xy)
        lon_rad = math.atan2(y_ecef, x_ecef)

        lat_deg = math.degrees(lat_rad)
        lon_deg = math.degrees(lon_rad)
        alt_km = (np.linalg.norm(r_eci_m) - EARTH_RADIUS_M) / 1000.0

        return lat_deg, lon_deg, alt_km

    @classmethod
    def simulate(
        cls,
        orbit: OrbitDefinition,
        duration_orbits: float = 3.0,
        samples_per_orbit: int = 120,
    ) -> OrbitSimulationSummary:
        """Run J2 numerical propagation for given orbits and return ground track & eclipse statistics."""
        period_s = orbit.period_seconds
        total_time_s = duration_orbits * period_s
        n_points = int(duration_orbits * samples_per_orbit)
        t_eval = np.linspace(0, total_time_s, n_points)

        r0, v0 = cls.kepler_to_eci(orbit)
        y0 = np.concatenate([r0, v0])

        sol = solve_ivp(
            fun=cls._j2_derivatives,
            t_span=(0.0, total_time_s),
            y0=y0,
            t_eval=t_eval,
            method="RK45",
            rtol=1e-8,
            atol=1e-8,
        )

        ground_track: list[OrbitStatePoint] = []
        eclipse_count = 0

        sun_vec = cls.get_sun_vector_eci(0.0)

        for i, t in enumerate(sol.t):
            r_eci = sol.y[:3, i]
            v_eci = sol.y[3:, i]

            is_eclipse = cls.check_eclipse(r_eci, sun_vec)
            if is_eclipse:
                eclipse_count += 1

            lat_deg, lon_deg, alt_km = cls.eci_to_lat_lon(r_eci, t)

            ground_track.append(
                OrbitStatePoint(
                    time_s=float(t),
                    position_eci_km=(r_eci[0] / 1000.0, r_eci[1] / 1000.0, r_eci[2] / 1000.0),
                    velocity_eci_km_s=(v_eci[0] / 1000.0, v_eci[1] / 1000.0, v_eci[2] / 1000.0),
                    latitude_deg=round(lat_deg, 3),
                    longitude_deg=round(lon_deg, 3),
                    altitude_km=round(alt_km, 2),
                    in_eclipse=is_eclipse,
                )
            )

        eclipse_frac = (eclipse_count / n_points) * 100.0
        sunlit_frac = 100.0 - eclipse_frac
        avg_eclipse_min = (eclipse_frac / 100.0) * (period_s / 60.0)

        # Orbit normal vector for Beta angle calculation
        h_vec = np.cross(r0, v0)
        h_hat = h_vec / np.linalg.norm(h_vec)
        # Beta angle: angle between orbit plane and Sun vector: sin(beta) = h_hat . s_hat
        sin_beta = np.dot(h_hat, sun_vec)
        beta_deg = math.degrees(math.asin(max(-1.0, min(1.0, sin_beta))))

        return OrbitSimulationSummary(
            duration_days=round(total_time_s / 86400.0, 3),
            orbit_period_minutes=round(period_s / 60.0, 2),
            eclipse_duration_avg_minutes=round(avg_eclipse_min, 2),
            eclipse_fraction_pct=round(eclipse_frac, 1),
            sunlit_fraction_pct=round(sunlit_frac, 1),
            beta_angle_deg=round(beta_deg, 2),
            ground_track=ground_track,
        )
