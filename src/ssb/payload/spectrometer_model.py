"""Hyperspectral and imaging spectrometer analytical performance models."""

import math
from dataclasses import dataclass
from ssb.core.constants import SPEED_OF_LIGHT, PLANCK_CONSTANT
from ssb.core.orbit import OrbitDefinition
from ssb.core.payload import SpectrometerPayload


@dataclass
class SpectrometerPerformance:
    gsd_spatial_nadir_m: float
    swath_width_km: float
    field_of_view_deg: float
    spectral_sampling_nm: float
    spectral_bands_count: int
    mean_snr_estimate: float
    data_rate_raw_mbps: float
    data_rate_compressed_mbps: float
    line_rate_hz: float
    aperture_diameter_m: float = 0.0
    focal_length_m: float = 0.0


class SpectrometerModel:
    """Computes spatial, spectral and radiometric parameters of an imaging spectrometer coupled to a front telescope."""

    @staticmethod
    def compute(
        payload: SpectrometerPayload,
        orbit: OrbitDefinition,
        aperture_diameter_m: float | None = None,
        focal_length_m: float | None = None,
        target_albedo: float = 0.25,
        solar_zenith_angle_deg: float = 35.0,
    ) -> SpectrometerPerformance:
        h_m = orbit.altitude_km * 1000.0
        p_m = payload.pixel_pitch_um * 1e-6
        f_m = focal_length_m if focal_length_m is not None else payload.focal_length_m
        d_m = aperture_diameter_m if aperture_diameter_m is not None else payload.aperture_diameter_m

        # Spectral sampling (determined by spectrometer dispersive back-end)
        spectral_span_nm = payload.spectral_range_max_nm - payload.spectral_range_min_nm
        delta_lambda_nm = spectral_span_nm / max(1, payload.number_of_spectral_bands)

        if f_m <= 0.0 or d_m <= 0.0:
            # Uncoupled back-end spectrometer: no front telescope collecting flux
            return SpectrometerPerformance(
                gsd_spatial_nadir_m=0.0,
                swath_width_km=0.0,
                field_of_view_deg=0.0,
                spectral_sampling_nm=round(delta_lambda_nm, 2),
                spectral_bands_count=payload.number_of_spectral_bands,
                mean_snr_estimate=0.0,
                data_rate_raw_mbps=0.0,
                data_rate_compressed_mbps=0.0,
                line_rate_hz=0.0,
                aperture_diameter_m=0.0,
                focal_length_m=0.0,
            )

        # 1. Spatial GSD and Swath (combining pixel pitch of slit/detector with telescope focal length)
        gsd_m = (p_m * h_m) / f_m
        swath_km = (payload.detector_spatial_pixels * gsd_m) / 1000.0

        sensor_width_m = payload.detector_spatial_pixels * p_m
        fov_rad = 2.0 * math.atan(sensor_width_m / (2.0 * f_m))
        fov_deg = math.degrees(fov_rad)

        # 2. Motion & line integration
        v_orbit_km_s = (2.0 * math.pi * orbit.semi_major_axis_km) / orbit.period_seconds
        v_ground_m_s = (v_orbit_km_s * (6378.137 / orbit.semi_major_axis_km)) * 1000.0

        line_rate_hz = v_ground_m_s / gsd_m
        t_int_s = 0.85 / line_rate_hz

        # 3. Radiometry / SNR per narrow band
        e_sun_per_nm = 1.65
        e_sun_band = e_sun_per_nm * delta_lambda_nm
        cos_sza = max(0.1, math.cos(math.radians(solar_zenith_angle_deg)))
        radiance_toa = (target_albedo / math.pi) * e_sun_band * cos_sza

        omega_pixel = (p_m / f_m) ** 2
        optics_trans = 0.75
        p_chan_w = radiance_toa * (math.pi * (d_m**2) / 4.0) * omega_pixel * optics_trans

        mid_lambda_m = ((payload.spectral_range_min_nm + payload.spectral_range_max_nm) / 2.0) * 1e-9
        photon_energy = (PLANCK_CONSTANT * SPEED_OF_LIGHT) / mid_lambda_m
        photon_rate = p_chan_w / photon_energy
        qe = 0.70

        tdi_stages = 12
        signal_electrons = photon_rate * t_int_s * qe * tdi_stages

        read_noise_e = 10.0
        total_noise_e = math.sqrt(signal_electrons + (read_noise_e**2 * tdi_stages))
        snr = signal_electrons / total_noise_e if total_noise_e > 0 else 0.0

        # 4. Data rate (Spatial pixels * Spectral bands * Bits * LineRate)
        raw_bps = payload.detector_spatial_pixels * payload.number_of_spectral_bands * payload.quantization_bits * line_rate_hz
        raw_mbps = raw_bps / 1e6
        comp_mbps = raw_mbps / 2.8

        return SpectrometerPerformance(
            gsd_spatial_nadir_m=round(gsd_m, 2),
            swath_width_km=round(swath_km, 2),
            field_of_view_deg=round(fov_deg, 2),
            spectral_sampling_nm=round(delta_lambda_nm, 2),
            spectral_bands_count=payload.number_of_spectral_bands,
            mean_snr_estimate=round(snr, 1),
            data_rate_raw_mbps=round(raw_mbps, 1),
            data_rate_compressed_mbps=round(comp_mbps, 1),
            line_rate_hz=round(line_rate_hz, 1),
            aperture_diameter_m=round(d_m, 3),
            focal_length_m=round(f_m, 3),
        )
