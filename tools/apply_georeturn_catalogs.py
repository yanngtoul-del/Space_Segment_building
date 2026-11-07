"""Update suppliers.json with clean country names and expand equipment.json and platforms.json with multi-country European options."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAT_DIR = ROOT / "data" / "catalogs"

SUPPLIER_COUNTRIES = {
    "newspace_micro": "Pays-Bas",
    "sstl_inspired": "Royaume-Uni",
    "heritage_aero": "France",
    "apex_inspired": "États-Unis",
    "heritage_prime": "France",
    "orbital_prop": "France",
    "comms_euro": "Allemagne",
    "space_avionics": "Espagne",
    "gyro_dyn": "Allemagne",
    "optics_lab": "Pays-Bas",
    "heritage_optics": "France",
    "stellare_ottica": "Italie",
    "cirrus_ir": "États-Unis",
    "spectra_tech": "Allemagne",
    "radar_tech": "Finlande",
    "boreal_sar": "Canada",
    "laser_space": "Allemagne",
    "tesa_link": "Allemagne",
    "quanta_space": "Autriche",
    "rf_payload": "Italie",
    "launch_global": "États-Unis",
    "heritage_launch": "France",
    "polar_launch": "Norvège",
    "euro_sar_prime": "Allemagne",
    "zephyr_microsar": "États-Unis",
    "med_radar_ital": "Italie",
    "nordic_nanocomm": "Suède",
    "gallia_satcom": "France",
    "celestia_broadband": "États-Unis",
    "helvetia_microwave": "Suisse",
    "celeste_photonics": "France",
    "nippon_optolink": "Japon",
    "lumina_hyperspec": "Belgique",
    "atmo_science_eu": "France",
    "edelweiss_quantum": "Suisse",
    "albion_quantum_optics": "Royaume-Uni",
}

COUNTRY_CODES = {
    "France": "FR",
    "Allemagne": "DE",
    "Italie": "IT",
    "Espagne": "ES",
    "Royaume-Uni": "UK",
    "Suisse": "CH",
    "Belgique": "BE",
    "Pays-Bas": "NL",
    "Suède": "SE",
    "Finlande": "FI",
    "Autriche": "AT",
    "Norvège": "NO",
    "États-Unis": "US",
    "Canada": "CA",
    "Japon": "JP",
}

NEW_EQUIPMENTS = [
    {
        "id": "ttc_sband_gallia_fr",
        "supplier_id": "gallia_satcom",
        "supplier_name": "Gallia SatCom Payloads",
        "name": "GalliaLink S-Band Transceiver",
        "function": "ttc",
        "description": "Transpondeur TM/TC bande S souverain conforme aux standards ECSS / CNES (France)",
        "mass_kg": 2.0,
        "power_w": 10.0,
        "peak_power_w": 25.0,
        "standby_power_w": 2.5,
        "volume_liters": 1.2,
        "price_meur": 0.28,
        "trl": 9,
        "specs": {"data_rate_kbps": 2048.0, "frequency_band": "S-Band", "rf_power_w": 5.0},
        "image": "equip_avionics_tmtc.jpg",
        "dimensions_mm": [160, 120, 85],
        "long_description": "Équipement de télémesure et télécommande (TM/TC) bande S développé en France (Toulouse) sous qualification CNES. Il assure la liaison de servitudes bord-sol sécurisée avec modulation BPSK/QPSK et codage LDPC conforme CCSDS.",
        "key_features": ["Conçu et fabriqué en France", "TRL 9 avec héritage sur plus de 40 missions", "Compatibilité totale réseaux 2 GHz ESA/CNES/NASA"],
        "interfaces": ["Alimentation bus 28 V / 50 V", "Liaisons série RS-422 et bus CAN", "Connecteurs RF SMA / N"],
    },
    {
        "id": "ttc_sband_aurora_it",
        "supplier_id": "rf_payload",
        "supplier_name": "Meridian RF Payloads",
        "name": "AlbaLink S-Band Redundant Transceiver",
        "function": "ttc",
        "description": "Transpondeur TM/TC bande S à double récepteur redondé développé en Italie (ASI heritage)",
        "mass_kg": 1.9,
        "power_w": 9.0,
        "peak_power_w": 22.0,
        "standby_power_w": 2.0,
        "volume_liters": 1.1,
        "price_meur": 0.26,
        "trl": 9,
        "specs": {"data_rate_kbps": 2048.0, "frequency_band": "S-Band", "rf_power_w": 4.5},
        "image": "equip_avionics_tmtc.jpg",
        "dimensions_mm": [155, 115, 80],
        "long_description": "Transpondeur de télécommande et télémesure développé en Italie (Milan/Rome) qualifié pour les missions de l'Agence Spatiale Italienne (ASI) et de l'ESA. Architecture entièrement redondée à chaud sur les voies de réception.",
        "key_features": ["Conçu et fabriqué en Italie", "Double récepteur redondé à chaud", "Consommation très optimisée (9 W)"],
        "interfaces": ["Bus 28 V régulé", "Bus SpaceWire / CAN", "Connecteurs SMA"],
    },
    {
        "id": "downlink_xband_toulouse_fr",
        "supplier_id": "gallia_satcom",
        "supplier_name": "Gallia SatCom Payloads",
        "name": "Gallia-Downlink X-800 High-Rate Transmitter",
        "function": "payload_downlink",
        "description": "Émetteur de télémesure charge utile bande X à 800 Mbit/s développé en France",
        "mass_kg": 3.4,
        "power_w": 48.0,
        "peak_power_w": 65.0,
        "standby_power_w": 3.0,
        "volume_liters": 2.1,
        "price_meur": 0.58,
        "trl": 9,
        "specs": {"data_rate_mbps": 800.0, "frequency_ghz": 8.2, "rf_power_w": 12.0},
        "image": "equip_telemetry_transmitter.jpg",
        "dimensions_mm": [220, 150, 95],
        "long_description": "Émetteur de données scientifiques et d'imagerie en bande X développé en France. Il délivre 12 W RF sous modulation DVB-S2 / VCM pour un débit utile effectif de 800 Mbit/s vers les stations sol.",
        "key_features": ["Industrie française (Toulouse)", "Débit utile 800 Mbit/s", "Modulation adaptative DVB-S2"],
        "interfaces": ["Alimentation 28 V ou 50 V", "Entrée données SpaceFibre / SpaceWire", "Guide d'ondes WR-112"],
    },
    {
        "id": "downlink_xband_milan_it",
        "supplier_id": "rf_payload",
        "supplier_name": "Meridian RF Payloads",
        "name": "Meridian X-Band 600 Mbps Transmitter",
        "function": "payload_downlink",
        "description": "Émetteur de charge utile bande X 600 Mbit/s compact développé en Italie",
        "mass_kg": 3.1,
        "power_w": 42.0,
        "peak_power_w": 55.0,
        "standby_power_w": 2.5,
        "volume_liters": 1.9,
        "price_meur": 0.52,
        "trl": 9,
        "specs": {"data_rate_mbps": 600.0, "frequency_ghz": 8.1, "rf_power_w": 10.0},
        "image": "equip_telemetry_transmitter.jpg",
        "dimensions_mm": [210, 140, 90],
        "long_description": "Émetteur de données spatiales développé en Italie, optimisé pour les microsatellites d'observation de la Terre nécessitant un écoulement rapide des données de charge utile.",
        "key_features": ["Industrie italienne (Lombardie)", "Débit 600 Mbit/s", "Très bon rendement PAE (> 38 %)"],
        "interfaces": ["Bus 28 V", "Entrée SpaceWire redondée", "Connecteur SMA RF"],
    },
    {
        "id": "downlink_kaband_milan_it",
        "supplier_id": "rf_payload",
        "supplier_name": "Meridian RF Payloads",
        "name": "Meridian-Ka Ultra-Downlink 2.5 Gbps",
        "function": "payload_downlink",
        "description": "Émetteur très haut débit bande Ka (26 GHz) délivrant 2,5 Gbit/s développé en Italie",
        "mass_kg": 5.4,
        "power_w": 72.0,
        "peak_power_w": 95.0,
        "standby_power_w": 4.0,
        "volume_liters": 3.5,
        "price_meur": 1.35,
        "trl": 8,
        "specs": {"data_rate_mbps": 2500.0, "frequency_ghz": 26.5, "rf_power_w": 20.0},
        "image": "equip_telemetry_transmitter.jpg",
        "dimensions_mm": [250, 180, 120],
        "long_description": "Émetteur bande Ka haute puissance conçu en Italie pour les charges utiles d'observation radar et optique très haute résolution générant des dizaines de gigabits par orbite.",
        "key_features": ["Filière spatiale italienne", "Débit record 2,5 Gbit/s", "Amplificateur GaN 20 W RF"],
        "interfaces": ["Bus 50 V régulé", "Liaison SpaceFibre 3,125 Gbit/s", "Bride guide d'ondes WR-34"],
    },
    {
        "id": "mass_mem_1tb_fr",
        "supplier_id": "heritage_aero",
        "supplier_name": "Astra Space Systems",
        "name": "AeroMemory 1 TB Ultra-Reliable Storage",
        "function": "mass_memory",
        "description": "Mémoire de masse flash 1 To durcie aux radiations développée en France",
        "mass_kg": 2.2,
        "power_w": 12.0,
        "peak_power_w": 20.0,
        "standby_power_w": 1.5,
        "volume_liters": 1.5,
        "price_meur": 0.40,
        "trl": 9,
        "specs": {"capacity_gb": 1024.0, "throughput_mbps": 4500.0, "rad_krad": 100.0},
        "image": "equip_avionics_obc.jpg",
        "dimensions_mm": [180, 140, 70],
        "long_description": "Unité de stockage de données de charge utile conçue en France par Astra Space Systems. Intègre une correction d'erreurs EDAC matérielle avancée et un partitionnement dynamique pour sécuriser les acquisitions critiques.",
        "key_features": ["Maîtrise technologique française", "Capacité 1 024 Go utiles", "Débit d'écriture/lecture 4,5 Gbit/s"],
        "interfaces": ["Bus 28 V ou 50 V", "4 ports SpaceWire + 2 SpaceFibre", "Structure aluminium 6061-T6"],
    },
    {
        "id": "mass_mem_1tb_de",
        "supplier_id": "spectra_tech",
        "supplier_name": "SpectraSpace Instruments",
        "name": "SpectraStore 1 TB High-Speed Space Flash",
        "function": "mass_memory",
        "description": "Mémoire de masse haute vitesse 1 To durcie développée en Allemagne",
        "mass_kg": 2.0,
        "power_w": 13.0,
        "peak_power_w": 22.0,
        "standby_power_w": 1.8,
        "volume_liters": 1.4,
        "price_meur": 0.38,
        "trl": 9,
        "specs": {"capacity_gb": 1024.0, "throughput_mbps": 5000.0, "rad_krad": 100.0},
        "image": "equip_avionics_obc.jpg",
        "dimensions_mm": [175, 135, 65],
        "long_description": "Module de mémoire de masse développé à Munich (Allemagne) pour les instruments scientifiques et capteurs d'observation. Conception modulaire à base de mémoires 3D NAND sous blindage hermétique.",
        "key_features": ["Industrie allemande (Bavière)", "Débit d'accès ultra-rapide 5 Gbit/s", "TRL 9 qualifié vol ESA"],
        "interfaces": ["Alimentation 28 V", "Bus SpaceWire / SpaceFibre", "Montage conductif chassis"],
    },
    {
        "id": "mass_mem_2tb_de",
        "supplier_id": "spectra_tech",
        "supplier_name": "SpectraSpace Instruments",
        "name": "SpectraStore 2 TB High-Capacity Memory",
        "function": "mass_memory",
        "description": "Mémoire de masse 2 To haute capacité durcie développée en Allemagne",
        "mass_kg": 2.6,
        "power_w": 17.0,
        "peak_power_w": 28.0,
        "standby_power_w": 2.2,
        "volume_liters": 1.8,
        "price_meur": 0.65,
        "trl": 9,
        "specs": {"capacity_gb": 2048.0, "throughput_mbps": 6000.0, "rad_krad": 100.0},
        "image": "equip_avionics_obc.jpg",
        "dimensions_mm": [190, 150, 75],
        "long_description": "Version double capacité de la gamme SpectraStore développée en Allemagne pour les missions radar SAR et d'imagerie hyperspectrale à très fort volume de données journalier.",
        "key_features": ["Technologie allemande de pointe", "Capacité 2 048 Go utiles", "Tolérance radiologique 100 krad"],
        "interfaces": ["Bus régulé 50 V", "Multi-ports SpaceFibre", "Interface mécanique 4 points"],
    },
    {
        "id": "mass_mem_1tb_ch",
        "supplier_id": "helvetia_microwave",
        "supplier_name": "Helvetia Microwave & RF",
        "name": "Helvetia Rad-Hard Mass Memory 1 TB",
        "function": "mass_memory",
        "description": "Mémoire de masse de haute précision 1 To développée en Suisse",
        "mass_kg": 1.9,
        "power_w": 11.0,
        "peak_power_w": 18.0,
        "standby_power_w": 1.2,
        "volume_liters": 1.3,
        "price_meur": 0.44,
        "trl": 9,
        "specs": {"capacity_gb": 1024.0, "throughput_mbps": 3800.0, "rad_krad": 100.0},
        "image": "equip_avionics_obc.jpg",
        "dimensions_mm": [170, 130, 60],
        "long_description": "Mémoire de masse spatiale haute fiabilité conçue en Suisse (Lausanne). Réputée pour son niveau d'intégrité de données et son faible taux de consommation électrique.",
        "key_features": ["Horlogerie et microélectronique spatiale suisse", "Consommation ultra-basse (11 W)", "Haute résistance aux radiations"],
        "interfaces": ["Bus 28 V", "SpaceWire redondé", "Connecteurs micro-D"],
    },
    {
        "id": "adcs_sodern_auriga_fr",
        "supplier_id": "heritage_optics",
        "supplier_name": "Helios Space Instruments",
        "name": "Helios-Auriga Autonomous Star Tracker & Wheels Pack",
        "function": "adcs",
        "description": "Pack de contrôle d'attitude haute précision (viseur d'étoiles autonome + 4 roues) développé en France",
        "mass_kg": 11.2,
        "power_w": 26.0,
        "peak_power_w": 65.0,
        "standby_power_w": 8.0,
        "volume_liters": 7.5,
        "price_meur": 0.88,
        "trl": 9,
        "specs": {"pointing_accuracy_deg": 0.003, "slew_rate_deg_s": 2.2, "jitter_arcsec": 0.8},
        "image": "equip_adcs_sensor_pack.jpg",
        "dimensions_mm": [280, 240, 190],
        "long_description": "Système de contrôle d'attitude complet développé en France intégrant un viseur stellaire autonome sub-arcseconde et 4 roues de réaction en tétraèdre. Il garantit une précision de pointage exceptionnelle de 0,003° pour l'observation de la Terre.",
        "key_features": ["Filière opto-spatiale française", "Précision de pointage 0,003° (11 arcsec)", "Vitesse de basculement agile 2,2°/s"],
        "interfaces": ["Alimentation 28 V", "Bus MIL-STD-1553B / CAN", "Fixation cinématique 3 points"],
    },
    {
        "id": "adcs_leonardo_pack_it",
        "supplier_id": "stellare_ottica",
        "supplier_name": "Stellara Ottica",
        "name": "Stellara Precision ADCS Suite",
        "function": "adcs",
        "description": "Suite ADCS haute précision avec viseur stellaire compact développée en Italie",
        "mass_kg": 11.8,
        "power_w": 28.0,
        "peak_power_w": 70.0,
        "standby_power_w": 9.0,
        "volume_liters": 7.8,
        "price_meur": 0.90,
        "trl": 9,
        "specs": {"pointing_accuracy_deg": 0.0035, "slew_rate_deg_s": 2.0, "jitter_arcsec": 0.9},
        "image": "equip_adcs_sensor_pack.jpg",
        "dimensions_mm": [290, 250, 195],
        "long_description": "Ensemble d'actionneurs gyroscopiques et de capteurs stellaires de haute précision développé en Italie (Florence). Particulièrement réputé pour sa tenue aux micro-vibrations sur les télescopes et charges utiles optiques.",
        "key_features": ["Excellence italienne en optomécanique spatiale", "Précision de pointage 0,0035°", "Amortisseurs viscoélastiques intégrés"],
        "interfaces": ["Bus 28 V / 50 V", "SpaceWire & CAN bus", "Interface de masse découplée"],
    },
    {
        "id": "prop_electric_hemp_de",
        "supplier_id": "spectra_tech",
        "supplier_name": "SpectraSpace Instruments",
        "name": "HEMPT-300 High-Efficiency Plasma Thruster",
        "function": "propulsion",
        "description": "Système de propulsion électrique plasmique HEMP à très haute impulsion spécifique développé en Allemagne",
        "mass_kg": 8.2,
        "power_w": 300.0,
        "peak_power_w": 350.0,
        "standby_power_w": 3.0,
        "volume_liters": 5.2,
        "price_meur": 0.68,
        "trl": 9,
        "specs": {"isp_s": 2200.0, "thrust_mn": 15.0, "propellant_mass_kg": 6.0},
        "image": "equip_propulsion_electric.jpg",
        "dimensions_mm": [260, 200, 160],
        "long_description": "Propulseur à plasma périodique à haut rendement développé en Allemagne. Son impulsion spécifique de 2 200 s réduit considérablement la masse de xénon requise pour le maintien à poste et le contrôle d'orbite.",
        "key_features": ["Technologie allemande HEMP", "Impulsion spécifique élevée (2 200 s)", "Électronique PPU intégrée"],
        "interfaces": ["Bus 50 V régulé", "Liaison de commande RS-422", "Alimentation fluide gaz xénon"],
    },
    {
        "id": "prop_chemical_biprop_400n_de",
        "supplier_id": "comms_euro",
        "supplier_name": "EuroSpace Link",
        "name": "AeroThrust 400N Apogee Engine",
        "function": "propulsion",
        "description": "Moteur d'apogée bi-liquide haute performance 400 N développé en Allemagne (Lampoldshausen heritage)",
        "mass_kg": 4.8,
        "power_w": 25.0,
        "peak_power_w": 40.0,
        "standby_power_w": 1.0,
        "volume_liters": 4.5,
        "price_meur": 1.15,
        "trl": 9,
        "specs": {"isp_s": 321.0, "thrust_mn": 400000.0, "propellant_mass_kg": 45.0},
        "image": "equip_propulsion_chemical.jpg",
        "dimensions_mm": [350, 280, 280],
        "long_description": "Moteur de circularisation et de transfert d'apogée développé en Allemagne (héritage Lampoldshausen). Utilisant le mélange MMH / NTO, il assure l'injection précise sur les orbites géostationnaires ou de transfert MEO.",
        "key_features": ["Filière propulsion spatiale allemande", "Poussée 400 N, Isp 321 s", "Tuyère en alliage de niobium radiatif"],
        "interfaces": ["Alimentation 28 V électrovannes", "Lignes ergols NTO/MMH 1/4 pouce", "Bride de poussée titane"],
    },
]


def main() -> None:
    # 1. Update suppliers.json with clean country names and codes
    sup_path = CAT_DIR / "suppliers.json"
    suppliers = json.loads(sup_path.read_text(encoding="utf-8"))
    for s in suppliers:
        sid = s["id"]
        if sid in SUPPLIER_COUNTRIES:
            c = SUPPLIER_COUNTRIES[sid]
            s["country"] = c
            s["country_code"] = COUNTRY_CODES.get(c, "")
    sup_path.write_text(json.dumps(suppliers, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Updated {len(suppliers)} suppliers with clean countries and codes.")

    # 2. Add new equipments to equipment.json
    eq_path = CAT_DIR / "equipment.json"
    equipments = json.loads(eq_path.read_text(encoding="utf-8"))
    existing_ids = {e["id"] for e in equipments}
    added_count = 0
    for neq in NEW_EQUIPMENTS:
        if neq["id"] not in existing_ids:
            equipments.append(neq)
            existing_ids.add(neq["id"])
            added_count += 1
    eq_path.write_text(json.dumps(equipments, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Added {added_count} new multi-country European equipment items.")

    # 3. Update platforms.json to allow these new equipment IDs in appropriate slots
    plat_path = CAT_DIR / "platforms.json"
    platforms = json.loads(plat_path.read_text(encoding="utf-8"))

    # Mapping of equipment function to new allowed items
    func_additions = {
        "ttc": ["ttc_sband_gallia_fr", "ttc_sband_aurora_it"],
        "payload_downlink": ["downlink_xband_toulouse_fr", "downlink_xband_milan_it", "downlink_kaband_milan_it"],
        "mass_memory": ["mass_mem_1tb_fr", "mass_mem_1tb_de", "mass_mem_2tb_de", "mass_mem_1tb_ch"],
        "adcs": ["adcs_sodern_auriga_fr", "adcs_leonardo_pack_it"],
        "propulsion": ["prop_electric_hemp_de"],
    }

    for plat in platforms:
        for slot in plat.get("slots", []):
            fn = slot.get("function")
            allowed = slot.get("allowed_equipment_ids", [])
            # For CubeSat 6U, keep only compact options
            if plat.get("category") == "cubesat" and "6u" in plat.get("id", ""):
                if fn == "ttc":
                    for nid in ["ttc_sband_gallia_fr", "ttc_sband_aurora_it"]:
                        if nid not in allowed:
                            allowed.append(nid)
                continue

            if fn in func_additions:
                for nid in func_additions[fn]:
                    if nid not in allowed:
                        allowed.append(nid)

            # For platforms with 400N apogee engine, add the German 400N engine
            if fn == "propulsion" and "prop_biprop_400n" in allowed:
                if "prop_chemical_biprop_400n_de" not in allowed:
                    allowed.append("prop_chemical_biprop_400n_de")

    plat_path.write_text(json.dumps(platforms, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Updated platform slot compatibilities across {len(platforms)} platforms.")


if __name__ == "__main__":
    main()
