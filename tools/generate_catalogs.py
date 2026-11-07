"""Expand the supplier and payload catalogs so every payload category (especially SAR, RF Telecom, Optical Telecom, Spectrometer, QKD, Optical Imager) has 4 to 6 distinct suppliers with rich NewSpace vs Heritage trade-offs and complete datasheets."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ssb.catalog.database import CatalogDatabase  # noqa: E402
from ssb.catalog.datasheet import build_datasheet  # noqa: E402
from ssb.core.orbit import OrbitDefinition  # noqa: E402

CATALOGS_DIR = ROOT / "data" / "catalogs"


NEW_SUPPLIERS: list[dict] = [
    # --- SAR new suppliers (bringing SAR to 5 suppliers) ---
    {
        "id": "euro_sar_prime",
        "name": "Aegis Radar & Defense",
        "country": "Allemagne / Espagne (fictif)",
        "kind": "historique",
        "categories": ["payload"],
        "founded": 1979,
        "description": (
            "Maître d'œuvre européen des radars spatiaux militaires et civils à synthèse d'ouverture (bandes X et C). "
            "Spécialiste des antennes actives à modules T/R GaN haute fiabilité, de la polarimétrie complète (Quad-Pol) "
            "et des modes Spotlight sub-métriques. Inspiré d'Airbus Defence & Space (TerraSAR-X / PAZ) et d'Indra."
        ),
    },
    {
        "id": "zephyr_microsar",
        "name": "Zephyr MicroRadar Inc.",
        "country": "États-Unis / Japon (fictif)",
        "kind": "newspace",
        "categories": ["payload"],
        "founded": 2017,
        "description": (
            "Pionnier NewSpace des radars SAR à réflecteur parabolique maillé déployable (mesh reflector) ultra-légers. "
            "En remplaçant le lourd panneau phasé actif par une parabole déployable à grand gain illuminée par une source "
            "centrale à semi-conducteurs GaN, Zephyr obtient un excellent NESZ (< -16 dB) avec une masse et une consommation "
            "divisées par deux. Inspiré de Capella Space, d'Umbra et d'iQPS."
        ),
    },
    {
        "id": "med_radar_ital",
        "name": "Alba Spazio Radar",
        "country": "Italie (fictif)",
        "kind": "historique",
        "categories": ["payload"],
        "founded": 1984,
        "description": (
            "Industriel transalpin de référence pour l'observation radar duale (civile et défense) en bande X et bande Ku. "
            "Fort de l'héritage d'une constellation opérationnelle méditerranéenne, Alba Spazio propose des instruments SAR "
            "à haute cadence de revisite et interférométrie différentielle. Inspiré de Thales Alenia Space Italia (COSMO-SkyMed)."
        ),
    },
    # --- RF Telecom new suppliers (bringing radio_comm to 5 suppliers) ---
    {
        "id": "nordic_nanocomm",
        "name": "Nordic NanoComm Systems",
        "country": "Danemark / Suède (fictif)",
        "kind": "newspace",
        "categories": ["payload"],
        "founded": 2013,
        "description": (
            "Leader scandinave des charges utiles radio-fréquence définies par logiciel (SDR) pour CubeSats et microsatellites : "
            "surveillance maritime AIS, suivi aéronautique ADS-B, collecte IoT satellitaire et surveillance du spectre RF. "
            "Produits très compacts, faible consommation et livraison rapide. Inspiré de GomSpace, Satlab et Kleos."
        ),
    },
    {
        "id": "gallia_satcom",
        "name": "Gallia SatCom Payloads",
        "country": "France / Royaume-Uni (fictif)",
        "kind": "historique",
        "categories": ["payload"],
        "founded": 1974,
        "description": (
            "Grand équipementier et systémier européen de charges utiles de télécommunications spatiales en bandes X, Ku et Ka. "
            "Conçoit des répéteurs numériques transparents et régénératifs à formation de faisceaux actifs (DRA) pour constellations "
            "LEO/MEO et missions souveraines. Inspiré d'Airbus (OneWeb) et de Thales Alenia Space."
        ),
    },
    {
        "id": "celestia_broadband",
        "name": "Celestia Broadband Corp.",
        "country": "États-Unis / Canada (fictif)",
        "kind": "newspace",
        "categories": ["payload"],
        "founded": 2016,
        "description": (
            "Entreprise NewSpace nord-américaine spécialisée dans la connectivité directe vers les terminaux mobiles (Direct-to-Device), "
            "l'IoT massif en bande L/S et les charges utiles bande Ka à antennes réseaux phasés électroniques à bas coût. "
            "Inspiré de Lynk, AST SpaceMobile et Telesat Lightspeed."
        ),
    },
    {
        "id": "helvetia_microwave",
        "name": "Helvetia Microwave & RF",
        "country": "Suisse (fictif)",
        "kind": "historique",
        "categories": ["payload"],
        "founded": 1996,
        "description": (
            "Spécialiste suisse de l'électronique hyperfréquence de haute précision, des charges utiles de relais inter-satellites "
            "en bande K/Ka et des récepteurs de collecte environnementale (type Argos / DCS) à très faible facteur de bruit. "
            "Inspiré de SWISSto12 et de Beyond Gravity."
        ),
    },
    # --- Optical Telecom new suppliers (bringing optical_comm to 4 suppliers) ---
    {
        "id": "celeste_photonics",
        "name": "Céleste Photonique Spatiale",
        "country": "France (fictif)",
        "kind": "newspace",
        "categories": ["payload"],
        "founded": 2018,
        "description": (
            "Start-up deeptech française issue de la recherche en optique adaptative et télécoms spatiales. Développe des "
            "terminaux laser LEO-sol et inter-satellites de 5 à 40 Gbit/s intégrant une pré-compensation des turbulences "
            "atmosphériques et des composants fibrés qualifiés espace. Inspiré de Cailabs, d'Unseenlabs et d'Airbus Laser."
        ),
    },
    {
        "id": "nippon_optolink",
        "name": "Kibo Optical Communications",
        "country": "Japon (fictif)",
        "kind": "historique",
        "categories": ["payload"],
        "founded": 1988,
        "description": (
            "Pionnier japonais des liaisons optiques spatiales bidirectionnelles (héritage OICETS / LUCAS / JDRS). "
            "Propose des terminaux laser ultra-fiables à acquisition rapide et faible masse pour microsatellites et "
            "relais de données gouvernementaux. Inspiré de NEC, Sony Space Communication et JAXA."
        ),
    },
    # --- Spectrometer new suppliers (bringing spectrometer to 4 suppliers) ---
    {
        "id": "lumina_hyperspec",
        "name": "Lumina Hyperspectral Oy",
        "country": "Finlande / Belgique (fictif)",
        "kind": "newspace",
        "categories": ["payload"],
        "founded": 2016,
        "description": (
            "Concepteur nordique d'imageurs hyperspectraux miniaturisés à interféromètre de Fabry-Pérot et filtres linéaires "
            "variables pour CubeSats et microsatellites. Permet l'analyse environnementale, forestière et agricole à une "
            "fraction du coût des spectromètres institutionnels. Inspiré de Kuva Space, VTT et imec."
        ),
    },
    {
        "id": "atmo_science_eu",
        "name": "AtmoSonde Scientific Instruments",
        "country": "Pays-Bas / France (fictif)",
        "kind": "historique",
        "categories": ["payload"],
        "founded": 1982,
        "description": (
            "Consortium instrumental européen spécialisé dans la chimie de l'atmosphère terrestre et le climat : "
            "spectromètres à réseau immergé UV-VIS-NIR-SWIR à très haute résolution spectrale (< 0,25 nm) pour le suivi "
            "du méthane (CH4), du CO2, du NO2 et de l'ozone. Inspiré de SRON / TNO / Airbus (TROPOMI, Sentinel-5, CO2M)."
        ),
    },
    # --- QKD new suppliers (bringing qkd to 4 suppliers) ---
    {
        "id": "edelweiss_quantum",
        "name": "Edelweiss Quantum Space",
        "country": "Autriche / Suisse (fictif)",
        "kind": "historique",
        "categories": ["payload"],
        "founded": 2004,
        "description": (
            "Laboratoire industriel alpin issu des travaux pionniers sur l'intrication quantique spatiale. "
            "Fournit des charges utiles QKD à états leurres et à paires de photons intriqués pour les infrastructures "
            "européennes de communication quantique (EuroQCI). Inspiré d'IQOQI, d'ID Quantique et du programme ESA Eagle-1."
        ),
    },
    {
        "id": "albion_quantum_optics",
        "name": "Albion Quantum Photonics",
        "country": "Royaume-Uni (fictif)",
        "kind": "newspace",
        "categories": ["payload"],
        "founded": 2019,
        "description": (
            "Entreprise NewSpace britannique développant des émetteurs quantiques à puce photonique intégrée pour CubeSats "
            "et petits satellites commerciaux, abaissant drastiquement la masse et le coût d'accès au chiffrement quantique. "
            "Inspiré de Craft Prospect, d'Arqit et de Toshiba UK."
        ),
    },
]


NEW_PAYLOADS: list[dict] = [
    # =========================================================================
    # SAR — New suppliers: euro_sar_prime, zephyr_microsar, med_radar_ital
    # =========================================================================
    {
        "id": "pl_sar_aegis_x_tactical",
        "supplier_id": "euro_sar_prime",
        "supplier_name": "Aegis Radar & Defense",
        "name": "TerraWatch-X Tactical Stripmap SAR",
        "payload_type": "sar",
        "description": "Radar SAR bande X institutionnel haute fiabilité (3,5 m x 1,0 m, GaN T/R) pour satellites 250–500 kg",
        "mass_kg": 68.0,
        "operational_power_w": 720.0,
        "peak_power_w": 1150.0,
        "standby_power_w": 18.0,
        "volume_liters": 75.0,
        "dimensions_mm": [1250, 720, 210],
        "required_pointing_accuracy_deg": 0.03,
        "required_pointing_stability_arcsec_s": 3.0,
        "max_tolerated_jitter_arcsec": 1.5,
        "thermal_dissipation_w": 340.0,
        "raw_data_rate_mbps": 2800.0,
        "compressed_data_rate_mbps": 750.0,
        "price_meur": 9.4,
        "trl": 9,
        "flight_heritage": "Héritage TerraSAR-X / PAZ (6 vols)",
        "image": "payload_sar.jpg",
        "long_description": (
            "Radar SAR en bande X d'Aegis Radar & Defense combinant 384 modules émission/réception GaN à haut rendement "
            "(6,5 kW crête RF, rapport cyclique 15 %) et une redondance électronique complète (TRL 9). Sa résolution "
            "azimutale de 1,75 m, sa fauchée de 32 km et son excellent NESZ (-16,2 dB à 500 km) lui permettent de "
            "satisfaire pleinement les missions de surveillance maritime et côtière tout-temps."
        ),
        "key_features": [
            "Bande X 9,65 GHz, antenne GaN 3,5 x 1,0 m",
            "Résolution azimutale ~1,75 m, fauchée ~32 km",
            "NESZ ~ -16,2 dB à 500 km (6,5 kW RF crête, NF 2,4 dB)",
            "Redondance complète, TRL 9",
        ],
        "interfaces": [
            "Bus 28/50 V régulé",
            "SpaceFibre redondé",
            "Panneau SAR rigide 2 volets",
        ],
        "frequency_ghz": 9.65,
        "band_name": "X",
        "antenna_length_m": 3.5,
        "antenna_width_m": 1.0,
        "antenna_type": "phased_array",
        "rf_peak_power_w": 6500.0,
        "duty_cycle_max_pct": 15.0,
        "chirp_bandwidth_mhz": 300.0,
        "system_noise_figure_db": 2.4,
        "incidence_angle_min_deg": 20.0,
        "incidence_angle_max_deg": 48.0,
    },
    {
        "id": "pl_sar_aegis_c_wide",
        "supplier_id": "euro_sar_prime",
        "supplier_name": "Aegis Radar & Defense",
        "name": "AegisSAR-C Wide-Swath Ocean Radar",
        "payload_type": "sar",
        "description": "Radar bande C compact (3,8 m x 1,1 m) à double polarisation pour surveillance océanique et glaces",
        "mass_kg": 98.0,
        "operational_power_w": 890.0,
        "peak_power_w": 1450.0,
        "standby_power_w": 20.0,
        "volume_liters": 115.0,
        "dimensions_mm": [1400, 750, 250],
        "required_pointing_accuracy_deg": 0.035,
        "required_pointing_stability_arcsec_s": 3.5,
        "max_tolerated_jitter_arcsec": 1.6,
        "thermal_dissipation_w": 430.0,
        "raw_data_rate_mbps": 2400.0,
        "compressed_data_rate_mbps": 680.0,
        "price_meur": 11.2,
        "trl": 9,
        "flight_heritage": "Héritage Sentinel-1 NextGen",
        "image": "payload_sar.jpg",
        "long_description": (
            "Alternative européenne plus compacte et moins coûteuse que le grand BorealSAR-C canadien : ce radar en bande C "
            "(5,4 GHz) de 98 kg s'intègre sur une plateforme de 300 à 500 kg tout en offrant une fauchée supérieure à 50 km, "
            "une résolution azimutale de 1,9 m et un NESZ de -16,5 dB à 500 km."
        ),
        "key_features": [
            "Bande C 5,4 GHz, antenne 3,8 x 1,1 m",
            "Masse 98 kg (37 kg de moins que BorealSAR-C)",
            "Résolution azimutale 1,9 m, fauchée ~54 km, NESZ < -16 dB",
            "Double polarisation VV+VH",
        ],
        "interfaces": [
            "Bus 50/100 V",
            "SpaceFibre 2 voies",
            "Antenne déployable 3 panneaux",
        ],
        "frequency_ghz": 5.4,
        "band_name": "C",
        "antenna_length_m": 3.8,
        "antenna_width_m": 1.1,
        "antenna_type": "phased_array",
        "rf_peak_power_w": 5500.0,
        "duty_cycle_max_pct": 14.0,
        "chirp_bandwidth_mhz": 200.0,
        "system_noise_figure_db": 2.4,
        "incidence_angle_min_deg": 20.0,
        "incidence_angle_max_deg": 46.0,
    },
    {
        "id": "pl_sar_zephyr_mesh_x",
        "supplier_id": "zephyr_microsar",
        "supplier_name": "Zephyr MicroRadar Inc.",
        "name": "ZephyrMesh-X35 Deployable Reflector SAR",
        "payload_type": "sar",
        "description": "SAR bande X NewSpace à réflecteur maillé déployable (38 kg, 420 W) à très haute sensibilité NESZ",
        "mass_kg": 38.0,
        "operational_power_w": 420.0,
        "peak_power_w": 680.0,
        "standby_power_w": 12.0,
        "volume_liters": 42.0,
        "dimensions_mm": [850, 520, 220],
        "required_pointing_accuracy_deg": 0.04,
        "required_pointing_stability_arcsec_s": 4.0,
        "max_tolerated_jitter_arcsec": 1.8,
        "thermal_dissipation_w": 210.0,
        "raw_data_rate_mbps": 2600.0,
        "compressed_data_rate_mbps": 700.0,
        "price_meur": 5.6,
        "trl": 8,
        "flight_heritage": "14 microsatellites (héritage Capella / Umbra)",
        "image": "payload_sar.jpg",
        "long_description": (
            "Architecture disruptive à réflecteur maillé en molybdène doré déployable en orbite (3,6 m x 1,15 m de surface "
            "collectrice équivalente) illuminé par une source GaN centrale à très faible perte. Grâce à cette grande surface "
            "d'antenne et son rapport cyclique de 18 %, le ZephyrMesh-X35 atteint un NESZ remarquable (~ -16,5 dB à 500 km) "
            "en ne consommant que 420 W et en ne pesant que 38 kg : un choix redoutable sur plateforme de 150 à 300 kg."
        ),
        "key_features": [
            "Réflecteur maillé déployable ultra-léger (38 kg, 3,6 x 1,15 m)",
            "Consommation réduite : 420 W en acquisition",
            "NESZ ~ -16,5 dB à 500 km, résolution azimutale 1,8 m",
            "Excellent rapport performance / prix (5,6 M€)",
        ],
        "interfaces": [
            "Bus 28 V standard",
            "SpaceFibre / LVDS",
            "Couronne de déploiement sans débris",
        ],
        "frequency_ghz": 9.65,
        "band_name": "X",
        "antenna_length_m": 3.6,
        "antenna_width_m": 1.15,
        "antenna_type": "deployable_reflector",
        "rf_peak_power_w": 4500.0,
        "duty_cycle_max_pct": 18.0,
        "chirp_bandwidth_mhz": 250.0,
        "system_noise_figure_db": 2.2,
        "incidence_angle_min_deg": 20.0,
        "incidence_angle_max_deg": 45.0,
    },
    {
        "id": "pl_sar_zephyr_sub25_x",
        "supplier_id": "zephyr_microsar",
        "supplier_name": "Zephyr MicroRadar Inc.",
        "name": "ZephyrDish-X1200 Sub-25cm Spotlight SAR",
        "payload_type": "sar",
        "description": "SAR bande X ultra-large bande (chirp 600 MHz, grand réflecteur 3,8 x 1,2 m) à très bas NESZ",
        "mass_kg": 64.0,
        "operational_power_w": 650.0,
        "peak_power_w": 1050.0,
        "standby_power_w": 15.0,
        "volume_liters": 68.0,
        "dimensions_mm": [1050, 620, 260],
        "required_pointing_accuracy_deg": 0.025,
        "required_pointing_stability_arcsec_s": 2.5,
        "max_tolerated_jitter_arcsec": 1.2,
        "thermal_dissipation_w": 310.0,
        "raw_data_rate_mbps": 4200.0,
        "compressed_data_rate_mbps": 1050.0,
        "price_meur": 8.4,
        "trl": 8,
        "flight_heritage": "6 satellites commerciaux HR",
        "image": "payload_sar.jpg",
        "long_description": (
            "Version haute performance de la gamme Zephyr dotée d'un grand réflecteur déployable de 3,8 m x 1,2 m et d'un "
            "amplificateur GaN de 7,5 kW crête. Il atteint une résolution azimutale de 1,9 m et un NESZ inférieur à -17 dB "
            "à 500 km, tout en restant nettement plus léger (64 kg) qu'un radar à antenne active de classe équivalente."
        ),
        "key_features": [
            "Chirp 600 MHz (résolution distance 0,25 m)",
            "NESZ ~ -17,1 dB à 500 km, fauchée 27 km",
            "Masse 64 kg, puissance 650 W",
            "Pointage agile par la plateforme requis",
        ],
        "interfaces": [
            "Bus 28/50 V",
            "SpaceFibre 2 voies",
            "Mât télescopique + réflecteur maillé",
        ],
        "frequency_ghz": 9.65,
        "band_name": "X",
        "antenna_length_m": 3.8,
        "antenna_width_m": 1.2,
        "antenna_type": "deployable_reflector",
        "rf_peak_power_w": 7500.0,
        "duty_cycle_max_pct": 18.0,
        "chirp_bandwidth_mhz": 600.0,
        "system_noise_figure_db": 2.1,
        "incidence_angle_min_deg": 18.0,
        "incidence_angle_max_deg": 48.0,
    },
    {
        "id": "pl_sar_alba_cosmo_x",
        "supplier_id": "med_radar_ital",
        "supplier_name": "Alba Spazio Radar",
        "name": "CosmoMed-X Dual-Use Surveillance SAR",
        "payload_type": "sar",
        "description": "Radar SAR bande X dual civil/défense à balayage électronique rapide (héritage COSMO-SkyMed)",
        "mass_kg": 82.0,
        "operational_power_w": 920.0,
        "peak_power_w": 1500.0,
        "standby_power_w": 18.0,
        "volume_liters": 90.0,
        "dimensions_mm": [1300, 700, 230],
        "required_pointing_accuracy_deg": 0.03,
        "required_pointing_stability_arcsec_s": 3.0,
        "max_tolerated_jitter_arcsec": 1.4,
        "thermal_dissipation_w": 450.0,
        "raw_data_rate_mbps": 3500.0,
        "compressed_data_rate_mbps": 900.0,
        "price_meur": 10.6,
        "trl": 9,
        "flight_heritage": "Héritage COSMO-SkyMed Second Generation",
        "image": "payload_sar.jpg",
        "long_description": (
            "Instrument radar bande X italien de seconde génération conçu pour la surveillance du bassin méditerranéen et "
            "des zones polaires. Son antenne active de 3,6 m x 1,05 m (8 kW RF crête) permet de commuter instantanément "
            "entre un mode Stripmap haute résolution (1,8 m azimut, fauchée 31 km, NESZ -17,5 dB) et un mode ScanSAR maritime."
        ),
        "key_features": [
            "Bande X 9,6 GHz, antenne active 3,6 x 1,05 m",
            "Agilité électronique de faisceau en élévation et azimut",
            "NESZ ~ -17,5 dB à 500 km",
            "Qualifié missions souveraines 7 ans",
        ],
        "interfaces": [
            "Bus 50 V",
            "SpaceFibre redondé",
            "Banc structurel CFRP thermiquement stable",
        ],
        "frequency_ghz": 9.6,
        "band_name": "X",
        "antenna_length_m": 3.6,
        "antenna_width_m": 1.05,
        "antenna_type": "phased_array",
        "rf_peak_power_w": 8000.0,
        "duty_cycle_max_pct": 16.0,
        "chirp_bandwidth_mhz": 350.0,
        "system_noise_figure_db": 2.3,
        "incidence_angle_min_deg": 20.0,
        "incidence_angle_max_deg": 50.0,
    },

    # =========================================================================
    # RADIO TELECOM — New suppliers: nordic_nanocomm, gallia_satcom, celestia_broadband, helvetia_microwave
    # =========================================================================
    {
        "id": "pl_rf_nordic_ais_sdr",
        "supplier_id": "nordic_nanocomm",
        "supplier_name": "Nordic NanoComm Systems",
        "name": "PolarWatch SDR AIS/VDES + S-Band Downlink",
        "payload_type": "radio_comm",
        "description": "Charge utile SDR ultra-compacte (1,8 kg) de collecte AIS/VDES maritime et descente bande S 20 Mbit/s",
        "mass_kg": 1.8,
        "operational_power_w": 10.0,
        "peak_power_w": 16.0,
        "standby_power_w": 1.0,
        "volume_liters": 1.6,
        "dimensions_mm": [160, 100, 95],
        "required_pointing_accuracy_deg": 0.25,
        "required_pointing_stability_arcsec_s": 25.0,
        "max_tolerated_jitter_arcsec": 12.0,
        "thermal_dissipation_w": 8.0,
        "raw_data_rate_mbps": 20.0,
        "compressed_data_rate_mbps": 20.0,
        "price_meur": 0.38,
        "trl": 9,
        "flight_heritage": ">55 CubeSats en orbite",
        "image": "payload_radio.jpg",
        "long_description": (
            "Charge utile radio logicielle (SDR) scandinave au format 1,5U dédiée au suivi maritime AIS et au nouveau "
            "standard VDES, avec émetteur bande S intégré délivrant 20 Mbit/s. Plus légère (1,8 kg) et plus économique "
            "(0,38 M€) que la suite MarTrack de Meridian RF, elle laisse davantage de marge sur un CubeSat 6U ou 12U."
        ),
        "key_features": [
            "Masse 1,8 kg, volume 1,6 L, prix 0,38 M€",
            "Réception AIS + VDES VHF, descente bande S 20 Mbit/s",
            "Puissance RF 5 W, antenne patch 9 dBi",
            "Reprogrammable en orbite (FPGA Zynq)",
        ],
        "interfaces": [
            "Alimentation 12/28 V",
            "CAN / SpaceWire / CSP",
            "Connecteurs SMA RF",
        ],
        "uplink_frequency_ghz": 0.162,
        "downlink_frequency_ghz": 2.24,
        "rf_output_power_w": 5.0,
        "antenna_gain_tx_dbi": 9.0,
        "antenna_gain_rx_dbi": 6.0,
        "bandwidth_mhz": 30.0,
        "max_data_rate_mbps": 20.0,
    },
    {
        "id": "pl_rf_nordic_xband_cubesat",
        "supplier_id": "nordic_nanocomm",
        "supplier_name": "Nordic NanoComm Systems",
        "name": "NordicLink-X150 CubeSat Relay Payload",
        "payload_type": "radio_comm",
        "description": "Charge utile relais bande S/X compacte (4,8 kg, 150 Mbit/s) pour CubeSats 12U/16U et microsatellites",
        "mass_kg": 4.8,
        "operational_power_w": 26.0,
        "peak_power_w": 40.0,
        "standby_power_w": 2.5,
        "volume_liters": 4.2,
        "dimensions_mm": [210, 140, 120],
        "required_pointing_accuracy_deg": 0.08,
        "required_pointing_stability_arcsec_s": 15.0,
        "max_tolerated_jitter_arcsec": 8.0,
        "thermal_dissipation_w": 20.0,
        "raw_data_rate_mbps": 150.0,
        "compressed_data_rate_mbps": 150.0,
        "price_meur": 0.88,
        "trl": 9,
        "flight_heritage": "16 satellites en vol",
        "image": "payload_radio.jpg",
        "long_description": (
            "Transpondeur numérique compact recevant les flux de stations isolées en bande S et les réémettant à haut débit "
            "(150 Mbit/s) en bande X grâce à une antenne réseau patch à gain de 16 dBi. Idéal pour établir un débit significatif "
            "sur une petite plateforme sans recourir à un équipement lourd."
        ),
        "key_features": [
            "Débit descendant 150 Mbit/s en bande X (8,2 GHz)",
            "Amplificateur GaN 10 W, antenne 16 dBi",
            "Masse 4,8 kg, budget < 0,9 M€",
            "Modulation DVB-S2X adaptative (ACM)",
        ],
        "interfaces": [
            "Alimentation 28 V",
            "SpaceWire / Ethernet Gigabit",
            "Guide d'onde WR112 / SMA",
        ],
        "uplink_frequency_ghz": 2.08,
        "downlink_frequency_ghz": 8.18,
        "rf_output_power_w": 10.0,
        "antenna_gain_tx_dbi": 16.0,
        "antenna_gain_rx_dbi": 10.0,
        "bandwidth_mhz": 110.0,
        "max_data_rate_mbps": 150.0,
    },
    {
        "id": "pl_rf_gallia_x_ku_repeater",
        "supplier_id": "gallia_satcom",
        "supplier_name": "Gallia SatCom Payloads",
        "name": "GalliaWave-Ku600 Regenerative Transponder",
        "payload_type": "radio_comm",
        "description": "Charge utile télécom régénérative en bande Ku (600 Mbit/s, 25 W RF) pour petits satellites",
        "mass_kg": 26.0,
        "operational_power_w": 95.0,
        "peak_power_w": 140.0,
        "standby_power_w": 10.0,
        "volume_liters": 28.0,
        "dimensions_mm": [450, 340, 240],
        "required_pointing_accuracy_deg": 0.03,
        "required_pointing_stability_arcsec_s": 15.0,
        "max_tolerated_jitter_arcsec": 6.0,
        "thermal_dissipation_w": 75.0,
        "raw_data_rate_mbps": 600.0,
        "compressed_data_rate_mbps": 600.0,
        "price_meur": 3.7,
        "trl": 9,
        "flight_heritage": "Constellation LEO européenne (30+ unités)",
        "image": "payload_radio.jpg",
        "long_description": (
            "Charge utile régénérative en bande Ku (montée 14,2 GHz, descente 11,9 GHz) développée par Gallia SatCom Payloads. "
            "Elle démodule et route à bord jusqu'à 600 Mbit/s de trafic IP avec une excellente marge de liaison grâce à son "
            "antenne de 25 dBi et son amplificateur de 25 W."
        ),
        "key_features": [
            "Bande Ku 14,2 / 11,9 GHz — 600 Mbit/s",
            "Processeur numérique transparent/régénératif",
            "Puissance RF 25 W, gain d'antenne 25 dBi",
            "Excellente tenue à la pluie par rapport à la bande Ka",
        ],
        "interfaces": [
            "Alimentation 28/50 V",
            "SpaceFibre / Ethernet",
            "Guides d'onde Ku",
        ],
        "uplink_frequency_ghz": 14.2,
        "downlink_frequency_ghz": 11.9,
        "rf_output_power_w": 25.0,
        "antenna_gain_tx_dbi": 25.0,
        "antenna_gain_rx_dbi": 24.0,
        "bandwidth_mhz": 350.0,
        "max_data_rate_mbps": 600.0,
    },
    {
        "id": "pl_rf_gallia_ka_dra_2500",
        "supplier_id": "gallia_satcom",
        "supplier_name": "Gallia SatCom Payloads",
        "name": "GalliaBeam-Ka2500 Multi-Spot Active Payload",
        "payload_type": "radio_comm",
        "description": "Charge utile bande Ka multifaisceaux à antenne active DRA (2,5 Gbit/s, 55 W RF) de haute capacité",
        "mass_kg": 62.0,
        "operational_power_w": 240.0,
        "peak_power_w": 350.0,
        "standby_power_w": 25.0,
        "volume_liters": 68.0,
        "dimensions_mm": [720, 520, 360],
        "required_pointing_accuracy_deg": 0.015,
        "required_pointing_stability_arcsec_s": 10.0,
        "max_tolerated_jitter_arcsec": 5.0,
        "thermal_dissipation_w": 190.0,
        "raw_data_rate_mbps": 2500.0,
        "compressed_data_rate_mbps": 2500.0,
        "price_meur": 7.9,
        "trl": 9,
        "flight_heritage": "Héritage OneWeb / IRIS²",
        "image": "payload_radio.jpg",
        "long_description": (
            "Charge utile télécom institutionnelle à très haut débit en bande Ka délivrant 2,5 Gbit/s grâce à une antenne "
            "active à rayonnement direct (DRA, 35 dBi) formant plusieurs spots agiles au sol. Conçue pour les plateformes "
            "de 300 à 800 kg des futures constellations souveraines."
        ),
        "key_features": [
            "Débit total 2,5 Gbit/s en bande Ka",
            "Antenne active multifaisceaux 35 dBi, 55 W RF",
            "Formation numérique de faisceaux (Digital Beamforming)",
            "Compatible normes 5G-NTN",
        ],
        "interfaces": [
            "Bus 50/100 V",
            "SpaceFibre 4 voies",
            "Panneau radiateur à caloducs dédié",
        ],
        "uplink_frequency_ghz": 29.6,
        "downlink_frequency_ghz": 19.8,
        "rf_output_power_w": 55.0,
        "antenna_gain_tx_dbi": 35.0,
        "antenna_gain_rx_dbi": 33.0,
        "bandwidth_mhz": 850.0,
        "max_data_rate_mbps": 2500.0,
    },
    {
        "id": "pl_rf_celestia_d2d_lband",
        "supplier_id": "celestia_broadband",
        "supplier_name": "Celestia Broadband Corp.",
        "name": "CellSpace-L80 Direct-to-Device & IoT Array",
        "payload_type": "radio_comm",
        "description": "Charge utile bande L/S à antenne phasée (80 Mbit/s) pour connectivité directe smartphones & IoT massif",
        "mass_kg": 15.0,
        "operational_power_w": 52.0,
        "peak_power_w": 80.0,
        "standby_power_w": 5.0,
        "volume_liters": 14.0,
        "dimensions_mm": [380, 320, 140],
        "required_pointing_accuracy_deg": 0.1,
        "required_pointing_stability_arcsec_s": 20.0,
        "max_tolerated_jitter_arcsec": 10.0,
        "thermal_dissipation_w": 40.0,
        "raw_data_rate_mbps": 80.0,
        "compressed_data_rate_mbps": 80.0,
        "price_meur": 1.85,
        "trl": 8,
        "flight_heritage": "9 satellites Direct-to-Device",
        "image": "payload_radio.jpg",
        "long_description": (
            "Charge utile NewSpace opérant en bande L/S (1,9 / 2,1 GHz) avec une antenne réseau phasé plane de 15 dBi "
            "permettant d'établir un lien direct avec des terminaux mobiles au sol et de redescendre 80 Mbit/s de trafic "
            "agrégé vers les stations passerelles."
        ),
        "key_features": [
            "Connectivité Direct-to-Device & IoT 3GPP NTN",
            "Débit 80 Mbit/s, puissance RF 15 W",
            "Masse contenue 15 kg pour microsatellites 50–150 kg",
            "Excellent bilan de liaison à 2,1 GHz (faibles pertes d'espace libre)",
        ],
        "interfaces": [
            "Alimentation 28 V",
            "Ethernet Gigabit / SpaceWire",
            "Panneau rayonnant nadir",
        ],
        "uplink_frequency_ghz": 1.98,
        "downlink_frequency_ghz": 2.17,
        "rf_output_power_w": 15.0,
        "antenna_gain_tx_dbi": 15.0,
        "antenna_gain_rx_dbi": 14.0,
        "bandwidth_mhz": 65.0,
        "max_data_rate_mbps": 80.0,
    },
    {
        "id": "pl_rf_celestia_ka_agile_900",
        "supplier_id": "celestia_broadband",
        "supplier_name": "Celestia Broadband Corp.",
        "name": "AeroCast-Ka900 Phased-Array Broadband",
        "payload_type": "radio_comm",
        "description": "Charge utile bande Ka NewSpace à balayage électronique (900 Mbit/s, 28 kg) sans pièce mobile",
        "mass_kg": 28.0,
        "operational_power_w": 115.0,
        "peak_power_w": 170.0,
        "standby_power_w": 12.0,
        "volume_liters": 26.0,
        "dimensions_mm": [480, 380, 180],
        "required_pointing_accuracy_deg": 0.03,
        "required_pointing_stability_arcsec_s": 15.0,
        "max_tolerated_jitter_arcsec": 8.0,
        "thermal_dissipation_w": 92.0,
        "raw_data_rate_mbps": 900.0,
        "compressed_data_rate_mbps": 900.0,
        "price_meur": 3.95,
        "trl": 8,
        "flight_heritage": "12 satellites de constellation",
        "image": "payload_radio.jpg",
        "long_description": (
            "Alternative NewSpace plus légère (28 kg contre 42 kg) et moins chère (3,95 M€ contre 5,4 M€) que le KaStream-1200 "
            "de Meridian RF. Son antenne active à commande de phase électronique élimine tout cardan mécanique tout en "
            "fournissant 900 Mbit/s de débit descendant."
        ),
        "key_features": [
            "900 Mbit/s en bande Ka sans mécanisme mobile",
            "Masse 28 kg, prix 3,95 M€",
            "Puissance RF équivalente 28 W, gain 30 dBi",
            "Commutation de faisceau < 1 ms",
        ],
        "interfaces": [
            "Alimentation 28/50 V",
            "SpaceFibre",
            "Montage encastré face nadir",
        ],
        "uplink_frequency_ghz": 29.2,
        "downlink_frequency_ghz": 19.5,
        "rf_output_power_w": 28.0,
        "antenna_gain_tx_dbi": 30.0,
        "antenna_gain_rx_dbi": 28.0,
        "bandwidth_mhz": 420.0,
        "max_data_rate_mbps": 900.0,
    },
    {
        "id": "pl_rf_helvetia_argos_dcs",
        "supplier_id": "helvetia_microwave",
        "supplier_name": "Helvetia Microwave & RF",
        "name": "SwissCollect-DCS Environmental & Maritime Receiver",
        "payload_type": "radio_comm",
        "description": "Charge utile suisse de haute sensibilité pour collecte de balises océanographiques/météo et liaison S 45 Mbit/s",
        "mass_kg": 6.2,
        "operational_power_w": 22.0,
        "peak_power_w": 34.0,
        "standby_power_w": 2.2,
        "volume_liters": 5.5,
        "dimensions_mm": [240, 180, 130],
        "required_pointing_accuracy_deg": 0.15,
        "required_pointing_stability_arcsec_s": 20.0,
        "max_tolerated_jitter_arcsec": 10.0,
        "thermal_dissipation_w": 17.0,
        "raw_data_rate_mbps": 45.0,
        "compressed_data_rate_mbps": 45.0,
        "price_meur": 1.05,
        "trl": 9,
        "flight_heritage": "Héritage Argos-4 / MetOp (10+ vols)",
        "image": "payload_radio.jpg",
        "long_description": (
            "Instrument de collecte de données environnementales et maritimes (401 MHz / VHF) doté d'oscillateurs suisses "
            "ultra-stables pour la localisation Doppler des balises et d'un émetteur bande S de 10 W descendant 45 Mbit/s "
            "avec une marge de liaison très confortable."
        ),
        "key_features": [
            "Débit descendant 45 Mbit/s en bande S (2,23 GHz)",
            "OCXO ultra-stable pour localisation Doppler fine",
            "Puissance RF 10 W, gain 13 dBi",
            "Masse 6,2 kg, prix 1,05 M€",
        ],
        "interfaces": [
            "Alimentation 28 V",
            "SpaceWire redondé",
            "Antenne hélice quadrifilaire déployable",
        ],
        "uplink_frequency_ghz": 0.401,
        "downlink_frequency_ghz": 2.23,
        "rf_output_power_w": 10.0,
        "antenna_gain_tx_dbi": 13.0,
        "antenna_gain_rx_dbi": 9.5,
        "bandwidth_mhz": 45.0,
        "max_data_rate_mbps": 45.0,
    },
    {
        "id": "pl_rf_helvetia_x_ka_precision",
        "supplier_id": "helvetia_microwave",
        "supplier_name": "Helvetia Microwave & RF",
        "name": "AlpineLink-X450 High-Efficiency Transponder",
        "payload_type": "radio_comm",
        "description": "Transpondeur bande X à cornet imprimé 3D RF (450 Mbit/s, 22 W RF) à très faible perte",
        "mass_kg": 16.5,
        "operational_power_w": 58.0,
        "peak_power_w": 85.0,
        "standby_power_w": 6.0,
        "volume_liters": 15.0,
        "dimensions_mm": [350, 260, 190],
        "required_pointing_accuracy_deg": 0.04,
        "required_pointing_stability_arcsec_s": 15.0,
        "max_tolerated_jitter_arcsec": 8.0,
        "thermal_dissipation_w": 42.0,
        "raw_data_rate_mbps": 450.0,
        "compressed_data_rate_mbps": 450.0,
        "price_meur": 2.95,
        "trl": 9,
        "flight_heritage": "8 missions institutionnelles",
        "image": "payload_radio.jpg",
        "long_description": (
            "Grâce à ses guides d'onde et antennes cornets monolithiques fabriqués par impression 3D métallique cuivrée, "
            "l'AlpineLink-X450 surpasse le RelayX-300 de Meridian RF (450 Mbit/s contre 300 Mbit/s, 21 dBi de gain) tout "
            "en étant plus léger (16,5 kg) et moins gourmand en énergie (58 W)."
        ),
        "key_features": [
            "450 Mbit/s en bande X (8,25 GHz)",
            "Antenne impression 3D RF à gain 21 dBi, 22 W RF",
            "Masse 16,5 kg, consommation 58 W seulement",
            "TRL 9",
        ],
        "interfaces": [
            "Alimentation 28 V",
            "SpaceFibre / SpaceWire",
            "Bride guide d'onde WR112",
        ],
        "uplink_frequency_ghz": 7.95,
        "downlink_frequency_ghz": 8.25,
        "rf_output_power_w": 22.0,
        "antenna_gain_tx_dbi": 21.0,
        "antenna_gain_rx_dbi": 18.5,
        "bandwidth_mhz": 300.0,
        "max_data_rate_mbps": 450.0,
    },

    # =========================================================================
    # OPTICAL TELECOM — New suppliers: celeste_photonics, nippon_optolink
    # =========================================================================
    {
        "id": "pl_opt_comm_celeste_10g",
        "supplier_id": "celeste_photonics",
        "supplier_name": "Céleste Photonique Spatiale",
        "name": "AéroLaser-10G Adaptive DTE Terminal",
        "payload_type": "optical_comm",
        "description": "Terminal laser LEO-sol 10 Gbit/s compact (11,5 kg) à mise en forme de faisceau MPLC",
        "mass_kg": 11.5,
        "operational_power_w": 52.0,
        "peak_power_w": 75.0,
        "standby_power_w": 6.0,
        "volume_liters": 9.8,
        "dimensions_mm": [290, 220, 200],
        "required_pointing_accuracy_deg": 0.012,
        "required_pointing_stability_arcsec_s": 0.6,
        "max_tolerated_jitter_arcsec": 0.6,
        "thermal_dissipation_w": 42.0,
        "raw_data_rate_mbps": 10000.0,
        "compressed_data_rate_mbps": 10000.0,
        "price_meur": 2.45,
        "trl": 8,
        "flight_heritage": "4 microsatellites français",
        "image": "payload_laser.jpg",
        "long_description": (
            "Concurrent français direct du LCT-10G de PhotonCom : l'AéroLaser-10G est plus léger (11,5 kg contre 14,5 kg), "
            "moins cher (2,45 M€) et consomme 52 W grâce à son amplificateur fibré erbium-ytterbium à haut rendement."
        ),
        "key_features": [
            "10 Gbit/s à 1550 nm (OOK / DPSK)",
            "Masse 11,5 kg, consommation 52 W, prix 2,45 M€",
            "Télescope SiC Ø 10 cm, laser 1,8 W",
            "Pointage fin 1,6 µrad",
        ],
        "interfaces": [
            "Alimentation 28 V",
            "SpaceFibre 10 Gbit/s",
            "Tête périscopique 2 axes",
        ],
        "telescope_aperture_m": 0.10,
        "wavelength_nm": 1550.0,
        "tx_optical_power_w": 1.8,
        "max_data_rate_gbps": 10.0,
        "beam_divergence_urad": 16.0,
        "pointing_tracking_accuracy_urad": 1.6,
        "compatible_standards": ["CCSDS_141.0-B-1"],
    },
    {
        "id": "pl_opt_comm_celeste_40g",
        "supplier_id": "celeste_photonics",
        "supplier_name": "Céleste Photonique Spatiale",
        "name": "CélesteLink-40G Coherent Downlink Terminal",
        "payload_type": "optical_comm",
        "description": "Terminal laser cohérent 40 Gbit/s (16 kg, Ø 13 cm, 3 W) idéal pour missions très haut débit",
        "mass_kg": 16.0,
        "operational_power_w": 72.0,
        "peak_power_w": 105.0,
        "standby_power_w": 8.0,
        "volume_liters": 14.0,
        "dimensions_mm": [340, 260, 240],
        "required_pointing_accuracy_deg": 0.008,
        "required_pointing_stability_arcsec_s": 0.4,
        "max_tolerated_jitter_arcsec": 0.4,
        "thermal_dissipation_w": 58.0,
        "raw_data_rate_mbps": 40000.0,
        "compressed_data_rate_mbps": 40000.0,
        "price_meur": 3.45,
        "trl": 8,
        "flight_heritage": "2 démonstrateurs souverains en orbite",
        "image": "payload_laser.jpg",
        "long_description": (
            "Terminal optique cohérent DP-QPSK délivrant jusqu'à 40 Gbit/s vers les stations sol optiques européennes. "
            "Avec un télescope de 13 cm et une puissance laser de 3,0 W pour un prix de 3,45 M€, il constitue une alternative "
            "très compétitive au TeraLink-25G (TeraLink Photonics) pour la mission TeraRelay."
        ),
        "key_features": [
            "40 Gbit/s cohérent à 1550 nm",
            "Télescope Ø 13 cm, laser 3,0 W",
            "Masse 16 kg, prix 3,45 M€",
            "Suivi fin 1,1 µrad",
        ],
        "interfaces": [
            "Alimentation 28 V",
            "SpaceFibre 4 voies",
            "Cardan azimut-élévation sans balais",
        ],
        "telescope_aperture_m": 0.13,
        "wavelength_nm": 1550.0,
        "tx_optical_power_w": 3.0,
        "max_data_rate_gbps": 40.0,
        "beam_divergence_urad": 13.0,
        "pointing_tracking_accuracy_urad": 1.1,
        "compatible_standards": ["CCSDS_141.0-B-1", "SDA_Tranche1"],
    },
    {
        "id": "pl_opt_comm_kibo_25g",
        "supplier_id": "nippon_optolink",
        "supplier_name": "Kibo Optical Communications",
        "name": "KiboLaser-25G Ultra-Reliable Optical Terminal",
        "payload_type": "optical_comm",
        "description": "Terminal optique japonais 25 Gbit/s (Ø 14 cm, 2,8 W, TRL 9) à haute immunité vibratoire",
        "mass_kg": 21.0,
        "operational_power_w": 76.0,
        "peak_power_w": 110.0,
        "standby_power_w": 9.0,
        "volume_liters": 18.0,
        "dimensions_mm": [370, 290, 260],
        "required_pointing_accuracy_deg": 0.008,
        "required_pointing_stability_arcsec_s": 0.45,
        "max_tolerated_jitter_arcsec": 0.45,
        "thermal_dissipation_w": 60.0,
        "raw_data_rate_mbps": 25000.0,
        "compressed_data_rate_mbps": 25000.0,
        "price_meur": 4.1,
        "trl": 9,
        "flight_heritage": "Héritage LUCAS / JDRS (5 vols sans défaillance)",
        "image": "payload_laser.jpg",
        "long_description": (
            "Terminal laser institutionnel japonais conçu pour une disponibilité maximale sur 7 ans. Sa boucle d'asservissement "
            "optique à 5 kHz offre une précision de poursuite de 1,0 µrad, procurant plus de 9 dB de marge de liaison "
            "vers une station sol de 80 cm à 500 km."
        ),
        "key_features": [
            "25 Gbit/s à 1550 nm, TRL 9",
            "Télescope Ø 14 cm, laser 2,8 W",
            "Poursuite ultra-stable 1,0 µrad (boucle 5 kHz)",
            "Qualification longue durée (> 7 ans)",
        ],
        "interfaces": [
            "Alimentation 28/50 V",
            "SpaceFibre redondé",
            "Isolateurs micro-vibrations intégrés",
        ],
        "telescope_aperture_m": 0.14,
        "wavelength_nm": 1550.0,
        "tx_optical_power_w": 2.8,
        "max_data_rate_gbps": 25.0,
        "beam_divergence_urad": 12.5,
        "pointing_tracking_accuracy_urad": 1.0,
        "compatible_standards": ["CCSDS_141.0-B-1", "SDA_Tranche1", "JAXA_LUCAS"],
    },

    # =========================================================================
    # SPECTROMETER — New suppliers: lumina_hyperspec, atmo_science_eu
    # =========================================================================
    {
        "id": "pl_spec_lumina_vnir_swir",
        "supplier_id": "lumina_hyperspec",
        "supplier_name": "Lumina Hyperspectral Oy",
        "name": "HyperCube-100 Compact VNIR/SWIR Imager",
        "payload_type": "spectrometer",
        "description": "Spectromètre Fabry-Pérot compact (12 kg, 450–1700 nm, 100 bandes) pour microsatellites",
        "mass_kg": 12.0,
        "operational_power_w": 34.0,
        "peak_power_w": 50.0,
        "standby_power_w": 3.5,
        "volume_liters": 11.0,
        "dimensions_mm": [310, 220, 190],
        "required_pointing_accuracy_deg": 0.025,
        "required_pointing_stability_arcsec_s": 2.5,
        "max_tolerated_jitter_arcsec": 1.2,
        "thermal_dissipation_w": 28.0,
        "raw_data_rate_mbps": 680.0,
        "compressed_data_rate_mbps": 220.0,
        "price_meur": 2.35,
        "trl": 9,
        "flight_heritage": "9 satellites en orbite (constellation Hyperfield)",
        "image": "payload_spectrometer.jpg",
        "long_description": (
            "Spectromètre imageur finlandais couvrant simultanément le VNIR et le début du SWIR (450 à 1700 nm) en 100 bandes "
            "de 8 nm de largeur, dans une enveloppe de seulement 12 kg. Idéal pour la foresterie, l'agriculture et la qualité "
            "des eaux côtières sur petite plateforme, mais sa résolution spectrale (8 nm) ne résout pas les raies fines du CH4."
        ),
        "key_features": [
            "450 à 1700 nm en 100 bandes programmables",
            "Masse 12 kg seulement, prix 2,35 M€",
            "GSD ~ 4,7 m à 500 km",
            "Résolution spectrale 8,0 nm",
        ],
        "interfaces": [
            "Alimentation 28 V",
            "SpaceWire / SpaceFibre",
            "Fixation 3 points",
        ],
        "aperture_diameter_m": 0.15,
        "focal_length_m": 0.95,
        "pixel_pitch_um": 9.0,
        "detector_spatial_pixels": 1600,
        "spectral_range_min_nm": 450.0,
        "spectral_range_max_nm": 1700.0,
        "number_of_spectral_bands": 100,
        "spectral_resolution_nm": 8.0,
        "quantization_bits": 12,
    },
    {
        "id": "pl_spec_atmo_tropo_ghg",
        "supplier_id": "atmo_science_eu",
        "supplier_name": "AtmoSonde Scientific Instruments",
        "name": "TropoSonde-CH4 Ultra-Fine Atmospheric Spectrometer",
        "payload_type": "spectrometer",
        "description": "Sondeur atmosphérique à réseau immergé (0,22 nm FWHM, 1550–1720 nm) pour CH4 et CO2",
        "mass_kg": 38.0,
        "operational_power_w": 78.0,
        "peak_power_w": 115.0,
        "standby_power_w": 9.0,
        "volume_liters": 34.0,
        "dimensions_mm": [520, 380, 330],
        "required_pointing_accuracy_deg": 0.012,
        "required_pointing_stability_arcsec_s": 1.2,
        "max_tolerated_jitter_arcsec": 0.8,
        "thermal_dissipation_w": 65.0,
        "raw_data_rate_mbps": 1100.0,
        "compressed_data_rate_mbps": 360.0,
        "price_meur": 6.4,
        "trl": 9,
        "flight_heritage": "Héritage TROPOMI / TANGO / CO2M",
        "image": "payload_spectrometer.jpg",
        "long_description": (
            "Spectromètre atmosphérique européen de référence utilisant un réseau de diffraction immergé en silicium (immersed "
            "grating) qui réduit d'un facteur 3,4 le volume optique à finesse spectrale donnée. Avec une résolution spectrale "
            "de 0,22 nm sur la bande 1550–1720 nm et un GSD de 5,0 m à 500 km, il surpasse toutes les exigences de la mission "
            "AtmoWatch (EXAM-2026-ATMO-GHG)."
        ),
        "key_features": [
            "Finesse spectrale exceptionnelle : 0,22 nm FWHM (420 canaux)",
            "Couverture SWIR 1550–1720 nm (raies CH4 et CO2)",
            "GSD ~ 5,0 m à 500 km, SNR > 90",
            "Réseau immergé silicium, TRL 9",
        ],
        "interfaces": [
            "Alimentation 28 V",
            "SpaceFibre redondé",
            "Cryorefroidisseur Pulse-Tube longue durée",
        ],
        "aperture_diameter_m": 0.24,
        "focal_length_m": 1.2,
        "pixel_pitch_um": 12.0,
        "detector_spatial_pixels": 1500,
        "spectral_range_min_nm": 1550.0,
        "spectral_range_max_nm": 1720.0,
        "number_of_spectral_bands": 420,
        "spectral_resolution_nm": 0.22,
        "quantization_bits": 14,
    },

    # =========================================================================
    # QKD — New suppliers: edelweiss_quantum, albion_quantum_optics
    # =========================================================================
    {
        "id": "pl_qkd_edelweiss_entangled",
        "supplier_id": "edelweiss_quantum",
        "supplier_name": "Edelweiss Quantum Space",
        "name": "EagleQKD-200 Sovereign Quantum Terminal",
        "payload_type": "qkd",
        "description": "Terminal QKD européen (Ø 20 cm, 180 MHz, 850 nm) qualifié EuroQCI pour microsatellites",
        "mass_kg": 24.0,
        "operational_power_w": 58.0,
        "peak_power_w": 85.0,
        "standby_power_w": 6.0,
        "volume_liters": 22.0,
        "dimensions_mm": [420, 310, 280],
        "required_pointing_accuracy_deg": 0.006,
        "required_pointing_stability_arcsec_s": 0.3,
        "max_tolerated_jitter_arcsec": 0.3,
        "thermal_dissipation_w": 46.0,
        "raw_data_rate_mbps": 18.0,
        "compressed_data_rate_mbps": 18.0,
        "price_meur": 4.7,
        "trl": 8,
        "flight_heritage": "Programme européen Eagle-1 / EuroQCI",
        "image": "payload_qkd.jpg",
        "long_description": (
            "Terminal QKD souverain développé par Edelweiss Quantum Space avec un télescope de 20 cm en carbure de silicium "
            "et une source quantique à 180 MHz. Positionné entre le QuantumKey-850 (15 cm, PhotonCom) et le lourd "
            "QuantaCore-250 (25 cm, QuantaSpace), il offre un excellent débit de clé secrète (> 4 500 bit/s à 500 km) "
            "pour un coût et une masse parfaitement adaptés aux plateformes de 150 kg."
        ),
        "key_features": [
            "Télescope Ø 20 cm, source 180 MHz à 850 nm",
            "Pointage fin 1,1 µrad, QBER < 2,8 %",
            "Masse 24 kg, prix 4,7 M€",
            "Conforme architecture européenne EuroQCI",
        ],
        "interfaces": [
            "Alimentation 28 V",
            "SpaceWire + synchronisation optique/PPS",
            "Banc optique SiC athermique",
        ],
        "protocol": "BB84_decoy_state",
        "telescope_aperture_m": 0.20,
        "source_rate_mhz": 180.0,
        "wavelength_nm": 850.0,
        "pointing_accuracy_urad": 1.1,
        "night_only_operation": True,
    },
    {
        "id": "pl_qkd_albion_micro12",
        "supplier_id": "albion_quantum_optics",
        "supplier_name": "Albion Quantum Photonics",
        "name": "Q-Blade 120 Integrated Photonic QKD",
        "payload_type": "qkd",
        "description": "Terminal QKD NewSpace à puce photonique intégrée (Ø 12 cm, 120 MHz, 10,5 kg) à coût maîtrisé",
        "mass_kg": 10.5,
        "operational_power_w": 32.0,
        "peak_power_w": 48.0,
        "standby_power_w": 4.5,
        "volume_liters": 9.5,
        "dimensions_mm": [280, 210, 190],
        "required_pointing_accuracy_deg": 0.008,
        "required_pointing_stability_arcsec_s": 0.5,
        "max_tolerated_jitter_arcsec": 0.5,
        "thermal_dissipation_w": 25.0,
        "raw_data_rate_mbps": 15.0,
        "compressed_data_rate_mbps": 15.0,
        "price_meur": 2.4,
        "trl": 8,
        "flight_heritage": "3 microsatellites UK/ESA",
        "image": "payload_qkd.jpg",
        "long_description": (
            "Grâce à une source d'états quantiques gravée sur puce photonique en nitrure de silicium et un télescope de 12 cm, "
            "le Q-Blade 120 d'Albion Quantum Photonics divise par près de deux la masse (10,5 kg) et le coût (2,4 M€) d'une "
            "charge utile QKD opérationnelle tout en délivrant plus de 1 200 bit/s de clés secrètes à 500 km."
        ),
        "key_features": [
            "Puce photonique intégrée 120 MHz, Ø 12 cm",
            "Masse 10,5 kg seulement, prix 2,40 M€",
            "Pointage fin 1,4 µrad (compatible pack ADCS 0,008°)",
            "Idéal pour mission QKD sur plateforme 50 à 150 kg",
        ],
        "interfaces": [
            "Alimentation 28 V",
            "SpaceWire / Ethernet",
            "Interface mécanique 4 points M6",
        ],
        "protocol": "BB84_decoy_state",
        "telescope_aperture_m": 0.12,
        "source_rate_mhz": 120.0,
        "wavelength_nm": 850.0,
        "pointing_accuracy_urad": 1.4,
        "night_only_operation": True,
    },
]


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    suppliers_path = CATALOGS_DIR / "suppliers.json"
    payloads_path = CATALOGS_DIR / "payloads.json"

    suppliers: list[dict] = json.loads(suppliers_path.read_text(encoding="utf-8"))
    payloads: list[dict] = json.loads(payloads_path.read_text(encoding="utf-8"))

    sup_by_id = {s["id"]: s for s in suppliers}
    for ns in NEW_SUPPLIERS:
        sup_by_id[ns["id"]] = ns
    merged_suppliers = list(sup_by_id.values())

    pl_by_id = {p["id"]: p for p in payloads}
    for np in NEW_PAYLOADS:
        pl_by_id[np["id"]] = np
    merged_payloads = list(pl_by_id.values())

    suppliers_path.write_text(json.dumps(merged_suppliers, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    payloads_path.write_text(json.dumps(merged_payloads, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # Validate with CatalogDatabase and build_datasheet
    db = CatalogDatabase()
    db.load_from_directory(CATALOGS_DIR)
    orbit = OrbitDefinition(altitude_km=500.0, inclination_deg=97.4)
    for p in db.payloads.values():
        ds = build_datasheet(p, orbit)
        assert ds.sections and ds.dimensions_mm

    # Print summary per payload_type
    by_type: dict[str, set[str]] = {}
    cnt_by_type: dict[str, int] = {}
    for p in db.payloads.values():
        t = p.payload_type.value
        by_type.setdefault(t, set()).add(f"{p.supplier_name} ({p.supplier_id})")
        cnt_by_type[t] = cnt_by_type.get(t, 0) + 1

    print(f"Total suppliers: {len(db.suppliers)}, Total payloads: {len(db.payloads)}")
    for t, sups in sorted(by_type.items()):
        print(f"  - {t}: {cnt_by_type[t]} payloads across {len(sups)} suppliers -> {sorted(sups)}")


if __name__ == "__main__":
    main()
