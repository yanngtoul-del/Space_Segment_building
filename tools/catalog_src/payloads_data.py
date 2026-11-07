"""Payloads catalog source: overlays for the 8 existing payloads + 25 new payloads."""

from common import base

IMG_OPT_S = "payload_optical_small.jpg"
IMG_OPT_L = "payload_optical_large.jpg"
IMG_SPEC = "payload_spectrometer.jpg"
IMG_SAR = "payload_sar.jpg"
IMG_LAS = "payload_laser.jpg"
IMG_QKD = "payload_qkd.jpg"
IMG_RAD = "payload_radio.jpg"

OVERLAY = {
    "pl_opt_pan_compact": dict(
        image=IMG_OPT_S, dimensions_mm=(220, 150, 120), flight_heritage=">15 CubeSats en vol",
        long_description="Télescope compact de 12 cm d'ouverture conçu pour les CubeSats 12U–16U et les petits microsatellites. Il fournit une résolution au sol d'environ 2,5 à 3 m à 500 km d'altitude en panchromatique et dans quatre bandes visibles/proche infrarouge. Peu exigeant en masse, en puissance et en pointage, mais insuffisant pour les missions sub-métriques.",
        key_features=["Ouverture Ø 12 cm, focale 1,05 m", "PAN + 4 bandes VNIR", "Masse 4,5 kg, 18 W", "GSD ~ 2,6 m à 500 km"],
        interfaces=["Alimentation 12/28 V", "Données SpaceWire / LVDS", "Fixation 4 x M5"]),
    "pl_opt_medium_25cm": dict(
        image=IMG_OPT_S, dimensions_mm=(380, 260, 260), flight_heritage="8 satellites en orbite",
        long_description="Télescope Cassegrain de 25 cm d'ouverture offrant une résolution métrique (~1,25 m à 500 km) et six bandes spectrales incluant le Red-Edge pour la végétation. Il s'intègre facilement sur des plateformes de 50 à 150 kg avec une consommation modérée.",
        key_features=["Ouverture Ø 25 cm, focale 2,2 m", "PAN + 5 bandes (dont Red-Edge)", "GSD ~ 1,25 m à 500 km", "Masse 16 kg"],
        interfaces=["Alimentation 28 V", "SpaceWire 2 liens", "Bride iso-statique 3 points"]),
    "pl_opt_submeter_highres": dict(
        image=IMG_OPT_L, dimensions_mm=(720, 520, 520), flight_heritage="Héritage Korsch, 6 vols",
        long_description="Télescope Korsch à trois miroirs de 45 cm d'ouverture en carbure de silicium, destiné à l'observation tactique sub-métrique (~0,77 m à 500 km). Sa longue focale impose une plateforme offrant un pointage meilleur que 0,008° et une dérive inférieure à 0,8 arcsec/s (souvent via un pack ADCS de précision).",
        key_features=["Ouverture Ø 45 cm, focale 4,2 m", "GSD ~ 0,77 m à 500 km", "Optique SiC athermique", "6 bandes VNIR, fauchée 18 km"],
        interfaces=["Alimentation 28 V", "SpaceFibre", "Montage iso-statique sur banc optique"]),
    "pl_opt_veryhighres_1m": dict(
        image=IMG_OPT_L, dimensions_mm=(1600, 1100, 1100), flight_heritage="Héritage Pléiades / WorldView",
        description="1.0 m primary mirror telescope for 30 cm ground resolution defense missions (inspired by Pléiades Neo / WorldView)",
        long_description="Grand instrument optique de 1 m de diamètre primaire pour les missions souveraines de très haute résolution (~0,29 m à 500 km). Il produit un débit brut de 6,5 Gbit/s et exige une stabilité de pointage extrême (0,15 arcsec/s) ainsi qu'une plateforme lourde (classe 700 à 1 500 kg).",
        key_features=["Miroir primaire Ø 1,0 m, focale 12 m", "GSD ~ 0,29 m à 500 km", "9 bandes spectrales, 14 bits", "TDI multi-étages"],
        interfaces=["Bus 50/100 V", "SpaceFibre 4 voies", "Interface 3 bipodes titane"]),
    "pl_spec_hyperspectral_vnir": dict(
        image=IMG_SPEC, dimensions_mm=(420, 280, 240), flight_heritage="Héritage EnMAP / PRISMA",
        long_description="Spectromètre imageur hyperspectral couvrant le domaine visible et proche infrarouge (400–1000 nm) en 120 bandes continues de 5 nm. Il permet l'identification minéralogique, le suivi de la qualité de l'eau et du stress végétal avec un GSD d'environ 3,4 m à 500 km.",
        key_features=["120 bandes de 400 à 1000 nm", "Résolution spectrale 5 nm", "Ouverture 18 cm, TDI 12 étages", "Calibration embarquée"],
        interfaces=["Alimentation 28 V", "SpaceFibre / SpaceWire", "Fixation 3 points"]),
    "pl_sar_xband_micro": dict(
        image=IMG_SAR, dimensions_mm=(1100, 600, 180), flight_heritage=">25 satellites de constellation",
        long_description="Radar à synthèse d'ouverture en bande X (9,6 GHz) à antenne active déployable de 3,2 m x 0,6 m, conçu pour l'observation tout-temps de jour comme de nuit. Sa résolution distance descend sous 0,5 m (bande 400 MHz), mais il demande une forte puissance pendant les prises de vue (850 W moyens en acquisition, 1,2 kW crête) et une dissipation thermique importante.",
        key_features=["Bande X 9,6 GHz, chirp 400 MHz", "Antenne active déployable 3,2 x 0,6 m", "Observation jour/nuit tout temps", "Masse 55 kg"],
        interfaces=["Bus 28/50 V haute puissance", "SpaceFibre", "Panneaux déployables verrouillés au lancement"]),
    "pl_opt_comm_terminal_10g": dict(
        image=IMG_LAS, dimensions_mm=(320, 240, 220), flight_heritage="Constellations LEO & SDA",
        long_description="Terminal de communication optique laser à 1550 nm assurant des liaisons directes vers le sol ou inter-satellites jusqu'à 10 Gbit/s. Sa tête optique de 10 cm intègre un miroir de pointage fin qui compense les vibrations de la plateforme jusqu'à 2 µrad. Sensible à la couverture nuageuse pour les liaisons vers le sol.",
        key_features=["Débit 10 Gbit/s à 1550 nm", "Télescope Ø 10 cm, laser 1,5 W", "Compatible SDA Tranche 1 & CCSDS", "Miroir de pointage fin intégré"],
        interfaces=["Alimentation 28 V", "SpaceFibre 10 Gbit/s", "Tête optique sur cardan 2 axes"]),
    "pl_qkd_terminal_decoy": dict(
        image=IMG_QKD, dimensions_mm=(360, 260, 240), flight_heritage="Démonstrateurs QKD LEO",
        long_description="Terminal spatial de distribution quantique de clés (QKD) mettant en œuvre le protocole BB84 à états leurres à 850 nm. Il émet des impulsions à 100 MHz à travers un télescope de 15 cm vers une station sol optique de 1 m, générant une clé secrète prouvée inviolable. Fonctionne de nuit pour limiter le bruit de fond solaire.",
        key_features=["Protocole BB84 decoy-state à 850 nm", "Source 100 MHz, télescope Ø 15 cm", "Pointage fin 1,5 µrad", "Canal classique de synchronisation inclus"],
        interfaces=["Alimentation 28 V", "SpaceWire + horloge GPS/PPS", "Banc optique isolé"]),
}


