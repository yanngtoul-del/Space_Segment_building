"""Quantum Key Distribution (QKD) analytical performance models."""

import math
from dataclasses import dataclass
from ssb.core.constants import SPEED_OF_LIGHT, PLANCK_CONSTANT


@dataclass
class QkdPerformanceResult:
    wavelength_nm: float
    slant_range_km: float
    geometric_channel_loss_db: float
    atmospheric_loss_db: float
    total_channel_loss_db: float
    overall_transmission_efficiency: float
    detected_count_rate_cps: float
    quantum_bit_error_rate_pct: float  # QBER
    asymptotic_secret_key_rate_bps: float
    secret_bits_per_pass: float


class QkdModel:
    """Computes satellite-to-ground decoy-state BB84 QKD link performance."""

    @staticmethod
    def compute(
        telescope_aperture_m: float,
        source_rate_mhz: float,
        wavelength_nm: float = 850.0,
        ground_telescope_aperture_m: float = 1.0,
        slant_range_km: float = 600.0,
        pointing_jitter_urad: float = 1.5,
        dark_count_rate_hz: float = 50.0,
        detector_efficiency: float = 0.50,
        pass_duration_seconds: float = 300.0,
    ) -> QkdPerformanceResult:
        lam_m = wavelength_nm * 1e-9
        r_m = slant_range_km * 1000.0

        # Diffraction beam divergence: theta_div = 1.22 * lambda / D_tx
        theta_div_rad = 1.22 * lam_m / telescope_aperture_m
        beam_waist_radius_ground_m = (theta_div_rad / 2.0) * r_m

        # Pointing jitter widens effective beam footprint:
        pt_sigma_m = (pointing_jitter_urad * 1e-6) * r_m
        effective_radius_m = math.sqrt(beam_waist_radius_ground_m**2 + 2.0 * (pt_sigma_m**2))
        effective_spot_area_m2 = math.pi * (effective_radius_m**2)

        # Ground collection aperture area:
        rx_area_m2 = math.pi * ((ground_telescope_aperture_m / 2.0) ** 2)

        # Geometric collection efficiency (fraction of photons hitting primary mirror):
        eta_geom = min(1.0, rx_area_m2 / max(rx_area_m2, effective_spot_area_m2))
        geom_loss_db = -10.0 * math.log10(max(1e-12, eta_geom))

        # Clear night zenith atmospheric transmission at 850 nm (~75% -> 1.25 dB)
        atmo_loss_db = 1.5
        eta_atmo = 10.0 ** (-atmo_loss_db / 10.0)

        # Satellite transmitter optical throughput (~65%) and OGS filtering/polarization (~40%)
        eta_optics = 0.65 * 0.40

        total_trans_efficiency = eta_geom * eta_atmo * eta_optics * detector_efficiency
        total_loss_db = -10.0 * math.log10(max(1e-12, total_trans_efficiency))

        # Mean photon number per pulse (decoy-state BB84 optimal signal ~0.5)
        mu = 0.5
        pulse_rate_hz = source_rate_mhz * 1e6

        # Signal photon count rate at ground station:
        signal_cps = pulse_rate_hz * mu * total_trans_efficiency

        # Background + dark count rate per detector:
        # 4 single-photon detectors for polarization states (H, V, D, A)
        total_dark_cps = 4.0 * dark_count_rate_hz
        total_detected_cps = signal_cps + total_dark_cps

        # Quantum Bit Error Rate (QBER):
        # QBER = (e_opt * Signal + 0.5 * DarkCounts) / TotalDetected
        # e_opt is optical alignment error (~1.5%)
        e_opt = 0.015
        qber = (e_opt * signal_cps + 0.5 * total_dark_cps) / max(1.0, total_detected_cps)
        qber_pct = qber * 100.0

        # Secret Key Rate (GLLP formula approximation for decoy-state BB84):
        # SKR = max(0, Gain * [1 - 2 * h2(QBER)]) - ErrorCorrectionLeakage
        # Binary entropy h2(x)
        if qber < 0.11:  # Absolute security bound for BB84 is ~11% QBER
            h2 = - (qber * math.log2(qber) + (1.0 - qber) * math.log2(1.0 - qber))
            f_ec = 1.15  # Error correction efficiency factor
            secret_fraction = max(0.0, 1.0 - (f_ec + 1.0) * h2)
            skr_bps = signal_cps * secret_fraction
        else:
            skr_bps = 0.0

        secret_bits_pass = skr_bps * pass_duration_seconds

        return QkdPerformanceResult(
            wavelength_nm=wavelength_nm,
            slant_range_km=slant_range_km,
            geometric_channel_loss_db=round(geom_loss_db, 1),
            atmospheric_loss_db=round(atmo_loss_db, 1),
            total_channel_loss_db=round(total_loss_db, 1),
            overall_transmission_efficiency=round(total_trans_efficiency, 6),
            detected_count_rate_cps=round(total_detected_cps, 1),
            quantum_bit_error_rate_pct=round(qber_pct, 2),
            asymptotic_secret_key_rate_bps=round(skr_bps, 1),
            secret_bits_per_pass=round(secret_bits_pass, 0),
        )
