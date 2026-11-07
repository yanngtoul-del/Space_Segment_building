"""Platform catalog source: overlays for the 5 existing platforms + 11 new platforms."""

from common import base

IMG_CUBE = "platform_cubesat.jpg"
IMG_SMALL = "platform_smallsat.jpg"
IMG_MED = "platform_medium.jpg"
IMG_LARGE = "platform_large.jpg"


def slot(fn, allowed, included=None, min_qty=0, max_qty=1, fix=0.0, pct=0.0, imass=0.0, ov=None):
    return dict(
        function=fn, allowed_equipment_ids=list(allowed), included_equipment_ids=list(included or []),
        min_qty=min_qty, max_qty=max_qty, integration_cost_fixed_meur=fix, integration_cost_pct=pct,
        interface_mass_kg=imass, equipment_overrides=ov or {},
    )


# ---------------------------------------------------------------- overlays (existing 5 platforms)
OVERLAY = {
    "plat_aeromicro_16u": dict(
        image=IMG_CUBE, dimensions_mm=(450, 226, 226), deployed_span_m=1.4,
        long_description="Plateforme CubeSat 16U d'AeroMicro Dynamics, dotée de panneaux solaires déployables, d'un calculateur COTS tolérant aux radiations et d'une baie de charge utile de 9 litres. Elle est conçue pour emporter de petits imageurs, des terminaux radio ou des démonstrateurs technologiques à coût très contenu. La puissance disponible, le volume et la précision de pointage limitent toutefois son usage aux instruments compacts.",
        key_features=["Format 16U compatible dispensers standards", "Baie charge utile 9 L / 10 kg", "Pointage 0,05° avec viseur d'étoiles", "Livraison rapide en 8 mois"],
        interfaces=["Bus 12 V non régulé", "CAN / RS-422 / SpaceWire", "Fixation rail CubeSat 16U"],
        slot_additions={
            "propulsion": ["prop_coldgas_1u", "prop_pptt_micro"],
            "ttc": ["ttc_uhf_cubesat"],
            "mass_memory": ["mass_mem_64gb"],
        },
        extra_slots=[
            slot("payload_downlink", ["downlink_sband_hr", "downlink_xband_tx_50mbps", "downlink_xband_tx_150mbps"], [], 0, 1, 0.02, 4.0, 0.2),
            slot("adcs", ["adcs_cubesat_basic", "adcs_cubesat_precision"], ["adcs_cubesat_precision"], 1, 1),
        ],
    ),
    "plat_sstl_micro50": dict(
        image=IMG_SMALL, dimensions_mm=(600, 600, 700), deployed_span_m=2.2,
        long_description="Microsatellite de classe 50 kg d'Albion Satellite Technologies, héritier d'une longue lignée de petits satellites d'observation et de télécommunications. Structure aluminium nid d'abeille, bus 28 V, roues à réaction et viseur d'étoiles de série. Bon compromis entre un CubeSat limité en puissance et une plateforme de 150 kg nettement plus coûteuse.",
        key_features=["Charge utile jusqu'à 30 kg / 28 L", "Bus 28 V, 70 W moyens pour la charge utile", "Compatible anneau ESPA", "Durée de vie 5 ans"],
        interfaces=["Bus 28 V", "SpaceWire / CAN / LVDS", "Plateau d'interface charge utile 500 x 500 mm", "Anneau de séparation 15 pouces"],
        slot_additions={
            "propulsion": ["prop_pptt_micro", "prop_green_5n"],
            "payload_downlink": ["downlink_xband_tx_150mbps"],
            "mass_memory": ["mass_mem_1tb"],
        },
        extra_slots=[
            slot("adcs", ["adcs_high_accuracy_pack"], [], 0, 1, 0.08, 5.0, 0.8),
        ],
    ),
    "plat_astra_flex150": dict(
        image=IMG_SMALL, dimensions_mm=(950, 850, 1100), deployed_span_m=3.8,
        long_description="Plateforme de 150 kg d'Astra Space Systems destinée aux missions opérationnelles d'observation de la Terre et de télécommunications. Elle offre deux emplacements de propulsion (permettant de combiner ou de redonder propulsion électrique et chimique), une avionique redondée et une bonne stabilité de pointage. C'est la plateforme polyvalente de référence pour les instruments de 30 à 75 kg.",
        key_features=["Jusqu'à 75 kg / 80 L de charge utile", "Double emplacement de propulsion (max 2)", "Avionique redondée, durée de vie 7 ans", "Compatible ESPA Grande, Vega-C, Falcon 9"],
        interfaces=["Bus 28 V régulé", "SpaceWire / SpaceFibre / MIL-1553", "Anneau de séparation 24 pouces"],
        slot_additions={
            "propulsion": ["prop_electric_hall_300w", "prop_green_5n"],
            "ttc": ["ttc_xband_tmtc", "ttc_sband_dual_redundant"],
            "payload_downlink": ["downlink_xband_tx_150mbps", "downlink_xband_tx_1200mbps"],
            "mass_memory": ["mass_mem_1tb"],
            "adcs": ["adcs_agile_wheels_medium"],
        },
        extra_slots=[],
    ),
    "plat_apex_pro500": dict(
        image=IMG_MED, dimensions_mm=(1400, 1300, 1700), deployed_span_m=6.5,
        long_description="Plateforme agile de classe 500 kg produite en série par Apex Orbital Manufacturing. Dotée de panneaux solaires de près d'un kilowatt, d'un contrôle d'attitude de haute précision inclus de base et d'une grande baie d'instrument, elle accueille des radars SAR, des télescopes sub-métriques ou des charges utiles multi-instruments.",
        key_features=["Charge utile 240 kg / 350 L", "950 W moyens en orbite (650 W charge utile)", "Propulsion Hall, X-band, mémoire 2 To et ADCS précis inclus", "Production en série, délai 14 mois"],
        interfaces=["Bus 50 V régulé", "SpaceFibre 4 voies / MIL-1553", "Interface lanceur 24 ou 38 pouces"],
        slot_additions={
            "propulsion": ["prop_electric_hall_300w", "prop_ion_500w", "prop_green_5n"],
            "ttc": ["ttc_xband_tmtc", "ttc_sband_dual_redundant"],
            "payload_downlink": ["downlink_xband_tx_1200mbps"],
            "mass_memory": ["mass_mem_8tb"],
            "adcs": ["adcs_agile_wheels_medium", "adcs_ultra_stable"],
        },
        extra_slots=[],
    ),
    "plat_europrime_heavy1500": dict(
        image=IMG_LARGE, dimensions_mm=(2200, 2000, 3100), deployed_span_m=11.5,
        long_description="Plateforme lourde de classe 1,5 tonne d'AeroPrime Defense & Space, qualifiée pour les grandes missions institutionnelles et de défense. Architecture entièrement redondée, bus 100 V de 2,5 kW, très haute stabilité de pointage et capacité d'emport de 800 kg. C'est la seule famille capable d'accueillir les grands télescopes métriques ou des radars à large antenne.",
        key_features=["Charge utile 800 kg / 1200 L", "2,5 kW moyens, bus 100 V", "Stabilité 0,15 arcsec/s, durée de vie 12 ans", "Tolérance radiations 100 krad"],
        interfaces=["Bus 100 V régulé", "SpaceFibre / MIL-1553B redondé", "Adaptateur lanceur 1194 mm"],
        slot_additions={
            "propulsion": ["prop_ion_500w"],
            "ttc": ["ttc_sband_dual_redundant", "ttc_xband_tmtc"],
            "payload_downlink": ["downlink_xband_tx_1200mbps"],
            "mass_memory": ["mass_mem_8tb"],
            "adcs": ["adcs_ultra_stable"],
        },
        extra_slots=[],
    ),
}