def opt(item_id, sup, name, mass, p_op, p_pk, vol, dims, pt_acc, pt_stab, jit, therm, raw, comp, price, trl, her,
        ap, foc, fn, pix, npx, bands, wl1, wl2, qe, rn, fwc, qbits, trans, mtf, desc, long, feats):
    return base(
        item_id, sup, name=name, payload_type="optical_imager", description=desc,
        mass_kg=mass, operational_power_w=p_op, peak_power_w=p_pk, standby_power_w=round(p_op * 0.1, 1),
        volume_liters=vol, dimensions_mm=dims, required_pointing_accuracy_deg=pt_acc,
        required_pointing_stability_arcsec_s=pt_stab, max_tolerated_jitter_arcsec=jit,
        thermal_dissipation_w=therm, raw_data_rate_mbps=raw, compressed_data_rate_mbps=comp,
        price_meur=price, trl=trl, flight_heritage=her,
        image=IMG_OPT_S if ap <= 0.32 else IMG_OPT_L,
        long_description=long, key_features=feats,
        interfaces=["Alimentation 28 V" if mass > 8 else "Alimentation 12 V", "SpaceWire / SpaceFibre", "Fixation iso-statique"],
        aperture_diameter_m=ap, focal_length_m=foc, f_number=fn, pixel_pitch_um=pix,
        detector_pixels_cross_track=npx, spectral_bands=bands, min_wavelength_nm=wl1, max_wavelength_nm=wl2,
        quantum_efficiency_avg=qe, read_noise_electrons=rn, full_well_capacity_electrons=fwc,
        quantization_bits=qbits, optics_transmission=trans, optics_mtf_at_nyquist=mtf,
    )


def spec(item_id, sup, name, mass, p_op, p_pk, vol, dims, pt_acc, pt_stab, jit, therm, raw, comp, price, trl, her,
         ap, foc, pix, npx, wl1, wl2, nbands, sres, qbits, desc, long, feats):
    return base(
        item_id, sup, name=name, payload_type="spectrometer", description=desc,
        mass_kg=mass, operational_power_w=p_op, peak_power_w=p_pk, standby_power_w=round(p_op * 0.12, 1),
        volume_liters=vol, dimensions_mm=dims, required_pointing_accuracy_deg=pt_acc,
        required_pointing_stability_arcsec_s=pt_stab, max_tolerated_jitter_arcsec=jit,
        thermal_dissipation_w=therm, raw_data_rate_mbps=raw, compressed_data_rate_mbps=comp,
        price_meur=price, trl=trl, flight_heritage=her, image=IMG_SPEC,
        long_description=long, key_features=feats,
        interfaces=["Alimentation 28 V", "SpaceFibre / SpaceWire", "Radiateur thermique dédié"],
        aperture_diameter_m=ap, focal_length_m=foc, pixel_pitch_um=pix, detector_spatial_pixels=npx,
        spectral_range_min_nm=wl1, spectral_range_max_nm=wl2, number_of_spectral_bands=nbands,
        spectral_resolution_nm=sres, quantization_bits=qbits,
    )


