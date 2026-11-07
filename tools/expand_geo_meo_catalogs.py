"""Add GEO and MEO platforms, launchers, and payloads to the catalogs."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ssb.catalog.database import CatalogDatabase  # noqa: E402
from ssb.catalog.datasheet import build_datasheet  # noqa: E402
from ssb.core.orbit import OrbitDefinition  # noqa: E402

CATALOGS_DIR = ROOT / "data" / "catalogs"


NEW_LAUNCHERS: list[dict] = [
    {
        "id": "ln_gto_rideshare",
        "supplier_id": "launch_global",
        "supplier_name": "Aether Launch Services",
        "name": "OrbitalShare GTO (Commercial Co-passenger)",
        "launcher_type": "rideshare",
        "price_base_meur": 2.2,
        "price_per_kg_meur": 0.014,
        "max_total_mass_kg": 2500.0,
        "lead_time_months": 15,
        "trl": 9,
        "flight_heritage": ">35 vols vers GTO",
        "image": "launcher_rideshare.jpg",
        "fairing_volume_m3": 25.0,
        "description": "Lancement partagé vers l'orbite de transfert géostationnaire (GTO/GEO) ou MEO pour satellites commerciaux",
        "long_description": (
            "Service régulier de lancement en covoiturage vers l'orbite de transfert géostationnaire (GTO) sur lanceur lourd "
            "commercial. Permet d'injecter des satellites de classe 500 à 2500 kg (SmallGEO, constellations MEO) avec un coût "
            "fixe réduit (2,2 M€) et un coût au kilogramme de 14 k€/kg. Le satellite circularise ensuite son orbite à l'apogée "
            "par sa propre propulsion chimique ou électrique."
        ),
        "key_features": [
            "Accès direct GTO / MEO en passager partagé",
            "Capacité jusqu'à 2 500 kg en GTO",
            "Coiffe grand volume (diamètre 3,8 m)",
            "Coût très attractif pour satellites GEO/MEO",
        ],
        "interfaces": [
            "Adaptateur standard 1194 mm ou 1666 mm",
            "Enveloppe mécanique 3,8 x 4,5 m",
        ],
        "capacities": [
            {
                "orbit_type": "gto",
                "max_payload_mass_kg": 2500.0,
                "fairing_diameter_m": 3.8,
                "fairing_height_m": 4.5,
            },
            {
                "orbit_type": "geo",
                "max_payload_mass_kg": 1400.0,
                "fairing_diameter_m": 3.8,
                "fairing_height_m": 4.5,
            },
            {
                "orbit_type": "meo",
                "max_payload_mass_kg": 1800.0,
                "fairing_diameter_m": 3.8,
                "fairing_height_m": 4.5,
            },
            {
                "orbit_type": "sso_500km",
                "max_payload_mass_kg": 2500.0,
                "fairing_diameter_m": 3.8,
                "fairing_height_m": 4.5,
            },
        ],
    },
]


NEW_PLATFORMS: list[dict] = [
    {
        "id": "plat_smallgeo_500",
        "supplier_id": "heritage_prime",
        "supplier_name": "AeroPrime Defense & Space",
        "name": "SmallGEO-Express Bus",
        "category": "geo_smallgeo",
        "description": "Plateforme géostationnaire compacte (580 kg sec, 15 ans) pour télécommunications régionales",
        "dry_mass_kg": 580.0,
        "max_payload_mass_kg": 280.0,
        "max_launch_mass_kg": 1600.0,
        "payload_volume_liters": 220.0,
        "orbit_avg_power_w": 3800.0,
        "payload_avg_power_w": 2100.0,
        "payload_peak_power_w": 3400.0,
        "bus_voltage_v": 50.0,
        "battery_capacity_wh": 5200.0,
        "battery_max_dod": 0.75,
        "pointing_accuracy_deg": 0.03,
        "pointing_stability_arcsec_s": 2.5,
        "slew_rate_deg_s": 1.0,
        "jitter_arcsec": 1.2,
        "payload_thermal_dissipation_w": 1400.0,
        "launch_environment_compatible": ["gto_rideshare", "ariane_fairing", "falcon_fairing"],
        "design_lifetime_years": 15.0,
        "rad_tolerance_krad": 100.0,
        "base_price_meur": 18.5,
        "base_lead_time_months": 24,
        "trl": 9,
        "image": "platform_large.jpg",
        "dimensions_mm": [2200, 1600, 1500],
        "deployed_span_m": 12.0,
        "long_description": (
            "Plateforme géostationnaire compacte (classe SmallGEO) conçue pour les missions de télécommunications "
            "commerciales régionales et les liaisons gouvernementales sécurisées. Elle intègre des générateurs solaires "
            "déployables de 3,8 kW, une avionique durcie aux ceintures de radiations (100 krad) et une durée de vie garantie "
            "de 15 ans en orbite géostationnaire. Compatible avec les lancements en passager partagé GTO."
        ),
        "key_features": [
            "Conçue spécifiquement pour l'orbite GEO (15 ans, 100 krad)",
            "Puissance utile charge utile : 2 100 W continus",
            "Capacité charge utile 280 kg / 220 L",
            "Maintien à poste N-S / E-W haute précision",
        ],
        "interfaces": [
            "Bus régulé 50 V",
            "SpaceWire / MIL-STD-1553B / SpaceFibre",
            "Fixation lanceur adaptateur 1194 mm",
        ],
        "slots": [
            {
                "function": "propulsion",
                "allowed_equipment_ids": [
                    "prop_biprop_400n",
                    "prop_electric_hall_1kw",
                    "prop_green_5n",
                ],
                "included_equipment_ids": ["prop_electric_hall_1kw"],
                "min_qty": 1,
                "max_qty": 1,
                "integration_cost_fixed_meur": 0.25,
                "integration_cost_pct": 5.0,
                "interface_mass_kg": 4.5,
            },
            {
                "function": "ttc",
                "allowed_equipment_ids": ["ttc_sband_transceiver"],
                "included_equipment_ids": ["ttc_sband_transceiver"],
                "min_qty": 1,
                "max_qty": 1,
                "integration_cost_fixed_meur": 0.0,
                "integration_cost_pct": 0.0,
                "interface_mass_kg": 0.0,
            },
            {
                "function": "mass_memory",
                "allowed_equipment_ids": ["mass_mem_512gb", "mass_mem_1tb", "mass_mem_2tb_highrel"],
                "included_equipment_ids": ["mass_mem_512gb"],
                "min_qty": 1,
                "max_qty": 1,
                "integration_cost_fixed_meur": 0.05,
                "integration_cost_pct": 2.0,
                "interface_mass_kg": 0.5,
            },
            {
                "function": "adcs",
                "allowed_equipment_ids": ["adcs_high_accuracy_pack", "adcs_agile_wheels_medium"],
                "included_equipment_ids": ["adcs_high_accuracy_pack"],
                "min_qty": 1,
                "max_qty": 1,
                "integration_cost_fixed_meur": 0.0,
                "integration_cost_pct": 0.0,
                "interface_mass_kg": 0.0,
            },
        ],
    },
    {
        "id": "plat_europrime_geo3000",
        "supplier_id": "heritage_prime",
        "supplier_name": "AeroPrime Defense & Space",
        "name": "PrimeBus-GEO Heavy Telecom",
        "category": "geo_heavy",
        "description": "Plateforme géostationnaire lourde multi-faisceaux (1850 kg sec, 15 ans, 6,8 kW utile)",
        "dry_mass_kg": 1850.0,
        "max_payload_mass_kg": 750.0,
        "max_launch_mass_kg": 4500.0,
        "payload_volume_liters": 580.0,
        "orbit_avg_power_w": 12500.0,
        "payload_avg_power_w": 6800.0,
        "payload_peak_power_w": 11000.0,
        "bus_voltage_v": 100.0,
        "battery_capacity_wh": 16000.0,
        "battery_max_dod": 0.8,
        "pointing_accuracy_deg": 0.02,
        "pointing_stability_arcsec_s": 2.0,
        "slew_rate_deg_s": 0.8,
        "jitter_arcsec": 1.0,
        "payload_thermal_dissipation_w": 4500.0,
        "launch_environment_compatible": ["ariane_heavy", "falcon_heavy", "gto_dedicated"],
        "design_lifetime_years": 15.0,
        "rad_tolerance_krad": 100.0,
        "base_price_meur": 32.0,
        "base_lead_time_months": 30,
        "trl": 9,
        "image": "platform_large.jpg",
        "dimensions_mm": [3800, 2600, 2400],
        "deployed_span_m": 28.0,
        "long_description": (
            "Grand bus de télécommunications géostationnaires lourd (inspiré de Spacebus Neo et Eurostar Neo). "
            "Il héberge jusqu'à 750 kg de répéteurs Ku/Ka ou optiques de forte puissance (6,8 kW utiles) avec une "
            "durée de vie opérationnelle de 15 ans et une redondance complète sur tous les sous-systèmes."
        ),
        "key_features": [
            "Puissance charge utile massive : 6 800 W en permanence",
            "Capacité d'emport 750 kg / 580 L",
            "Maintien à poste électrique ou bi-liquide",
            "TRL 9 avec dizaines de missions en vol",
        ],
        "interfaces": [
            "Bus haute tension 100 V régulé",
            "SpaceFibre / SpaceWire redondés",
            "Adaptateur 1666 mm",
        ],
        "slots": [
            {
                "function": "propulsion",
                "allowed_equipment_ids": ["prop_electric_hall_1kw", "prop_biprop_400n"],
                "included_equipment_ids": ["prop_electric_hall_1kw"],
                "min_qty": 1,
                "max_qty": 1,
                "integration_cost_fixed_meur": 0.4,
                "integration_cost_pct": 5.0,
                "interface_mass_kg": 6.0,
            },
            {
                "function": "ttc",
                "allowed_equipment_ids": ["ttc_sband_transceiver"],
                "included_equipment_ids": ["ttc_sband_transceiver"],
                "min_qty": 1,
                "max_qty": 1,
                "integration_cost_fixed_meur": 0.0,
                "integration_cost_pct": 0.0,
                "interface_mass_kg": 0.0,
            },
            {
                "function": "mass_memory",
                "allowed_equipment_ids": ["mass_mem_1tb", "mass_mem_2tb_highrel"],
                "included_equipment_ids": ["mass_mem_2tb_highrel"],
                "min_qty": 1,
                "max_qty": 1,
                "integration_cost_fixed_meur": 0.05,
                "integration_cost_pct": 2.0,
                "interface_mass_kg": 0.5,
            },
            {
                "function": "adcs",
                "allowed_equipment_ids": ["adcs_high_accuracy_pack", "adcs_cmg_agility_pack"],
                "included_equipment_ids": ["adcs_high_accuracy_pack"],
                "min_qty": 1,
                "max_qty": 1,
                "integration_cost_fixed_meur": 0.0,
                "integration_cost_pct": 0.0,
                "interface_mass_kg": 0.0,
            },
        ],
    },
    {
        "id": "plat_meo_constellation_700",
        "supplier_id": "heritage_aero",
        "supplier_name": "Astra Space Systems",
        "name": "AstraMEO-700 Constellation Bus",
        "category": "meo_constellation",
        "description": "Plateforme MEO durcie aux radiations (390 kg sec, 12 ans, 100 krad) pour constellations de connectivité",
        "dry_mass_kg": 390.0,
        "max_payload_mass_kg": 220.0,
        "max_launch_mass_kg": 920.0,
        "payload_volume_liters": 150.0,
        "orbit_avg_power_w": 2800.0,
        "payload_avg_power_w": 1300.0,
        "payload_peak_power_w": 2200.0,
        "bus_voltage_v": 50.0,
        "battery_capacity_wh": 3400.0,
        "battery_max_dod": 0.65,
        "pointing_accuracy_deg": 0.025,
        "pointing_stability_arcsec_s": 2.5,
        "slew_rate_deg_s": 1.5,
        "jitter_arcsec": 1.2,
        "payload_thermal_dissipation_w": 850.0,
        "launch_environment_compatible": ["gto_rideshare", "falcon_fairing", "ariane_fairing"],
        "design_lifetime_years": 12.0,
        "rad_tolerance_krad": 100.0,
        "base_price_meur": 12.8,
        "base_lead_time_months": 18,
        "trl": 9,
        "image": "platform_medium.jpg",
        "dimensions_mm": [2000, 1400, 1300],
        "deployed_span_m": 8.5,
        "long_description": (
            "Plateforme MEO durcie aux flux intenses de protons et d'électrons des ceintures de Van Allen (8 000 à 23 000 km "
            "d'altitude). Elle convient aux satellites de navigation (type Galileo) et aux constellations de données très bas "
            "temps de latence (type O3b mPOWER)."
        ),
        "key_features": [
            "Blindage radiatif renforcé (100 krad)",
            "Orbite MEO 8 000 à 23 200 km",
            "1 300 W utiles charge utile",
            "Durée de vie garantie 12 ans",
        ],
        "interfaces": [
            "Bus régulé 50 V",
            "SpaceWire / MIL-STD-1553B",
            "Adaptateur 1194 mm",
        ],
        "slots": [
            {
                "function": "propulsion",
                "allowed_equipment_ids": ["prop_electric_hall_1kw", "prop_green_5n"],
                "included_equipment_ids": ["prop_electric_hall_1kw"],
                "min_qty": 1,
                "max_qty": 1,
                "integration_cost_fixed_meur": 0.15,
                "integration_cost_pct": 4.0,
                "interface_mass_kg": 3.0,
            },
            {
                "function": "ttc",
                "allowed_equipment_ids": ["ttc_sband_transceiver"],
                "included_equipment_ids": ["ttc_sband_transceiver"],
                "min_qty": 1,
                "max_qty": 1,
                "integration_cost_fixed_meur": 0.0,
                "integration_cost_pct": 0.0,
                "interface_mass_kg": 0.0,
            },
            {
                "function": "mass_memory",
                "allowed_equipment_ids": ["mass_mem_512gb", "mass_mem_1tb"],
                "included_equipment_ids": ["mass_mem_512gb"],
                "min_qty": 1,
                "max_qty": 1,
                "integration_cost_fixed_meur": 0.04,
                "integration_cost_pct": 2.0,
                "interface_mass_kg": 0.4,
            },
            {
                "function": "adcs",
                "allowed_equipment_ids": ["adcs_high_accuracy_pack"],
                "included_equipment_ids": ["adcs_high_accuracy_pack"],
                "min_qty": 1,
                "max_qty": 1,
                "integration_cost_fixed_meur": 0.0,
                "integration_cost_pct": 0.0,
                "interface_mass_kg": 0.0,
            },
        ],
    },
]


NEW_PAYLOADS: list[dict] = [
    {
        "id": "pl_rf_geo_transponder_c_ku",
        "supplier_id": "rf_payload",
        "supplier_name": "Meridian RF Payloads",
        "name": "GeoSat-Ku24 Classical GEO Telecom Transponder Suite",
        "payload_type": "radio_comm",
        "description": "Charge utile géostationnaire classique (24 répéteurs Ku 36 MHz, 1800 W RF, antenne 2,4 m) pour diffusion TV et données",
        "mass_kg": 175.0,
        "operational_power_w": 1400.0,
        "peak_power_w": 2100.0,
        "standby_power_w": 120.0,
        "volume_liters": 160.0,
        "dimensions_mm": [1800, 1200, 850],
        "required_pointing_accuracy_deg": 0.05,
        "required_pointing_stability_arcsec_s": 5.0,
        "max_tolerated_jitter_arcsec": 2.5,
        "thermal_dissipation_w": 850.0,
        "raw_data_rate_mbps": 1800.0,
        "compressed_data_rate_mbps": 1800.0,
        "price_meur": 15.5,
        "trl": 9,
        "flight_heritage": ">30 satellites GEO en service (Eutelsat / SES / Astra)",
        "image": "payload_radio.jpg",
        "long_description": (
            "Suite de 24 transpondeurs en bande Ku (montée 14,0–14,5 GHz, descente 11,7–12,2 GHz) à amplificateurs à tubes "
            "(TWTA) de 120 W RF et réflecteur déployable de 2,4 m à double grille. Assure la diffusion de chaînes de télévision, "
            "de liaisons VSAT et de dorsales Internet régionales avec une disponibilité de 99,99 % et un débit total de 1,8 Gbit/s."
        ),
        "key_features": [
            "24 transpondeurs Ku 36 MHz (1 800 Mbit/s agrégés)",
            "Antenne réflecteur 2,4 m déployable, gain 38,5 dBi",
            "Marge de liaison > 4 dB à 38 000 km vers antennes 1,8 m",
            "Conçu pour 15 ans d'exploitation continue en GEO",
        ],
        "interfaces": [
            "Alimentation bus 50/100 V",
            "SpaceWire / MIL-STD-1553B",
            "Guides d'onde WR75",
        ],
        "uplink_frequency_ghz": 14.25,
        "downlink_frequency_ghz": 11.95,
        "rf_output_power_w": 120.0,
        "antenna_gain_tx_dbi": 38.5,
        "antenna_gain_rx_dbi": 36.0,
        "bandwidth_mhz": 864.0,
        "max_data_rate_mbps": 1800.0,
    },
    {
        "id": "pl_rf_smallgeo_ku_relay",
        "supplier_id": "helvetia_microwave",
        "supplier_name": "Helvetia Microwave & RF",
        "name": "SmallGEO-Ku8 Regional Telecom Payload",
        "payload_type": "radio_comm",
        "description": "Charge utile géostationnaire compacte (8 répéteurs Ku 72 MHz, 650 W RF, antenne 1,8 m) pour plateformes SmallGEO",
        "mass_kg": 82.0,
        "operational_power_w": 680.0,
        "peak_power_w": 980.0,
        "standby_power_w": 60.0,
        "volume_liters": 75.0,
        "dimensions_mm": [1300, 900, 600],
        "required_pointing_accuracy_deg": 0.05,
        "required_pointing_stability_arcsec_s": 5.0,
        "max_tolerated_jitter_arcsec": 2.5,
        "thermal_dissipation_w": 420.0,
        "raw_data_rate_mbps": 750.0,
        "compressed_data_rate_mbps": 750.0,
        "price_meur": 8.2,
        "trl": 9,
        "flight_heritage": "Héritage Hispasat 36W-1 (SmallGEO)",
        "image": "payload_radio.jpg",
        "long_description": (
            "Charge utile géostationnaire allégée développée par Helvetia Microwave & RF pour les plateformes de classe "
            "SmallGEO (500 à 1 500 kg). Avec ses 8 transpondeurs large bande (72 MHz) et son antenne de 1,8 m (36 dBi), elle "
            "assure une capacité de 750 Mbit/s avec une marge de liaison supérieure à 4,5 dB à 38 000 km pour un budget "
            "divisé par deux par rapport aux grands satellites GEO."
        ),
        "key_features": [
            "8 canaux Ku 72 MHz (débit 750 Mbit/s)",
            "Masse contenue : 82 kg, puissance 680 W",
            "Antenne 1,8 m en fibre de carbone, gain 36 dBi",
            "Idéal pour sujet télécom GEO sous budget contraint",
        ],
        "interfaces": [
            "Alimentation 50 V régulé",
            "SpaceWire / CAN",
            "Guides d'onde WR75",
        ],
        "uplink_frequency_ghz": 14.15,
        "downlink_frequency_ghz": 12.10,
        "rf_output_power_w": 60.0,
        "antenna_gain_tx_dbi": 36.0,
        "antenna_gain_rx_dbi": 34.0,
        "bandwidth_mhz": 576.0,
        "max_data_rate_mbps": 750.0,
    },
    {
        "id": "pl_rf_geo_vhts_ka",
        "supplier_id": "gallia_satcom",
        "supplier_name": "Gallia SatCom Payloads",
        "name": "GeoBeam-Ka50 VHTS High-Throughput GEO Payload",
        "payload_type": "radio_comm",
        "description": "Charge utile GEO Très Haut Débit bande Ka (50 spots étroits, antenne 2,8 m, 25 Gbit/s) pour large bande continentale",
        "mass_kg": 260.0,
        "operational_power_w": 2900.0,
        "peak_power_w": 4200.0,
        "standby_power_w": 200.0,
        "volume_liters": 280.0,
        "dimensions_mm": [2100, 1500, 1100],
        "required_pointing_accuracy_deg": 0.03,
        "required_pointing_stability_arcsec_s": 3.0,
        "max_tolerated_jitter_arcsec": 1.5,
        "thermal_dissipation_w": 1800.0,
        "raw_data_rate_mbps": 25000.0,
        "compressed_data_rate_mbps": 25000.0,
        "price_meur": 22.0,
        "trl": 9,
        "flight_heritage": "Héritage Konnect VHTS / Eutelsat",
        "image": "payload_radio.jpg",
        "long_description": (
            "Charge utile géostationnaire à très grand débit (VHTS) de Gallia SatCom Payloads. Elle exploite la bande Ka "
            "(29,5 GHz montée / 19,7 GHz descente) et forme 50 faisceaux étroits réutilisant les fréquences pour totaliser "
            "25 Gbit/s de bande passante utile. S'intègre sur les grands bus de 3 à 4 tonnes."
        ),
        "key_features": [
            "25 Gbit/s de débit utile en bande Ka",
            "50 faisceaux spots, antenne 2,8 m (45 dBi)",
            "Amplificateurs GaN 250 W",
            "Durée de vie 15 ans",
        ],
        "interfaces": [
            "Bus 100 V haute tension",
            "SpaceFibre 4 voies",
            "Radiateur cryogénique/caloducs",
        ],
        "uplink_frequency_ghz": 29.5,
        "downlink_frequency_ghz": 19.7,
        "rf_output_power_w": 250.0,
        "antenna_gain_tx_dbi": 45.0,
        "antenna_gain_rx_dbi": 43.0,
        "bandwidth_mhz": 2500.0,
        "max_data_rate_mbps": 25000.0,
    },
]


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    launchers_path = CATALOGS_DIR / "launchers.json"
    platforms_path = CATALOGS_DIR / "platforms.json"
    payloads_path = CATALOGS_DIR / "payloads.json"

    launchers: list[dict] = json.loads(launchers_path.read_text(encoding="utf-8"))
    platforms: list[dict] = json.loads(platforms_path.read_text(encoding="utf-8"))
    payloads: list[dict] = json.loads(payloads_path.read_text(encoding="utf-8"))

    # Update existing heavy launcher with GTO, GEO and MEO capacities
    for ln in launchers:
        if ln["id"] == "ln_heavy_institutional":
            caps = {c["orbit_type"]: c for c in ln["capacities"]}
            if "gto" not in caps:
                ln["capacities"].append({
                    "orbit_type": "gto",
                    "max_payload_mass_kg": 7200.0,
                    "fairing_diameter_m": 4.5,
                    "fairing_height_m": 8.0,
                })
            if "geo" not in caps:
                ln["capacities"].append({
                    "orbit_type": "geo",
                    "max_payload_mass_kg": 3500.0,
                    "fairing_diameter_m": 4.5,
                    "fairing_height_m": 8.0,
                })
            if "meo" not in caps:
                ln["capacities"].append({
                    "orbit_type": "meo",
                    "max_payload_mass_kg": 5200.0,
                    "fairing_diameter_m": 4.5,
                    "fairing_height_m": 8.0,
                })
        elif ln["id"] == "ln_dedicated_medium":
            caps = {c["orbit_type"]: c for c in ln["capacities"]}
            if "gto" not in caps:
                ln["capacities"].append({
                    "orbit_type": "gto",
                    "max_payload_mass_kg": 600.0,
                    "fairing_diameter_m": 2.6,
                    "fairing_height_m": 4.5,
                })
            if "meo" not in caps:
                ln["capacities"].append({
                    "orbit_type": "meo",
                    "max_payload_mass_kg": 750.0,
                    "fairing_diameter_m": 2.6,
                    "fairing_height_m": 4.5,
                })

    ln_by_id = {l["id"]: l for l in launchers}
    for nl in NEW_LAUNCHERS:
        ln_by_id[nl["id"]] = nl
    launchers_path.write_text(json.dumps(list(ln_by_id.values()), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    plat_by_id = {p["id"]: p for p in platforms}
    for np in NEW_PLATFORMS:
        plat_by_id[np["id"]] = np
    platforms_path.write_text(json.dumps(list(plat_by_id.values()), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    pl_by_id = {p["id"]: p for p in payloads}
    for np in NEW_PAYLOADS:
        pl_by_id[np["id"]] = np
    payloads_path.write_text(json.dumps(list(pl_by_id.values()), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # Validate catalog load
    db = CatalogDatabase()
    db.load_from_directory(CATALOGS_DIR)
    orbit_geo = OrbitDefinition(altitude_km=35786.0, inclination_deg=0.0)
    for p in db.platforms.values():
        ds = build_datasheet(p, orbit_geo)
        assert ds.sections
    for p in db.payloads.values():
        ds = build_datasheet(p, orbit_geo)
        assert ds.sections

    print(f"Catalog expanded: {len(db.launchers)} launchers, {len(db.platforms)} platforms, {len(db.payloads)} payloads.")


if __name__ == "__main__":
    main()