def plat(item_id, sup, name, cat, dry, max_pl, max_ln, vol, dims, span, p_orb, p_pl, p_pk, vbus, bat, dod,
         pt_acc, pt_stab, slew, jit, therm, env, life, rad, price, lead, trl, img, desc, long, feats, ifaces, slots):
    return base(
        item_id, sup, name=name, category=cat, description=desc, dimensions_mm=dims, deployed_span_m=span,
        dry_mass_kg=dry, max_payload_mass_kg=max_pl, max_launch_mass_kg=max_ln, payload_volume_liters=vol,
        orbit_avg_power_w=p_orb, payload_avg_power_w=p_pl, payload_peak_power_w=p_pk, bus_voltage_v=vbus,
        battery_capacity_wh=bat, battery_max_dod=dod, pointing_accuracy_deg=pt_acc,
        pointing_stability_arcsec_s=pt_stab, slew_rate_deg_s=slew, jitter_arcsec=jit,
        payload_thermal_dissipation_w=therm, launch_environment_compatible=env,
        design_lifetime_years=life, rad_tolerance_krad=rad, base_price_meur=price,
        base_lead_time_months=lead, trl=trl, image=img, long_description=long,
        key_features=feats, interfaces=ifaces, slots=slots,
    )


NEW = [
    # ---- AeroMicro Dynamics (newspace_micro) : add 6U, 12U, ESPA-50
    plat("plat_aeromicro_6u", "newspace_micro", "MicroBus-6U", "cubesat_6u",
         5.0, 4.0, 12.0, 3.5, (340, 226, 100), 0.9, 25.0, 12.0, 35.0, 12.0, 65.0, 0.3,
         0.15, 25.0, 1.5, 8.0, 12.0, ["rideshare_deployer"], 2.5, 10.0, 0.28, 6, 9, IMG_CUBE,
         "CubeSat 6U d'entrée de gamme pour petits instruments et IoT/AIS",
         "La plus petite plateforme du catalogue : un CubeSat 6U standardisé offrant 3,5 U à la charge utile. Très économique et livrable en 6 mois, elle convient aux récepteurs radio (AIS/IoT) ou à une caméra miniature, mais sa puissance et sa précision de pointage interdisent les charges utiles exigeantes.",
         ["3,5 L / 4 kg pour la charge utile", "Prix de base 0,28 M€", "Livraison 6 mois", "Compatible tous déployeurs 6U"],
         ["Bus 5 V / 12 V", "CAN / UART / I2C", "Rails CubeSat 6U"],
         [slot("propulsion", ["prop_coldgas_1u"], [], 0, 1, 0.01, 3.0, 0.1),
          slot("ttc", ["ttc_uhf_cubesat", "ttc_sband_transceiver"], ["ttc_uhf_cubesat"], 1, 1),
          slot("payload_downlink", ["downlink_sband_hr", "downlink_xband_tx_50mbps"], [], 0, 1, 0.01, 3.0, 0.1),
          slot("mass_memory", ["mass_mem_64gb"], ["mass_mem_64gb"], 1, 1),
          slot("adcs", ["adcs_cubesat_basic", "adcs_cubesat_precision"], ["adcs_cubesat_basic"], 1, 1)]),

    plat("plat_aeromicro_12u", "newspace_micro", "MicroBus-12U", "cubesat_12u",
         9.0, 8.0, 20.0, 6.5, (340, 226, 226), 1.2, 45.0, 22.0, 60.0, 12.0, 130.0, 0.3,
         0.08, 18.0, 2.0, 6.0, 20.0, ["rideshare_deployer"], 3.0, 12.0, 0.42, 7, 9, IMG_CUBE,
         "CubeSat 12U polyvalent pour imagerie compacte et démonstration",
         "Plateforme CubeSat 12U offrant 6,5 L à la charge utile et des panneaux solaires déployables de 45 W moyens. Elle comble l'écart entre le 6U très contraint et le 16U, à un tarif attractif pour les missions universitaires ou les constellations à bas coût.",
         ["6,5 L / 8 kg de charge utile", "45 W moyens en orbite", "ADCS 3 axes avec viseur d'étoiles en option", "Compatible déployeurs 12U"],
         ["Bus 12 V", "CAN / SpaceWire / LVDS", "Rails CubeSat 12U"],
         [slot("propulsion", ["prop_coldgas_1u", "prop_coldgas_10u", "prop_pptt_micro"], [], 0, 1, 0.02, 4.0, 0.2),
          slot("ttc", ["ttc_uhf_cubesat", "ttc_sband_transceiver"], ["ttc_sband_transceiver"], 1, 1),
          slot("payload_downlink", ["downlink_sband_hr", "downlink_xband_tx_50mbps", "downlink_xband_tx_150mbps"], [], 0, 1, 0.02, 4.0, 0.15),
          slot("mass_memory", ["mass_mem_64gb", "mass_mem_512gb"], ["mass_mem_64gb"], 1, 1),
          slot("adcs", ["adcs_cubesat_basic", "adcs_cubesat_precision"], ["adcs_cubesat_precision"], 1, 1)]),

    plat("plat_aeromicro_espa50", "newspace_micro", "MicroBus-ESPA60", "smallsat_50kg",
         32.0, 35.0, 80.0, 35.0, (550, 550, 650), 2.0, 120.0, 65.0, 160.0, 28.0, 320.0, 0.3,
         0.03, 4.0, 2.5, 2.2, 45.0, ["espa_ring", "rideshare_deployer"], 4.0, 18.0, 1.45, 10, 8, IMG_SMALL,
         "Microsatellite NewSpace de 60 kg à bas coût pour anneau ESPA",
         "Première plateforme hors-CubeSat d'AeroMicro Dynamics, conçue pour les ports ESPA en covoiturage. Plus économique que l'AlbionMicro-50 grâce à l'utilisation d'avionique issue des CubeSats, mais avec une durée de vie et une tenue aux radiations plus modestes.",
         ["35 kg / 35 L de charge utile", "Tarif NewSpace (1,45 M€)", "Délai court 10 mois", "Propulsion électrique 100 W possible"],
         ["Bus 28 V", "CAN / SpaceWire", "Séparation 15 pouces ESPA"],
         [slot("propulsion", ["prop_coldgas_10u", "prop_electric_hall_100w", "prop_green_5n"], [], 0, 1, 0.06, 5.0, 0.8),
          slot("ttc", ["ttc_sband_transceiver"], ["ttc_sband_transceiver"], 1, 1),
          slot("payload_downlink", ["downlink_xband_tx_50mbps", "downlink_xband_tx_150mbps", "downlink_xband_tx"], [], 0, 1, 0.03, 4.0, 0.3),
          slot("mass_memory", ["mass_mem_512gb", "mass_mem_1tb"], ["mass_mem_512gb"], 1, 1),
          slot("adcs", ["adcs_cubesat_precision", "adcs_high_accuracy_pack"], [], 0, 1, 0.06, 5.0, 0.6)]),

    # ---- Albion Satellite Technologies (sstl_inspired) : add Mini-150, Midi-300
    plat("plat_sstl_mini150", "sstl_inspired", "AlbionMini-150", "smallsat_150kg",
         90.0, 70.0, 190.0, 75.0, (900, 800, 1000), 3.4, 240.0, 120.0, 300.0, 28.0, 720.0, 0.3,
         0.015, 1.5, 2.5, 1.0, 100.0, ["espa_ring", "dedicated_smallsat"], 6.0, 25.0, 3.9, 14, 9, IMG_SMALL,
         "Microsatellite 150 kg économique à fort héritage",
         "Concurrente directe de l'AstraFlex-150, l'AlbionMini-150 privilégie une architecture simple et éprouvée pour contenir le prix sous 4 M€. Elle emporte un seul système de propulsion et offre un peu moins de puissance, mais reste très compétitive pour l'imagerie optique moyenne résolution ou la spectrométrie.",
         ["70 kg / 75 L de charge utile", "Prix maîtrisé 3,9 M€", "Héritage > 25 satellites en vol", "Durée de vie 6 ans"],
         ["Bus 28 V", "SpaceWire / CAN", "Anneau ESPA 24 pouces"],
         [slot("propulsion", ["prop_electric_hall_100w", "prop_monoprop_1n", "prop_green_5n"], [], 0, 1, 0.1, 6.0, 1.5),
          slot("ttc", ["ttc_sband_transceiver", "ttc_xband_tmtc"], ["ttc_sband_transceiver"], 1, 1),
          slot("payload_downlink", ["downlink_xband_tx_150mbps", "downlink_xband_tx", "downlink_xband_tx_1200mbps"], [], 0, 1, 0.04, 5.0, 0.4),
          slot("mass_memory", ["mass_mem_512gb", "mass_mem_1tb", "mass_mem_2tb_highrel"], ["mass_mem_512gb"], 1, 2),
          slot("adcs", ["adcs_high_accuracy_pack", "adcs_agile_wheels_medium"], [], 0, 1, 0.08, 5.0, 0.8)]),

    plat("plat_sstl_midi300", "sstl_inspired", "AlbionMidi-300", "smallsat_300kg",
         165.0, 140.0, 360.0, 180.0, (1200, 1100, 1400), 4.8, 520.0, 320.0, 900.0, 28.0, 1600.0, 0.3,
         0.008, 0.8, 2.8, 0.7, 250.0, ["espa_ring", "dedicated_smallsat", "vega_c"], 7.0, 30.0, 6.4, 16, 9, IMG_MED,
         "Plateforme 300 kg pour charges utiles optiques ou radar compact",
         "Plateforme intermédiaire de 300 kg au lancement, idéale lorsque les 150 kg sont trop justes en masse ou en puissance mais qu'un bus de 500 kg serait surdimensionné. Sa structure hexagonale offre un grand plateau supérieur pour fixer un télescope de 40 cm ou un radar en bande X.",
         ["140 kg / 180 L de charge utile", "320 W moyens (900 W crête) pour la charge utile", "Pointage 0,008° de base", "Double propulsion possible"],
         ["Bus 28 V régulé", "SpaceWire / SpaceFibre", "Adaptateur 24 pouces"],
         [slot("propulsion", ["prop_electric_hall_100w", "prop_electric_hall_300w", "prop_monoprop_1n", "prop_green_5n"], ["prop_green_5n"], 1, 2, 0.12, 6.0, 2.0),
          slot("ttc", ["ttc_sband_transceiver", "ttc_sband_dual_redundant"], ["ttc_sband_transceiver"], 1, 1),
          slot("payload_downlink", ["downlink_xband_tx", "downlink_xband_tx_1200mbps", "downlink_kaband_tx_2gbps"], ["downlink_xband_tx"], 1, 2, 0.06, 5.0, 0.6),
          slot("mass_memory", ["mass_mem_1tb", "mass_mem_2tb_highrel"], ["mass_mem_1tb"], 1, 2),
          slot("adcs", ["adcs_high_accuracy_pack", "adcs_agile_wheels_medium", "adcs_cmg_agility_pack"], [], 0, 1, 0.1, 5.0, 1.0)]),

    # ---- Astra Space Systems (heritage_aero) : add Flex-300, Flex-700
    plat("plat_astra_flex300", "heritage_aero", "AstraFlex-300", "smallsat_300kg",
         175.0, 150.0, 390.0, 210.0, (1250, 1150, 1450), 5.2, 620.0, 420.0, 1300.0, 50.0, 1900.0, 0.3,
         0.006, 0.6, 3.2, 0.5, 320.0, ["dedicated_smallsat", "vega_c", "falcon9_rideshare"], 8.0, 40.0, 7.8, 18, 9, IMG_MED,
         "Plateforme institutionnelle 300 kg haute fiabilité",
         "Version agrandie de l'AstraFlex-150 avec bus 50 V et redondance complète. Conçue pour les missions institutionnelles exigeant 8 ans de durée de vie et une forte puissance crête (SAR compact ou charge utile multi-instruments).",
         ["150 kg / 210 L de charge utile", "Bus 50 V, 420 W moyens / 1,3 kW crête", "Avionique entièrement redondée", "Durée de vie 8 ans"],
         ["Bus 50 V régulé", "SpaceFibre / MIL-1553", "Anneau 24 pouces"],
         [slot("propulsion", ["prop_electric_hall_300w", "prop_ion_500w", "prop_monoprop_1n", "prop_green_5n"], ["prop_monoprop_1n"], 1, 2, 0.18, 8.0, 2.5),
          slot("ttc", ["ttc_sband_dual_redundant", "ttc_xband_tmtc"], ["ttc_sband_dual_redundant"], 1, 1),
          slot("payload_downlink", ["downlink_xband_tx", "downlink_xband_tx_1200mbps", "downlink_kaband_tx_2gbps"], ["downlink_xband_tx"], 1, 2, 0.07, 5.0, 0.8),
          slot("mass_memory", ["mass_mem_1tb", "mass_mem_2tb_highrel", "mass_mem_8tb"], ["mass_mem_1tb"], 1, 2),
          slot("adcs", ["adcs_high_accuracy_pack", "adcs_agile_wheels_medium", "adcs_cmg_agility_pack"], ["adcs_high_accuracy_pack"], 1, 1)]),

    plat("plat_astra_flex700", "heritage_aero", "AstraFlex-700", "medium_700kg",
         360.0, 340.0, 820.0, 520.0, (1650, 1500, 2100), 8.0, 1400.0, 950.0, 2800.0, 50.0, 3800.0, 0.3,
         0.003, 0.3, 3.5, 0.3, 750.0, ["dedicated_smallsat", "vega_c", "falcon9", "ariane6"], 10.0, 60.0, 14.5, 22, 9, IMG_MED,
         "Plateforme 700 kg pour télescopes très haute résolution et radars",
         "Haut de gamme d'Astra Space Systems, capable d'emporter 340 kg d'instruments avec près d'un kilowatt de puissance moyenne. Sa très grande stabilité mécanique (plateau optique en carbone) permet d'exploiter des télescopes sub-métriques exigeants sans dégradation par le jitter.",
         ["340 kg / 520 L de charge utile", "950 W moyens pour la charge utile", "Stabilité 0,3 arcsec/s, jitter 0,3 arcsec", "Durée de vie 10 ans"],
         ["Bus 50 V régulé", "SpaceFibre redondé / MIL-1553", "Adaptateur 937 mm"],
         [slot("propulsion", ["prop_electric_hall_300w", "prop_electric_hall_1kw", "prop_ion_500w", "prop_monoprop_1n", "prop_biprop_400n"], ["prop_monoprop_1n"], 1, 2, 0.25, 8.0, 4.0),
          slot("ttc", ["ttc_sband_dual_redundant", "ttc_xband_tmtc"], ["ttc_sband_dual_redundant"], 1, 2),
          slot("payload_downlink", ["downlink_xband_tx_1200mbps", "downlink_kaband_tx_2gbps"], ["downlink_xband_tx_1200mbps"], 1, 2, 0.1, 5.0, 1.2),
          slot("mass_memory", ["mass_mem_2tb_highrel", "mass_mem_8tb"], ["mass_mem_2tb_highrel"], 1, 2),
          slot("adcs", ["adcs_agile_wheels_medium", "adcs_cmg_agility_pack", "adcs_ultra_stable"], ["adcs_agile_wheels_medium"], 1, 1)]),

    # ---- Apex Orbital Manufacturing (apex_inspired) : add Apex-200, Apex-800
    plat("plat_apex_200", "apex_inspired", "ApexBus-200", "smallsat_200kg",
         105.0, 110.0, 240.0, 120.0, (1050, 950, 1200), 4.2, 420.0, 260.0, 850.0, 28.0, 1200.0, 0.35,
         0.008, 0.8, 3.8, 0.7, 200.0, ["espa_ring", "falcon9_rideshare", "dedicated_smallsat"], 6.0, 30.0, 5.2, 11, 9, IMG_SMALL,
         "SmallSat 200 kg produit en série à forte puissance",
         "Plateforme NewSpace de 200 kg pensée pour les constellations d'observation et de radar léger. Par rapport aux plateformes de 150 kg, elle se distingue par une puissance électrique élevée (420 W moyens, 850 W crête) et un délai de livraison réduit à 11 mois.",
         ["110 kg / 120 L de charge utile", "260 W moyens / 850 W crête pour la charge utile", "Livraison sur étagère en 11 mois", "Compatible ESPA Grande"],
         ["Bus 28 V", "SpaceFibre / SpaceWire / Ethernet spatial", "Anneau ESPA 24 pouces"],
         [slot("propulsion", ["prop_electric_hall_100w", "prop_electric_hall_300w", "prop_green_5n"], ["prop_electric_hall_100w"], 1, 1, 0.1, 5.0, 1.5),
          slot("ttc", ["ttc_sband_transceiver", "ttc_xband_tmtc"], ["ttc_sband_transceiver"], 1, 1),
          slot("payload_downlink", ["downlink_xband_tx", "downlink_xband_tx_1200mbps", "downlink_kaband_tx_2gbps"], ["downlink_xband_tx"], 1, 1, 0.05, 4.0, 0.5),
          slot("mass_memory", ["mass_mem_512gb", "mass_mem_1tb", "mass_mem_2tb_highrel"], ["mass_mem_1tb"], 1, 2),
          slot("adcs", ["adcs_high_accuracy_pack", "adcs_agile_wheels_medium", "adcs_cmg_agility_pack"], ["adcs_high_accuracy_pack"], 1, 1)]),

    plat("plat_apex_800", "apex_inspired", "ApexBus-800", "medium_800kg",
         410.0, 420.0, 950.0, 620.0, (1750, 1600, 2200), 8.8, 1750.0, 1250.0, 3400.0, 100.0, 4500.0, 0.35,
         0.004, 0.35, 4.2, 0.4, 900.0, ["falcon9", "vega_c", "ariane6"], 8.0, 50.0, 13.8, 16, 8, IMG_MED,
         "Plateforme NewSpace 800 kg à forte puissance pour SAR et charges multiples",
         "La plus grande plateforme d'Apex Orbital : 420 kg de capacité d'emport et 1,25 kW moyens pour la charge utile, à un prix sensiblement inférieur aux plateformes institutionnelles de même masse. Très adaptée aux radars SAR puissants ou aux missions combinant imagerie et liaison laser.",
         ["420 kg / 620 L de charge utile", "1,25 kW moyens / 3,4 kW crête", "Bus 100 V", "Tarif compétitif 13,8 M€"],
         ["Bus 100 V", "SpaceFibre 8 voies", "Adaptateur 937 mm"],
         [slot("propulsion", ["prop_electric_hall_300w", "prop_electric_hall_1kw", "prop_ion_500w", "prop_monoprop_1n"], ["prop_electric_hall_1kw"], 1, 2, 0.22, 6.0, 4.0),
          slot("ttc", ["ttc_sband_transceiver", "ttc_sband_dual_redundant", "ttc_xband_tmtc"], ["ttc_sband_dual_redundant"], 1, 1),
          slot("payload_downlink", ["downlink_xband_tx_1200mbps", "downlink_kaband_tx_2gbps"], ["downlink_kaband_tx_2gbps"], 1, 2, 0.08, 4.0, 1.0),
          slot("mass_memory", ["mass_mem_2tb_highrel", "mass_mem_8tb"], ["mass_mem_2tb_highrel"], 1, 2),
          slot("adcs", ["adcs_agile_wheels_medium", "adcs_cmg_agility_pack", "adcs_ultra_stable"], ["adcs_agile_wheels_medium"], 1, 1)]),

    # ---- AeroPrime Defense & Space (heritage_prime) : add PrimeBus-1000, PrimeBus-3000
    plat("plat_europrime_1000", "heritage_prime", "PrimeBus-1000", "medium_1000kg",
         520.0, 520.0, 1200.0, 800.0, (1900, 1750, 2500), 9.5, 1800.0, 1250.0, 3200.0, 100.0, 5000.0, 0.25,
         0.0025, 0.2, 4.0, 0.25, 1050.0, ["vega_c", "falcon9", "ariane6"], 10.0, 80.0, 21.0, 24, 9, IMG_LARGE,
         "Plateforme institutionnelle de classe 1 tonne à très haute stabilité",
         "Version compacte de la gamme PrimeBus d'AeroPrime, dimensionnée pour un lancement sur Vega-C ou Falcon 9. Elle reprend l'architecture redondée et la très haute stabilité de pointage de la PrimeBus-1500 pour un coût et une masse réduits.",
         ["520 kg / 800 L de charge utile", "Compatible Vega-C en lancement dédié", "Pointage 0,0025°, stabilité 0,2 arcsec/s", "Durée de vie 10 ans, 80 krad"],
         ["Bus 100 V régulé", "SpaceFibre / MIL-1553B redondé", "Adaptateur 937 ou 1194 mm"],
         [slot("propulsion", ["prop_electric_hall_1kw", "prop_ion_500w", "prop_monoprop_1n", "prop_biprop_400n"], ["prop_monoprop_1n"], 1, 2, 0.4, 8.0, 6.0),
          slot("ttc", ["ttc_sband_dual_redundant", "ttc_xband_tmtc"], ["ttc_sband_dual_redundant"], 1, 2),
          slot("payload_downlink", ["downlink_xband_tx_1200mbps", "downlink_kaband_tx_2gbps"], ["downlink_kaband_tx_2gbps"], 1, 2),
          slot("mass_memory", ["mass_mem_2tb_highrel", "mass_mem_8tb"], ["mass_mem_2tb_highrel"], 1, 2),
          slot("adcs", ["adcs_agile_wheels_medium", "adcs_cmg_agility_pack", "adcs_ultra_stable"], ["adcs_ultra_stable"], 1, 1)]),

    plat("plat_europrime_3000", "heritage_prime", "PrimeBus-3000", "heavy_3000kg",
         1400.0, 1500.0, 3400.0, 2500.0, (2600, 2400, 3800), 15.0, 4500.0, 3200.0, 8000.0, 100.0, 14000.0, 0.25,
         0.0015, 0.1, 3.0, 0.15, 2800.0, ["ariane6", "falcon9"], 15.0, 120.0, 48.0, 34, 9, IMG_LARGE,
         "Plateforme lourde de 3 tonnes pour grands observatoires et multi-charges utiles",
         "La plus grande plateforme du catalogue, destinée aux missions phares d'observation ou de télécommunications gouvernementales. Elle peut emporter simultanément plusieurs grands instruments (télescope métrique, radar bande L, terminaux laser) avec 15 ans de durée de vie, au prix d'un budget et d'un lanceur lourd.",
         ["1500 kg / 2500 L de charge utile", "3,2 kW moyens / 8 kW crête", "Stabilité 0,1 arcsec/s", "Durée de vie 15 ans"],
         ["Bus 100 V régulé", "Réseau SpaceFibre redondé", "Adaptateur lanceur lourd 1194 / 1666 mm"],
         [slot("propulsion", ["prop_electric_hall_1kw", "prop_ion_500w", "prop_biprop_400n"], ["prop_biprop_400n"], 1, 2, 0.6, 10.0, 10.0),
          slot("ttc", ["ttc_sband_dual_redundant", "ttc_xband_tmtc"], ["ttc_sband_dual_redundant"], 1, 2),
          slot("payload_downlink", ["downlink_xband_tx_1200mbps", "downlink_kaband_tx_2gbps"], ["downlink_kaband_tx_2gbps"], 1, 2),
          slot("mass_memory", ["mass_mem_2tb_highrel", "mass_mem_8tb"], ["mass_mem_8tb"], 1, 2),
          slot("adcs", ["adcs_cmg_agility_pack", "adcs_ultra_stable"], ["adcs_ultra_stable"], 1, 1)]),
]