def sar(item_id, sup, name, mass, p_op, p_pk, vol, dims, pt_acc, pt_stab, jit, therm, raw, comp, price, trl, her,
        freq, band, alen, awid, atype, rfpk, duty, bw, nf, inc1, inc2, desc, long, feats):
    return base(
        item_id, sup, name=name, payload_type="sar", description=desc,
        mass_kg=mass, operational_power_w=p_op, peak_power_w=p_pk, standby_power_w=20.0,
        volume_liters=vol, dimensions_mm=dims, required_pointing_accuracy_deg=pt_acc,
        required_pointing_stability_arcsec_s=pt_stab, max_tolerated_jitter_arcsec=jit,
        thermal_dissipation_w=therm, raw_data_rate_mbps=raw, compressed_data_rate_mbps=comp,
        price_meur=price, trl=trl, flight_heritage=her, image=IMG_SAR,
        long_description=long, key_features=feats,
        interfaces=["Bus haute puissance 28/50/100 V", "SpaceFibre", "Mécanisme de déploiement d'antenne"],
        frequency_ghz=freq, band_name=band, antenna_length_m=alen, antenna_width_m=awid, antenna_type=atype,
        rf_peak_power_w=rfpk, duty_cycle_max_pct=duty, chirp_bandwidth_mhz=bw, system_noise_figure_db=nf,
        incidence_angle_min_deg=inc1, incidence_angle_max_deg=inc2,
    )


def ocomm(item_id, sup, name, mass, p_op, p_pk, vol, dims, pt_acc, pt_stab, jit, therm, rate_g, price, trl, her,
          ap, wl, txp, div, trk, stds, desc, long, feats):
    return base(
        item_id, sup, name=name, payload_type="optical_comm", description=desc,
        mass_kg=mass, operational_power_w=p_op, peak_power_w=p_pk, standby_power_w=round(p_op * 0.12, 1),
        volume_liters=vol, dimensions_mm=dims, required_pointing_accuracy_deg=pt_acc,
        required_pointing_stability_arcsec_s=pt_stab, max_tolerated_jitter_arcsec=jit,
        thermal_dissipation_w=therm, raw_data_rate_mbps=rate_g * 1000.0, compressed_data_rate_mbps=rate_g * 1000.0,
        price_meur=price, trl=trl, flight_heritage=her, image=IMG_LAS,
        long_description=long, key_features=feats,
        interfaces=["Alimentation 28 V", "SpaceFibre", "Ouverture dégagée zénith/nadir"],
        telescope_aperture_m=ap, wavelength_nm=wl, tx_optical_power_w=txp, max_data_rate_gbps=rate_g,
        beam_divergence_urad=div, pointing_tracking_accuracy_urad=trk, compatible_standards=stds,
    )


def qkd(item_id, sup, name, mass, p_op, p_pk, vol, dims, pt_acc, pt_stab, jit, therm, price, trl, her,
        proto, ap, srate, wl, p_urad, night, desc, long, feats):
    return base(
        item_id, sup, name=name, payload_type="qkd", description=desc,
        mass_kg=mass, operational_power_w=p_op, peak_power_w=p_pk, standby_power_w=5.0,
        volume_liters=vol, dimensions_mm=dims, required_pointing_accuracy_deg=pt_acc,
        required_pointing_stability_arcsec_s=pt_stab, max_tolerated_jitter_arcsec=jit,
        thermal_dissipation_w=therm, raw_data_rate_mbps=15.0, compressed_data_rate_mbps=15.0,
        price_meur=price, trl=trl, flight_heritage=her, image=IMG_QKD,
        long_description=long, key_features=feats,
        interfaces=["Alimentation 12/28 V", "SpaceWire + PPS", "Télescope sur table optique"],
        protocol=proto, telescope_aperture_m=ap, source_rate_mhz=srate, wavelength_nm=wl,
        pointing_accuracy_urad=p_urad, night_only_operation=night,
    )


def rcomm(item_id, sup, name, mass, p_op, p_pk, vol, dims, pt_acc, therm, price, trl, her,
          f_up, f_dn, rfp, gtx, grx, bw, rate, desc, long, feats):
    return base(
        item_id, sup, name=name, payload_type="radio_comm", description=desc,
        mass_kg=mass, operational_power_w=p_op, peak_power_w=p_pk, standby_power_w=round(p_op * 0.1, 1),
        volume_liters=vol, dimensions_mm=dims, required_pointing_accuracy_deg=pt_acc,
        required_pointing_stability_arcsec_s=20.0, max_tolerated_jitter_arcsec=10.0,
        thermal_dissipation_w=therm, raw_data_rate_mbps=rate, compressed_data_rate_mbps=rate,
        price_meur=price, trl=trl, flight_heritage=her, image=IMG_RAD,
        long_description=long, key_features=feats,
        interfaces=["Alimentation 28 V", "SpaceWire / Ethernet", "Interfaces guides d'onde / coaxiaux"],
        uplink_frequency_ghz=f_up, downlink_frequency_ghz=f_dn, rf_output_power_w=rfp,
        antenna_gain_tx_dbi=gtx, antenna_gain_rx_dbi=grx, bandwidth_mhz=bw, max_data_rate_mbps=rate,
    )


