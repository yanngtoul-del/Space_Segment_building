"""Test spectrometer and QKD models, plus teacher project replay and integrity verification."""

from pathlib import Path
from ssb.core.orbit import OrbitDefinition
from ssb.core.payload import SpectrometerPayload, QkdPayload, PayloadType
from ssb.core.mission import (
    MissionSpecification,
    MissionRequirement,
    RequirementType,
    RequirementOperator,
)
from ssb.core.project import StudentProject, SystemConfiguration, SelectedOption
from ssb.catalog.database import CatalogDatabase
from ssb.payload.spectrometer_model import SpectrometerModel
from ssb.payload.qkd_model import QkdModel
from ssb.system.evaluator import SystemEvaluator, CheckStatus


def test_spectrometer_model():
    orbit = OrbitDefinition(altitude_km=500.0)
    spectro = SpectrometerPayload(
        id="pl_spec_hyperspectral",
        supplier_id="sup_hyperspec",
        supplier_name="SpectraSpace",
        name="HyperEye-VNIR",
        payload_type=PayloadType.SPECTROMETER,
        mass_kg=18.0,
        operational_power_w=45.0,
        peak_power_w=65.0,
        volume_liters=14.0,
        thermal_dissipation_w=35.0,
        raw_data_rate_mbps=850.0,
        compressed_data_rate_mbps=300.0,
        price_meur=2.4,
        aperture_diameter_m=0.15,
        focal_length_m=0.90,
        pixel_pitch_um=7.0,
        detector_spatial_pixels=2048,
        spectral_range_min_nm=400.0,
        spectral_range_max_nm=1000.0,
        number_of_spectral_bands=120,
        spectral_resolution_nm=5.0,
    )

    perf = SpectrometerModel.compute(spectro, orbit)
    # GSD = 7 um * 500 km / 0.9 m = 3.89 m
    assert 3.5 < perf.gsd_spatial_nadir_m < 4.2
    # Spectral sampling = 600 nm / 120 bands = 5.0 nm
    assert perf.spectral_sampling_nm == 5.0
    assert perf.spectral_bands_count == 120
    assert perf.mean_snr_estimate > 50.0  # Quality SNR > 50 in daylight


def test_qkd_model():
    qkd_perf = QkdModel.compute(
        telescope_aperture_m=0.20,
        source_rate_mhz=100.0,
        wavelength_nm=850.0,
        ground_telescope_aperture_m=1.0,
        slant_range_km=600.0,
        pointing_jitter_urad=1.5,
        pass_duration_seconds=300.0,
    )

    # Free-space satellite QKD link verification:
    # QBER must be below threshold 11% for secret key generation
    assert qkd_perf.quantum_bit_error_rate_pct < 6.0
    # Secret Key Rate > 1 kbps
    assert qkd_perf.asymptotic_secret_key_rate_bps > 1000.0
    # Secret bits per 5-min pass > 300,000 bits
    assert qkd_perf.secret_bits_per_pass > 300_000.0


def test_teacher_replay_and_integrity_tampering(tmp_path: Path):
    db = CatalogDatabase()
    db.load_from_directory("data/catalogs")
    evaluator = SystemEvaluator(db)

    orbit = OrbitDefinition(altitude_km=500.0)
    mission = MissionSpecification(
        id="M-EXAM-TEACHER",
        title="Exam Subject",
        context="",
        mission_type="optical_eo",
        max_budget_meur=20.0,
        requirements=[
            MissionRequirement(
                id="REQ-GSD",
                title="GSD <= 1.0 m",
                description="",
                req_type=RequirementType.PAYLOAD_PERF,
                parameter="gsd_nadir_m",
                operator=RequirementOperator.LE,
                threshold=1.0,
            )
        ],
    )

    config = SystemConfiguration(
        orbit=orbit,
        platform_id="plat_astra_flex150",
        selected_options=[
            SelectedOption(slot_function="payload_downlink", equipment_id="downlink_xband_tx"),
            SelectedOption(slot_function="adcs", equipment_id="adcs_high_accuracy_pack"),
        ],
        selected_payload_ids=["pl_opt_submeter_highres"],
        launcher_id="ln_rideshare_sso",
    )

    project = StudentProject(
        project_id="PROJ_TEST_100",
        student_name="Alice Martin",
        student_id="ETU-007",
        mission=mission,
        configuration=config,
    )
    project.update_integrity()

    # 1. Integrity check passes on original project
    assert project.verify_integrity()

    # 2. Replay evaluation yields matching results
    budgets = evaluator.evaluate(project.configuration, project.mission)
    assert not budgets.has_blocking_errors

    # 3. Simulate unauthorized student file modification (cheating / alteration)
    project.configuration.selected_payload_ids = ["pl_opt_pan_compact"]
    # Without calling update_integrity(), verification must detect tampering:
    assert not project.verify_integrity()
