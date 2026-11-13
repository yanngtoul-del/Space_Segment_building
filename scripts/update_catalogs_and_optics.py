"""Update payloads.json, optical_systems_bridge.json, suppliers.json, and platforms.json."""

import json
from pathlib import Path

ROOT = Path(r"C:\Users\Lapto\PycharmProjects\Space_Segment_building")
CAT_DIR = ROOT / "data" / "catalogs"
BRIDGE_FILE = ROOT / "data" / "optical_systems_bridge.json"
PYOPTIC_BRIDGE_FILE = Path(r"C:\Users\Lapto\PycharmProjects\Conception_optique\data\space_segment_optics.json")

# ---------------------------------------------------------------------------
# 1. Update optical_imager payloads with sensor_architecture, tdi_stages, detector_format_label
# ---------------------------------------------------------------------------
OPTICAL_SENSOR_METADATA = {
    "pl_opt_cubesat_6cm": {
        "sensor_architecture": "frame_matrix",
        "tdi_stages": 1,
        "detector_format_label": "Matrice CMOS 2D Global Shutter 4 096 × 3 072 px (acquisition Frame par clichés, sans TDI)",
        "description": "Caméra 1,2U de 6 cm d'ouverture à capteur matriciel CMOS 2D Global Shutter (sans TDI) pour CubeSats 6U et 12U",
        "long_description": (
            "La plus petite caméra d'observation du catalogue : un objectif réfractif athermique de 6 cm tenant dans un peu plus de 1U, "
            "couplé à un capteur matriciel CMOS 2D à obturation globale (Global Shutter, 4 096 × 3 072 pixels, sans TDI). "
            "L'acquisition par clichés matriciels instantanés (« Frame / Snapshot ») tolère les dérives d'attitude des petits CubeSats "
            "(jusqu'à 20 arcsec/s) sans distorsion géométrique inter-lignes. Elle fournit un GSD d'environ 6,1 m à 500 km sur une fauchée de 25 km."
        ),
        "feature_tag": "Capteur matriciel 2D Global Shutter (sans TDI)",
    },
    "pl_opt_pan_compact": {
        "sensor_architecture": "pushbroom_linear",
        "tdi_stages": 1,
        "detector_format_label": "Barrette linéaire CMOS 8 000 px × 5 bandes (Push-Broom mono-ligne sans TDI)",
        "description": "Télescope compact 12 cm à balayage Push-Broom linéaire mono-ligne (sans TDI) pour CubeSats 12U–16U et MicroSats",
        "long_description": (
            "Télescope Ritchey-Chrétien compact de 12 cm d'ouverture conçu pour les CubeSats 12U–16U et les petits microsatellites. "
            "Son plan focal utilise une barrette linéaire CMOS Push-Broom mono-ligne de 8 000 pixels par bande (PAN + 4 bandes VNIR) fonctionnant "
            "sans intégration TDI (1 seule ligne par canal spectral). Cette architecture Push-Broom simple évite la complexité d'horloge de synchronisation TDI "
            "et tolère une stabilité de pointage modérée (8 arcsec/s), tout en offrant un GSD d'environ 2,6 m à 500 km."
        ),
        "feature_tag": "Push-Broom linéaire 8 000 px (sans TDI)",
    },
    "pl_opt_wide_swath_18cm": {
        "sensor_architecture": "pushbroom_linear",
        "tdi_stages": 1,
        "detector_format_label": "Barrette linéaire CMOS 16 000 px × 5 bandes (Push-Broom grand champ f/5 sans TDI)",
        "description": "Imageur Push-Broom linéaire 18 cm grand champ (>55 km de fauchée, f/5, sans TDI) pour revisite fréquente",
        "long_description": (
            "Instrument multispectral à focale courte (f = 0,90 m) et grande ouverture numérique (f/5) privilégiant la largeur de fauchée (~58 km à 500 km) "
            "plutôt que la résolution pure (~3,6 m). Grâce à son optique très lumineuse ouverte à f/5 et à son grand pas de pixel (6,5 µm), "
            "sa barrette Push-Broom linéaire de 16 000 pixels collecte suffisamment de photons en une seule ligne d'intégration sans nécessiter d'étages TDI."
        ),
        "feature_tag": "Push-Broom linéaire 16 000 px f/5 (sans TDI)",
    },
    "pl_opt_stellara_20cm": {
        "sensor_architecture": "frame_matrix",
        "tdi_stages": 1,
        "detector_format_label": "Matrice CMOS 2D plein format 12 000 × 4 096 px (mode Frame / Step-and-Stare à bandes filtrées, sans TDI)",
        "description": "Télescope Ritchey-Chrétien 20 cm à capteur matriciel CMOS 2D (Frame / Step-and-Stare, sans TDI) pour microsatellites",
        "long_description": (
            "Télescope italien de 20 cm d'ouverture à miroirs en Zerodur et structure carbone, délivrant environ 1,5 m de GSD à 500 km. "
            "Il se distingue par son plan focal matriciel CMOS 2D grand format (12 000 × 4 096 pixels à filtres en bandes « Butcher-block ») "
            "opérant par clichés successifs (mode Frame / Step-and-Stare sans TDI), ce qui permet aussi bien la couverture continue par recouvrement "
            "que l'acquisition vidéo haute cadence ou multi-angles d'une cible fixe."
        ),
        "feature_tag": "Capteur matriciel 2D 12 000 × 4 096 px (sans TDI)",
    },
    "pl_opt_swir_20cm": {
        "sensor_architecture": "frame_matrix",
        "tdi_stages": 1,
        "detector_format_label": "Matrice focale 2D InGaAs refroidie 4 096 × 2 048 px (imagerie Frame SWIR tri-bande, sans TDI)",
        "description": "Imageur infrarouge SWIR (1,0–2,4 µm) à capteur matriciel 2D InGaAs refroidi (acquisition Frame, sans TDI)",
        "long_description": (
            "Caméra infrarouge SWIR équipée d'une matrice focale 2D InGaAs refroidie par machine Stirling miniature (4 096 × 2 048 pixels au pas de 10 µm, "
            "mode Frame par clichés instantanés sans TDI). Elle observe à travers la fumée, détecte les départs de feux, les fuites industrielles "
            "et le stress hydrique des sols avec un GSD de 4,0 m à 500 km."
        ),
        "feature_tag": "Matrice 2D InGaAs refroidie (Frame, sans TDI)",
    },
    "pl_opt_medium_25cm": {
        "sensor_architecture": "pushbroom_tdi",
        "tdi_stages": 8,
        "detector_format_label": "Barrette Push-Broom CMOS avec TDI numérique (14 000 px, 8 étages TDI en PAN / 4 étages en MS)",
        "description": "Télescope Cassegrain 25 cm à balayage Push-Broom et intégration TDI (8 étages) pour microsatellites",
        "long_description": (
            "Télescope Cassegrain de 25 cm d'ouverture offrant une résolution métrique (~1,25 m à 500 km) et six bandes spectrales incluant le Red-Edge. "
            "Son plan focal Push-Broom de 14 000 pixels intègre un dispositif TDI (Time Delay Integration) numérique à 8 étages pour compenser "
            "le court temps d'intégration ligne (~0,16 ms) et maintenir un SNR élevé à f/8,8. L'usage du TDI impose une stabilité d'attitude ≤ 2,5 arcsec/s."
        ),
        "feature_tag": "Push-Broom 14 000 px avec TDI 8 étages",
    },
    "pl_opt_stellara_35cm": {
        "sensor_architecture": "pushbroom_tdi",
        "tdi_stages": 16,
        "detector_format_label": "Barrette Push-Broom CCD/CMOS avec TDI (20 000 px, 16 étages TDI en PAN / 8 étages en MS)",
        "description": "Télescope 35 cm sub-métrique (~0,86 m GSD) à balayage Push-Broom avec TDI (16 étages)",
        "long_description": (
            "Télescope sub-métrique compact de 35 cm (f/10) pesant seulement 30 kg. Pour atteindre un rapport signal-sur-bruit supérieur à 60 malgré "
            "un GSD sub-métrique (~0,86 m à 500 km, fréquence ligne ~8,2 kHz), son détecteur Push-Broom de 20 000 pixels met en œuvre une intégration "
            "à décalage temporel (TDI) sur 16 étages, requérant une stabilité de pointage plateforme ≤ 1,2 arcsec/s."
        ),
        "feature_tag": "Push-Broom 20 000 px avec TDI 16 étages",
    },
    "pl_opt_submeter_highres": {
        "sensor_architecture": "pushbroom_tdi",
        "tdi_stages": 32,
        "detector_format_label": "Barrette Push-Broom TDI haute cadence (24 000 px, 32 étages TDI programmables)",
        "description": "Télescope Korsch 45 cm sub-métrique à balayage Push-Broom avec TDI (32 étages programmables)",
        "long_description": (
            "Télescope Korsch à trois miroirs de 45 cm d'ouverture en carbure de silicium, destiné à l'observation tactique sub-métrique (~0,77 m à 500 km). "
            "Son plan focal Push-Broom de 24 000 pixels dispose de 32 étages TDI programmables (8/16/24/32 lignes) synchronisés à la vitesse de défilement "
            "au sol, ce qui exige un pointage meilleur que 0,008° et une dérive gyroscopique inférieure à 0,8 arcsec/s."
        ),
        "feature_tag": "Push-Broom 24 000 px avec TDI 32 étages",
    },
    "pl_opt_stellara_60cm": {
        "sensor_architecture": "pushbroom_tdi",
        "tdi_stages": 32,
        "detector_format_label": "Plan focal hybride : Barrette Push-Broom 32 000 px (32 étages TDI) + mosaïque matricielle 2D pour poses longues Step-and-Stare",
        "description": "Télescope Korsch 60 cm (GSD ~0,5 m) à plan focal hybride Push-Broom TDI (32 étages) & Matriciel 2D Step-and-Stare",
        "long_description": (
            "Télescope Korsch de 60 cm atteignant 0,50 m de résolution au nadir à 500 km. Son plan focal hybride combine une barrette Push-Broom de 32 000 pixels "
            "à 32 étages TDI (pour le balayage continu d'observation de la Terre) et une mosaïque matricielle 2D dédiée aux poses longues stabilisées "
            "(« Step-and-Stare ») pour l'astrométrie et l'imagerie de champ profond."
        ),
        "feature_tag": "Plan focal hybride Push-Broom TDI 32 étages + Matrice 2D",
    },
    "pl_opt_helios_70cm": {
        "sensor_architecture": "pushbroom_tdi",
        "tdi_stages": 64,
        "detector_format_label": "Barrette Push-Broom TDI multi-étages (36 000 px, 64 étages TDI asservis au gyrolaser)",
        "description": "Télescope 70 cm très haute résolution (~0,39 m GSD) à balayage Push-Broom avec TDI (64 étages)",
        "long_description": (
            "Instrument de 70 cm d'Helios Space Instruments offrant une résolution de ~39 cm à 500 km (f/12). À cette résolution, le temps de passage "
            "d'une ligne au sol n'est que de 55 µs (~18 kHz) : le plan focal Push-Broom de 36 000 pixels intègre donc 64 étages TDI asservis en temps réel "
            "aux gyrolasers du banc optique, exigeant une stabilité d'attitude ≤ 0,30 arcsec/s et un jitter ≤ 0,25 arcsec."
        ),
        "feature_tag": "Push-Broom 36 000 px avec TDI 64 étages",
    },
    "pl_opt_veryhighres_1m": {
        "sensor_architecture": "pushbroom_tdi",
        "tdi_stages": 128,
        "detector_format_label": "Plan focal Push-Broom TDI très haute sensibilité (48 000 px, 128 étages TDI bidirectionnels)",
        "description": "Télescope Korsch 1,0 m très haute résolution (~0,29 m GSD) à balayage Push-Broom avec TDI (128 étages)",
        "long_description": (
            "Grand instrument optique de 1 m de diamètre primaire pour les missions souveraines de très haute résolution (~0,29 m à 500 km, f/12). "
            "Son plan focal Push-Broom de 48 000 pixels met en œuvre 128 étages TDI bidirectionnels pour compenser la cadence ligne de 24 kHz "
            "et permettre des prises de vue sous faible éclairement solaire. Il produit un débit brut de 6,5 Gbit/s et exige une stabilité extrême (0,15 arcsec/s)."
        ),
        "feature_tag": "Push-Broom 48 000 px avec TDI 128 étages",
    },
}