NEW = [
    # ---- 7 new optical imagers
    opt("pl_opt_cubesat_6cm", "optics_lab", "OptiCam-6 Nano Imager",
        1.5, 8.0, 12.0, 1.2, (110, 95, 95), 0.12, 20.0, 6.0, 6.0, 140.0, 45.0, 0.32, 9, ">30 CubeSats",
        0.06, 0.45, 7.5, 5.5, 4096, ["R", "G", "B", "NIR"], 450.0, 880.0, 0.62, 14.0, 18000.0, 12, 0.80, 0.20,
        "Caméra 1,2U de 6 cm d'ouverture pour CubeSats 6U et 12U",
        "La plus petite caméra d'observation du catalogue : un objectif réfractif athermique de 6 cm tenant dans un peu plus de 1U. Elle fournit un GSD d'environ 6 m à 500 km sur une fauchée de 25 km, idéal pour le suivi agricole ou côtier sur CubeSat 6U à budget très réduit.",
        ["Format 1,2U, masse 1,5 kg", "GSD ~ 6,1 m à 500 km, fauchée 25 km", "4 bandes RGB+NIR", "Prix 0,32 M€"]),

    opt("pl_opt_wide_swath_18cm", "optics_lab", "WideView-18 Multispectral Mapper",
        9.5, 26.0, 38.0, 8.5, (280, 220, 200), 0.04, 5.0, 2.0, 20.0, 750.0, 220.0, 1.45, 9, "12 satellites",
        0.18, 0.90, 5.0, 6.5, 16000, ["B", "G", "R", "RE", "NIR"], 440.0, 900.0, 0.68, 10.0, 24000.0, 12, 0.83, 0.22,
        "Imageur 18 cm à large fauchée (>55 km) pour revisite fréquente",
        "Instrument multispectral à focale courte privilégiant la largeur de fauchée (~58 km à 500 km) plutôt que la résolution pure (~3,6 m). Il permet de couvrir de vastes zones agricoles ou forestières en peu de passages.",
        ["Fauchée ~58 km à 500 km", "GSD ~ 3,6 m, 5 bandes VNIR", "Ouverture Ø 18 cm, f/5", "Compatible plateformes 16U et 50 kg"]),

    opt("pl_opt_stellara_20cm", "stellare_ottica", "STELLA-20 Ritchey-Chrétien Telescope",
        11.0, 28.0, 42.0, 10.0, (320, 230, 230), 0.025, 3.0, 1.5, 22.0, 850.0, 250.0, 1.75, 9, "14 vols",
        0.20, 1.80, 9.0, 5.5, 12000, ["PAN", "B", "G", "R", "NIR"], 450.0, 900.0, 0.68, 10.0, 24000.0, 12, 0.85, 0.24,
        "Télescope Ritchey-Chrétien 20 cm à miroirs Zerodur pour microsatellites",
        "Télescope italien de 20 cm d'ouverture à miroirs en Zerodur et structure carbone, délivrant environ 1,5 m de GSD à 500 km. Positionné entre les caméras CubeSat 12 cm et le 25 cm, il entre facilement sur une plateforme de 50 kg.",
        ["Ouverture Ø 20 cm, focale 1,8 m", "GSD ~ 1,53 m à 500 km", "Miroirs Zerodur, tube CFRP", "Masse 11 kg"]),

    opt("pl_opt_stellara_35cm", "stellare_ottica", "STELLA-35 Sub-Meter Telescope",
        30.0, 60.0, 90.0, 28.0, (540, 400, 400), 0.012, 1.2, 0.7, 48.0, 1800.0, 500.0, 4.1, 9, "7 vols",
        0.35, 3.50, 10.0, 6.0, 20000, ["PAN", "B", "G", "R", "RE", "NIR"], 450.0, 900.0, 0.72, 9.0, 28000.0, 12, 0.85, 0.25,
        "Télescope 35 cm sub-métrique (~0,86 m GSD) pour plateformes 150 kg",
        "Télescope sub-métrique compact de 35 cm pesant seulement 30 kg. Il permet d'atteindre un GSD inférieur à 0,9 m à 500 km sur une plateforme de classe 150 kg tout en laissant de la marge de masse pour un terminal de descente rapide ou un second petit instrument.",
        ["Ouverture Ø 35 cm, focale 3,5 m", "GSD ~ 0,86 m à 500 km", "Masse contenue 30 kg", "6 bandes spectrales"]),

    opt("pl_opt_stellara_60cm", "stellare_ottica", "STELLA-60 High-Resolution Korsch",
        92.0, 140.0, 210.0, 110.0, (950, 680, 680), 0.005, 0.45, 0.35, 115.0, 3400.0, 900.0, 10.5, 9, "4 vols",
        0.60, 6.50, 10.83, 6.5, 32000, ["PAN", "B", "G", "R", "RE", "NIR"], 450.0, 900.0, 0.75, 7.0, 32000.0, 14, 0.86, 0.26,
        "Télescope Korsch 60 cm (GSD ~0,5 m) pour plateformes 300 à 500 kg",
        "Télescope de 60 cm atteignant 0,50 m de résolution au nadir à 500 km. Idéal pour les missions demandant une résolution demi-métrique sans payer le prix ni la masse d'un miroir de 70 cm ou 1 m. Compatible avec les plateformes de 300 à 500 kg.",
        ["Ouverture Ø 60 cm, focale 6,5 m", "GSD ~ 0,50 m à 500 km", "Fauchée 16 km, 14 bits", "Masse 92 kg"]),

    opt("pl_opt_helios_70cm", "heritage_optics", "EagleEye-70 Sub-50cm Imager",
        145.0, 210.0, 320.0, 195.0, (1150, 820, 820), 0.004, 0.3, 0.25, 175.0, 4500.0, 1150.0, 15.2, 9, "Héritage CSO / Pléiades",
        0.70, 8.40, 12.0, 6.5, 36000, ["PAN", "Coastal", "B", "G", "R", "RE", "NIR"], 420.0, 920.0, 0.76, 6.5, 36000.0, 14, 0.87, 0.27,
        "Télescope 70 cm très haute résolution (~0,39 m GSD à 500 km)",
        "Instrument de 70 cm d'Helios Space Instruments offrant une résolution de ~39 cm à 500 km. Il s'installe sur les plateformes de 500 à 800 kg équipées d'un ADCS de haute précision, pour les missions de renseignement ou de cartographie urbaine fine.",
        ["Ouverture Ø 70 cm, focale 8,4 m", "GSD ~ 0,39 m à 500 km", "7 bandes spectrales", "Banc SiC monobloc"]),

    opt("pl_opt_swir_20cm", "cirrus_ir", "CirrusSWIR-20 Short-Wave IR Imager",
        14.0, 45.0, 65.0, 12.0, (340, 240, 240), 0.03, 4.0, 1.8, 38.0, 520.0, 160.0, 2.8, 8, "3 vols",
        0.20, 1.25, 6.25, 10.0, 4096, ["SWIR1_1240", "SWIR2_1610", "SWIR3_2200"], 1000.0, 2400.0, 0.70, 25.0, 60000.0, 14, 0.80, 0.22,
        "Imageur infrarouge à ondes courtes (SWIR 1,0–2,4 µm) pour humidité, feux et méthane",
        "Caméra infrarouge SWIR à détecteur InGaAs refroidi par machine Stirling miniature. Elle observe à travers la fumée, détecte les départs de feux, les fuites industrielles et le stress hydrique des sols avec un GSD de 4 m à 500 km.",
        ["Domaine SWIR 1000–2400 nm (3 bandes)", "Détecteur InGaAs refroidi", "GSD ~ 4,0 m à 500 km", "Vision à travers la fumée"]),

    # ---- 4 new spectrometers
    spec("pl_spec_vnir_compact", "spectra_tech", "MiniSpec-VNIR CubeSat Spectrometer",
         6.8, 22.0, 32.0, 6.0, (240, 180, 150), 0.04, 4.0, 2.0, 18.0, 480.0, 160.0, 1.45, 8, "5 CubeSats",
         0.10, 0.55, 8.0, 1024, 420.0, 980.0, 60, 9.5, 12,
         "Spectromètre hyperspectral compact 60 bandes pour CubeSat 16U et SmallSat 50 kg",
         "Version miniaturisée de la gamme SpectraSpace permettant de faire de l'imagerie hyperspectrale sur un budget de microsatellite ou de 16U. 60 bandes VNIR de ~9,5 nm et GSD d'environ 7,3 m à 500 km.",
         ["60 bandes VNIR (420–980 nm)", "Masse 6,8 kg, 22 W", "Résolution spectrale 9,5 nm", "GSD ~ 7,3 m à 500 km"]),

    spec("pl_spec_swir_180", "spectra_tech", "HyperEye-SWIR Mineral & Methane Mapper",
         36.0, 82.0, 120.0, 32.0, (520, 360, 320), 0.012, 1.2, 0.7, 70.0, 1500.0, 500.0, 5.9, 8, "Héritage PRISMA",
         0.22, 1.20, 12.0, 1500, 900.0, 2500.0, 180, 9.0, 14,
         "Spectromètre imageur SWIR 900–2500 nm (180 bandes) à détecteur MCT refroidi",
         "Spectromètre SWIR refroidi couvrant 900 à 2500 nm en 180 bandes continues. Indispensable pour l'identification fine des minéraux (argiles, carbonates), des hydrocarbures et des panaches de méthane.",
         ["180 bandes de 900 à 2500 nm", "Détecteur HgCdTe refroidi", "GSD ~ 5,0 m à 500 km", "Résolution spectrale 9 nm"]),

    spec("pl_spec_vnir_swir_full", "spectra_tech", "HyperEye-FullRange 400-2500nm",
         68.0, 135.0, 195.0, 65.0, (750, 500, 450), 0.008, 0.8, 0.5, 115.0, 2600.0, 850.0, 9.8, 9, "Héritage EnMAP / CHIME",
         0.28, 1.50, 9.0, 2048, 400.0, 2500.0, 240, 8.5, 14,
         "Spectromètre complet VNIR+SWIR (400–2500 nm, 240 bandes) de classe institutionnelle",
         "Instrument hyperspectral de référence combinant deux spectromètres (VNIR et SWIR) derrière un télescope commun de 28 cm. Il couvre tout le spectre solaire réfléchi en 240 bandes avec un GSD de 3,0 m à 500 km.",
         ["400 à 2500 nm en 240 bandes", "GSD ~ 3,0 m à 500 km", "Télescope Ø 28 cm", "Double plan focal VNIR + SWIR"]),

    spec("pl_spec_ghg_sounder", "cirrus_ir", "AtmoTrace-GHG High-Spectral-Resolution Sounder",
         29.0, 65.0, 95.0, 26.0, (460, 340, 300), 0.015, 1.5, 0.9, 55.0, 900.0, 300.0, 5.2, 8, "4 vols (suivi méthane)",
         0.20, 1.00, 12.0, 1200, 1590.0, 1680.0, 300, 0.3, 14,
         "Spectromètre haute finesse spectrale (0,3 nm) dédié aux panaches de CH4 et CO2",
         "Spectromètre à réseau échelle centré sur les raies d'absorption du méthane et du CO2 autour de 1,65 µm. Sa résolution spectrale de 0,3 nm permet de quantifier les fuites ponctuelles d'installations pétrolières et gazières.",
         ["Résolution spectrale 0,3 nm (300 canaux)", "Bande CH4 / CO2 1590–1680 nm", "GSD ~ 6,0 m à 500 km", "Détection de panaches industriels"]),

    # ---- 5 new SAR payloads
    sar("pl_sar_xband_compact", "radar_tech", "NanoSAR-X Lite",
        32.0, 480.0, 750.0, 36.0, (900, 500, 150), 0.06, 6.0, 2.5, 240.0, 2000.0, 550.0, 4.9, 8, "10 vols",
        9.65, "X", 2.5, 0.5, "phased_array", 1200.0, 7.0, 300.0, 3.5, 22.0, 42.0,
        "SAR bande X allégé (32 kg) pour plateformes de 150 à 200 kg",
        "Version allégée du MicroSAR-X, conçue pour tenir sur des plateformes de 150 à 200 kg. L'antenne plus courte et la puissance RF réduite à 1,2 kW dégradent légèrement le NESZ, mais permettent un satellite radar beaucoup plus économique.",
        ["Masse 32 kg seulement", "Bande X, chirp 300 MHz (rés. < 0,7 m)", "480 W en acquisition", "Compatible plateformes 150–200 kg"]),

    sar("pl_sar_xband_spotlight", "radar_tech", "SpotlightSAR-X Ultra",
        95.0, 1250.0, 2100.0, 110.0, (1400, 750, 250), 0.025, 2.5, 1.2, 600.0, 4800.0, 1200.0, 12.5, 9, "8 vols",
        9.65, "X", 3.8, 0.8, "phased_array", 3800.0, 10.0, 800.0, 2.8, 20.0, 50.0,
        "SAR bande X très haute résolution (chirp 800 MHz, sub-30 cm) et excellent NESZ",
        "Radar bande X de forte puissance doté d'une bande passante de 800 MHz et d'une puissance crête RF de 3,8 kW. Il atteint une résolution distance sub-30 cm et un NESZ inférieur à −22 dB jusqu'à 600 km d'altitude, au prix d'une consommation dépassant le kilowatt.",
        ["Bande passante 800 MHz (rés. < 0,3 m)", "RF crête 3,8 kW, NF 2,8 dB", "Antenne active 3,8 x 0,8 m", "Idéal missions surveillance exigeantes"]),

    sar("pl_sar_cband_maritime", "boreal_sar", "BorealSAR-C Maritime & Ice Monitor",
        135.0, 1100.0, 1800.0, 160.0, (1600, 850, 300), 0.03, 3.0, 1.5, 520.0, 2800.0, 750.0, 13.8, 9, "Héritage Radarsat / Sentinel-1",
        5.405, "C", 4.5, 0.85, "phased_array", 3000.0, 9.0, 200.0, 3.0, 20.0, 48.0,
        "SAR en bande C (5,4 GHz) pour la surveillance maritime, les glaces et les déformations",
        "Radar en bande C moins sensible à l'état de surface et à la pluie que la bande X, offrant une large fauchée pour la surveillance maritime, le suivi des glaces polaires et l'interférométrie InSAR.",
        ["Bande C 5,405 GHz", "Antenne 4,5 x 0,85 m", "Fauchée > 35 km", "Double polarisation VV/VH ou HH/HV"]),

    sar("pl_sar_lband_biomass", "boreal_sar", "BorealSAR-L Foliage & InSAR Radar",
        185.0, 1350.0, 2400.0, 240.0, (1900, 1000, 400), 0.04, 4.0, 2.0, 650.0, 2200.0, 600.0, 17.5, 8, "Héritage ALOS / ROSE-L",
        1.275, "L", 6.0, 1.4, "deployable_reflector", 3500.0, 10.0, 100.0, 2.9, 22.0, 45.0,
        "SAR en bande L (1,27 GHz) pénétrant le couvert végétal pour la biomasse et l'InSAR",
        "Radar à grande longueur d'onde (23 cm) capable de pénétrer la canopée forestière et de maintenir la cohérence interférométrique sur de longues périodes pour mesurer la subsidence des sols et l'humidité.",
        ["Bande L 1,275 GHz (longueur d'onde 23,5 cm)", "Pénétration de la végétation", "Antenne déployable 6,0 x 1,4 m", "Excellente cohérence InSAR"]),

    sar("pl_sar_sband_compact", "boreal_sar", "NovaWave-S Multi-Mode Radar",
        78.0, 780.0, 1300.0, 95.0, (1250, 700, 240), 0.04, 4.0, 1.8, 380.0, 2400.0, 650.0, 9.2, 9, "Héritage NovaSAR-1",
        3.20, "S", 3.4, 0.9, "phased_array", 2200.0, 8.0, 250.0, 3.1, 20.0, 45.0,
        "SAR en bande S (3,2 GHz) offrant un compromis entre bande X et bande C",
        "Radar en bande S inspiré de NovaSAR, conçu pour fonctionner sur des plateformes de 300 à 500 kg avec une bonne robustesse aux fortes pluies tropicales et un mode maritime grand champ.",
        ["Bande S 3,2 GHz", "Masse 78 kg, 780 W en acquisition", "Mode maritime et mode stripmap", "Bande 250 MHz"]),

    # ---- 3 new optical comm terminals
    ocomm("pl_opt_comm_cubesat_1g", "laser_space", "NanoLink-1G CubeSat Laser Terminal",
          2.2, 18.0, 28.0, 1.8, (150, 100, 100), 0.05, 3.0, 1.5, 14.0, 1.0, 0.65, 9, ">20 CubeSats",
          0.05, 1550.0, 0.5, 35.0, 3.5, ["CCSDS_141.0-B-1"],
          "Mini-terminal laser 1 Gbit/s (2,2 kg) pour CubeSats 12U/16U et microsatellites",
          "Tête optique laser miniaturisée de 5 cm d'ouverture destinée aux CubeSats et petits satellites souhaitant descendre jusqu'à 1 Gbit/s vers une station sol optique sans coordination de fréquence RF.",
          ["1 Gbit/s à 1550 nm", "Format < 2U, masse 2,2 kg", "Laser 0,5 W, ouverture 5 cm", "Prix 0,65 M€"]),

    ocomm("pl_opt_comm_isl_25g", "tesa_link", "TeraLink-25G Constellation Terminal",
          19.0, 80.0, 115.0, 16.0, (360, 280, 260), 0.008, 0.4, 0.4, 65.0, 25.0, 3.8, 9, "Héritage SDA / EDRS",
          0.12, 1550.0, 2.5, 14.0, 1.2, ["SDA_Tranche1", "SDA_Tranche2", "CCSDS_141.0-B-1"],
          "Terminal laser 25 Gbit/s à détection cohérente pour liaisons inter-satellites et sol",
          "Terminal optique cohérent BPSK/QPSK de TeraLink Photonics, doté d'un amplificateur optique de 2,5 W et d'un télescope de 12 cm. Il assure des liaisons à 25 Gbit/s avec une marge de liaison élevée même à basse élévation.",
          ["25 Gbit/s cohérent à 1550 nm", "Puissance optique 2,5 W, Ø 12 cm", "Pointage fin 1,2 µrad", "Compatible SDA Tranche 1/2"]),

    ocomm("pl_opt_comm_heavy_100g", "tesa_link", "TeraLink-100G Trunk Optical Terminal",
          34.0, 125.0, 175.0, 30.0, (480, 360, 340), 0.005, 0.25, 0.25, 105.0, 100.0, 6.5, 8, "Héritage relais GEO/LEO",
          0.18, 1550.0, 5.0, 10.0, 0.8, ["SDA_Tranche2", "CCSDS_141.0-B-1", "EDRS"],
          "Terminal laser très haut débit 100 Gbit/s (Ø 18 cm, 5 W) pour dorsales spatiales",
          "Terminal optique de grande ouverture (18 cm) et de forte puissance laser (5 W) conçu pour vider en quelques dizaines de secondes les mémoires de masse de satellites SAR ou très haute résolution.",
          ["100 Gbit/s à 1550 nm", "Télescope Ø 18 cm, laser 5 W", "Suivi ultra-fin 0,8 µrad", "Marge de liaison très confortable"]),

    # ---- 2 new QKD payloads
    qkd("pl_qkd_cubesat_compact", "quanta_space", "SpeQ-Cube-850 Nano QKD Payload",
        5.5, 22.0, 32.0, 5.0, (220, 160, 140), 0.015, 0.8, 0.8, 18.0, 1.65, 8, "2 CubeSats en vol",
        "BB84_decoy_state", 0.09, 60.0, 850.0, 2.2, True,
        "Charge utile QKD miniaturisée (9 cm, 60 MHz) pour CubeSat 16U ou SmallSat 50 kg",
        "Terminal QKD compact permettant de démontrer la distribution quantique de clés sur une petite plateforme. Son télescope de 9 cm et sa source à 60 MHz génèrent un débit de clé plus modeste que les grands terminaux, mais à moins de la moitié du prix.",
        ["Masse 5,5 kg, volume 5 L", "Télescope Ø 9 cm, source 60 MHz", "BB84 decoy-state à 850 nm", "Prix 1,65 M€"]),

    qkd("pl_qkd_highrate_25cm", "quanta_space", "QuantaCore-250 High-Rate QKD Terminal",
        38.0, 75.0, 110.0, 36.0, (550, 400, 380), 0.003, 0.2, 0.2, 60.0, 6.4, 8, "Héritage QEYSSat / Eagle-1",
        "BB84_decoy_state", 0.25, 250.0, 850.0, 0.9, True,
        "Terminal QKD haute performance (Ø 25 cm, source 250 MHz) pour fort débit de clés",
        "Terminal QKD institutionnel doté d'un télescope de 25 cm, d'une source à 250 MHz et d'un système d'acquisition et de suivi sub-microradian. Il maximise le débit de clé secrète même sur des orbites à 600–800 km.",
        ["Télescope Ø 25 cm, source 250 MHz", "Pointage fin 0,9 µrad", "Fort taux de clés secrètes (sifted > 30 kbit/s)", "Conçu pour réseaux gouvernementaux"]),

    # ---- 4 new Radio Comm payloads
    rcomm("pl_rf_ais_adsb", "rf_payload", "MarTrack AIS + ADS-B Receiver Suite",
          3.2, 14.0, 20.0, 3.0, (200, 150, 100), 0.2, 11.0, 0.55, 9, ">40 satellites",
          0.162, 2.25, 4.0, 8.0, 6.0, 25.0, 15.0,
          "Récepteur de surveillance maritime (AIS VHF) et aérienne (ADS-B 1090 MHz)",
          "Charge utile secondaire ou principale légère combinant un récepteur AIS multi-canaux à décollision par traitement du signal et un récepteur ADS-B pour le suivi du trafic maritime et aérien mondial.",
          ["AIS 162 MHz + ADS-B 1090 MHz", "Faible masse 3,2 kg et puissance 14 W", "Idéal en passager secondaire (hosted payload)", "Descente des pistes en bande S"]),

    rcomm("pl_rf_iot_uhf_sband", "rf_payload", "NetSat-IoT Store & Forward Payload",
          7.5, 28.0, 45.0, 7.0, (260, 200, 140), 0.15, 22.0, 1.15, 9, "18 satellites de constellation",
          0.401, 2.22, 8.0, 12.0, 9.0, 40.0, 35.0,
          "Charge utile IoT spatiale (collecte UHF/L et redescente bande S)",
          "Charge utile de collecte de données pour balises environnementales, bouées océanographiques et capteurs isolés. Elle reçoit des milliers de messages courts et les retransmet aux stations sol en bande S.",
          ["Collecte multi-canaux 400 MHz / bande L", "Émission bande S 8 W (12 dBi)", "Débit jusqu'à 35 Mbit/s", "Traitement SDR reconfigurable en vol"]),

    rcomm("pl_rf_xband_relay", "rf_payload", "RelayX-300 Tactical Transponder",
          19.0, 65.0, 95.0, 18.0, (380, 280, 200), 0.05, 50.0, 2.6, 9, "12 vols",
          7.9, 8.2, 18.0, 19.0, 17.0, 220.0, 300.0,
          "Transpondeur et relais de données en bande X (300 Mbit/s, 18 W RF)",
          "Charge utile de télécommunications en bande X assurant le relais de données haut débit entre théâtres d'opérations et stations principales, avec antenne cornet à grand gain (19 dBi) et amplificateur GaN de 18 W.",
          ["Bande X 7,9 / 8,2 GHz", "Puissance RF 18 W, gain 19 dBi", "Jusqu'à 300 Mbit/s", "Amplificateur GaN haut rendement"]),

    rcomm("pl_rf_kaband_broadband", "rf_payload", "KaStream-1200 High-Throughput Payload",
          42.0, 150.0, 220.0, 45.0, (580, 440, 320), 0.02, 120.0, 5.4, 9, "Constellations LEO haut débit",
          29.5, 19.7, 35.0, 32.0, 30.0, 500.0, 1200.0,
          "Charge utile large bande en bande Ka (1,2 Gbit/s, antenne orientable 32 dBi)",
          "Charge utile de télécommunications à haut débit en bande Ka (montée 29,5 GHz, descente 19,7 GHz) dotée d'une antenne orientable de 32 dBi et d'un tube/SSPA de 35 W RF.",
          ["Bande Ka 29,5 / 19,7 GHz", "RF 35 W, antenne 32 dBi", "Débit 1,2 Gbit/s (bande 500 MHz)", "Faisceau orientable"]),
]
