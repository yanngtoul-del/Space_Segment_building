"""Script de génération du fichier de liaison des systèmes optiques de Space_Segment_building
vers Conception_optique (PyOptic).

Ce fichier structure chaque système optique avec :
- Métadonnées et contexte mission SSB (GSD, fauchée, altitude nominale, satellite cible)
- Spécifications optiques complètes (EPD, EFL, F/#, FOV, longueurs d'onde, capteur)
- Architecture optique et prescription PyOptic (surfaces, rayons de courbure, coniques, épaisseurs, matériaux)
- Benchmarks et critères d'évaluation pour les étudiants (tache d'Airy, rapport d'échantillonnage Q, limite de diffraction vs taille de pixel, MTF à Nyquist)
- Fiches pédagogiques et comportements optiques clés à observer dans PyOptic
"""
import json
import math
from pathlib import Path


def calculate_rc_prescriptions(efl_mm: float, epd_mm: float, back_focus_mm: float):
    """Calcule la prescription géométrique exacte d'un Ritchey-Chrétien (k1 et k2 hyperboliques)."""
    d = 0.25 * efl_mm
    L = d + back_focus_mm
    m = (efl_mm - L) / max(1e-6, d)
    R1 = -2.0 * d * efl_mm / (efl_mm - L)
    R2 = -2.0 * d * L / (efl_mm - L - d)
    k1 = -1.0 - 2.0 * (L / d) / (m ** 3)
    k2 = -1.0 - (2.0 / ((m - 1.0) ** 3)) * (m * (2.0 * m - 1.0) + (L / d))
    return {
        "d_mm": round(d, 3),
        "L_mm": round(L, 3),
        "R1_mm": round(R1, 3),
        "k1": round(k1, 6),
        "R2_mm": round(R2, 3),
        "k2": round(k2, 6),
        "m_sec": round(m, 3)
    }


def calculate_cassegrain_prescriptions(efl_mm: float, epd_mm: float, back_focus_mm: float):
    """Calcule la prescription d'un Cassegrain classique (k1=-1 parabole, k2 hyperbolique)."""
    d = 0.25 * efl_mm
    L = d + back_focus_mm
    m = (efl_mm - L) / max(1e-6, d)
    R1 = -2.0 * d * efl_mm / (efl_mm - L)
    R2 = -2.0 * d * L / (efl_mm - L - d)
    k1 = -1.0
    k2 = -((m + 1.0) / (m - 1.0)) ** 2
    return {
        "d_mm": round(d, 3),
        "L_mm": round(L, 3),
        "R1_mm": round(R1, 3),
        "k1": round(k1, 6),
        "R2_mm": round(R2, 3),
        "k2": round(k2, 6),
        "m_sec": round(m, 3)
    }


def calculate_korsch_tma_prescriptions(efl_mm: float, epd_mm: float):
    """Calcule la prescription normalisée d'un Anastigmat à Trois Miroirs de Korsch."""
    c1, c2 = -0.50, -1.25
    c3 = c2 - c1  # -0.75 condition de Petzval plate S_IV = 0
    t1 = -0.75
    t2 = 1.80
    u1 = -2.0 * c1
    y2 = 1.0 + t1 * u1
    u2 = -u1 - 2.0 * c2 * y2
    y3 = y2 + t2 * u2
    u3 = -u2 - 2.0 * c3 * y3
    t3 = -y3 / u3
    efl_unit = abs(1.0 / u3)
    s = efl_mm / efl_unit

    R1, R2, R3 = s / c1, s / c2, s / c3
    d1, d2, d3 = s * t1, s * t2, s * t3

    k1 = -0.8851
    k2 = -3.4242
    k3 = -0.2898

    return {
        "R1_mm": round(R1, 3),
        "k1": k1,
        "d1_mm": round(d1, 3),
        "R2_mm": round(R2, 3),
        "k2": k2,
        "d2_mm": round(d2, 3),
        "R3_mm": round(R3, 3),
        "k3": k3,
        "d3_mm": round(d3, 3)
    }


