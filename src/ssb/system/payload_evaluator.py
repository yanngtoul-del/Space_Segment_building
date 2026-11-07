"""Extend system evaluator to check optical, SAR, spectrometer, optical comm, QKD, and radio comm performance."""

from ssb.core.payload import (
    BasePayload,
    OpticalImagerPayload,
    SpectrometerPayload,
    SarPayload,
    OpticalCommPayload,
    QkdPayload,
    RadioCommPayload,
    PayloadType,
)
from ssb.payload.optical_model import OpticalImagerModel
from ssb.payload.sar_model import SarModel
from ssb.payload.spectrometer_model import SpectrometerModel
from ssb.payload.comm_model import OpticalCommModel, RadioCommModel
from ssb.payload.qkd_model import QkdModel
from ssb.core.orbit import OrbitDefinition
from ssb.core.mission import MissionSpecification, RequirementOperator
from ssb.system.checks import RuleCheckResult, CheckStatus


def evaluate_payload_requirements(
    payload: BasePayload,
    orbit: OrbitDefinition,
    mission: MissionSpecification,
) -> tuple[dict, list[RuleCheckResult]]:
    """Compute performance for any payload type and verify against mission requirements."""
    perfs: dict = {}
    compliance: list[RuleCheckResult] = []

    if payload.payload_type == PayloadType.OPTICAL_IMAGER:
        assert isinstance(payload, OpticalImagerPayload)
        p = OpticalImagerModel.compute(payload, orbit)
        perfs = p.__dict__
        perfs["aperture_diameter_m"] = payload.aperture_diameter_m

    elif payload.payload_type == PayloadType.SAR:
        assert isinstance(payload, SarPayload)
        p = SarModel.compute(payload, orbit)
        perfs = p.__dict__

    elif payload.payload_type == PayloadType.SPECTROMETER:
        assert isinstance(payload, SpectrometerPayload)
        p = SpectrometerModel.compute(payload, orbit)
        perfs = p.__dict__
        perfs["spectral_resolution_nm"] = payload.spectral_resolution_nm
        perfs["spectral_range_max_nm"] = payload.spectral_range_max_nm

    elif payload.payload_type == PayloadType.OPTICAL_COMM:
        assert isinstance(payload, OpticalCommPayload)
        p = OpticalCommModel.compute_leo_to_ground_link(
            tx_power_w=payload.tx_optical_power_w,
            tx_aperture_m=payload.telescope_aperture_m,
            rx_aperture_m=0.80,
            wavelength_nm=payload.wavelength_nm,
            slant_range_km=orbit.altitude_km * 1.5,
            pointing_error_urad=payload.pointing_tracking_accuracy_urad,
            target_data_rate_gbps=payload.max_data_rate_gbps,
        )
        perfs = p.__dict__

    elif payload.payload_type == PayloadType.QKD:
        assert isinstance(payload, QkdPayload)
        p = QkdModel.compute(
            telescope_aperture_m=payload.telescope_aperture_m,
            source_rate_mhz=payload.source_rate_mhz,
            wavelength_nm=payload.wavelength_nm,
            ground_telescope_aperture_m=1.0,
            slant_range_km=orbit.altitude_km * 1.3,
            pointing_jitter_urad=payload.pointing_accuracy_urad,
        )
        perfs = p.__dict__

    elif payload.payload_type == PayloadType.RADIO_COMM:
        assert isinstance(payload, RadioCommPayload)
        p = RadioCommModel.compute_downlink_budget(
            rf_power_w=payload.rf_output_power_w,
            carrier_freq_ghz=payload.downlink_frequency_ghz,
            satellite_antenna_gain_dbi=payload.antenna_gain_tx_dbi,
            ground_antenna_diameter_m=5.0,
            data_rate_mbps=payload.max_data_rate_mbps,
            slant_range_km=orbit.altitude_km * 1.5,
        )
        perfs = p.__dict__

    for req in mission.requirements:
        if req.parameter in perfs:
            calc_val = perfs[req.parameter]
            thresh_val = float(req.threshold)
            status = CheckStatus.PASS

            if req.operator == RequirementOperator.LE:
                status = CheckStatus.PASS if calc_val <= thresh_val else CheckStatus.FAIL
            elif req.operator == RequirementOperator.GE:
                status = CheckStatus.PASS if calc_val >= thresh_val else CheckStatus.FAIL
            elif req.operator == RequirementOperator.EQ:
                status = CheckStatus.PASS if calc_val == thresh_val else CheckStatus.FAIL

            compliance.append(
                RuleCheckResult(
                    rule_id=req.id,
                    category="Mission Requirement",
                    status=status,
                    message=f"{req.title}: computed {req.parameter} = {calc_val} {req.unit} (threshold: {req.threshold} {req.unit})",
                    current_value=calc_val,
                    target_value=thresh_val,
                    unit=req.unit,
                )
            )

    return perfs, compliance
