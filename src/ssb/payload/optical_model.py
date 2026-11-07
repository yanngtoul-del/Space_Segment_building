"""Analytical performance models for optical imagers."""

import math
from dataclasses import dataclass
from ssb.core.constants import SPEED_OF_LIGHT, PLANCK_CONSTANT, SOLAR_CONSTANT_W_M2
from ssb.core.orbit import OrbitDefinition
from ssb.core.payload import OpticalImagerPayload


@dataclass
class OpticalImagerPerformance:
    gsd_nadir_m: float
    swath_width_km: float
    field_of_view_deg: float
    instantaneous_fov_urad: float
    nyquist_frequency_lp_mm: float
    diffraction_limit_rad: float
    diffraction_ground_spot_m: float
    ground_track_speed_km_s: float
    line_rate_hz: float
    integration_time_ms: float
    data_rate_raw_mbps: float
    data_rate_compressed_mbps: float
    snr_nadir_estimate: float
    niirs_estimate: float  # Approximation based on GIQE 4/5


class OpticalImagerModel:
    """Computes geometric and radiometric performance of an optical imager on orbit."""

    @staticmethod
    def compute(
        payload: OpticalImagerPayload,
        orbit: OrbitDefinition,
        target_albedo: float = 0.3,
        solar_zenith_angle_deg: float = 30.0,
    ) -> OpticalImagerPerformance:
        # Altitude in meters
        h_m = orbit.altitude_km * 1000.0

        # GSD at nadir (geometric projection): GSD = p * h / f
        p_m = payload.pixel_pitch_um * 1e-6
        f_m = payload.focal_length_m
        d_m = payload.aperture_diameter_m

        gsd_m = (p_m * h_m) / f_m

        # IFOV (Instantaneous Field of View)
        ifov_rad = p_m / f_m
        ifov_urad = ifov_rad * 1e6

        # Cross-track swath width: W = N_pixels * GSD
        swath_km = (payload.detector_pixels_cross_track * gsd_m) / 1000.0

        # Field of View (cross-track): FOV = 2 * arctan((N * p / 2) / f)
        sensor_width_m = payload.detector_pixels_cross_track * p_m
        fov_rad = 2.0 * math.atan(sensor_width_m / (2.0 * f_m))
        fov_deg = math.degrees(fov_rad)

        # Nyquist frequency: f_Nyq = 1 / (2 * p)
        f_nyq_lp_mm = 1.0 / (2.0 * (payload.pixel_pitch_um * 1e-3))

        # Optical diffraction limit: theta = 1.22 * lambda / D
        mid_lambda_m = ((payload.min_wavelength_nm + payload.max_wavelength_nm) / 2.0) * 1e-9
        diff_lim_rad = 1.22 * mid_lambda_m / d_m
        diff_spot_m = diff_lim_rad * h_m

        # Satellite ground track velocity: v_ground = v_orbit * (R_E / (R_E + h))
        v_orbit_km_s = (2.0 * math.pi * orbit.semi_major_axis_km) / orbit.period_seconds
        v_ground_km_s = v_orbit_km_s * (6378.137 / orbit.semi_major_axis_km)
        v_ground_m_s = v_ground_km_s * 1000.0

        # Push-broom line rate: f_line = v_ground / GSD
        line_rate_hz = v_ground_m_s / gsd_m
        t_int_max_s = 1.0 / line_rate_hz
        t_int_ms = (t_int_max_s * 0.9) * 1000.0  # nominal 90% duty cycle

        # Data rate: N_pixels * bits * bands * line_rate
        n_bands = len(payload.spectral_bands)
        raw_bps = payload.detector_pixels_cross_track * payload.quantization_bits * n_bands * line_rate_hz
        raw_mbps = raw_bps / 1e6
        # Assume typical JPEG-LS / CCSDS 122 compression ratio ~ 3.5:1
        comp_mbps = raw_mbps / 3.5

        # --- Radiometry / SNR Approximation ---
        # TOA solar irradiance across band
        cos_sza = max(0.1, math.cos(math.radians(solar_zenith_angle_deg)))
        e_sun_band = SOLAR_CONSTANT_W_M2 * ((payload.max_wavelength_nm - payload.min_wavelength_nm) / 800.0)
        radiance_toa = (target_albedo / math.pi) * e_sun_band * cos_sza  # W / (m^2 * sr)

        # Photon flux per pixel:
        # P_pixel = L * (pi * D^2 / 4) * (A_pixel / f^2) * tau_optics
        omega_pixel = (p_m / f_m) ** 2
        p_pixel_w = radiance_toa * (math.pi * (d_m**2) / 4.0) * omega_pixel * payload.optics_transmission

        photon_energy = (PLANCK_CONSTANT * SPEED_OF_LIGHT) / mid_lambda_m
        photon_rate = p_pixel_w / photon_energy
        signal_electrons = photon_rate * (t_int_ms * 1e-3) * payload.quantum_efficiency_avg

        # Noise = sqrt(Signal_e + Noise_read^2)
        total_noise_e = math.sqrt(signal_electrons + (payload.read_noise_electrons**2))
        snr = signal_electrons / total_noise_e if total_noise_e > 0 else 0.0

        # --- GIQE (General Image Quality Equation) estimate for NIIRS ---
        # NIIRS = 10.251 - a * log10(GSD_inches) + b * log10(RER) - 0.656 * H - 0.344 * (G/SNR)
        gsd_inches = gsd_m * 39.3701
        niirs = 10.251 - 3.32 * math.log10(max(0.1, gsd_inches)) + 1.559 * math.log10(max(0.1, payload.optics_mtf_at_nyquist))
        niirs = max(0.0, min(9.0, niirs))

        return OpticalImagerPerformance(
            gsd_nadir_m=round(gsd_m, 3),
            swath_width_km=round(swath_km, 2),
            field_of_view_deg=round(fov_deg, 3),
            instantaneous_fov_urad=round(ifov_urad, 2),
            nyquist_frequency_lp_mm=round(f_nyq_lp_mm, 2),
            diffraction_limit_rad=diff_lim_rad,
            diffraction_ground_spot_m=round(diff_spot_m, 3),
            ground_track_speed_km_s=round(v_ground_km_s, 3),
            line_rate_hz=round(line_rate_hz, 1),
            integration_time_ms=round(t_int_ms, 3),
            data_rate_raw_mbps=round(raw_mbps, 1),
            data_rate_compressed_mbps=round(comp_mbps, 1),
            snr_nadir_estimate=round(snr, 1),
            niirs_estimate=round(niirs, 2),
        )
