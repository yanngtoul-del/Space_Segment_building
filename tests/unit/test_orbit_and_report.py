"""Test orbit propagation, ground station access, and report generation."""

from pathlib import Path
from ssb.core.orbit import OrbitDefinition, OrbitType
from ssb.core.mission import (
    MissionSpecification,
    MissionRequirement,
    RequirementType,
    RequirementOperator,
    GroundStationTarget,
)
from ssb.core.project import StudentProject, SystemConfiguration, SelectedOption
from ssb.catalog.database import CatalogDatabase
from ssb.orbit.propagator import OrbitPropagator
from ssb.orbit.station_access import StationAccessCalculator
from ssb.system.evaluator import SystemEvaluator
from ssb.report.generator import ReportGenerator


def test_orbit_propagator_j2_and_eclipses():
    orbit = OrbitDefinition(
        orbit_type=OrbitType.SSO,
        altitude_km=500.0,
        eccentricity=0.0,
        inclination_deg=97.4,
    )
    # Simulate 1 orbit
    summary = OrbitPropagator.simulate(orbit, duration_orbits=1.0, samples_per_orbit=60)

    assert 90.0 < summary.orbit_period_minutes < 100.0
    assert len(summary.ground_track) == 60
    # On 500 km SSO, eclipse duration is typically ~30-36 minutes
    assert 25.0 < summary.eclipse_duration_avg_minutes < 40.0
    assert 25.0 < summary.eclipse_fraction_pct < 45.0


def test_station_access_passes():
    orbit = OrbitDefinition(
        orbit_type=OrbitType.SSO,
        altitude_km=500.0,
        inclination_deg=97.4,
    )
    # Simulate 2 orbits
    summary = OrbitPropagator.simulate(orbit, duration_orbits=2.0, samples_per_orbit=120)

    # Polar station Svalbard: high latitude, frequent passes
    svalbard = GroundStationTarget(
        id="sta_svalbard",
        name="Svalbard Satellite Station",
        latitude_deg=78.22,
        longitude_deg=15.40,
        min_elevation_deg=5.0,
    )

    passes = StationAccessCalculator.find_passes(summary.ground_track, svalbard)
    assert len(passes) >= 1
    assert passes[0].duration_seconds > 60.0
    assert passes[0].max_elevation_deg >= 5.0


def test_full_report_generation(tmp_path: Path):
    db = CatalogDatabase()
    db.load_from_directory("data/catalogs")
    evaluator = SystemEvaluator(db)

    orbit = OrbitDefinition(altitude_km=500.0, inclination_deg=97.4)
    mission = MissionSpecification(
        id="EXAM-2026-EO",
        title="Mission EarthScan Tactical",
        context="Surveillance optique haute résolution sur théâtres d'opérations",
        mission_type="optical_eo",
        max_budget_meur=20.0,
        target_lifetime_years=5.0,
        requirements=[
            MissionRequirement(
                id="REQ-GSD-01",
                title="Résolution au sol GSD",
                description="GSD nadir <= 1.0 m",
                req_type=RequirementType.PAYLOAD_PERF,
                parameter="gsd_nadir_m",
                operator=RequirementOperator.LE,
                threshold=1.0,
                unit="m",
            )
        ],
    )

    config = SystemConfiguration(
        orbit=orbit,
        platform_id="plat_astra_flex150",
        selected_options=[
            SelectedOption(slot_function="propulsion", equipment_id="prop_electric_hall_100w"),
            SelectedOption(slot_function="payload_downlink", equipment_id="downlink_xband_tx"),
            SelectedOption(slot_function="adcs", equipment_id="adcs_high_accuracy_pack"),
        ],
        selected_payload_ids=["pl_opt_submeter_highres"],
        launcher_id="ln_rideshare_sso",
    )

    project = StudentProject(
        project_id="PROJ_STUDENT_001",
        student_name="Camille Dupont",
        student_id="ETU-2026-8841",
        mission=mission,
        configuration=config,
        conops_text="Le satellite opère en mode acquisition au-dessus des latitudes tempérées avec un duty cycle de 15%...",
    )
    project.update_integrity()
    assert project.verify_integrity()

    budgets = evaluator.evaluate(config, mission)
    sim = OrbitPropagator.simulate(orbit, duration_orbits=2.0, samples_per_orbit=60)

    out_docx = tmp_path / "Rapport_Examen_PROJ_STUDENT_001.docx"
    generated_path = ReportGenerator.generate(
        project=project,
        budgets=budgets,
        output_docx_path=out_docx,
        ground_track=sim.ground_track,
    )

    assert generated_path.exists()
    assert generated_path.stat().st_size > 10_000  # Should be a valid non-empty docx (>10 KB)
