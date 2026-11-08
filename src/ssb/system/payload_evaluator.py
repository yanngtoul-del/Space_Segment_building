"""Extend system evaluator to check optical, SAR, spectrometer, optical comm, QKD, and radio comm performance."""

import math
from ssb.core.constants import EARTH_RADIUS_KM
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


def _geometric_slant_range_km(altitude_km: float, elevation_deg: float = 10.0) -> float:
    """Compute geometric line-of-sight slant range to ground station at given minimum elevation angle."""
    r_e = EARTH_RADIUS_KM
    h = altitude_km
    eps_rad = math.radians(elevation_deg)
    cos_eps = math.cos(eps_rad)
    sin_eps = math.sin(eps_rad)
    r_slant = math.sqrt((r_e + h) ** 2 - (r_e * cos_eps) ** 2) - r_e * sin_eps
    return max(h, round(r_slant, 1))


def evaluate_payload_requirements(
    payload: BasePayload,
    orbit: OrbitDefinition,
    mission: MissionSpecification,
    all_payloads: list[BasePayload] | None = None,
    resolved_options: list | None = None,
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

        # Detect front optical telescope
        telescope: OpticalImagerPayload | None = None
        if all_payloads:
            for p_cand in all_payloads:
                if isinstance(p_cand, OpticalImagerPayload) and p_cand.id != payload.id:
                    telescope = p_cand
                    break

        # Detect optical slit interface
        slit_opt = None
        if resolved_options:
            for opt in resolved_options:
                fn = getattr(opt.equipment, "function", None)
                fn_val = fn.value if hasattr(fn, "value") else str(fn)
                if fn_val == "optical_interface":
                    slit_opt = opt.equipment
                    break

        # Verification of the complete spectrometer chain
        if telescope is not None and slit_opt is not None:
            p = SpectrometerModel.compute(
                payload,
                orbit,
                aperture_diameter_m=telescope.aperture_diameter_m,
                focal_length_m=telescope.focal_length_m,
            )
            compliance.append(
                RuleCheckResult(
                    rule_id="RULE_SPECTRO_CHAIN_OK",
                    category="Chaîne Instrumentale Spectromètre",
                    status=CheckStatus.PASS,
                    message=(
                        f"Chaîne spectrométrique complète couplée : "
                        f"Télescope avant '{telescope.name}' (D={telescope.aperture_diameter_m:.2f} m, f={telescope.focal_length_m:.2f} m) "
                        f"-> Interface '{slit_opt.name}' "
                        f"-> Spectromètre dispersif '{payload.name}'."
                    ),
                )
            )
        elif telescope is None and slit_opt is None:
            if payload.aperture_diameter_m > 0 and payload.focal_length_m > 0:
                p = SpectrometerModel.compute(payload, orbit)
            else:
                p = SpectrometerModel.compute(payload, orbit, aperture_diameter_m=0.0, focal_length_m=0.0)
                compliance.append(
                    RuleCheckResult(
                        rule_id="RULE_SPECTRO_MISSING_TELESCOPE",
                        category="Chaîne Instrumentale Spectromètre",
                        status=CheckStatus.FAIL,
                        message=(
                            f"Chaîne spectrométrique incomplète : Le banc spectromètre '{payload.name}' "
                            f"nécessite un télescope collecteur avant (charge utile optique) "
                            f"et une interface « Fente spectrométrique »."
                        ),
                    )
                )
        elif telescope is None:
            p = SpectrometerModel.compute(payload, orbit, aperture_diameter_m=0.0, focal_length_m=0.0)
            compliance.append(
                RuleCheckResult(
                    rule_id="RULE_SPECTRO_MISSING_TELESCOPE",
                    category="Chaîne Instrumentale Spectromètre",
                    status=CheckStatus.FAIL,
                    message=(
                        f"Chaîne spectrométrique incomplète : Le banc spectromètre '{payload.name}' "
                        f"nécessite un télescope avant pour collecter le flux incident."
                    ),
                )
            )
        else:  # telescope is present, but slit_opt is missing
            p = SpectrometerModel.compute(payload, orbit, aperture_diameter_m=0.0, focal_length_m=0.0)
            compliance.append(
                RuleCheckResult(
                    rule_id="RULE_SPECTRO_MISSING_SLIT",
                    category="Chaîne Instrumentale Spectromètre",
                    status=CheckStatus.FAIL,
                    message=(
                        f"Interface optomécanique manquante : Le plan focal du télescope '{telescope.name}' "
                        f"doit être équipé de l'option « Fente spectrométrique » (sous-système Interface Optique) "
                        f"pour alimenter le spectromètre '{payload.name}'."
                    ),
                )
            )

        perfs = p.__dict__
        perfs["spectral_resolution_nm"] = payload.spectral_resolution_nm
        perfs["spectral_range_max_nm"] = payload.spectral_range_max_nm

    elif payload.payload_type == PayloadType.OPTICAL_COMM:
        assert isinstance(payload, OpticalCommPayload)
        slant_range = _geometric_slant_range_km(orbit.altitude_km, elevation_deg=15.0)
        p = OpticalCommModel.compute_leo_to_ground_link(
            tx_power_w=payload.tx_optical_power_w,
            tx_aperture_m=payload.telescope_aperture_m,
            rx_aperture_m=0.80,
            wavelength_nm=payload.wavelength_nm,
            slant_range_km=slant_range,
            pointing_error_urad=payload.pointing_tracking_accuracy_urad,
            target_data_rate_gbps=payload.max_data_rate_gbps,
        )
        perfs = p.__dict__

    elif payload.payload_type == PayloadType.QKD:
        assert isinstance(payload, QkdPayload)
        slant_range = _geometric_slant_range_km(orbit.altitude_km, elevation_deg=15.0)
        p = QkdModel.compute(
            telescope_aperture_m=payload.telescope_aperture_m,
            source_rate_mhz=payload.source_rate_mhz,
            wavelength_nm=payload.wavelength_nm,
            ground_telescope_aperture_m=1.0,
            slant_range_km=slant_range,
            pointing_jitter_urad=payload.pointing_accuracy_urad,
        )
        perfs = p.__dict__

    elif payload.payload_type == PayloadType.RADIO_COMM:
        assert isinstance(payload, RadioCommPayload)
        slant_range = _geometric_slant_range_km(orbit.altitude_km, elevation_deg=10.0)
        # Ground dish diameter: 4.5 m for GEO/MEO, 3.5 m for LEO
        ground_dish_m = 4.5 if orbit.altitude_km >= 2000.0 else 3.5
        p = RadioCommModel.compute_downlink_budget(
            rf_power_w=payload.rf_output_power_w,
            carrier_freq_ghz=payload.downlink_frequency_ghz,
            satellite_antenna_gain_dbi=payload.antenna_gain_tx_dbi,
            ground_antenna_diameter_m=ground_dish_m,
            data_rate_mbps=payload.max_data_rate_mbps,
            slant_range_km=slant_range,
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