def update_payloads_and_bridge() -> None:
    payloads_path = CAT_DIR / "payloads.json"
    payloads = json.loads(payloads_path.read_text(encoding="utf-8"))

    updated_count = 0
    for item in payloads:
        pid = item["id"]
        if pid in OPTICAL_SENSOR_METADATA:
            meta = OPTICAL_SENSOR_METADATA[pid]
            item["sensor_architecture"] = meta["sensor_architecture"]
            item["tdi_stages"] = meta["tdi_stages"]
            item["detector_format_label"] = meta["detector_format_label"]
            item["description"] = meta["description"]
            item["long_description"] = meta["long_description"]
            # Ensure feature_tag is present in key_features without duplicating
            kf = [f for f in item.get("key_features", []) if "TDI" not in f and "Push-Broom" not in f and "matriciel" not in f.lower() and "Matrice" not in f]
            kf.append(meta["feature_tag"])
            item["key_features"] = kf
            updated_count += 1

    payloads_path.write_text(json.dumps(payloads, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Updated {updated_count} optical_imager payloads in payloads.json")

    if BRIDGE_FILE.exists():
        bridge = json.loads(BRIDGE_FILE.read_text(encoding="utf-8"))
        for sys_entry in bridge.get("systems", []):
            sid = sys_entry["id"]
            if sid in OPTICAL_SENSOR_METADATA:
                meta = OPTICAL_SENSOR_METADATA[sid]
                sys_entry["description"] = meta["description"]
                sys_entry["long_description"] = meta["long_description"]
                sys_entry["optical_specifications"]["sensor_architecture"] = meta["sensor_architecture"]
                sys_entry["optical_specifications"]["tdi_stages"] = meta["tdi_stages"]
                sys_entry["optical_specifications"]["detector_format_label"] = meta["detector_format_label"]
                kf = [f for f in sys_entry.get("key_features", []) if "TDI" not in f and "Push-Broom" not in f and "matriciel" not in f.lower() and "Matrice" not in f]
                kf.append(meta["feature_tag"])
                sys_entry["key_features"] = kf
        BRIDGE_FILE.write_text(json.dumps(bridge, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print("Updated data/optical_systems_bridge.json")
        if PYOPTIC_BRIDGE_FILE.exists():
            PYOPTIC_BRIDGE_FILE.write_text(json.dumps(bridge, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            print("Updated Conception_optique/data/space_segment_optics.json")


# ---------------------------------------------------------------------------
# 2. Update suppliers.json and platforms.json with 10 new platforms
# ---------------------------------------------------------------------------
NEW_PLATFORM_SUPPLIERS = {
    "nordic_nanocomm",
    "stellare_ottica",
    "med_radar_ital",
    "euro_sar_prime",
    "space_avionics",
}

NEW_PLATFORMS = [
    {
        "id": "plat_nordic_3u",
        "supplier_id": "nordic_nanocomm",
        "supplier_name": "Nordic NanoComm Systems",
        "name": "NordicCube-3U NanoBus",
        "category": "cubesat_3u",
        "description": "Plateforme CubeSat 3U ultra-légère pour démonstrateurs IoT, AIS et petits capteurs en orbite basse",
        "dry_mass_kg": 2.2,
        "max_payload_mass_kg": 2.2,
        "max_launch_mass_kg": 5.5,
        "payload_volume_liters": 1.8,
        "dimensions_mm": [340.0, 100.0, 100.0],
        "deployed_span_m": 0.75,
        "orbit_avg_power_w": 14.0,
        "payload_avg_power_w": 8.0,
        "payload_peak_power_w": 18.0,
        "bus_voltage_v": 12.0,
        "battery_capacity_wh": 42.0,
        "battery_max_dod": 0.25,
        "pointing_accuracy_deg": 0.8,
        "pointing_stability_arcsec_s": 45.0,
        "slew_rate_deg_s": 1.5,
        "jitter_arcsec": 20.0,
        "payload_thermal_dissipation_w": 10.0,
        "base_price_meur": 0.16,
        "base_lead_time_months": 5,
        "design_lifetime_years": 2.0,
        "rad_tolerance_krad": 10.0,
        "trl": 9,
        "launch_environment_compatible": ["Falcon9_Rideshare", "VegaC_SSMS", "Electron"],
        "slots": [
            {
                "function": "propulsion",
                "min_qty": 0,
                "max_qty": 1,
                "allowed_equipment_ids": ["prop_coldgas_1u"],
                "included_equipment_ids": [],
                "integration_cost_fixed_meur": 0.02,
                "integration_cost_pct": 5.0
            },
            {
                "function": "ttc",
                "min_qty": 1,
                "max_qty": 1,
                "allowed_equipment_ids": ["ttc_uhf_cubesat", "ttc_sband_transceiver"],
                "included_equipment_ids": ["ttc_uhf_cubesat"],
                "integration_cost_fixed_meur": 0.01,
                "integration_cost_pct": 5.0
            },
            {
                "function": "payload_downlink",
                "min_qty": 0,
                "max_qty": 1,
                "allowed_equipment_ids": ["downlink_sband_hr"],
                "included_equipment_ids": [],
                "integration_cost_fixed_meur": 0.02,
                "integration_cost_pct": 5.0
            },
            {
                "function": "mass_memory",
                "min_qty": 1,
                "max_qty": 1,
                "allowed_equipment_ids": ["mass_mem_64gb"],
                "included_equipment_ids": ["mass_mem_64gb"],
                "integration_cost_fixed_meur": 0.01,
                "integration_cost_pct": 0.0
            },
            {
                "function": "adcs",
                "min_qty": 0,
                "max_qty": 1,
                "allowed_equipment_ids": ["adcs_cubesat_basic", "adcs_cubesat_precision"],
                "included_equipment_ids": [],
                "integration_cost_fixed_meur": 0.02,
                "integration_cost_pct": 5.0
            },
            {
                "function": "optical_interface",
                "min_qty": 0,
                "max_qty": 1,
                "allowed_equipment_ids": ["opt_slit_micro_nanosat"],
                "included_equipment_ids": [],
                "integration_cost_fixed_meur": 0.02,
                "integration_cost_pct": 5.0
            }
        ],
        "image": "platform_cubesat.jpg",
        "long_description": (
            "Plateforme CubeSat 3U scandinave d'entrée de gamme développée en Suède pour les démonstrations technologiques universitaires, "
            "la collecte maritime AIS et l'IoT léger. Elle offre 1,8 U de volume utile (jusqu'à 2,2 kg) et 8 W de puissance moyenne "
            "pour un coût basal imbattable de 0,16 M€, mais sa taille et sa durée de vie nominale de 2,0 ans limitent son usage aux charges utiles ultra-compactes."
        ),
        "key_features": [
            "Format CubeSat 3U (2,2 kg sec), baie charge utile 1,8 L / 2,2 kg",
            "8 W moyens pour la charge utile, batterie 42 Wh",
            "Transpondeur UHF et mémoire 64 Go inclus de série",
            "Idéale pour récepteurs SDR AIS/IoT ou caméra 1,2U à budget minimal"
        ],
        "interfaces": [
            "Bus PC/104 CubeSat (5 V / 12 V)",
            "Interfaces I2C, SPI, UART, CAN",
            "Compatible déployeurs 3U/6U standardisés"
        ]
    },
    {
        "id": "plat_nordic_12u_hp",
        "supplier_id": "nordic_nanocomm",
        "supplier_name": "Nordic NanoComm Systems",
        "name": "NordicCube-12U High-Power",
        "category": "cubesat_12u",
        "description": "Plateforme CubeSat 12U scandinave à panneaux solaires déployables double-face (38 W CU, 3,5 ans)",
        "dry_mass_kg": 9.5,
        "max_payload_mass_kg": 9.5,
        "max_launch_mass_kg": 22.0,
        "payload_volume_liters": 7.5,
        "dimensions_mm": [226.0, 226.0, 340.0],
        "deployed_span_m": 1.35,
        "orbit_avg_power_w": 58.0,
        "payload_avg_power_w": 38.0,
        "payload_peak_power_w": 85.0,
        "bus_voltage_v": 28.0,
        "battery_capacity_wh": 165.0,
        "battery_max_dod": 0.25,
        "pointing_accuracy_deg": 0.08,
        "pointing_stability_arcsec_s": 10.0,
        "slew_rate_deg_s": 2.0,
        "jitter_arcsec": 4.0,
        "payload_thermal_dissipation_w": 42.0,
        "base_price_meur": 0.62,
        "base_lead_time_months": 7,
        "design_lifetime_years": 3.5,
        "rad_tolerance_krad": 18.0,
        "trl": 9,
        "launch_environment_compatible": ["Falcon9_Rideshare", "VegaC_SSMS", "Electron"],
        "slots": [
            {
                "function": "propulsion",
                "min_qty": 0,
                "max_qty": 1,
                "allowed_equipment_ids": ["prop_coldgas_1u", "prop_coldgas_10u", "prop_pptt_micro"],
                "included_equipment_ids": [],
                "integration_cost_fixed_meur": 0.04,
                "integration_cost_pct": 8.0
            },
            {
                "function": "ttc",
                "min_qty": 1,
                "max_qty": 1,
                "allowed_equipment_ids": ["ttc_uhf_cubesat", "ttc_sband_transceiver", "ttc_sband_gallia_fr", "ttc_sband_aurora_it"],
                "included_equipment_ids": ["ttc_sband_transceiver"],
                "integration_cost_fixed_meur": 0.02,
                "integration_cost_pct": 5.0
            },
            {
                "function": "payload_downlink",
                "min_qty": 0,
                "max_qty": 1,
                "allowed_equipment_ids": ["downlink_sband_hr", "downlink_xband_tx_50mbps", "downlink_xband_tx_150mbps"],
                "included_equipment_ids": [],
                "integration_cost_fixed_meur": 0.04,
                "integration_cost_pct": 8.0
            },
            {
                "function": "mass_memory",
                "min_qty": 1,
                "max_qty": 1,
                "allowed_equipment_ids": ["mass_mem_64gb", "mass_mem_512gb"],
                "included_equipment_ids": ["mass_mem_64gb"],
                "integration_cost_fixed_meur": 0.02,
                "integration_cost_pct": 5.0
            },
            {
                "function": "adcs",
                "min_qty": 0,
                "max_qty": 1,
                "allowed_equipment_ids": ["adcs_cubesat_basic", "adcs_cubesat_precision"],
                "included_equipment_ids": [],
                "integration_cost_fixed_meur": 0.04,
                "integration_cost_pct": 8.0
            },
            {
                "function": "optical_interface",
                "min_qty": 0,
                "max_qty": 1,
                "allowed_equipment_ids": ["opt_slit_micro_nanosat", "opt_slit_std_vnir"],
                "included_equipment_ids": [],
                "integration_cost_fixed_meur": 0.03,
                "integration_cost_pct": 5.0
            }
        ],
        "image": "platform_cubesat.jpg",
        "long_description": (
            "Version haute puissance du bus 12U développée en Suède par Nordic NanoComm Systems. Dotée de panneaux solaires articulés "
            "délivrant 38 W moyens pour la charge utile (contre 22 W sur un 12U standard) et d'une capacité d'emport de 9,5 kg, "
            "elle permet d'alimenter confortablement un transpondeur bande S, un émetteur bande X et un imageur compact ou une charge utile IoT gourmande "
            "avec une durée de vie nominale de 3,5 ans."
        ),
        "key_features": [
            "Génération solaire renforcée : 58 W orbite / 38 W disponibles pour CU + options",
            "Capacité charge utile 9,5 kg / 7,5 L (compatible imageurs 12–18 cm et IoT lourd)",
            "Durée de vie nominale 3,5 ans, transpondeur bande S inclus",
            "Filière industrielle suédoise (ESA)"
        ],
        "interfaces": [
            "Bus 28 V régulé + rails 5 V / 12 V",
            "SpaceWire, CAN, RS-422, LVDS",
            "Compatible déployeur CubePod 12U/16U"
        ]
    },
    {
        "id": "plat_ital_argocube_27u",
        "supplier_id": "stellare_ottica",
        "supplier_name": "Stellara Ottica",
        "name": "ArgoBus-27U Heavy NanoSat",
        "category": "cubesat_27u",
        "description": "Grand nanosatellite 27U italien optimisé pour l'optique compacte (jusqu'à 18 kg de CU, 4,5 ans)",
        "dry_mass_kg": 18.0,
        "max_payload_mass_kg": 18.0,
        "max_launch_mass_kg": 40.0,
        "payload_volume_liters": 15.0,
        "dimensions_mm": [340.0, 340.0, 340.0],
        "deployed_span_m": 1.65,
        "orbit_avg_power_w": 82.0,
        "payload_avg_power_w": 52.0,
        "payload_peak_power_w": 120.0,
        "bus_voltage_v": 28.0,
        "battery_capacity_wh": 240.0,
        "battery_max_dod": 0.25,
        "pointing_accuracy_deg": 0.03,
        "pointing_stability_arcsec_s": 3.5,
        "slew_rate_deg_s": 2.2,
        "jitter_arcsec": 1.5,
        "payload_thermal_dissipation_w": 55.0,
        "base_price_meur": 1.10,
        "base_lead_time_months": 9,
        "design_lifetime_years": 4.5,
        "rad_tolerance_krad": 22.0,
        "trl": 8,
        "launch_environment_compatible": ["Falcon9_Rideshare", "VegaC_SSMS", "OrbitalShare"],
        "slots": [
            {
                "function": "propulsion",
                "min_qty": 0,
                "max_qty": 1,
                "allowed_equipment_ids": ["prop_coldgas_10u", "prop_pptt_micro", "prop_green_5n", "prop_electric_hall_100w"],
                "included_equipment_ids": ["prop_coldgas_10u"],
                "integration_cost_fixed_meur": 0.06,
                "integration_cost_pct": 8.0
            },
            {
                "function": "ttc",
                "min_qty": 1,
                "max_qty": 1,
                "allowed_equipment_ids": ["ttc_sband_transceiver", "ttc_sband_aurora_it", "ttc_sband_gallia_fr"],
                "included_equipment_ids": ["ttc_sband_aurora_it"],
                "integration_cost_fixed_meur": 0.03,
                "integration_cost_pct": 5.0
            },
            {
                "function": "payload_downlink",
                "min_qty": 0,
                "max_qty": 1,
                "allowed_equipment_ids": ["downlink_sband_hr", "downlink_xband_tx_50mbps", "downlink_xband_tx_150mbps", "downlink_xband_tx", "downlink_xband_milan_it"],
                "included_equipment_ids": [],
                "integration_cost_fixed_meur": 0.05,
                "integration_cost_pct": 8.0
            },
            {
                "function": "mass_memory",
                "min_qty": 1,
                "max_qty": 1,
                "allowed_equipment_ids": ["mass_mem_64gb", "mass_mem_512gb", "mass_mem_1tb"],
                "included_equipment_ids": ["mass_mem_512gb"],
                "integration_cost_fixed_meur": 0.04,
                "integration_cost_pct": 5.0
            },
            {
                "function": "adcs",
                "min_qty": 0,
                "max_qty": 1,
                "allowed_equipment_ids": ["adcs_cubesat_precision", "adcs_high_accuracy_pack", "adcs_leonardo_pack_it"],
                "included_equipment_ids": [],
                "integration_cost_fixed_meur": 0.06,
                "integration_cost_pct": 8.0
            },
            {
                "function": "optical_interface",
                "min_qty": 0,
                "max_qty": 1,
                "allowed_equipment_ids": ["opt_slit_micro_nanosat", "opt_slit_std_vnir", "opt_slit_athermal_ghg"],
                "included_equipment_ids": [],
                "integration_cost_fixed_meur": 0.04,
                "integration_cost_pct": 5.0
            }
        ],
        "image": "platform_cubesat.jpg",
        "long_description": (
            "Plateforme nanosatellite lourde de format 27U (340 × 340 × 340 mm) développée en Italie par Stellara Ottica (inspirée d'Argotec ArgoMoon / LICIACube "
            "et des bus PLATiNO compacts). Elle comble le fossé entre les CubeSats 16U et les microsatellites ESPA : capable d'accueillir un télescope "
            "de 20 à 25 cm (jusqu'à 18 kg et 15 L) avec une précision de pointage native de 0,03° et une durée de vie de 4,5 ans."
        ),
        "key_features": [
            "Format cubique 27U offrant 15 L et 18 kg de capacité charge utile",
            "Pointage natif 0,03° optimisé pour télescopes compacts 18–25 cm",
            "Propulsion gaz froid 10U, TT&C bande S italien et mémoire 512 Go inclus",
            "Durée de vie 4,5 ans (excellente contribution au retour géographique italien)"
        ],
        "interfaces": [
            "Bus 28 V régulé",
            "SpaceWire, SpaceFibre, CAN",
            "Interface anneau léger Rideshare ou déployeur 27U"
        ]
    },
    {
        "id": "plat_iberia_micro90",
        "supplier_id": "space_avionics",
        "supplier_name": "Starlight Avionics",
        "name": "IberiaSat-90 Agile MicroBus",
        "category": "smallsat_90kg",
        "description": "Microsatellite espagnol de classe 90 kg à avionique intégrée pour imagerie optique et télécoms LEO",
        "dry_mass_kg": 48.0,
        "max_payload_mass_kg": 42.0,
        "max_launch_mass_kg": 100.0,
        "payload_volume_liters": 48.0,
        "dimensions_mm": [620.0, 580.0, 680.0],
        "deployed_span_m": 2.1,
        "orbit_avg_power_w": 145.0,
        "payload_avg_power_w": 95.0,
        "payload_peak_power_w": 220.0,
        "bus_voltage_v": 28.0,
        "battery_capacity_wh": 460.0,
        "battery_max_dod": 0.25,
        "pointing_accuracy_deg": 0.012,
        "pointing_stability_arcsec_s": 1.2,
        "slew_rate_deg_s": 2.4,
        "jitter_arcsec": 0.8,
        "payload_thermal_dissipation_w": 85.0,
        "base_price_meur": 2.65,
        "base_lead_time_months": 12,
        "design_lifetime_years": 5.0,
        "rad_tolerance_krad": 28.0,
        "trl": 9,
        "launch_environment_compatible": ["Falcon9_Rideshare", "VegaC_SSMS", "OrbitalShare", "Borealis_Dedicated"],
        "slots": [
            {
                "function": "propulsion",
                "min_qty": 0,
                "max_qty": 1,
                "allowed_equipment_ids": ["prop_coldgas_10u", "prop_green_5n", "prop_electric_hall_100w", "prop_electric_hall_300w", "prop_electric_hemp_de"],
                "included_equipment_ids": ["prop_green_5n"],
                "integration_cost_fixed_meur": 0.12,
                "integration_cost_pct": 8.0
            },
            {
                "function": "ttc",
                "min_qty": 1,
                "max_qty": 1,
                "allowed_equipment_ids": ["ttc_sband_transceiver", "ttc_sband_dual_redundant", "ttc_sband_gallia_fr", "ttc_sband_aurora_it"],
                "included_equipment_ids": ["ttc_sband_transceiver"],
                "integration_cost_fixed_meur": 0.05,
                "integration_cost_pct": 5.0
            },
            {
                "function": "payload_downlink",
                "min_qty": 0,
                "max_qty": 1,
                "allowed_equipment_ids": ["downlink_xband_tx_150mbps", "downlink_xband_tx", "downlink_xband_milan_it", "downlink_xband_toulouse_fr"],
                "included_equipment_ids": ["downlink_xband_tx_150mbps"],
                "integration_cost_fixed_meur": 0.08,
                "integration_cost_pct": 8.0
            },
            {
                "function": "mass_memory",
                "min_qty": 1,
                "max_qty": 1,
                "allowed_equipment_ids": ["mass_mem_512gb", "mass_mem_1tb", "mass_mem_2tb_highrel", "mass_mem_1tb_fr", "mass_mem_1tb_de", "mass_mem_1tb_ch"],
                "included_equipment_ids": ["mass_mem_512gb"],
                "integration_cost_fixed_meur": 0.06,
                "integration_cost_pct": 5.0
            },
            {
                "function": "adcs",
                "min_qty": 0,
                "max_qty": 1,
                "allowed_equipment_ids": ["adcs_high_accuracy_pack", "adcs_agile_wheels_medium", "adcs_sodern_auriga_fr", "adcs_leonardo_pack_it"],
                "included_equipment_ids": [],
                "integration_cost_fixed_meur": 0.10,
                "integration_cost_pct": 8.0
            },
            {
                "function": "optical_interface",
                "min_qty": 0,
                "max_qty": 1,
                "allowed_equipment_ids": ["opt_slit_std_vnir", "opt_slit_athermal_ghg", "opt_slit_wide_mapper"],
                "included_equipment_ids": [],
                "integration_cost_fixed_meur": 0.05,
                "integration_cost_pct": 5.0
            }
        ],
        "image": "platform_smallsat.jpg",
        "long_description": (
            "Plateforme microsatellite agile de 48 kg à sec développée à Madrid par Starlight Avionics (inspirée des plateformes espagnoles "
            "SENER / Satlantis / Deimos). Capable d'emporter jusqu'à 42 kg de charge utile (télescope de 35 cm, chaîne spectrométrique légère ou terminal QKD/laser) "
            "pour un prix de base très compétitif de 2,65 M€, elle constitue un levier idéal pour équilibrer les retours géographiques espagnols et européens."
        ),
        "key_features": [
            "Capacité charge utile 42 kg / 48 L pour une masse sèche contenue à 48 kg",
            "95 W moyens pour la charge utile, durée de vie nominale 5,0 ans",
            "Propulsion verte 5 N, TT&C bande S, émetteur X 150 Mbps et mémoire 512 Go inclus",
            "Filière industrielle espagnole (ESA)"
        ],
        "interfaces": [
            "Bus 28 V régulé",
            "SpaceWire, SpaceFibre, CAN, MIL-STD-1553",
            "Anneau de séparation ESPA 15 pouces"
        ]
    },
    {
        "id": "plat_ital_platino100",
        "supplier_id": "med_radar_ital",
        "supplier_name": "Alba Spazio Radar",
        "name": "AlbaBus-100 All-Electric MicroSat",
        "category": "smallsat_100kg",
        "description": "Plateforme microsatellite italienne 100 kg tout-électrique haute stabilité (inspirée de PLATiNO ASI)",
        "dry_mass_kg": 58.0,
        "max_payload_mass_kg": 55.0,
        "max_launch_mass_kg": 125.0,
        "payload_volume_liters": 62.0,
        "dimensions_mm": [700.0, 650.0, 800.0],
        "deployed_span_m": 2.4,
        "orbit_avg_power_w": 175.0,
        "payload_avg_power_w": 115.0,
        "payload_peak_power_w": 280.0,
        "bus_voltage_v": 28.0,
        "battery_capacity_wh": 580.0,
        "battery_max_dod": 0.25,
        "pointing_accuracy_deg": 0.008,
        "pointing_stability_arcsec_s": 0.9,
        "slew_rate_deg_s": 2.5,
        "jitter_arcsec": 0.6,
        "payload_thermal_dissipation_w": 100.0,
        "base_price_meur": 3.20,
        "base_lead_time_months": 13,
        "design_lifetime_years": 5.5,
        "rad_tolerance_krad": 30.0,
        "trl": 9,
        "launch_environment_compatible": ["Falcon9_Rideshare", "VegaC_SSMS", "OrbitalShare", "Borealis_Dedicated"],
        "slots": [
            {
                "function": "propulsion",
                "min_qty": 1,
                "max_qty": 1,
                "allowed_equipment_ids": ["prop_electric_hall_100w", "prop_electric_hall_300w", "prop_electric_hemp_de", "prop_green_5n", "prop_monoprop_1n"],
                "included_equipment_ids": ["prop_electric_hall_100w"],
                "integration_cost_fixed_meur": 0.12,
                "integration_cost_pct": 8.0
            },
            {
                "function": "ttc",
                "min_qty": 1,
                "max_qty": 1,
                "allowed_equipment_ids": ["ttc_sband_aurora_it", "ttc_sband_transceiver", "ttc_sband_dual_redundant", "ttc_sband_gallia_fr"],
                "included_equipment_ids": ["ttc_sband_aurora_it"],
                "integration_cost_fixed_meur": 0.05,
                "integration_cost_pct": 5.0
            },
            {
                "function": "payload_downlink",
                "min_qty": 1,
                "max_qty": 1,
                "allowed_equipment_ids": ["downlink_xband_tx_150mbps", "downlink_xband_tx", "downlink_xband_milan_it", "downlink_xband_toulouse_fr", "downlink_kaband_tx_2gbps"],
                "included_equipment_ids": ["downlink_xband_milan_it"],
                "integration_cost_fixed_meur": 0.08,
                "integration_cost_pct": 8.0
            },
            {
                "function": "mass_memory",
                "min_qty": 1,
                "max_qty": 1,
                "allowed_equipment_ids": ["mass_mem_512gb", "mass_mem_1tb", "mass_mem_2tb_highrel", "mass_mem_1tb_fr", "mass_mem_1tb_de", "mass_mem_1tb_ch"],
                "included_equipment_ids": ["mass_mem_1tb"],
                "integration_cost_fixed_meur": 0.08,
                "integration_cost_pct": 5.0
            },
            {
                "function": "adcs",
                "min_qty": 0,
                "max_qty": 1,
                "allowed_equipment_ids": ["adcs_high_accuracy_pack", "adcs_leonardo_pack_it", "adcs_sodern_auriga_fr", "adcs_agile_wheels_medium", "adcs_cmg_agility_pack"],
                "included_equipment_ids": [],
                "integration_cost_fixed_meur": 0.12,
                "integration_cost_pct": 8.0
            },
            {
                "function": "optical_interface",
                "min_qty": 0,
                "max_qty": 1,
                "allowed_equipment_ids": ["opt_slit_std_vnir", "opt_slit_athermal_ghg", "opt_slit_wide_mapper"],
                "included_equipment_ids": [],
                "integration_cost_fixed_meur": 0.06,
                "integration_cost_pct": 5.0
            }
        ],
        "image": "platform_smallsat.jpg",
        "long_description": (
            "Plateforme microsatellite italienne tout-électrique de classe 100 kg développée sous l'égide de l'Agence Spatiale Italienne (inspirée de SITAEL / Thales Alenia Space PLATiNO). "
            "Équipée de série d'un propulseur à effet Hall de 100 W, d'un émetteur bande X italien à 600 Mbit/s et d'un enregistreur de 1 To, "
            "elle accueille jusqu'à 55 kg de charge utile (télescopes sub-métriques de 35 à 45 cm, spectromètres ou terminaux laser/QKD) pour une durée de vie de 5,5 ans."
        ),
        "key_features": [
            "Capacité charge utile 55 kg / 62 L, puissance CU 115 W moyens",
            "Pointage de base 0,008° (extensible à 0,003° avec pack ADCS)",
            "Propulseur Hall 100 W, émetteur X 600 Mbps italien et SSR 1 To inclus de série",
            "Durée de vie 5,5 ans, maîtrise d'œuvre italienne (ASI/ESA)"
        ],
        "interfaces": [
            "Bus 28 V régulé",
            "SpaceWire, SpaceFibre, MIL-STD-1553B, CAN",
            "Compatible Vega-C SSMS et Rideshare ESPA"
        ]
    },
    {
        "id": "plat_bavaria_reflex180",
        "supplier_id": "euro_sar_prime",
        "supplier_name": "Aegis Radar & Defense",
        "name": "BavariaBus-180 High-Density",
        "category": "smallsat_180kg",
        "description": "Plateforme microsatellite allemande 180 kg à forte densité énergétique (260 W CU, 7,0 ans)",
        "dry_mass_kg": 95.0,
        "max_payload_mass_kg": 90.0,
        "max_launch_mass_kg": 210.0,
        "payload_volume_liters": 115.0,
        "dimensions_mm": [880.0, 820.0, 1020.0],
        "deployed_span_m": 3.4,
        "orbit_avg_power_w": 380.0,
        "payload_avg_power_w": 260.0,
        "payload_peak_power_w": 650.0,
        "bus_voltage_v": 28.0,
        "battery_capacity_wh": 1150.0,
        "battery_max_dod": 0.25,
        "pointing_accuracy_deg": 0.006,
        "pointing_stability_arcsec_s": 0.6,
        "slew_rate_deg_s": 2.6,
        "jitter_arcsec": 0.5,
        "payload_thermal_dissipation_w": 210.0,
        "base_price_meur": 5.10,
        "base_lead_time_months": 15,
        "design_lifetime_years": 7.0,
        "rad_tolerance_krad": 40.0,
        "trl": 9,
        "launch_environment_compatible": ["Falcon9_Rideshare", "VegaC_SSMS", "OrbitalShare", "Borealis_Dedicated", "Ariane6_Dual"],
        "slots": [
            {
                "function": "propulsion",
                "min_qty": 1,
                "max_qty": 1,
                "allowed_equipment_ids": ["prop_electric_hemp_de", "prop_electric_hall_300w", "prop_ion_500w", "prop_monoprop_1n", "prop_green_5n"],
                "included_equipment_ids": ["prop_electric_hemp_de"],
                "integration_cost_fixed_meur": 0.15,
                "integration_cost_pct": 8.0
            },
            {
                "function": "ttc",
                "min_qty": 1,
                "max_qty": 1,
                "allowed_equipment_ids": ["ttc_sband_transceiver", "ttc_sband_dual_redundant", "ttc_xband_tmtc", "ttc_sband_gallia_fr", "ttc_sband_aurora_it"],
                "included_equipment_ids": ["ttc_sband_dual_redundant"],
                "integration_cost_fixed_meur": 0.06,
                "integration_cost_pct": 5.0
            },
            {
                "function": "payload_downlink",
                "min_qty": 1,
                "max_qty": 1,
                "allowed_equipment_ids": ["downlink_xband_tx", "downlink_xband_tx_1200mbps", "downlink_kaband_tx_2gbps", "downlink_xband_toulouse_fr", "downlink_xband_milan_it"],
                "included_equipment_ids": ["downlink_xband_tx"],
                "integration_cost_fixed_meur": 0.10,
                "integration_cost_pct": 8.0
            },
            {
                "function": "mass_memory",
                "min_qty": 1,
                "max_qty": 1,
                "allowed_equipment_ids": ["mass_mem_1tb", "mass_mem_2tb_highrel", "mass_mem_1tb_de", "mass_mem_2tb_de", "mass_mem_1tb_fr", "mass_mem_1tb_ch"],
                "included_equipment_ids": ["mass_mem_1tb_de"],
                "integration_cost_fixed_meur": 0.08,
                "integration_cost_pct": 5.0
            },
            {
                "function": "adcs",
                "min_qty": 0,
                "max_qty": 1,
                "allowed_equipment_ids": ["adcs_high_accuracy_pack", "adcs_agile_wheels_medium", "adcs_cmg_agility_pack", "adcs_ultra_stable", "adcs_sodern_auriga_fr", "adcs_leonardo_pack_it"],
                "included_equipment_ids": [],
                "integration_cost_fixed_meur": 0.15,
                "integration_cost_pct": 8.0
            },
            {
                "function": "optical_interface",
                "min_qty": 0,
                "max_qty": 1,
                "allowed_equipment_ids": ["opt_slit_std_vnir", "opt_slit_athermal_ghg", "opt_slit_wide_mapper"],
                "included_equipment_ids": [],
                "integration_cost_fixed_meur": 0.06,
                "integration_cost_pct": 5.0
            }
        ],
        "image": "platform_smallsat.jpg",
        "long_description": (
            "Plateforme microsatellite allemande de haute densité développée à Munich et Brême (inspirée des bus OHB Tet-1/BiROS et Reflex Aerospace). "
            "Avec 90 kg de capacité d'emport charge utile, 260 W de puissance moyenne disponible et une durée de vie nominale de 7,0 ans, "
            "elle embarque de série la propulsion plasmique allemande HEMP-300 et une mémoire SpectraStore de 1 To. Idéale pour les missions optiques "
            "sub-métriques (35 à 45 cm), les missions atmosphériques multi-instruments et les relais optiques laser."
        ),
        "key_features": [
            "Capacité charge utile 90 kg / 115 L, puissance disponible 260 W moyens",
            "Durée de vie nominale 7,0 ans, tolérance radiative 40 krad",
            "Propulsion HEMP-300, TT&C redondé, émetteur X 500 Mbps et mémoire 1 To allemands inclus",
            "Maîtrise d'œuvre allemande (idéale pour les quotas ESA Allemagne)"
        ],
        "interfaces": [
            "Bus 28 V / 50 V régulé",
            "SpaceFibre, SpaceWire, MIL-STD-1553B",
            "Anneau ESPA Grande 24 pouces"
        ]
    },
    {
        "id": "plat_ital_prima220",
        "supplier_id": "stellare_ottica",
        "supplier_name": "Stellara Ottica",
        "name": "AlbaBus-220 Multi-Mission",
        "category": "smallsat_220kg",
        "description": "Minisatellite italien multi-mission de classe 220 kg (CU max 105 kg, 7,0 ans, héritage PRISMA)",
        "dry_mass_kg": 115.0,
        "max_payload_mass_kg": 105.0,
        "max_launch_mass_kg": 250.0,
        "payload_volume_liters": 140.0,
        "dimensions_mm": [950.0, 900.0, 1150.0],
        "deployed_span_m": 3.6,
        "orbit_avg_power_w": 360.0,
        "payload_avg_power_w": 240.0,
        "payload_peak_power_w": 600.0,
        "bus_voltage_v": 28.0,
        "battery_capacity_wh": 1200.0,
        "battery_max_dod": 0.25,
        "pointing_accuracy_deg": 0.005,
        "pointing_stability_arcsec_s": 0.5,
        "slew_rate_deg_s": 2.4,
        "jitter_arcsec": 0.45,
        "payload_thermal_dissipation_w": 200.0,
        "base_price_meur": 5.50,
        "base_lead_time_months": 15,
        "design_lifetime_years": 7.0,
        "rad_tolerance_krad": 40.0,
        "trl": 9,
        "launch_environment_compatible": ["Falcon9_Rideshare", "VegaC_SSMS", "Borealis_Dedicated", "Ariane6_Dual"],
        "slots": [
            {
                "function": "propulsion",
                "min_qty": 1,
                "max_qty": 1,
                "allowed_equipment_ids": ["prop_monoprop_1n", "prop_green_5n", "prop_electric_hall_300w", "prop_electric_hemp_de", "prop_ion_500w"],
                "included_equipment_ids": ["prop_monoprop_1n"],
                "integration_cost_fixed_meur": 0.15,
                "integration_cost_pct": 8.0
            },
            {
                "function": "ttc",
                "min_qty": 1,
                "max_qty": 1,
                "allowed_equipment_ids": ["ttc_sband_aurora_it", "ttc_sband_dual_redundant", "ttc_xband_tmtc", "ttc_sband_gallia_fr"],
                "included_equipment_ids": ["ttc_sband_aurora_it"],
                "integration_cost_fixed_meur": 0.06,
                "integration_cost_pct": 5.0
            },
            {
                "function": "payload_downlink",
                "min_qty": 1,
                "max_qty": 1,
                "allowed_equipment_ids": ["downlink_xband_milan_it", "downlink_kaband_milan_it", "downlink_xband_tx", "downlink_xband_tx_1200mbps", "downlink_kaband_tx_2gbps", "downlink_xband_toulouse_fr"],
                "included_equipment_ids": ["downlink_xband_milan_it"],
                "integration_cost_fixed_meur": 0.10,
                "integration_cost_pct": 8.0
            },
            {
                "function": "mass_memory",
                "min_qty": 1,
                "max_qty": 1,
                "allowed_equipment_ids": ["mass_mem_1tb", "mass_mem_2tb_highrel", "mass_mem_1tb_fr", "mass_mem_1tb_de", "mass_mem_2tb_de", "mass_mem_1tb_ch"],
                "included_equipment_ids": ["mass_mem_1tb"],
                "integration_cost_fixed_meur": 0.08,
                "integration_cost_pct": 5.0
            },
            {
                "function": "adcs",
                "min_qty": 0,
                "max_qty": 1,
                "allowed_equipment_ids": ["adcs_leonardo_pack_it", "adcs_sodern_auriga_fr", "adcs_agile_wheels_medium", "adcs_cmg_agility_pack", "adcs_ultra_stable"],
                "included_equipment_ids": [],
                "integration_cost_fixed_meur": 0.15,
                "integration_cost_pct": 8.0
            },
            {
                "function": "optical_interface",
                "min_qty": 0,
                "max_qty": 1,
                "allowed_equipment_ids": ["opt_slit_std_vnir", "opt_slit_athermal_ghg", "opt_slit_wide_mapper"],
                "included_equipment_ids": [],
                "integration_cost_fixed_meur": 0.06,
                "integration_cost_pct": 5.0
            }
        ],
        "image": "platform_smallsat.jpg",
        "long_description": (
            "Plateforme minisatellite italienne de classe 220 kg dérivée de la lignée PRISMA / MITA de l'Agence Spatiale Italienne. "
            "Dotée d'un plateau optique thermo-stable capable de porter jusqu'à 105 kg de charge utile (télescopes Korsch de 45 à 60 cm ou "
            "combinaison télescope + spectromètre SWIR complet), elle offre un pointage natif de 0,005° et une durée de vie de 7,0 ans."
        ),
        "key_features": [
            "Capacité charge utile 105 kg / 140 L (compatible STELLA-60 et chaînes hyperspectrales complètes)",
            "Pointage natif 0,005° (0,5 arcsec/s), durée de vie 7,0 ans",
            "Propulsion hydrazine 1 N, TT&C italien redondé, émetteur X 600 Mbps et SSR 1 To inclus",
            "Maîtrise d'œuvre italienne (Stellara Ottica)"
        ],
        "interfaces": [
            "Bus 28 V régulé",
            "SpaceFibre, SpaceWire, MIL-STD-1553B",
            "Adaptateur Vega-C / Falcon 9 Rideshare"
        ]
    },
    {
        "id": "plat_bavaria_sar450",
        "supplier_id": "euro_sar_prime",
        "supplier_name": "Aegis Radar & Defense",
        "name": "BavariaBus-450 SAR & Dawn-Dusk",
        "category": "smallsat_450kg",
        "description": "Plateforme allemande 450 kg haute puissance (780 W CU, 1,8 kW crête) optimisée pour radars SAR et imagerie THR",
        "dry_mass_kg": 230.0,
        "max_payload_mass_kg": 210.0,
        "max_launch_mass_kg": 500.0,
        "payload_volume_liters": 290.0,
        "dimensions_mm": [1350.0, 1150.0, 1550.0],
        "deployed_span_m": 5.2,
        "orbit_avg_power_w": 1050.0,
        "payload_avg_power_w": 780.0,
        "payload_peak_power_w": 1850.0,
        "bus_voltage_v": 50.0,
        "battery_capacity_wh": 3400.0,
        "battery_max_dod": 0.30,
        "pointing_accuracy_deg": 0.004,
        "pointing_stability_arcsec_s": 0.4,
        "slew_rate_deg_s": 2.8,
        "jitter_arcsec": 0.35,
        "payload_thermal_dissipation_w": 550.0,
        "base_price_meur": 8.90,
        "base_lead_time_months": 18,
        "design_lifetime_years": 8.0,
        "rad_tolerance_krad": 50.0,
        "trl": 9,
        "launch_environment_compatible": ["Falcon9_Rideshare", "VegaC_SSMS", "Ariane6_Dual", "EuroLaunch_Medium"],
        "slots": [
            {
                "function": "propulsion",
                "min_qty": 1,
                "max_qty": 1,
                "allowed_equipment_ids": ["prop_electric_hemp_de", "prop_electric_hall_300w", "prop_ion_500w", "prop_electric_hall_1kw", "prop_monoprop_1n", "prop_biprop_400n"],
                "included_equipment_ids": ["prop_electric_hemp_de"],
                "integration_cost_fixed_meur": 0.22,
                "integration_cost_pct": 10.0
            },
            {
                "function": "ttc",
                "min_qty": 1,
                "max_qty": 1,
                "allowed_equipment_ids": ["ttc_sband_dual_redundant", "ttc_xband_tmtc", "ttc_sband_gallia_fr", "ttc_sband_aurora_it"],
                "included_equipment_ids": ["ttc_sband_dual_redundant"],
                "integration_cost_fixed_meur": 0.08,
                "integration_cost_pct": 5.0
            },
            {
                "function": "payload_downlink",
                "min_qty": 1,
                "max_qty": 1,
                "allowed_equipment_ids": ["downlink_xband_tx", "downlink_xband_tx_1200mbps", "downlink_kaband_tx_2gbps", "downlink_xband_toulouse_fr", "downlink_xband_milan_it", "downlink_kaband_milan_it"],
                "included_equipment_ids": ["downlink_xband_tx_1200mbps"],
                "integration_cost_fixed_meur": 0.14,
                "integration_cost_pct": 8.0
            },
            {
                "function": "mass_memory",
                "min_qty": 1,
                "max_qty": 1,
                "allowed_equipment_ids": ["mass_mem_1tb_de", "mass_mem_2tb_de", "mass_mem_2tb_highrel", "mass_mem_8tb", "mass_mem_1tb_fr", "mass_mem_1tb_ch"],
                "included_equipment_ids": ["mass_mem_2tb_de"],
                "integration_cost_fixed_meur": 0.10,
                "integration_cost_pct": 5.0
            },
            {
                "function": "adcs",
                "min_qty": 0,
                "max_qty": 1,
                "allowed_equipment_ids": ["adcs_agile_wheels_medium", "adcs_cmg_agility_pack", "adcs_ultra_stable", "adcs_sodern_auriga_fr", "adcs_leonardo_pack_it"],
                "included_equipment_ids": [],
                "integration_cost_fixed_meur": 0.18,
                "integration_cost_pct": 10.0
            },
            {
                "function": "optical_interface",
                "min_qty": 0,
                "max_qty": 1,
                "allowed_equipment_ids": ["opt_slit_std_vnir", "opt_slit_athermal_ghg", "opt_slit_wide_mapper"],
                "included_equipment_ids": [],
                "integration_cost_fixed_meur": 0.08,
                "integration_cost_pct": 5.0
            }
        ],
        "image": "platform_medium.jpg",
        "long_description": (
            "Plateforme minisatellite lourde allemande de 230 kg à sec conçue par Aegis Radar & Defense sur l'héritage TerraSAR-X / TanDEM-X. "
            "Sa structure hexagonale rigide et son bus 50 V de 1 050 W moyens (780 W disponibles pour la charge utile, 1 850 W crête) "
            "sont taillés pour supporter les antennes SAR actives à forte dissipation thermique (jusqu'à 550 W) ou les télescopes de 60 à 70 cm sur 8 ans."
        ),
        "key_features": [
            "Puissance exceptionnelle pour SAR : 780 W moyens CU / 1 850 W crête / batterie 3,4 kWh",
            "Capacité charge utile 210 kg / 290 L, dissipation thermique 550 W",
            "Propulsion HEMP-300, émetteur X 1,2 Gbps et mémoire 2 To allemands inclus de série",
            "Durée de vie 8,0 ans, pointage natif 0,004°"
        ],
        "interfaces": [
            "Bus primaire 50 V régulé haute intensité",
            "SpaceFibre 4 voies, MIL-STD-1553B",
            "Panneau latéral renforcé pour déploiement d'antenne SAR"
        ]
    },
    {
        "id": "plat_ital_cosmo600",
        "supplier_id": "med_radar_ital",
        "supplier_name": "Alba Spazio Radar",
        "name": "AlbaBus-600 High-Stability Science & EO",
        "category": "medium_600kg",
        "description": "Plateforme moyenne italienne 600 kg ultra-stable pour grands télescopes d'astrophysique/EO et radars lourds (8,5 ans)",
        "dry_mass_kg": 310.0,
        "max_payload_mass_kg": 280.0,
        "max_launch_mass_kg": 680.0,
        "payload_volume_liters": 420.0,
        "dimensions_mm": [1650.0, 1400.0, 1850.0],
        "deployed_span_m": 6.0,
        "orbit_avg_power_w": 920.0,
        "payload_avg_power_w": 620.0,
        "payload_peak_power_w": 1600.0,
        "bus_voltage_v": 50.0,
        "battery_capacity_wh": 3800.0,
        "battery_max_dod": 0.30,
        "pointing_accuracy_deg": 0.003,
        "pointing_stability_arcsec_s": 0.25,
        "slew_rate_deg_s": 2.2,
        "jitter_arcsec": 0.2,
        "payload_thermal_dissipation_w": 520.0,
        "base_price_meur": 11.20,
        "base_lead_time_months": 20,
        "design_lifetime_years": 8.5,
        "rad_tolerance_krad": 60.0,
        "trl": 9,
        "launch_environment_compatible": ["Falcon9_Rideshare", "VegaC_SSMS", "Ariane6_Dual", "EuroLaunch_Medium"],
        "slots": [
            {
                "function": "propulsion",
                "min_qty": 1,
                "max_qty": 1,
                "allowed_equipment_ids": ["prop_monoprop_1n", "prop_biprop_400n", "prop_electric_hall_300w", "prop_ion_500w", "prop_electric_hall_1kw", "prop_electric_hemp_de"],
                "included_equipment_ids": ["prop_monoprop_1n"],
                "integration_cost_fixed_meur": 0.25,
                "integration_cost_pct": 10.0
            },
            {
                "function": "ttc",
                "min_qty": 1,
                "max_qty": 1,
                "allowed_equipment_ids": ["ttc_sband_aurora_it", "ttc_sband_dual_redundant", "ttc_xband_tmtc", "ttc_sband_gallia_fr"],
                "included_equipment_ids": ["ttc_sband_aurora_it"],
                "integration_cost_fixed_meur": 0.08,
                "integration_cost_pct": 5.0
            },
            {
                "function": "payload_downlink",
                "min_qty": 1,
                "max_qty": 1,
                "allowed_equipment_ids": ["downlink_xband_milan_it", "downlink_kaband_milan_it", "downlink_xband_tx_1200mbps", "downlink_kaband_tx_2gbps", "downlink_xband_toulouse_fr"],
                "included_equipment_ids": ["downlink_xband_milan_it"],
                "integration_cost_fixed_meur": 0.15,
                "integration_cost_pct": 8.0
            },
            {
                "function": "mass_memory",
                "min_qty": 1,
                "max_qty": 1,
                "allowed_equipment_ids": ["mass_mem_2tb_highrel", "mass_mem_8tb", "mass_mem_1tb_fr", "mass_mem_1tb_de", "mass_mem_2tb_de", "mass_mem_1tb_ch"],
                "included_equipment_ids": ["mass_mem_2tb_highrel"],
                "integration_cost_fixed_meur": 0.12,
                "integration_cost_pct": 5.0
            },
            {
                "function": "adcs",
                "min_qty": 0,
                "max_qty": 1,
                "allowed_equipment_ids": ["adcs_leonardo_pack_it", "adcs_sodern_auriga_fr", "adcs_agile_wheels_medium", "adcs_cmg_agility_pack", "adcs_ultra_stable"],
                "included_equipment_ids": [],
                "integration_cost_fixed_meur": 0.20,
                "integration_cost_pct": 10.0
            },
            {
                "function": "optical_interface",
                "min_qty": 0,
                "max_qty": 1,
                "allowed_equipment_ids": ["opt_slit_std_vnir", "opt_slit_athermal_ghg", "opt_slit_wide_mapper"],
                "included_equipment_ids": [],
                "integration_cost_fixed_meur": 0.08,
                "integration_cost_pct": 5.0
            }
        ],
        "image": "platform_medium.jpg",
        "long_description": (
            "Plateforme de classe moyenne (310 kg à sec, 280 kg de charge utile) développée à Turin et Rome sur l'héritage COSMO-SkyMed et Euclid. "
            "Son architecture à découplage micro-vibratoire et isolation thermique multicouche garantit une stabilité de pointage native de 0,25 arcsec/s "
            "(précision 0,003°) et une durée de vie de 8,5 ans. Elle constitue la plateforme italienne de référence pour les missions de cosmologie "
            "(STELLA-60 / EagleEye-70), d'observation optique THR ou de radar SAR institutionnel."
        ),
        "key_features": [
            "Capacité charge utile 280 kg / 420 L, puissance 620 W moyens",
            "Haute stabilité native : pointage 0,003°, dérive 0,25 arcsec/s, jitter 0,20 arcsec",
            "Durée de vie 8,5 ans (conforme aux exigences scientifiques longue durée)",
            "Maîtrise d'œuvre italienne (Alba Spazio Radar)"
        ],
        "interfaces": [
            "Bus 50 V régulé",
            "SpaceFibre redondé, MIL-STD-1553B",
            "Interface lanceur Vega-C / Ariane 6 / Rideshare lourd"
        ]
    },
    {
        "id": "plat_bavaria_geo1200",
        "supplier_id": "euro_sar_prime",
        "supplier_name": "Aegis Radar & Defense",
        "name": "LuxorGEO-1200 Modular Telecom Bus",
        "category": "geo_compact",
        "description": "Plateforme géostationnaire compacte allemande (classe SmallGEO / Electra, 320 kg CU, 2,6 kW CU, 15 ans)",
        "dry_mass_kg": 640.0,
        "max_payload_mass_kg": 320.0,
        "max_launch_mass_kg": 1380.0,
        "payload_volume_liters": 900.0,
        "dimensions_mm": [2100.0, 1850.0, 2400.0],
        "deployed_span_m": 15.5,
        "orbit_avg_power_w": 3600.0,
        "payload_avg_power_w": 2600.0,
        "payload_peak_power_w": 4200.0,
        "bus_voltage_v": 100.0,
        "battery_capacity_wh": 14500.0,
        "battery_max_dod": 0.65,
        "pointing_accuracy_deg": 0.008,
        "pointing_stability_arcsec_s": 0.6,
        "slew_rate_deg_s": 0.6,
        "jitter_arcsec": 0.5,
        "payload_thermal_dissipation_w": 2200.0,
        "base_price_meur": 19.80,
        "base_lead_time_months": 24,
        "design_lifetime_years": 15.0,
        "rad_tolerance_krad": 100.0,
        "trl": 9,
        "launch_environment_compatible": ["Ariane6_GTO", "Falcon9_GTO", "Heavy_GEO"],
        "slots": [
            {
                "function": "propulsion",
                "min_qty": 1,
                "max_qty": 1,
                "allowed_equipment_ids": ["prop_electric_hall_1kw", "prop_chemical_biprop_400n_de", "prop_biprop_400n", "prop_ion_500w"],
                "included_equipment_ids": ["prop_chemical_biprop_400n_de"],
                "integration_cost_fixed_meur": 0.35,
                "integration_cost_pct": 10.0
            },
            {
                "function": "ttc",
                "min_qty": 1,
                "max_qty": 1,
                "allowed_equipment_ids": ["ttc_sband_dual_redundant", "ttc_xband_tmtc", "ttc_sband_gallia_fr", "ttc_sband_aurora_it"],
                "included_equipment_ids": ["ttc_sband_dual_redundant"],
                "integration_cost_fixed_meur": 0.10,
                "integration_cost_pct": 5.0
            },
            {
                "function": "payload_downlink",
                "min_qty": 0,
                "max_qty": 1,
                "allowed_equipment_ids": ["downlink_xband_tx_1200mbps", "downlink_kaband_tx_2gbps", "downlink_kaband_milan_it"],
                "included_equipment_ids": [],
                "integration_cost_fixed_meur": 0.15,
                "integration_cost_pct": 8.0
            },
            {
                "function": "mass_memory",
                "min_qty": 1,
                "max_qty": 1,
                "allowed_equipment_ids": ["mass_mem_1tb_de", "mass_mem_2tb_de", "mass_mem_1tb_ch", "mass_mem_1tb_fr", "mass_mem_2tb_highrel"],
                "included_equipment_ids": ["mass_mem_1tb_de"],
                "integration_cost_fixed_meur": 0.10,
                "integration_cost_pct": 5.0
            },
            {
                "function": "adcs",
                "min_qty": 0,
                "max_qty": 1,
                "allowed_equipment_ids": ["adcs_agile_wheels_medium", "adcs_ultra_stable", "adcs_sodern_auriga_fr", "adcs_leonardo_pack_it"],
                "included_equipment_ids": [],
                "integration_cost_fixed_meur": 0.20,
                "integration_cost_pct": 8.0
            },
            {
                "function": "optical_interface",
                "min_qty": 0,
                "max_qty": 1,
                "allowed_equipment_ids": ["opt_slit_std_vnir", "opt_slit_wide_mapper"],
                "included_equipment_ids": [],
                "integration_cost_fixed_meur": 0.10,
                "integration_cost_pct": 5.0
            }
        ],
        "image": "platform_heavy.jpg",
        "long_description": (
            "Plateforme géostationnaire compacte allemande développée dans le cadre du programme ESA ARTES SmallGEO (inspirée de la plateforme OHB Luxor / Hispasat 36W-1). "
            "Capable d'emporter jusqu'à 320 kg et 2,6 kW de charge utile télécom en restant sous la limite de 1 400 kg au lancement (compatible avec le créneau "
            "GTO Rideshare à 14,50 M€), elle inclut de série le moteur d'apogée bi-ergol allemand 400 N et offre une alternative industrielle allemande aux bus GEO français."
        ),
        "key_features": [
            "Capacité charge utile GEO 320 kg / 2 600 W moyens, masse max au lancement 1 380 kg",
            "Compatible lancement partagé GTO Rideshare (≤ 1 400 kg)",
            "Durée de vie 15,0 ans en GEO, blindage 100 krad, moteur d'apogée 400 N allemand inclus",
            "Maîtrise d'œuvre allemande (programme ESA SmallGEO)"
        ],
        "interfaces": [
            "Bus 100 V régulé haute puissance",
            "MIL-STD-1553B, SpaceWire, SpaceFibre",
            "Adaptateur standard 1194 mm GTO"
        ]
    }
]


def update_suppliers_and_platforms() -> None:
    sup_path = CAT_DIR / "suppliers.json"
    suppliers = json.loads(sup_path.read_text(encoding="utf-8"))
    for s in suppliers:
        if s["id"] in NEW_PLATFORM_SUPPLIERS:
            if "platform" not in s["categories"]:
                s["categories"].insert(0, "platform")
    sup_path.write_text(json.dumps(suppliers, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("Updated suppliers.json with new platform suppliers")

    plat_path = CAT_DIR / "platforms.json"
    platforms = json.loads(plat_path.read_text(encoding="utf-8"))
    existing_ids = {p["id"] for p in platforms}
    added = 0
    for np in NEW_PLATFORMS:
        if np["id"] in existing_ids:
            # replace
            for i, p in enumerate(platforms):
                if p["id"] == np["id"]:
                    platforms[i] = np
                    break
        else:
            platforms.append(np)
            added += 1
    plat_path.write_text(json.dumps(platforms, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Updated platforms.json: added {added} new platforms (total = {len(platforms)})")


if __name__ == "__main__":
    update_payloads_and_bridge()
    update_suppliers_and_platforms()
