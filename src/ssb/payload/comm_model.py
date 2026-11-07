"""Optical and Radio Communication link budget models."""

import math
from dataclasses import dataclass
from ssb.core.constants import SPEED_OF_LIGHT, BOLTZMANN_CONSTANT


@dataclass
class OpticalCommLinkResult:
    wavelength_nm: float
    slant_range_km: float
    tx_gain_dbi: float
    rx_gain_dbi: float
    free_space_loss_db: float
    pointing_loss_db: float
    atmospheric_loss_db: float
    received_optical_power_dbm: float
    received_optical_power_nw: float
    margin_db: float
    achievable_data_rate_gbps: float


class OpticalCommModel:
    """Computes free-space optical link budget (LEO-ground, ISL)."""

    @staticmethod
    def compute_leo_to_ground_link(
        tx_power_w: float,
        tx_aperture_m: float,
        rx_aperture_m: float,
        wavelength_nm: float = 1550.0,
        slant_range_km: float = 1000.0,
        pointing_error_urad: float = 2.0,
        target_data_rate_gbps: float = 2.5,
        rx_sensitivity_dbm: float = -38.0,
    ) -> OpticalCommLinkResult:
        lam_m = wavelength_nm * 1e-9
        r_m = slant_range_km * 1000.0

        # Antenna gains: G = (pi * D / lambda)^2
        g_tx_linear = (math.pi * tx_aperture_m / lam_m) ** 2
        g_tx_dbi = 10.0 * math.log10(g_tx_linear)

        g_rx_linear = (math.pi * rx_aperture_m / lam_m) ** 2
        g_rx_dbi = 10.0 * math.log10(g_rx_linear)

        # Free space path loss: FSPL = (4 * pi * R / lambda)^2
        fspl_db = 20.0 * math.log10(4.0 * math.pi * r_m / lam_m)

        # Pointing loss (Gaussian beam approximation): L_pt = exp(-2 * (theta_err / theta_div)^2)
        div_rad = 1.22 * lam_m / tx_aperture_m
        pt_err_rad = pointing_error_urad * 1e-6
        pointing_loss_db = 4.343 * 2.0 * ((pt_err_rad / div_rad) ** 2)

        # Atmospheric and scintillation losses at 1550 nm (clear sky zenith ~1.5-3 dB)
        atmo_loss_db = 2.5

        # Transmitter power in dBm: P_dBm = 10 * log10(P_W * 1000)
        p_tx_dbm = 10.0 * math.log10(tx_power_w * 1000.0)

        # Link budget: P_rx = P_tx + G_tx + G_rx - FSPL - L_pointing - L_atmo
        p_rx_dbm = p_tx_dbm + g_tx_dbi + g_rx_dbi - fspl_db - pointing_loss_db - atmo_loss_db
        p_rx_mw = 10.0 ** (p_rx_dbm / 10.0)
        p_rx_nw = p_rx_mw * 1e6

        margin_db = p_rx_dbm - rx_sensitivity_dbm

        return OpticalCommLinkResult(
            wavelength_nm=wavelength_nm,
            slant_range_km=slant_range_km,
            tx_gain_dbi=round(g_tx_dbi, 1),
            rx_gain_dbi=round(g_rx_dbi, 1),
            free_space_loss_db=round(fspl_db, 1),
            pointing_loss_db=round(pointing_loss_db, 2),
            atmospheric_loss_db=round(atmo_loss_db, 1),
            received_optical_power_dbm=round(p_rx_dbm, 1),
            received_optical_power_nw=round(p_rx_nw, 2),
            margin_db=round(margin_db, 1),
            achievable_data_rate_gbps=target_data_rate_gbps if margin_db >= 3.0 else 0.0,
        )


@dataclass
class RadioLinkResult:
    carrier_frequency_ghz: float
    slant_range_km: float
    eirp_dbw: float
    free_space_loss_db: float
    atmospheric_loss_db: float
    rx_gt_db_k: float
    c_over_n0_dbhz: float
    eb_over_n0_db: float
    link_margin_db: float
    max_data_rate_mbps: float


class RadioCommModel:
    """Computes RF space-to-ground downlink budget (X/Ka-band)."""

    @staticmethod
    def compute_downlink_budget(
        rf_power_w: float,
        carrier_freq_ghz: float,
        satellite_antenna_gain_dbi: float,
        ground_antenna_diameter_m: float,
        data_rate_mbps: float,
        slant_range_km: float = 1200.0,
        ground_system_temp_k: float = 135.0,
        req_eb_n0_db: float = 6.5,  # DVB-S2 QPSK 3/4 with LDPC
    ) -> RadioLinkResult:
        lam_m = SPEED_OF_LIGHT / (carrier_freq_ghz * 1e9)
        r_m = slant_range_km * 1000.0

        # EIRP = P_tx (dBW) + G_tx (dBi) - LineLoss (1.5 dB)
        p_tx_dbw = 10.0 * math.log10(rf_power_w)
        line_loss_tx_db = 1.5
        eirp_dbw = p_tx_dbw + satellite_antenna_gain_dbi - line_loss_tx_db

        # Free space path loss:
        fspl_db = 20.0 * math.log10(4.0 * math.pi * r_m / lam_m)
        atmo_loss_db = 1.0  # Clear sky X-band

        # Ground station antenna gain (55% efficiency):
        a_phys = math.pi * ((ground_antenna_diameter_m / 2.0) ** 2)
        g_rx_linear = (4.0 * math.pi * 0.55 * a_phys) / (lam_m**2)
        g_rx_dbi = 10.0 * math.log10(g_rx_linear)

        # Ground G/T:
        gt_db_k = g_rx_dbi - 10.0 * math.log10(ground_system_temp_k)

        # C/N0 = EIRP - FSPL - Atmo + (G/T) - k_B (in dB)
        k_dbw_hz_k = 10.0 * math.log10(BOLTZMANN_CONSTANT)  # -228.6 dBW/(Hz*K)
        c_n0_dbhz = eirp_dbw - fspl_db - atmo_loss_db + gt_db_k - k_dbw_hz_k

        # Eb/N0 = C/N0 - 10*log10(Data_rate_bps)
        rate_bps = data_rate_mbps * 1e6
        eb_n0_db = c_n0_dbhz - 10.0 * math.log10(rate_bps)
        margin_db = eb_n0_db - req_eb_n0_db

        return RadioLinkResult(
            carrier_frequency_ghz=carrier_freq_ghz,
            slant_range_km=slant_range_km,
            eirp_dbw=round(eirp_dbw, 1),
            free_space_loss_db=round(fspl_db, 1),
            atmospheric_loss_db=round(atmo_loss_db, 1),
            rx_gt_db_k=round(gt_db_k, 1),
            c_over_n0_dbhz=round(c_n0_dbhz, 1),
            eb_over_n0_db=round(eb_n0_db, 1),
            link_margin_db=round(margin_db, 1),
            max_data_rate_mbps=data_rate_mbps,
        )