def build_system_record(p: dict) -> dict:
    pid = p["id"]
    ptype = p["payload_type"]
    name = p["name"]

    # Paramètres de base
    epd_m = p.get("aperture_diameter_m") or p.get("telescope_aperture_m") or 0.1
    if epd_m == 0.0:
        if "spec_vnir_compact" in pid:
            epd_m = 0.05
        elif "spec_hyperspectral_vnir" in pid:
            epd_m = 0.18
        elif "spec_lumina" in pid:
            epd_m = 0.08
        elif "spec_swir_180" in pid:
            epd_m = 0.20
        elif "spec_vnir_swir_full" in pid:
            epd_m = 0.28
        elif "spec_ghg_sounder" in pid:
            epd_m = 0.22
        elif "spec_atmo_tropo_ghg" in pid:
            epd_m = 0.24
        else:
            epd_m = 0.10

    epd_mm = epd_m * 1000.0

    efl_m = p.get("focal_length_m") or 0.0
    if efl_m == 0.0:
        f_num_default = 6.0 if "spec" in ptype else 10.0
        efl_m = epd_m * f_num_default
    efl_mm = efl_m * 1000.0
    f_num = p.get("f_number") or round(efl_mm / epd_mm, 2)

    p_pitch_um = p.get("pixel_pitch_um") or 5.5
    n_pix = p.get("detector_pixels_cross_track") or 8000
    if "spec" in ptype:
        n_pix = p.get("detector_spatial_pixels") or 2048

    # Longueurs d'onde
    w_min_nm = p.get("min_wavelength_nm") or p.get("spectral_range_min_nm") or 450.0
    w_max_nm = p.get("max_wavelength_nm") or p.get("spectral_range_max_nm") or 900.0
    if "comm" in ptype:
        w_min_nm = 1530.0
        w_max_nm = 1565.0
        w_center_nm = p.get("wavelength_nm") or 1550.0
    elif "qkd" in ptype:
        w_min_nm = 840.0
        w_max_nm = 860.0
        w_center_nm = p.get("wavelength_nm") or 850.0
    elif "swir" in pid:
        w_min_nm = 1000.0
        w_max_nm = 2400.0
        w_center_nm = 1600.0
    else:
        w_center_nm = (w_min_nm + w_max_nm) / 2.0

    primary_wl_um = round(w_center_nm / 1000.0, 4)
    w_min_um = round(w_min_nm / 1000.0, 4)
    w_max_um = round(w_max_nm / 1000.0, 4)

    # Champ de vue
    sensor_width_mm = (n_pix * p_pitch_um) / 1000.0
    fov_rad = 2.0 * math.atan(sensor_width_mm / (2.0 * max(1e-3, efl_mm)))
    fov_deg = round(math.degrees(fov_rad), 3)

    # Métriques de diffraction & échantillonnage à 500 km
    alt_m = 500e3
    airy_radius_um = round(1.22 * primary_wl_um * f_num, 3)
    diff_lim_rad = 1.22 * (primary_wl_um * 1e-6) / epd_m
    diff_spot_ground_m = round(diff_lim_rad * alt_m, 3)
    gsd_nadir_500km_m = round((p_pitch_um * 1e-6 * alt_m) / efl_m, 3) if efl_m > 0 else 0.0
    swath_500km_km = round((n_pix * gsd_nadir_500km_m) / 1000.0, 2)
    nyquist_lp_mm = round(1000.0 / (2.0 * p_pitch_um), 2)
    q_sampling = round((primary_wl_um * f_num) / p_pitch_um, 3)

    # Détermination de l'architecture optique et des surfaces
    surfaces = []
    arch_type = ""
    pyoptic_preset_call = ""
    pedagogical_focus = ""

    if "pl_opt_cubesat_6cm" in pid:
        arch_type = "Refractive_Petzval_Achromat"
        pyoptic_preset_call = "cooke_triplet_or_petzval_scaled(efl_mm=450, epd_mm=60)"
        pedagogical_focus = (
            "Comportement d'un objectif refractif compact pour CubeSat : "
            "aberration chromatique axiale et laterale (verres Crown/Flint), "
            "vignettage en bord de champ (loi en cos^4), courbure de champ de Petzval "
            "et sensibilite au cyclage thermique (defocalisation thermique df/dT)."
        )
        surfaces = [
            {"label": "STOP_Aperture", "type": "Plane", "thickness": 10.0, "material": "AIR", "is_stop": True, "semi_diameter": 30.0},
            {"label": "L1_Front", "type": "Spherical", "radius": 140.0, "thickness": 12.0, "material": "N-LAK9", "semi_diameter": 32.0},
            {"label": "L1_Rear", "type": "Spherical", "radius": -280.0, "thickness": 25.0, "material": "AIR", "semi_diameter": 32.0},
            {"label": "L2_Flint_Front", "type": "Spherical", "radius": -110.0, "thickness": 6.0, "material": "F2", "semi_diameter": 28.0},
            {"label": "L2_Flint_Rear", "type": "Spherical", "radius": 160.0, "thickness": 45.0, "material": "AIR", "semi_diameter": 28.0},
            {"label": "L3_Rear_Crown", "type": "Spherical", "radius": 180.0, "thickness": 10.0, "material": "N-LAK9", "semi_diameter": 25.0},
            {"label": "L3_Rear_Flat", "type": "Plane", "thickness": 340.0, "material": "AIR", "semi_diameter": 25.0},
            {"label": "Focal_Plane", "type": "Plane", "thickness": 0.0, "material": "AIR", "semi_diameter": 15.0}
        ]

    elif "pl_opt_wide_swath_18cm" in pid:
        arch_type = "Compact_TMA_Cook"
        pyoptic_preset_call = "three_mirror_anastigmat_tma(focal_length_mm=900, epd_mm=180)"
        pedagogical_focus = (
            "Anastigmat compact grand champ sans foyer intermediaire : "
            "correction simultanee de l'aberration spherique, coma et astigmatisme "
            "sur une fauchee geante (>55 km a 500 km). Obscuration centrale nulle "
            "en configuration desaxee (off-axis), preservant la fonction de transfert "
            "de modulation (MTF) aux moyennes frequences."
        )
        korsch_p = calculate_korsch_tma_prescriptions(efl_mm, epd_mm)
        surfaces = [
            {"label": "M1_Primary_TMA", "type": "Conic", "radius": korsch_p["R1_mm"], "conic": korsch_p["k1"], "thickness": korsch_p["d1_mm"], "material": "AIR", "is_mirror": True, "is_stop": True, "semi_diameter": epd_mm * 0.52},
            {"label": "M2_Secondary_TMA", "type": "Conic", "radius": korsch_p["R2_mm"], "conic": korsch_p["k2"], "thickness": korsch_p["d2_mm"], "material": "AIR", "is_mirror": True, "semi_diameter": epd_mm * 0.22},
            {"label": "M3_Tertiary_TMA", "type": "Conic", "radius": korsch_p["R3_mm"], "conic": korsch_p["k3"], "thickness": korsch_p["d3_mm"], "material": "AIR", "is_mirror": True, "semi_diameter": epd_mm * 0.40},
            {"label": "Focal_Plane", "type": "Plane", "thickness": 0.0, "material": "AIR", "semi_diameter": sensor_width_mm / 2.0}
        ]

    elif any(k in pid for k in ["korsch", "submeter_highres", "veryhighres_1m", "helios_70cm"]):
        arch_type = "Korsch_TMA_Three_Mirror"
        pyoptic_preset_call = f"korsch_tma_telescope(focal_length_mm={efl_mm:.1f}, epd_mm={epd_mm:.1f})"
        pedagogical_focus = (
            "Telescope de Korsch a trois miroirs avec foyer intermediaire et diaphragme de Lyot : "
            "elimination totale des 4 aberrations de Seidel (S_I=0, S_II=0, S_III=0, champ de Petzval plat S_IV=0). "
            "Permet d'atteindre des resolutions sub-metriques extremes (0,29 m a 0,77 m) avec un miroir en SiC athermique. "
            "Les etudiants peuvent verifier l'absence d'astigmatisme hors-axe et la rejection de lumiere parasite au foyer intermediaire."
        )
        korsch_p = calculate_korsch_tma_prescriptions(efl_mm, epd_mm)
        surfaces = [
            {"label": "M1_Primary_Ellipsoid", "type": "Conic", "radius": korsch_p["R1_mm"], "conic": korsch_p["k1"], "thickness": korsch_p["d1_mm"], "material": "AIR", "is_mirror": True, "is_stop": True, "semi_diameter": epd_mm * 0.52},
            {"label": "M2_Secondary_Hyperboloid", "type": "Conic", "radius": korsch_p["R2_mm"], "conic": korsch_p["k2"], "thickness": korsch_p["d2_mm"], "material": "AIR", "is_mirror": True, "semi_diameter": epd_mm * 0.22},
            {"label": "M3_Tertiary_Relay", "type": "Conic", "radius": korsch_p["R3_mm"], "conic": korsch_p["k3"], "thickness": korsch_p["d3_mm"], "material": "AIR", "is_mirror": True, "semi_diameter": epd_mm * 0.42},
            {"label": "Focal_Plane", "type": "Plane", "thickness": 0.0, "material": "AIR", "semi_diameter": sensor_width_mm / 2.0}
        ]

    elif any(k in pid for k in ["stellara_20cm", "stellara_35cm", "opt_pan_compact"]):
        arch_type = "Ritchey_Chretien_Cassegrain"
        pyoptic_preset_call = f"ritchey_chretien_telescope(focal_length_mm={efl_mm:.1f}, epd_mm={epd_mm:.1f}, back_focus_mm=180.0)"
        pedagogical_focus = (
            "Telescope Ritchey-Chretien a deux miroirs hyperboliques (k1 < -1, k2 < -1) : "
            "correction simultanee de l'aberration spherique et de la coma (systeme aplanetique). "
            "Les etudiants observent l'astigmatisme residuel et la courbure de champ en bord de capteur, "
            "expliquant pourquoi les grands telescopes RC ajoutent souvent un groupe correcteur a deux lentilles."
        )
        rc_p = calculate_rc_prescriptions(efl_mm, epd_mm, 180.0)
        surfaces = [
            {"label": "M1_Primary_Hyperbola", "type": "Conic", "radius": rc_p["R1_mm"], "conic": rc_p["k1"], "thickness": -rc_p["d_mm"], "material": "AIR", "is_mirror": True, "is_stop": True, "semi_diameter": epd_mm * 0.52},
            {"label": "M2_Secondary_Hyperbola", "type": "Conic", "radius": rc_p["R2_mm"], "conic": rc_p["k2"], "thickness": rc_p["L_mm"], "material": "AIR", "is_mirror": True, "semi_diameter": epd_mm * 0.24},
            {"label": "Focal_Plane", "type": "Plane", "thickness": 0.0, "material": "AIR", "semi_diameter": sensor_width_mm / 2.0}
        ]

    elif "opt_medium_25cm" in pid:
        arch_type = "Classical_Cassegrain"
        pyoptic_preset_call = f"cassegrain_telescope(focal_length_mm={efl_mm:.1f}, epd_mm={epd_mm:.1f}, back_focus_mm=200.0)"
        pedagogical_focus = (
            "Cassegrain classique (primaire parabolique k1=-1, secondaire hyperbolique k2 < -1) : "
            "aberration spherique nulle sur l'axe, mais coma hors axe lineaire avec l'angle de champ. "
            "Les etudiants comparent son diagramme de spot hors-axe avec le Ritchey-Chretien pour visualiser "
            "la celebre tache de coma triangulaire."
        )
        cas_p = calculate_cassegrain_prescriptions(efl_mm, epd_mm, 200.0)
        surfaces = [
            {"label": "M1_Primary_Parabola", "type": "Conic", "radius": cas_p["R1_mm"], "conic": cas_p["k1"], "thickness": -cas_p["d_mm"], "material": "AIR", "is_mirror": True, "is_stop": True, "semi_diameter": epd_mm * 0.52},
            {"label": "M2_Secondary_Hyperbola", "type": "Conic", "radius": cas_p["R2_mm"], "conic": cas_p["k2"], "thickness": cas_p["L_mm"], "material": "AIR", "is_mirror": True, "semi_diameter": epd_mm * 0.25},
            {"label": "Focal_Plane", "type": "Plane", "thickness": 0.0, "material": "AIR", "semi_diameter": sensor_width_mm / 2.0}
        ]

    elif "opt_swir_20cm" in pid:
        arch_type = "Catadioptric_SWIR"
        pyoptic_preset_call = f"catadioptric_swir_telescope(focal_length_mm={efl_mm:.1f}, epd_mm={epd_mm:.1f})"
        pedagogical_focus = (
            "Optique infrarouge SWIR (1,0 a 2,4 um) combinant miroirs et lentilles en Silicium/Germanium : "
            "gestion de l'indice de refraction eleve du Silicium (n ~ 3,48) et du Germanium (n ~ 4,0), "
            "minimisation des reflexions de Fresnel par traitement multicouche dielectrique, "
            "et ecran froid de Lyot integre pour limiter le fond thermique parasite."
        )
        rc_p = calculate_rc_prescriptions(efl_mm, epd_mm, 150.0)
        surfaces = [
            {"label": "M1_Primary", "type": "Conic", "radius": rc_p["R1_mm"], "conic": rc_p["k1"], "thickness": -rc_p["d_mm"], "material": "AIR", "is_mirror": True, "is_stop": True, "semi_diameter": epd_mm * 0.52},
            {"label": "M2_Secondary", "type": "Conic", "radius": rc_p["R2_mm"], "conic": rc_p["k2"], "thickness": rc_p["L_mm"] - 40.0, "material": "AIR", "is_mirror": True, "semi_diameter": epd_mm * 0.25},
            {"label": "SWIR_Corrector_Si", "type": "Spherical", "radius": -120.0, "thickness": 6.0, "material": "SILICON", "semi_diameter": 25.0},
            {"label": "SWIR_Corrector_Rear", "type": "Plane", "thickness": 34.0, "material": "AIR", "semi_diameter": 25.0},
            {"label": "Cold_Shield_Detector", "type": "Plane", "thickness": 0.0, "material": "AIR", "semi_diameter": 15.0}
        ]

    elif "spec" in ptype:
        if "atmo_tropo_ghg" in pid:
            arch_type = "Immersed_Silicon_Grating_Spectrometer"
            pyoptic_preset_call = "immersed_grating_spectrometer(lines_mm=400, order=1, index=3.48)"
            pedagogical_focus = (
                "Reseau de diffraction par immersion dans le Silicium monocristallin : "
                "la dispersion angulaire est multipliee par l'indice de refraction n ~ 3,48, ce qui "
                "permet d'atteindre une finesse spectrale record de 0,22 nm (resolution des doublets fins "
                "de CO2 et CH4) dans un volume 3,4 fois plus compact qu'un reseau en reflexion dans l'air. "
                "Comportement cle : equation du reseau d'immersion n*(sin alpha + sin beta) = m*lambda / d."
            )
        elif "ghg_sounder" in pid:
            arch_type = "Echelle_Grating_Spectrometer"
            pyoptic_preset_call = "echelle_spectrometer(lines_mm=79, blaze_deg=63.5, order=5)"
            pedagogical_focus = (
                "Spectrometre echelle fonctionnant a ordre de diffraction eleve (m=5 a 10) et fort angle de blaze : "
                "dispersion tres elevee pour l'analyse isotopique des gaz a effet de serre (0,3 nm de resolution). "
                "Separation des ordres par dispersion croisee (prisme ou filtre passe-bande)."
            )
        elif "lumina" in pid:
            arch_type = "Fabry_Perot_Interferometer"
            pyoptic_preset_call = "fabry_perot_tunable_filter(gap_um=15.0, finesse=35)"
            pedagogical_focus = (
                "Spectrometre par interferometre Fabry-Perot a commande piezoelectrique : "
                "selection agile des bandes spectrales par balayage de l'epaisseur d'air inter-miroirs. "
                "Etude de l'intervalle spectral libre (FSR = lambda^2 / 2d) et de la finesse optique F."
            )
        else:
            arch_type = "Offner_Czerny_Turner_Spectrometer"
            pyoptic_preset_call = f"offner_convex_grating_spectrometer(aperture_mm={epd_mm:.1f}, bands={p.get('number_of_spectral_bands', 120)})"
            pedagogical_focus = (
                "Spectrometre imageur Offner a reseau convexe ou Czerny-Turner : "
                "l'architecture Offner annule l'astigmatisme et la coma de Seidel tout en conservant "
                "une distorsion spectrale (smile) et spatiale (keystone) inferieure a 1% d'un pixel. "
                "Crucial pour l'inversion geophysique et mineralogique hyperspectrale."
            )

        surfaces = [
            {"label": "Fore_Telescope_Pupil", "type": "Plane", "thickness": 120.0, "material": "AIR", "is_stop": True, "semi_diameter": epd_mm * 0.5},
            {"label": "Slit_Plane", "type": "Plane", "thickness": 150.0, "material": "AIR", "semi_diameter": 12.0},
            {"label": "Collimator_Mirror", "type": "Spherical", "radius": -300.0, "thickness": -150.0, "material": "AIR", "is_mirror": True, "semi_diameter": 35.0},
            {"label": "Diffraction_Grating", "type": "Plane", "thickness": 150.0, "material": "AIR", "is_mirror": True, "semi_diameter": 30.0, "grating_lines_per_mm": 600.0 if "atmo" not in pid else 400.0},
            {"label": "Camera_Mirror", "type": "Spherical", "radius": -300.0, "thickness": -150.0, "material": "AIR", "is_mirror": True, "semi_diameter": 40.0},
            {"label": "Spectrometer_Detector", "type": "Plane", "thickness": 0.0, "material": "AIR", "semi_diameter": sensor_width_mm / 2.0}
        ]

    elif "comm" in ptype or "qkd" in ptype:
        is_qkd = "qkd" in ptype
        arch_type = "Afocal_Beam_Expander_Cassegrain" if not is_qkd else "Afocal_QKD_Transceiver"
        pyoptic_preset_call = f"afocal_beam_expander(epd_in_mm=5.0, epd_out_mm={epd_mm:.1f}, mag={epd_mm/5.0:.1f})"
        beam_type_label = "quantique QKD a 850 nm" if is_qkd else "laser optique telecom a 1550 nm"
        pedagogical_focus = (
            f"Terminal {beam_type_label} : "
            "telescope d'emission afocal elargisseur de faisceau (Beam Expander) diffraction-limited. "
            "L'angle de divergence du faisceau emis theta ~ 1.22 * lambda / D est inversement proportionnel "
            "a l'ouverture. Les etudiants simulent l'impact des aberrations du front d'onde (WFE RMS < lambda/14) "
            "sur la baisse de gain d'antenne (critere de Marechal / formule de Ruze) et l'exigence de stabilite ADCS/FSM."
        )
        div_urad = round(1.22 * (primary_wl_um * 1e-6 / epd_m) * 1e6, 2)
        surfaces = [
            {"label": "Laser_Fiber_Waist", "type": "Plane", "thickness": 30.0, "material": "AIR", "semi_diameter": 2.5},
            {"label": "Collimator_Lens", "type": "EvenAsphere", "radius": 15.0, "conic": -0.5, "thickness": 80.0, "material": "N-SF11", "semi_diameter": 6.0},
            {"label": "M2_Secondary_Beam_Expander", "type": "Conic", "radius": -epd_mm * 0.4, "conic": -2.5, "thickness": -epd_mm * 0.6, "material": "AIR", "is_mirror": True, "semi_diameter": epd_mm * 0.18},
            {"label": "M1_Primary_Collimator", "type": "Conic", "radius": -epd_mm * 1.5, "conic": -1.0, "thickness": epd_mm * 1.0, "material": "AIR", "is_mirror": True, "semi_diameter": epd_mm * 0.52},
            {"label": "Far_Field_Aperture", "type": "Plane", "thickness": 0.0, "material": "AIR", "semi_diameter": epd_mm * 0.55}
        ]

    regime_str = (
        "Diffraction-Limited (Oversampled, Q > 1.5)" if q_sampling > 1.5 else (
            "Well-Matched (Nyquist Balanced, 0.9 <= Q <= 1.5)" if q_sampling >= 0.9 else
            "Detector-Limited (Undersampled, Q < 0.9)"
        )
    )
    spot_vs_pixel_desc = "Tache d'Airy etalee sur plusieurs pixels" if q_sampling > 1.5 else "Pixel plus grand que la tache de diffraction"

    record = {
        "id": pid,
        "name": name,
        "payload_type": ptype,
        "supplier_name": p.get("supplier_name", "Unknown"),
        "flight_heritage": p.get("flight_heritage", "Standard"),
        "trl": p.get("trl", 9),
        "dimensions_mm": p.get("dimensions_mm", [200, 200, 200]),
        "mass_kg": p.get("mass_kg", 10.0),
        "power_w": p.get("operational_power_w", 20.0),
        "cost_meur": p.get("price_meur", 1.0),
        "description": p.get("description", ""),
        "long_description": p.get("long_description", ""),
        "key_features": p.get("key_features", []),
        "optical_specifications": {
            "aperture_diameter_m": epd_m,
            "aperture_diameter_mm": epd_mm,
            "focal_length_m": efl_m,
            "focal_length_mm": efl_mm,
            "f_number": f_num,
            "pixel_pitch_um": p_pitch_um,
            "detector_pixels_cross_track": n_pix,
            "sensor_width_mm": round(sensor_width_mm, 2),
            "fov_full_deg": fov_deg,
            "field_angles_deg": [0.0, round(fov_deg * 0.25, 3), round(fov_deg * 0.5, 3)],
            "primary_wavelength_um": primary_wl_um,
            "min_wavelength_um": w_min_um,
            "max_wavelength_um": w_max_um,
            "wavelengths_library": [
                {"value_um": w_min_um, "weight": 0.5, "label": "Band_Min"},
                {"value_um": primary_wl_um, "weight": 1.0, "label": "Band_Center", "is_primary": True},
                {"value_um": w_max_um, "weight": 0.5, "label": "Band_Max"}
            ],
            "optics_transmission": p.get("optics_transmission", 0.85),
            "optics_mtf_at_nyquist": p.get("optics_mtf_at_nyquist", 0.25),
            "quantum_efficiency_avg": p.get("quantum_efficiency_avg", 0.70)
        },
        "mission_context": {
            "reference_altitude_km": 500.0,
            "gsd_nadir_at_500km_m": gsd_nadir_500km_m,
            "swath_at_500km_km": swath_500km_km,
            "diffraction_spot_ground_500km_m": diff_spot_ground_m,
            "pointing_accuracy_deg": p.get("required_pointing_accuracy_deg", 0.02),
            "pointing_stability_arcsec_s": p.get("required_pointing_stability_arcsec_s", 2.0),
            "max_jitter_arcsec": p.get("max_tolerated_jitter_arcsec", 1.0)
        },
        "optical_architecture": {
            "family": arch_type,
            "pyoptic_preset_call": pyoptic_preset_call,
            "prescription_surfaces": surfaces
        },
        "benchmarks_and_physics": {
            "airy_radius_um": airy_radius_um,
            "nyquist_frequency_lp_mm": nyquist_lp_mm,
            "diffraction_limit_rad": round(diff_lim_rad, 8),
            "diffraction_limit_arcsec": round(math.degrees(diff_lim_rad) * 3600.0, 2),
            "sampling_ratio_Q": q_sampling,
            "regime": regime_str,
            "beam_divergence_urad": round(diff_lim_rad * 1e6, 2) if "comm" in ptype or "qkd" in ptype else None
        },
        "student_pedagogical_insights": {
            "learning_objectives": pedagogical_focus,
            "key_tradeoffs": [
                f"Compromis GSD vs Fauchee : GSD = {gsd_nadir_500km_m} m vs Fauchee = {swath_500km_km} km a 500 km.",
                f"Regime optique Q = {q_sampling:.2f} ({spot_vs_pixel_desc}).",
                f"Sensibilite au pointage : stabilite requise {p.get('required_pointing_stability_arcsec_s', 'N/A')} arcsec/s vis-a-vis du temps d'integration."
            ]
        }
    }
    return record


