"""Payload models covering optical imagers, spectrometers, SAR, optical comms, QKD, radio comms."""

from enum import Enum
from typing import Literal
from pydantic import BaseModel, Field


class PayloadType(str, Enum):
    OPTICAL_IMAGER = "optical_imager"
    SPECTROMETER = "spectrometer"
    SAR = "sar"
    OPTICAL_COMM = "optical_comm"
    QKD = "qkd"
    RADIO_COMM = "radio_comm"


class BasePayload(BaseModel):
    """Shared physical and interface attributes for all payloads."""

    id: str
    supplier_id: str
    supplier_name: str
    name: str
    payload_type: PayloadType
    description: str = ""

    mass_kg: float = Field(..., ge=0.0)
    operational_power_w: float = Field(..., ge=0.0)
    peak_power_w: float = Field(..., ge=0.0)
    standby_power_w: float = Field(0.0, ge=0.0)
    volume_liters: float = Field(..., ge=0.0)
    dimensions_mm: tuple[float, float, float] = (0.0, 0.0, 0.0)

    # Pointing / stability requirements demanded from platform
    required_pointing_accuracy_deg: float = Field(0.1, ge=0.0)
    required_pointing_stability_arcsec_s: float = Field(10.0, ge=0.0)
    max_tolerated_jitter_arcsec: float = Field(2.0, ge=0.0)

    # Thermal dissipation needed from platform
    thermal_dissipation_w: float = Field(..., ge=0.0)

    # Data generation
    raw_data_rate_mbps: float = Field(..., ge=0.0)
    compressed_data_rate_mbps: float = Field(..., ge=0.0)

    price_meur: float = Field(..., ge=0.0)
    trl: int = Field(9, ge=1, le=9)
    flight_heritage: str = ""


class OpticalImagerPayload(BasePayload):
    """High-resolution optical telescope (push-broom or matrix)."""

    payload_type: Literal[PayloadType.OPTICAL_IMAGER] = PayloadType.OPTICAL_IMAGER

    aperture_diameter_m: float = Field(..., ge=0.01, le=3.0)
    focal_length_m: float = Field(..., ge=0.05)
    f_number: float = Field(..., ge=1.0)
    pixel_pitch_um: float = Field(..., ge=1.0, le=50.0)
    detector_pixels_cross_track: int = Field(..., ge=100)
    spectral_bands: list[str] = Field(default_factory=lambda: ["PAN", "B", "G", "R", "NIR"])
    min_wavelength_nm: float = Field(450.0, ge=200.0)
    max_wavelength_nm: float = Field(900.0, le=14000.0)
    quantum_efficiency_avg: float = Field(0.65, ge=0.0, le=1.0)
    read_noise_electrons: float = Field(10.0, ge=0.0)
    full_well_capacity_electrons: float = Field(20000.0, ge=100.0)
    quantization_bits: int = Field(12, ge=8, le=16)
    optics_transmission: float = Field(0.8, ge=0.0, le=1.0)
    optics_mtf_at_nyquist: float = Field(0.2, ge=0.0, le=1.0)


class SpectrometerPayload(BasePayload):
    """Imaging spectrometer / hyperspectral sensor."""

    payload_type: Literal[PayloadType.SPECTROMETER] = PayloadType.SPECTROMETER

    aperture_diameter_m: float = Field(..., ge=0.01)
    focal_length_m: float = Field(..., ge=0.05)
    pixel_pitch_um: float = Field(..., ge=1.0)
    detector_spatial_pixels: int = Field(..., ge=100)
    spectral_range_min_nm: float = Field(400.0, ge=200.0)
    spectral_range_max_nm: float = Field(2500.0, le=15000.0)
    number_of_spectral_bands: int = Field(..., ge=10, le=500)
    spectral_resolution_nm: float = Field(..., ge=0.1)
    quantization_bits: int = Field(14, ge=10, le=16)


class SarPayload(BasePayload):
    """Synthetic Aperture Radar payload."""

    payload_type: Literal[PayloadType.SAR] = PayloadType.SAR

    frequency_ghz: float = Field(..., ge=0.1, le=40.0)
    band_name: str = Field(..., description="X, C, S, L, P")
    antenna_length_m: float = Field(..., ge=0.5)
    antenna_width_m: float = Field(..., ge=0.2)
    antenna_type: str = Field("phased_array", description="phased_array, deployable_reflector")
    rf_peak_power_w: float = Field(..., ge=100.0)
    duty_cycle_max_pct: float = Field(10.0, ge=0.5, le=50.0)
    chirp_bandwidth_mhz: float = Field(..., ge=10.0, le=1200.0)
    system_noise_figure_db: float = Field(3.5, ge=0.5)
    incidence_angle_min_deg: float = Field(20.0, ge=10.0)
    incidence_angle_max_deg: float = Field(45.0, le=65.0)


class OpticalCommPayload(BasePayload):
    """Laser communication terminal (LEO-ground, ISL, relay)."""

    payload_type: Literal[PayloadType.OPTICAL_COMM] = PayloadType.OPTICAL_COMM

    telescope_aperture_m: float = Field(..., ge=0.02, le=0.5)
    wavelength_nm: float = Field(1550.0, ge=800.0, le=2000.0)
    tx_optical_power_w: float = Field(..., ge=0.1, le=10.0)
    max_data_rate_gbps: float = Field(..., ge=0.1)
    beam_divergence_urad: float = Field(..., ge=1.0)
    pointing_tracking_accuracy_urad: float = Field(..., ge=0.1)
    compatible_standards: list[str] = Field(default_factory=lambda: ["SDA_Tranche1", "CCSDS_141.0-B-1"])


class QkdPayload(BasePayload):
    """Quantum Key Distribution space terminal."""

    payload_type: Literal[PayloadType.QKD] = PayloadType.QKD

    protocol: str = Field("BB84_decoy_state", description="BB84_decoy_state, entangled_photons")
    telescope_aperture_m: float = Field(..., ge=0.05, le=0.6)
    source_rate_mhz: float = Field(..., ge=1.0)
    wavelength_nm: float = Field(850.0)
    pointing_accuracy_urad: float = Field(1.5, ge=0.1)
    night_only_operation: bool = True


class RadioCommPayload(BasePayload):
    """Radio Frequency communication payload (transponder, relay, Ka/Ku downlink)."""

    payload_type: Literal[PayloadType.RADIO_COMM] = PayloadType.RADIO_COMM

    uplink_frequency_ghz: float = Field(..., ge=0.1)
    downlink_frequency_ghz: float = Field(..., ge=0.1)
    rf_output_power_w: float = Field(..., ge=1.0)
    antenna_gain_tx_dbi: float = Field(..., ge=0.0)
    antenna_gain_rx_dbi: float = Field(..., ge=0.0)
    bandwidth_mhz: float = Field(..., ge=0.1)
    max_data_rate_mbps: float = Field(..., ge=0.1)
