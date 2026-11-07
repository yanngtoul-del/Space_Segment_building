"""Ground station access and visibility geometry calculations."""

import math
from dataclasses import dataclass
import numpy as np
from ssb.core.constants import EARTH_RADIUS_KM
from ssb.core.mission import GroundStationTarget
from ssb.orbit.propagator import OrbitStatePoint


@dataclass
class GroundStationPass:
    station_id: str
    station_name: str
    start_time_s: float
    end_time_s: float
    duration_seconds: float
    max_elevation_deg: float


class StationAccessCalculator:
    """Computes satellite elevation angles from ground stations and pass intervals."""

    @staticmethod
    def lat_lon_to_ecef(lat_deg: float, lon_deg: float, alt_km: float = 0.0) -> np.ndarray:
        phi = math.radians(lat_deg)
        lam = math.radians(lon_deg)
        r = EARTH_RADIUS_KM + alt_km
        return np.array([
            r * math.cos(phi) * math.cos(lam),
            r * math.cos(phi) * math.sin(lam),
            r * math.sin(phi),
        ])

    @classmethod
    def calculate_elevation_deg(
        cls, sat_lat_deg: float, sat_lon_deg: float, sat_alt_km: float, station: GroundStationTarget
    ) -> float:
        """Calculate elevation angle of satellite from ground station."""
        r_sat = cls.lat_lon_to_ecef(sat_lat_deg, sat_lon_deg, sat_alt_km)
        r_sta = cls.lat_lon_to_ecef(station.latitude_deg, station.longitude_deg, station.altitude_m / 1000.0)

        rho_vec = r_sat - r_sta
        rho_mag = np.linalg.norm(rho_vec)
        if rho_mag == 0:
            return 90.0

        # Station local zenith unit vector
        zenith = r_sta / np.linalg.norm(r_sta)
        cos_zenith_angle = np.dot(rho_vec, zenith) / rho_mag
        cos_zenith_angle = max(-1.0, min(1.0, cos_zenith_angle))

        elevation_rad = (math.pi / 2.0) - math.acos(cos_zenith_angle)
        return math.degrees(elevation_rad)

    @classmethod
    def find_passes(
        cls,
        ground_track: list[OrbitStatePoint],
        station: GroundStationTarget,
    ) -> list[GroundStationPass]:
        """Detect all visibility passes over a given ground station."""
        passes: list[GroundStationPass] = []
        in_pass = False
        pass_start_t = 0.0
        max_elev = 0.0

        for pt in ground_track:
            elev = cls.calculate_elevation_deg(
                pt.latitude_deg, pt.longitude_deg, pt.altitude_km, station
            )
            if elev >= station.min_elevation_deg:
                if not in_pass:
                    in_pass = True
                    pass_start_t = pt.time_s
                    max_elev = elev
                else:
                    if elev > max_elev:
                        max_elev = elev
            else:
                if in_pass:
                    in_pass = False
                    passes.append(
                        GroundStationPass(
                            station_id=station.id,
                            station_name=station.name,
                            start_time_s=pass_start_t,
                            end_time_s=pt.time_s,
                            duration_seconds=round(pt.time_s - pass_start_t, 1),
                            max_elevation_deg=round(max_elev, 1),
                        )
                    )

        # If still in pass at the end of the simulation timeline (e.g. permanent GEO visibility)
        if in_pass and ground_track:
            passes.append(
                GroundStationPass(
                    station_id=station.id,
                    station_name=station.name,
                    start_time_s=pass_start_t,
                    end_time_s=ground_track[-1].time_s,
                    duration_seconds=round(ground_track[-1].time_s - pass_start_t, 1),
                    max_elevation_deg=round(max_elev, 1),
                )
            )

        return passes