def main():
    payloads = json.load(open('data/catalogs/payloads.json', encoding='utf-8'))
    optical_payloads = [p for p in payloads if p.get('payload_type') in ['optical_imager', 'spectrometer', 'optical_comm', 'qkd']]

    registry = {
        "metadata": {
            "title": "Space Segment Building - Optical Systems Reference Registry (Fichier de Liaison)",
            "version": "1.0.0",
            "source_repository": "Space_Segment_building",
            "target_software": "Conception_optique (PyOptic)",
            "author": "Antigravity Assistant for Space Segment Building & PyOptic Education",
            "date": "2026-11-11",
            "description": "Fichier de liaison exhaustif isolant tous les systemes optiques spatiaux (imageurs pan/multi/hyperspectraux, spectrometres imageurs et atmospheriques, terminaux de telecommunications optiques laser et terminaux quantiques QKD) avec leurs specifications physiques, architectures optiques, prescriptions geometriques et bancs d'essais pedagogiques pour PyOptic.",
            "total_systems": len(optical_payloads),
            "categories_breakdown": {
                "optical_imager": sum(1 for p in optical_payloads if p["payload_type"] == "optical_imager"),
                "spectrometer": sum(1 for p in optical_payloads if p["payload_type"] == "spectrometer"),
                "optical_comm": sum(1 for p in optical_payloads if p["payload_type"] == "optical_comm"),
                "qkd": sum(1 for p in optical_payloads if p["payload_type"] == "qkd")
            }
        },
        "systems": [build_system_record(p) for p in optical_payloads]
    }

    # 1. Sauvegarde dans Space_Segment_building
    out_ssb = Path("data/optical_systems_bridge.json")
    out_ssb.parent.mkdir(parents=True, exist_ok=True)
    with open(out_ssb, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)
    print(f"Enregistre dans SSB : {out_ssb.resolve()} ({len(registry['systems'])} systemes)")

    # 2. Sauvegarde dans Conception_optique
    target_dir = Path(r"C:\Users\Lapto\PycharmProjects\Conception_optique\data")
    target_dir.mkdir(parents=True, exist_ok=True)
    out_pyoptic = target_dir / "space_segment_optics.json"
    with open(out_pyoptic, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)
    print(f"Enregistre dans Conception_optique : {out_pyoptic.resolve()}")


if __name__ == "__main__":
    main()
