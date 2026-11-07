"""Synthetic Aperture Radar (SAR) analytical performance models."""

import math
from dataclasses import dataclass
from ssb.core.constants import SPEED_OF_LIGHT, BOLTZMANN_CONSTANT
from ssb.core.orbit import OrbitDefinition
from ssb.core.payload import SarPayload


@dataclass
class SarPerformance:
    wavelength_m: float
    slant_range_nadir_km: float
    slant_range_mid_swath_km: float
    azimuth_resolution_stripmap_m: float
    ground_range_resolution_m: float
    swath_width_ground_km: float
    ground_track_speed_km_s: float
    prf_min_hz: float
    prf_max_hz: float
    nesz_db: float
    raw_data_rate_mbps: float
    compressed_data_rate_mbps: float


class SarModel:
    """Analytical SAR performance calculator."""

    @staticmethod
    def compute(
        payload: SarPayload,
        orbit: OrbitDefinition,
        incidence_angle_deg: float = 35.0,
    ) -> SarPerformance:
        h_m = orbit.altitude_km * 1000.0
        theta_inc_rad = math.radians(incidence_angle_deg)

        lambda_m = SPEED_OF_LIGHT / (payload.frequency_ghz * 1e9)
        r_slant_m = h_m / max(0.1, math.cos(theta_inc_rad))

        delta_az_m = payload.antenna_length_m / 2.0

        b_chirp_hz = payload.chirp_bandwidth_mhz * 1e6
        delta_slant_range_m = SPEED_OF_LIGHT / (2.0 * b_chirp_hz)

        sin_inc = max(0.1, math.sin(theta_inc_rad))
        delta_ground_range_m = delta_slant_range_m / sin_inc

        beta_el_rad = lambda_m / payload.antenna_width_m
        swath_slant_m = r_slant_m * beta_el_rad
        swath_ground_km = (swath_slant_m / sin_inc) / 1000.0

        v_orbit_m_s = (2.0 * math.pi * orbit.semi_major_axis_km * 1000.0) / orbit.period_seconds
        v_ground_m_s = v_orbit_m_s * (6378.137 / orbit.semi_major_axis_km)

        prf_min_hz = 2.0 * v_ground_m_s / payload.antenna_length_m
        prf_max_hz = SPEED_OF_LIGHT / (2.0 * swath_slant_m)
        prf_nom_hz = prf_min_hz * 1.2

        a_phys = payload.antenna_length_m * payload.antenna_width_m
        a_eff = a_phys * 0.6
        g_ant = (4.0 * math.pi * a_eff) / (lambda_m**2)

        t0 = 290.0
        f_sys_linear = 10.0 ** (payload.system_noise_figure_db / 10.0)
        l_sys_linear = 10.0 ** (3.5 / 10.0)

        tau_pulse_s = (payload.duty_cycle_max_pct / 100.0) / prf_nom_hz
        t_syn_s = (lambda_m * r_slant_m) / (2.0 * v_ground_m_s * delta_az_m)
        n_pulses_coherent = prf_nom_hz * t_syn_s

        pixel_area_m2 = delta_ground_range_m * delta_az_m

        p_rx_sigma0_1 = (
            payload.rf_peak_power_w * (g_ant**2) * (lambda_m**2) * pixel_area_m2
        ) / (((4.0 * math.pi) ** 3) * (r_slant_m**4) * l_sys_linear)

        noise_power = BOLTZMANN_CONSTANT * t0 * f_sys_linear * b_chirp_hz
        snr_raw = p_rx_sigma0_1 / noise_power if noise_power > 0 else 1.0

        compression_gain = b_chirp_hz * tau_pulse_s
        total_processing_gain = compression_gain * n_pulses_coherent
        snr_focused_image = snr_raw * total_processing_gain

        nesz_db = - 10.0 * math.log10(max(1e-10, snr_focused_image))

        f_sample_hz = b_chirp_hz * 1.2
        raw_mbps = (2.0 * 8.0 * f_sample_hz * (payload.duty_cycle_max_pct / 100.0)) / 1e6
        comp_mbps = raw_mbps / 4.0

        return SarPerformance(
            wavelength_m=round(lambda_m, 4),
            slant_range_nadir_km=round(orbit.altitude_km, 1),
            slant_range_mid_swath_km=round(r_slant_m / 1000.0, 1),
            azimuth_resolution_stripmap_m=round(delta_az_m, 2),
            ground_range_resolution_m=round(delta_ground_range_m, 2),
            swath_width_ground_km=round(swath_ground_km, 1),
            ground_track_speed_km_s=round(v_ground_m_s / 1000.0, 2),
            prf_min_hz=round(prf_min_hz, 1),
            prf_max_hz=round(prf_max_hz, 1),
            nesz_db=round(nesz_db, 1),
            raw_data_rate_mbps=round(raw_mbps, 1),
            compressed_data_rate_mbps=round(comp_mbps, 1),
        )
