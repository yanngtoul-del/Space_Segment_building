"""Generate the official set of mission specification sheets (fiches de spécification mission) in data/missions/."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ssb.core.mission import MissionSpecification  # noqa: E402

MISSIONS_DIR = ROOT / "data" / "missions"


MISSIONS: list[tuple[str, dict]] = [
    # ------------------------------------------------------------------ 1. Observation Optique Légère & Bas-Coût (NewSpace)
    (
        "exam_optical_light_lowcost.mission.json",
        dict(
            schema_version="1.0.0",
            id="EXAM-2026-EO-LIGHT",
            title="Mission PicOptic — Observation Optique Légère et Bas-Coût (NewSpace)",
            client_agency="Agence Régionale de Surveillance Environnementale & Pépinière NewSpace",
            domain_label="Observation de la Terre — Imagerie optique compacte et économique",
            mission_type="optical_eo",
            max_budget_meur=2.80,
            target_lifetime_years=3.0,
            min_trl=8,
            context=(
                "Dans le cadre d'un programme d'amorçage NewSpace pour le suivi de la déforestation, des incendies "
                "et des cultures agricoles, l'agence souhaite déployer un satellite d'observation optique ultra-économique "
                "en orbite héliosynchrone pour un budget total inférieur ou égal à 2,80 M€ tout compris."
            ),
            primary_objective=(
                "Délivrer des images multispectrales ou panchromatiques avec une résolution spatiale au nadir (GSD) "
                "inférieure ou égale à 3,5 m (objectif 2,5 m) et une fauchée au sol d'au moins 12,0 km (objectif 20 km), "
                "avec un SNR radiométrique supérieur ou égal à 50, en utilisant une plateforme nanosatellite ou microsatellite légère."
            ),
            secondary_objectives=[
                "Contenir la masse au lancement sous 40 kg pour exploiter les vols partagés (rideshare CubeSat ou petit plateau).",
                "Assurer une durée de vie opérationnelle minimale de 3 ans en orbite basse.",
                "Garantir une marge de puissance positive sur l'ensemble des modes orbitaux.",
            ],
            scientific_or_operational_need=(
                "Les coopératives agricoles et les services forestiers régionaux nécessitent des passages fréquents à résolution "
                "métrique/décamétrique sans encourir le coût prohibitif des satellites institutionnels de grande taille."
            ),
            orbit_constraints_description=(
                "Orbite basse héliosynchrone (SSO) standard entre 480 km et 540 km d'altitude (LTAN 10h30–11h30), accessible "
                "via les services de lancement partagé fréquents."
            ),
            conops_guidance=(
                "Prises de vue programmées au-dessus des forêts et parcelles agricoles le jour, stockage dans la mémoire "
                "de masse et vidage rapide en bande S ou X lors des passages au-dessus de la station sol universitaire."
            ),
            deliverables_expected=[
                "Démontrer le respect du plafond budgétaire de 2,80 M€ en justifiant l'arbitrage plateforme (CubeSat 12U/16U vs Smallsat 50 kg).",
                "Vérifier le compromis d'altitude vis-à-vis du GSD <= 3,5 m et de la fauchée >= 12 km.",
                "Valider le bilan de masse et de puissance de la plateforme choisie.",
            ],
            requirements=[
                dict(
                    id="REQ-LIGHT-GSD",
                    title="Résolution spatiale au nadir (GSD)",
                    description="La distance d'échantillonnage au sol (GSD) au nadir doit être <= 3,5 m.",
                    req_type="payload_perf",
                    parameter="gsd_nadir_m",
                    operator="<=",
                    threshold=3.5,
                    goal=2.5,
                    unit="m",
                    weight=1.5,
                ),
                dict(
                    id="REQ-LIGHT-SWATH",
                    title="Largeur de fauchée au sol",
                    description="La fauchée cross-track au nadir doit être >= 12,0 km.",
                    req_type="payload_perf",
                    parameter="swath_width_km",
                    operator=">=",
                    threshold=12.0,
                    goal=20.0,
                    unit="km",
                    weight=1.0,
                ),
                dict(
                    id="REQ-LIGHT-SNR",
                    title="Rapport signal sur bruit (SNR)",
                    description="Le SNR au nadir doit être >= 50.",
                    req_type="payload_perf",
                    parameter="snr_nadir_estimate",
                    operator=">=",
                    threshold=50.0,
                    goal=70.0,
                    unit="",
                    weight=1.0,
                ),
            ],
            ground_stations=[
                dict(
                    id="sta_brest_light",
                    name="Station Universitaire de Brest",
                    latitude_deg=48.39,
                    longitude_deg=-4.49,
                    altitude_m=50.0,
                    min_elevation_deg=10.0,
                    bands_supported=["S", "X"],
                    cost_per_pass_eur=60.0,
                )
            ],
            target_zones=[
                dict(
                    id="zone_landes",
                    name="Massif des Landes & Bassin Aquitain",
                    points_lat_lon=[(44.0, -1.0), (45.0, 0.0), (43.5, -0.5)],
                    priority=1,
                )
            ],
        ),
    ),

    # ------------------------------------------------------------------ 2. Observation Optique Très Haute Performance (Sub-métrique)
    (
        "exam_optical_highperf.mission.json",
        dict(
            schema_version="1.0.0",
            id="EXAM-2026-EO-HIGHPERF",
            title="Mission Iris-Vanguard — Imagerie Optique Sub-Métrique Très Haute Performance",
            client_agency="Délégation Générale à l'Observation Spatiale Souveraine (DGOSS)",
            domain_label="Observation de la Terre — Imagerie optique sub-métrique de très haute performance",
            mission_type="optical_eo",
            max_budget_meur=35.0,
            target_lifetime_years=7.0,
            min_trl=8,
            context=(
                "La DGOSS requiert une capacité d'imagerie optique d'élite pour la reconnaissance tactique, la sécurité "
                "des frontières et le renseignement stratégique. Le satellite doit fournir des détails d'identification "
                "d'une extrême précision (GSD <= 0,40 m) avec un diamètre d'ouverture d'au moins 0,70 m."
            ),
            primary_objective=(
                "Délivrer des scènes optiques panchromatiques avec une résolution spatiale au nadir (GSD) <= 0,40 m "
                "(objectif 0,35 m), un miroir primaire d'ouverture >= 0,70 m, un rapport SNR >= 60 et une plateforme ultra-stable "
                "offrant une précision de pointage <= 0,004° avec contrôle de ligne de visée agile."
            ),
            secondary_objectives=[
                "Maintenir une durée de vie opérationnelle garantie d'au moins 7 ans en orbite basse.",
                "Intégrer une mémoire de masse d'au moins 1 To à 2 To pour absorber les acquisitions multiples par orbite.",
                "Garantir le respect de l'enveloppe budgétaire stricte de 35,0 M€ (lancement et plateforme inclus).",
            ],
            scientific_or_operational_need=(
                "La distinction d'équipements tactiques fins, de marquages au sol et de détails d'infrastructures sensibles "
                "nécessite de descendre sous la barre des 40 cm de résolution avec une dynamique radiométrique élevée."
            ),
            orbit_constraints_description=(
                "Orbite basse héliosynchrone (SSO) entre 450 km et 520 km (LTAN 10h30 ou 13h30) pour combiner résolution "
                "optimale, fauchée utile et éclairement sous angle d'élévation solaire favorable."
            ),
            conops_guidance=(
                "Prises de vue agiles le long de la trace ou en dépointage latéral rapide (pitch/roll). Vidage haute cadence "
                "en bande Ka ou lien optique vers les stations polaires (Svalbard/Kiruna)."
            ),
            deliverables_expected=[
                "Justifier le choix du grand instrument optique (diamètre >= 0,70 m) et le respect de la limite GSD <= 0,40 m.",
                "Valider le couplage avec une plateforme lourde et son pack ADCS garantissant un pointage <= 0,004°.",
                "Établir le bilan de masse au lancement et sélectionner le lanceur adéquat (rideshare lourd ou lanceur dédié).",
            ],
            requirements=[
                dict(
                    id="REQ-HP-GSD",
                    title="Résolution spatiale au nadir (GSD)",
                    description="Le GSD panchromatique au nadir doit être <= 0,40 m.",
                    req_type="payload_perf",
                    parameter="gsd_nadir_m",
                    operator="<=",
                    threshold=0.40,
                    goal=0.35,
                    unit="m",
                    weight=2.0,
                ),
                dict(
                    id="REQ-HP-APERTURE",
                    title="Diamètre d'ouverture du télescope",
                    description="Le diamètre du miroir primaire doit être >= 0,70 m.",
                    req_type="payload_perf",
                    parameter="aperture_diameter_m",
                    operator=">=",
                    threshold=0.70,
                    goal=0.80,
                    unit="m",
                    weight=1.5,
                ),
                dict(
                    id="REQ-HP-POINTING",
                    title="Précision de pointage plateforme",
                    description="La précision de pointage effective doit être <= 0,004 deg pour éviter tout flou dynamique.",
                    req_type="payload_perf",
                    parameter="pointing_accuracy_deg",
                    operator="<=",
                    threshold=0.004,
                    goal=0.002,
                    unit="deg",
                    weight=1.5,
                ),
                dict(
                    id="REQ-HP-SNR",
                    title="Rapport signal sur bruit (SNR)",
                    description="Le SNR radiométrique au nadir doit être >= 40.",
                    req_type="payload_perf",
                    parameter="snr_nadir_estimate",
                    operator=">=",
                    threshold=40.0,
                    goal=60.0,
                    unit="",
                    weight=1.0,
                ),
                dict(
                    id="REQ-HP-LIFETIME",
                    title="Durée de vie nominale de la plateforme",
                    description="La durée de vie certifiée de la plateforme doit être >= 7,0 ans.",
                    req_type="lifetime",
                    parameter="design_lifetime_years",
                    operator=">=",
                    threshold=7.0,
                    goal=10.0,
                    unit="yr",
                    weight=1.0,
                ),
            ],
            ground_stations=[
                dict(
                    id="svalbard_hp",
                    name="Svalbard Satellite Station (KSAT)",
                    latitude_deg=78.22,
                    longitude_deg=15.40,
                    altitude_m=450.0,
                    min_elevation_deg=5.0,
                    bands_supported=["S", "X", "Ka"],
                    cost_per_pass_eur=260.0,
                ),
                dict(
                    id="toulouse_hp",
                    name="Station Spatiale de Toulouse",
                    latitude_deg=43.60,
                    longitude_deg=1.44,
                    altitude_m=150.0,
                    min_elevation_deg=10.0,
                    bands_supported=["S", "X", "Ka"],
                    cost_per_pass_eur=190.0,
                ),
            ],
            target_zones=[
                dict(
                    id="zone_strategic_eu",
                    name="Détroits et corridors maritimes européens",
                    points_lat_lon=[(35.0, -6.0), (37.0, 15.0), (45.0, 30.0)],
                    priority=1,
                )
            ],
        ),
    ),

    # ------------------------------------------------------------------ 3. Spectrométrie Atmosphérique SWIR (Gaz à effet de serre CH4/CO2)
    (
        "exam_atmosphere_greenhouse_gas.mission.json",
        dict(
            schema_version="1.0.0",
            id="EXAM-2026-ATMO-GHG",
            title="Mission AtmoWatch — Chimie de l'Atmosphère Terrestre & Panaches de Gaz à Effet de Serre (SWIR)",
            client_agency="Institut Spatial du Climat & de l'Atmosphère (ISCA)",
            domain_label="Connaissance de l'Atmosphère Terrestre — Spectrométrie SWIR pour gaz atmosphériques",
            mission_type="atmosphere",
            max_budget_meur=16.5,
            target_lifetime_years=5.0,
            min_trl=8,
            context=(
                "Dans le cadre de la surveillance indépendante des émissions anthropiques et des traités internationaux, "
                "l'ISCA requiert un spectromètre imageur dans les bandes infrarouges courtes (SWIR, 1,6–1,7 µm) capable de "
                "détecter et quantifier les panaches de méthane (CH4) et de dioxyde de carbone (CO2)."
            ),
            primary_objective=(
                "Mesurer par spectrométrie imageuse dans le SWIR (jusqu'à au moins 1650 nm) les colonnes atmosphériques de CH4 et CO2 "
                "avec une résolution spectrale <= 1,0 nm (objectif 0,3 nm), une résolution spatiale au nadir <= 10 m permettant "
                "d'attribuer les émissions aux sites industriels sources, et un SNR spectral moyen >= 50."
            ),
            secondary_objectives=[
                "Couvrir les principaux bassins industriels et gaziers mondiaux avec un temps de revisite inférieur à 5 jours.",
                "Garantir une compatibilité thermique avec la cryogénie passive/active du détecteur SWIR.",
                "Maintenir le coût complet du segment spatial sous le plafond de 16,5 M€.",
            ],
            scientific_or_operational_need=(
                "La détection précise des fuites fugitives de méthane requiert d'isoler des raies d'absorption très étroites "
                "dans la fenêtre SWIR au-delà de 1600 nm sans être confondues avec la vapeur d'eau ou le CO2 ambiant."
            ),
            orbit_constraints_description=(
                "Orbite basse héliosynchrone (SSO) entre 500 km et 650 km d'altitude avec heure de passage solaire LTAN 11h30–13h00 "
                "afin de disposer du flux solaire réfléchi maximal dans le SWIR."
            ),
            conops_guidance=(
                "Observations au nadir le long de la trace sur les continents éclairés. Vidage de la mémoire de masse vers les "
                "stations polaires de Kiruna et Kourou."
            ),
            deliverables_expected=[
                "Justifier le choix d'un spectromètre imageur SWIR (>= 1650 nm, finesse spectrale <= 1,0 nm) par rapport aux spectromètres VNIR.",
                "Démontrer la conformité du bilan de puissance et de pointage de la plateforme microsatellite sélectionnée.",
                "Valider le budget global et le dimensionnement de la télémesure pour écouler le flux de données hyperspectrales.",
            ],
            requirements=[
                dict(
                    id="REQ-ATMO-SRES",
                    title="Finesse spectrale (résolution FWHM)",
                    description="La résolution spectrale de l'instrument doit être <= 1,0 nm pour résoudre les raies de CH4/CO2.",
                    req_type="payload_perf",
                    parameter="spectral_resolution_nm",
                    operator="<=",
                    threshold=1.0,
                    goal=0.3,
                    unit="nm",
                    weight=2.0,
                ),
                dict(
                    id="REQ-ATMO-SWIR",
                    title="Couverture spectrale infrarouge (SWIR)",
                    description="La longueur d'onde maximale couverte doit atteindre au moins 1650 nm.",
                    req_type="payload_perf",
                    parameter="spectral_range_max_nm",
                    operator=">=",
                    threshold=1650.0,
                    goal=1680.0,
                    unit="nm",
                    weight=1.5,
                ),
                dict(
                    id="REQ-ATMO-GSD",
                    title="Résolution spatiale d'attribution des panaches",
                    description="Le GSD spatial au nadir doit être <= 10,0 m.",
                    req_type="payload_perf",
                    parameter="gsd_spatial_nadir_m",
                    operator="<=",
                    threshold=10.0,
                    goal=6.0,
                    unit="m",
                    weight=1.0,
                ),
                dict(
                    id="REQ-ATMO-SNR",
                    title="Rapport signal sur bruit spectral moyen",
                    description="Le SNR moyen par canal spectral doit être >= 50.",
                    req_type="payload_perf",
                    parameter="mean_snr_estimate",
                    operator=">=",
                    threshold=50.0,
                    goal=80.0,
                    unit="",
                    weight=1.0,
                ),
            ],
            ground_stations=[
                dict(
                    id="kiruna_sta",
                    name="Station Polaire de Kiruna (Estrack)",
                    latitude_deg=67.88,
                    longitude_deg=20.96,
                    altitude_m=400.0,
                    min_elevation_deg=5.0,
                    bands_supported=["S", "X"],
                    cost_per_pass_eur=210.0,
                ),
                dict(
                    id="kourou_sta",
                    name="Station Équatoriale de Kourou",
                    latitude_deg=5.25,
                    longitude_deg=-52.80,
                    altitude_m=20.0,
                    min_elevation_deg=5.0,
                    bands_supported=["S", "X"],
                    cost_per_pass_eur=200.0,
                ),
            ],
            target_zones=[
                dict(
                    id="zone_permian_me",
                    name="Bassins gaziers & industriels (Moyen-Orient / Eurasie / Amérique)",
                    points_lat_lon=[(25.0, 50.0), (40.0, 55.0), (31.0, -102.0)],
                    priority=1,
                )
            ],
        ),
    ),

    # ------------------------------------------------------------------ 4. Surveillance Radar SAR Tout-Temps
    (
        "exam_sar_surveillance.mission.json",
        dict(
            schema_version="1.0.0",
            id="EXAM-2026-SAR",
            title="Mission RadarGuard — Surveillance Maritime & Terrestre Tout-Temps par Radar SAR",
            client_agency="Direction de la Surveillance Maritime & Polaire (DSMP)",
            domain_label="Observation de la Terre — Imagerie Radar SAR micro-ondes tout-temps",
            mission_type="sar_eo",
            max_budget_meur=25.0,
            target_lifetime_years=5.0,
            min_trl=8,
            context=(
                "Concevoir un satellite d'observation radar à synthèse d'ouverture (SAR) capable d'imager les zones maritimes, "
                "les détroits stratégiques et les glaces arctiques de jour comme de nuit, indépendamment de la couverture nuageuse."
            ),
            primary_objective=(
                "Assurer l'imagerie radar tout-temps en mode Stripmap avec une résolution azimutale <= 2,0 m (objectif 1,5 m), "
                "une fauchée au sol d'au moins 15 km et une sensibilité radiométrique (NESZ) <= -15,0 dB afin de détecter les "
                "navires non coopératifs, les pollutions marines et la dérive des glaces."
            ),
            secondary_objectives=[
                "Dimensionner l'alimentation électrique pour absorber la puissance crête RF élevée de l'antenne réseau active.",
                "Maintenir le coût complet du satellite et du lancement sous 25,0 M€.",
            ],
            scientific_or_operational_need=(
                "Les zones polaires et les mers septentrionales sont couvertes de nuages plus de 70 % de l'année et plongées "
                "dans l'obscurité hivernale : seul un radar imageur actif micro-ondes assure une surveillance continue."
            ),
            orbit_constraints_description=(
                "Orbite polaire ou héliosynchrone crépusculaire (dawn-dusk 06h00/18h00) à 500–580 km d'altitude afin de maximiser "
                "l'ensoleillement des panneaux solaires et minimiser les cycles d'éclipse lors des tirs radar."
            ),
            conops_guidance=(
                "Séquences radar de 60 à 120 secondes par orbite. Stockage des données brutes I/Q dans la mémoire de masse "
                "et vidage haut débit bande X vers les stations boréales (Svalbard/Inuvik)."
            ),
            deliverables_expected=[
                "Analyser l'influence de l'altitude et de la taille d'antenne sur la résolution SAR et le bilan de bruit NESZ.",
                "Valider le bilan de puissance moyenne et crête de la plateforme face aux tirs radar.",
                "Vérifier le choix du lanceur compatible avec la masse humide et ses marges.",
            ],
            requirements=[
                dict(
                    id="REQ-SAR-AZ-01",
                    title="Résolution Azimutale Stripmap",
                    description="Résolution azimutale le long de la trace <= 2.0 m",
                    req_type="payload_perf",
                    parameter="azimuth_resolution_stripmap_m",
                    operator="<=",
                    threshold=2.0,
                    goal=1.5,
                    unit="m",
                    weight=1.0,
                ),
                dict(
                    id="REQ-SAR-SWATH-01",
                    title="Fauchée au Sol",
                    description="Largeur de fauchée au sol >= 15.0 km",
                    req_type="payload_perf",
                    parameter="swath_width_ground_km",
                    operator=">=",
                    threshold=15.0,
                    goal=25.0,
                    unit="km",
                    weight=1.0,
                ),
                dict(
                    id="REQ-SAR-NESZ-01",
                    title="Sensibilité Radiométrique (NESZ)",
                    description="Noise Equivalent Sigma Zero <= -15.0 dB pour détecter les cibles de faible réflectivité",
                    req_type="payload_perf",
                    parameter="nesz_db",
                    operator="<=",
                    threshold=-15.0,
                    goal=-22.0,
                    unit="dB",
                    weight=1.0,
                ),
            ],
            ground_stations=[
                dict(
                    id="svalbard_sta",
                    name="Svalbard Arctic Station",
                    latitude_deg=78.22,
                    longitude_deg=15.40,
                    altitude_m=450.0,
                    min_elevation_deg=5.0,
                    bands_supported=["S", "X", "Ka"],
                    cost_per_pass_eur=250.0,
                ),
                dict(
                    id="inuvik_sta",
                    name="Inuvik Canadian Station",
                    latitude_deg=68.36,
                    longitude_deg=-133.72,
                    altitude_m=100.0,
                    min_elevation_deg=5.0,
                    bands_supported=["S", "X"],
                    cost_per_pass_eur=220.0,
                ),
            ],
            target_zones=[
                dict(
                    id="zone_baltic",
                    name="Mer Baltique & Détroits Arctiques",
                    points_lat_lon=[(54.0, 10.0), (60.0, 18.0), (65.0, 24.0)],
                    priority=1,
                )
            ],
        ),
    ),

    # ------------------------------------------------------------------ 5. Télécom Optique Laser Haut Débit (>= 25 Gbit/s)
    (
        "exam_high_throughput_datalink.mission.json",
        dict(
            schema_version="1.0.0",
            id="EXAM-2026-DATARATE",
            title="Mission TeraRelay — Établissement d'une Liaison Optique Très Haut Débit (>= 25 Gbit/s)",
            client_agency="Opérateur Européen de Dorsale Spatiale Souveraine",
            domain_label="Télécommunications Spatiales — Établir un très haut débit de données laser optique",
            mission_type="telecom_opt",
            max_budget_meur=15.0,
            target_lifetime_years=6.0,
            min_trl=8,
            context=(
                "Pour désengorger les liaisons radio-fréquence saturées et rapatrier en temps quasi-réel des téraoctets de données "
                "issues de capteurs spatiaux, l'opérateur souhaite déployer un terminal laser capable d'établir une liaison directe "
                "vers le sol à un débit supérieur ou égal à 25 Gbit/s."
            ),
            primary_objective=(
                "Établir une liaison descendante laser à 1550 nm délivrant un débit effectif >= 25,0 Gbit/s vers des stations sol "
                "optiques de 80 cm, avec une marge de liaison d'au moins 6,0 dB en ciel clair et une précision de pointage plateforme "
                "inférieure ou égale à 0,008° pour garantir l'acquisition rapide du faisceau optique."
            ),
            secondary_objectives=[
                "Respecter le plafond budgétaire de 15,0 M€ pour permettre la réplication en constellation.",
                "Embarquer un pack de contrôle d'attitude de précision adapté aux exigences de pointage sub-microradian du terminal laser.",
            ],
            scientific_or_operational_need=(
                "Les constellations d'observation modernes génèrent des volumes massifs incompatibles avec les bandes RF étroites. "
                "Une liaison laser à 25 Gbit/s transfère plus de 1,1 To de données utiles lors d'un passage unique de 6 minutes."
            ),
            orbit_constraints_description=(
                "Orbite basse circulaire entre 500 km et 750 km d'altitude. L'altitude modérée réduit les pertes de propagation en 1/R²."
            ),
            conops_guidance=(
                "Pointage grossier du satellite vers la station sol optique sélectionnée, détection du balisage montant (beacon), "
                "asservissement fin par le miroir rapide PAT et transmission plein débit de la mémoire de masse."
            ),
            deliverables_expected=[
                "Calculer le volume de données transféré par passage à 25 Gbit/s.",
                "Démontrer la fermeture du bilan de liaison optique (puissance émise, diamètres d'ouverture, marge >= 6,0 dB).",
                "Justifier le choix de la plateforme et du pack ADCS associé.",
            ],
            requirements=[
                dict(
                    id="REQ-DATA-RATE-01",
                    title="Débit de données optique effectif",
                    description="Le débit de données de la liaison descendante laser doit être >= 25,0 Gbit/s.",
                    req_type="payload_perf",
                    parameter="achievable_data_rate_gbps",
                    operator=">=",
                    threshold=25.0,
                    goal=100.0,
                    unit="Gbps",
                    weight=2.0,
                ),
                dict(
                    id="REQ-LINK-MARGIN-01",
                    title="Marge du bilan de liaison optique",
                    description="La marge du lien laser à 1550 nm doit être >= 6,0 dB.",
                    req_type="payload_perf",
                    parameter="margin_db",
                    operator=">=",
                    threshold=6.0,
                    goal=10.0,
                    unit="dB",
                    weight=1.0,
                ),
                dict(
                    id="REQ-POINTING-LASER",
                    title="Précision de pointage plateforme pour acquisition",
                    description="La précision de pointage plateforme doit être <= 0,008 deg.",
                    req_type="payload_perf",
                    parameter="pointing_accuracy_deg",
                    operator="<=",
                    threshold=0.008,
                    goal=0.005,
                    unit="deg",
                    weight=1.0,
                ),
            ],
            ground_stations=[
                dict(
                    id="ogs_tenerife",
                    name="ESA Optical Ground Station Tenerife",
                    latitude_deg=28.30,
                    longitude_deg=-16.51,
                    altitude_m=2390.0,
                    min_elevation_deg=15.0,
                    bands_supported=["Optical", "S"],
                    cost_per_pass_eur=350.0,
                ),
                dict(
                    id="ogs_calern",
                    name="Station Optique du Plateau de Calern (OCA)",
                    latitude_deg=43.75,
                    longitude_deg=6.92,
                    altitude_m=1270.0,
                    min_elevation_deg=15.0,
                    bands_supported=["Optical", "S"],
                    cost_per_pass_eur=350.0,
                ),
            ],
            target_zones=[],
        ),
    ),

    # ------------------------------------------------------------------ 6. Télécommunications Classiques en Orbite Géostationnaire (GEO)
    (
        "exam_geo_telecom_classical.mission.json",
        dict(
            schema_version="1.0.0",
            id="EXAM-2026-GEO-COMMS",
            title="Mission EuroCom-GEO — Télécommunications Régionales en Orbite Géostationnaire",
            client_agency="Opérateur Européen de Télécommunications par Satellite (EUTELSAT/ESA)",
            domain_label="Télécommunications Spatiales — Orbite géostationnaire (GEO), répéteurs Ku/Ka et couverture permanente",
            mission_type="telecom_radio",
            max_budget_meur=55.0,
            target_lifetime_years=12.0,
            min_trl=8,
            context=(
                "Pour assurer la connectivité souveraine et la diffusion audiovisuelle et de données sécurisées 24h/24 "
                "sans interruption au-dessus de l'Europe et du bassin méditerranéen, l'opérateur lance le dimensionnement "
                "d'un satellite géostationnaire (GEO, altitude 35 786 km, inclinaison 0,0°)."
            ),
            primary_objective=(
                "Fournir un débit descendant utile d'au moins 600,0 Mbit/s (objectif 1 800 Mbit/s) sur antenne sol de 4,5 m "
                "avec une marge de liaison Eb/N0 >= 3,5 dB en bande Ku/Ka, une durée de vie garantie de la plateforme "
                "d'au moins 12 ans (objectif 15 ans) et une précision de maintien à poste et pointage <= 0,05°."
            ),
            secondary_objectives=[
                "Assurer une visibilité permanente 24h/24 sans interruption d'élévation sur les stations européennes.",
                "Maintenir le coût complet (plateforme GEO + charge utile répéteur + lancement GTO/GEO) sous 55,0 M€.",
                "Garantir la tenue aux radiations de l'orbite géostationnaire (blindage 100 krad).",
            ],
            scientific_or_operational_need=(
                "Contrairement aux constellations LEO dont les satellites défilent à grande vitesse, l'orbite géostationnaire "
                "permet à une antenne sol fixe de pointer en continu le même relais spatial, offrant une disponibilité de "
                "service de 99,99 % pour les liaisons gouvernementales critiques et les faisceaux de diffusion."
            ),
            orbit_constraints_description=(
                "Orbite géostationnaire (GEO) : altitude exacte 35 786 km, inclinaison 0,0°, période de révolution 24h00. "
                "Injection via transfert géostationnaire (GTO) ou injection directe GEO."
            ),
            conops_guidance=(
                "Fonctionnement permanent des répéteurs RF (100 % du temps d'orbite, y compris durant les courtes éclipses "
                "d'équinoxe grâce au parc de batteries lithium-ion). Maintien à poste fin Nord-Sud et Est-Ouest par propulsion "
                "électrique ou chimique."
            ),
            deliverables_expected=[
                "Démontrer la conformité de l'orbite GEO (35 786 km, 0°) et la couverture permanente 24/7 sur les stations sol.",
                "Établir le bilan de liaison RF à 35 786 km (puissance RF, gain d'antenne satellite, station sol 4,5 m, marge Eb/N0 >= 3,5 dB).",
                "Justifier le choix de la plateforme GEO (durée de vie >= 12 ans, puissance continue > 2 000 W) et du lanceur GTO.",
            ],
            requirements=[
                dict(
                    id="REQ-GEO-DATARATE",
                    title="Débit de données RF descendant total",
                    description="Le débit RF descendant de la charge utile de télécommunications doit être >= 600,0 Mbit/s.",
                    req_type="payload_perf",
                    parameter="max_data_rate_mbps",
                    operator=">=",
                    threshold=600.0,
                    goal=1800.0,
                    unit="Mbps",
                    weight=2.0,
                ),
                dict(
                    id="REQ-GEO-MARGIN",
                    title="Marge du bilan de liaison RF (Eb/N0)",
                    description="La marge Eb/N0 sur la liaison descendante vers station 4,5 m doit être >= 3,5 dB.",
                    req_type="payload_perf",
                    parameter="link_margin_db",
                    operator=">=",
                    threshold=3.5,
                    goal=6.0,
                    unit="dB",
                    weight=1.5,
                ),
                dict(
                    id="REQ-GEO-LIFETIME",
                    title="Durée de vie nominale de la plateforme",
                    description="La durée de vie certifiée de la plateforme géostationnaire doit être >= 12,0 ans.",
                    req_type="lifetime",
                    parameter="design_lifetime_years",
                    operator=">=",
                    threshold=12.0,
                    goal=15.0,
                    unit="yr",
                    weight=1.5,
                ),
                dict(
                    id="REQ-GEO-POINTING",
                    title="Précision de pointage antenne plateforme",
                    description="La précision de pointage de la plateforme doit être <= 0,05 deg pour maintenir le faisceau sol.",
                    req_type="payload_perf",
                    parameter="pointing_accuracy_deg",
                    operator="<=",
                    threshold=0.05,
                    goal=0.02,
                    unit="deg",
                    weight=1.0,
                ),
            ],
            ground_stations=[
                dict(
                    id="sta_fucino_geo",
                    name="Téléport Spatial de Fucino (Italie)",
                    latitude_deg=41.97,
                    longitude_deg=13.60,
                    altitude_m=650.0,
                    min_elevation_deg=10.0,
                    bands_supported=["C", "Ku", "Ka"],
                    cost_per_pass_eur=180.0,
                ),
                dict(
                    id="sta_rambouillet_geo",
                    name="Téléport de Rambouillet (Eutelsat)",
                    latitude_deg=48.64,
                    longitude_deg=1.83,
                    altitude_m=160.0,
                    min_elevation_deg=10.0,
                    bands_supported=["Ku", "Ka"],
                    cost_per_pass_eur=180.0,
                ),
            ],
            target_zones=[
                dict(
                    id="zone_euro_med",
                    name="Couverture Européenne & Bassin Méditerranéen",
                    points_lat_lon=[(34.0, -10.0), (60.0, 5.0), (36.0, 35.0)],
                    priority=1,
                )
            ],
        ),
    ),

    # ------------------------------------------------------------------ 7. Observation Optique Métrique Standard (Preserved)
    (
        "exam_optical_earth_observation.mission.json",
        dict(
            schema_version="1.0.0",
            id="EXAM-2026-EO-OPT",
            title="Mission Sentinel-Vision — Observation de la Terre Haute Résolution",
            client_agency="Agence Européenne d'Observation Civile & Sécurité (AEOCS)",
            domain_label="Observation de la Terre — Imagerie optique métrique standard",
            mission_type="optical_eo",
            max_budget_meur=18.0,
            target_lifetime_years=5.0,
            min_trl=8,
            context=(
                "L'agence souhaite déployer un microsatellite d'observation optique sub-métrique en orbite héliosynchrone "
                "pour le suivi quotidien des infrastructures critiques et la cartographie urbaine fine."
            ),
            primary_objective=(
                "Fournir des images optiques panchromatiques et multispectrales avec une résolution au sol au nadir "
                "inférieure ou égale à 1,0 m (objectif 0,80 m) et une fauchée d'au moins 10 km, tout en garantissant un rapport "
                "signal-sur-bruit supérieur à 55 (objectif 80)."
            ),
            secondary_objectives=[
                "Permettre des prises de vue dépointées pour réduire le temps de revisite.",
                "Maintenir une marge de puissance moyenne d'au moins 15 % sur l'orbite héliosynchrone choisie.",
                "Contenir le coût complet sous 18,0 M€.",
            ],
            scientific_or_operational_need=(
                "Les services de protection civile ont besoin d'une résolution métrique pour qualifier les dégâts matériels "
                "et suivre l'évolution des territoires."
            ),
            orbit_constraints_description=(
                "Orbite basse héliosynchrone (SSO) recommandée entre 450 km et 600 km d'altitude."
            ),
            conops_guidance=(
                "Acquisition sur les terres éclairées, stockage mémoire et vidage vers la station polaire de Svalbard."
            ),
            deliverables_expected=[
                "Justifier le choix du télescope et de l'altitude au regard de la résolution et de la fauchée.",
                "Justifier la plateforme et l'ADCS choisi.",
            ],
            requirements=[
                dict(
                    id="REQ-GSD-01",
                    title="Résolution spatiale au nadir (GSD)",
                    description="La distance d'échantillonnage au sol (GSD) au nadir doit être <= 1,0 m.",
                    req_type="payload_perf",
                    parameter="gsd_nadir_m",
                    operator="<=",
                    threshold=1.0,
                    goal=0.8,
                    unit="m",
                    weight=1.5,
                ),
                dict(
                    id="REQ-SWATH-01",
                    title="Largeur de fauchée au nadir",
                    description="La largeur de fauchée cross-track doit être >= 10,0 km.",
                    req_type="payload_perf",
                    parameter="swath_width_km",
                    operator=">=",
                    threshold=10.0,
                    goal=15.0,
                    unit="km",
                    weight=1.0,
                ),
                dict(
                    id="REQ-SNR-01",
                    title="Rapport signal sur bruit radiométrique (SNR)",
                    description="Le SNR au nadir doit être >= 55.",
                    req_type="payload_perf",
                    parameter="snr_nadir_estimate",
                    operator=">=",
                    threshold=55.0,
                    goal=80.0,
                    unit="",
                    weight=1.0,
                ),
            ],
            ground_stations=[
                dict(
                    id="svalbard",
                    name="Svalbard Satellite Station (KSAT)",
                    latitude_deg=78.22,
                    longitude_deg=15.40,
                    altitude_m=450.0,
                    min_elevation_deg=5.0,
                    bands_supported=["S", "X", "Ka"],
                    cost_per_pass_eur=240.0,
                )
            ],
            target_zones=[],
        ),
    ),

    # ------------------------------------------------------------------ 8. Cosmologie & Champ Profond (Preserved)
    (
        "exam_cosmology_deep_field.mission.json",
        dict(
            schema_version="1.0.0",
            id="EXAM-2026-COSMO",
            title="Mission DarkLens — Cosmologie, Lentilles Gravitationnelles & Champ Profond",
            client_agency="Consortium Scientifique Européen d'Astrophysique & Cosmologie",
            domain_label="Cosmologie & Astrophysique — Télescope spatial à grand collecteur",
            mission_type="cosmology",
            max_budget_meur=32.0,
            target_lifetime_years=6.0,
            min_trl=8,
            context=(
                "Pour cartographier la distribution de matière noire par cisaillement gravitationnel faible et suivre "
                "les supernovæ distantes, le consortium souhaite placer en orbite un télescope optique à grand diamètre primaire."
            ),
            primary_objective=(
                "Disposer d'un télescope spatial d'au moins 0,60 m d'ouverture primaire (objectif 0,70 m) limité par la diffraction, "
                "monté sur une plateforme garantissant une précision de pointage <= 0,004°."
            ),
            secondary_objectives=[
                "Assurer un stockage bord d'au moins 1 à 2 To.",
                "Privilégier un contrôle d'attitude à très faibles micro-vibrations.",
            ],
            scientific_or_operational_need=(
                "La déformation cohérente de galaxies lointaines exige une qualité d'image affranchie de la turbulence terrestre."
            ),
            orbit_constraints_description=(
                "Orbite héliosynchrone crépusculaire (dawn-dusk, 550–700 km)."
            ),
            conops_guidance=(
                "Pointage inertiel prolongé (poses de 300 à 600 s) puis vidage quotidien en bande X/Ka."
            ),
            deliverables_expected=[
                "Justifier le diamètre du miroir primaire vis-à-vis de la limite de diffraction.",
                "Démontrer que le pointage respecte l'exigence <= 0,004°.",
            ],
            requirements=[
                dict(
                    id="REQ-COSMO-APERTURE",
                    title="Diamètre du miroir primaire collecteur",
                    description="Le diamètre d'ouverture du télescope doit être >= 0,60 m.",
                    req_type="payload_perf",
                    parameter="aperture_diameter_m",
                    operator=">=",
                    threshold=0.60,
                    goal=0.70,
                    unit="m",
                    weight=2.0,
                ),
                dict(
                    id="REQ-COSMO-DIFF",
                    title="Finesse optique (limite de diffraction)",
                    description="La tache de diffraction de référence doit être <= 0,72 m.",
                    req_type="payload_perf",
                    parameter="diffraction_ground_spot_m",
                    operator="<=",
                    threshold=0.72,
                    goal=0.55,
                    unit="m",
                    weight=1.0,
                ),
                dict(
                    id="REQ-COSMO-POINTING",
                    title="Précision de pointage astrophysique",
                    description="La précision de pointage effective de la plateforme doit être <= 0,004 deg.",
                    req_type="payload_perf",
                    parameter="pointing_accuracy_deg",
                    operator="<=",
                    threshold=0.004,
                    goal=0.002,
                    unit="deg",
                    weight=1.5,
                ),
            ],
            ground_stations=[
                dict(
                    id="cebreros_sta",
                    name="Station ESA Cebreros / Madrid",
                    latitude_deg=40.45,
                    longitude_deg=-4.36,
                    altitude_m=790.0,
                    min_elevation_deg=10.0,
                    bands_supported=["S", "X", "Ka"],
                    cost_per_pass_eur=300.0,
                )
            ],
            target_zones=[],
        ),
    ),

    # ------------------------------------------------------------------ 9. Distribution Quantique de Clés (Preserved)
    (
        "exam_qkd_secure_links.mission.json",
        dict(
            schema_version="1.0.0",
            id="EXAM-2026-QKD",
            title="Mission QuantumShield — Relais Sécurisé Gouvernemental par Clés Quantiques",
            client_agency="Agence Nationale de Sécurité des Communications Souveraines",
            domain_label="Télécommunications Quantiques — Distribution quantique de clés (QKD)",
            mission_type="qkd",
            max_budget_meur=22.0,
            target_lifetime_years=4.0,
            min_trl=7,
            context=(
                "Concevoir un satellite de distribution quantique de clés (QKD) en orbite basse (LEO) pour alimenter les centres "
                "de calcul souverains en clés cryptographiques inviolables par faisceau laser nocturne."
            ),
            primary_objective=(
                "Distribuer des clés quantiques (BB84 à états leurres à 850 nm) avec un taux d'erreur quantique QBER <= 6,0 % "
                "et un débit de clé secrète asymptotique >= 1 000 bit/s."
            ),
            secondary_objectives=[
                "Garantir un pointage plateforme <= 0,008°.",
                "Assurer l'authentification et la distillation des clés via un canal radio classique.",
            ],
            scientific_or_operational_need=(
                "Protéger les communications souveraines contre l'essor futur des calculateurs quantiques."
            ),
            orbit_constraints_description=(
                "Orbite basse héliosynchrone à 450–550 km d'altitude."
            ),
            conops_guidance=(
                "Émission quantique exclusivement nocturne lors des passages au-dessus des stations optiques."
            ),
            deliverables_expected=[
                "Analyser le compromis entre altitude et pertes du canal optique quantique.",
                "Justifier le choix du terminal QKD et du pack ADCS.",
            ],
            requirements=[
                dict(
                    id="REQ-QKD-QBER-01",
                    title="Taux d'Erreur Quantique (QBER)",
                    description="Quantum Bit Error Rate <= 6.0 %",
                    req_type="payload_perf",
                    parameter="quantum_bit_error_rate_pct",
                    operator="<=",
                    threshold=6.0,
                    goal=3.0,
                    unit="%",
                    weight=1.5,
                ),
                dict(
                    id="REQ-QKD-SKR-01",
                    title="Débit de Clé Secrète Asymptotique",
                    description="Secret Key Rate moyen >= 1000 bps",
                    req_type="payload_perf",
                    parameter="asymptotic_secret_key_rate_bps",
                    operator=">=",
                    threshold=1000.0,
                    goal=5000.0,
                    unit="bps",
                    weight=1.0,
                ),
                dict(
                    id="REQ-POINTING-QKD",
                    title="Précision de Pointage Plateforme",
                    description="Précision de pointage de la plateforme <= 0.008 deg",
                    req_type="payload_perf",
                    parameter="pointing_accuracy_deg",
                    operator="<=",
                    threshold=0.008,
                    unit="deg",
                    weight=1.0,
                ),
            ],
            ground_stations=[
                dict(
                    id="sta_nice_ogs",
                    name="Observatoire de la Côte d'Azur (OGS Calern)",
                    latitude_deg=43.75,
                    longitude_deg=6.92,
                    altitude_m=1270.0,
                    min_elevation_deg=15.0,
                    bands_supported=["Optical", "S"],
                    cost_per_pass_eur=500.0,
                )
            ],
            target_zones=[],
        ),
    ),

    # ------------------------------------------------------------------ 10. CubeSat Bas-Coût IoT / Maritime (Preserved)
    (
        "exam_cubesat_maritime_iot.mission.json",
        dict(
            schema_version="1.0.0",
            id="EXAM-2026-CUBESAT-RF",
            title="Mission NanoSentinel — CubeSat Bas-Coût de Collecte IoT/AIS & Imagerie Côtière",
            client_agency="Pôle Universitaire & Maritime NewSpace",
            domain_label="Nanosatellite Bas-Coût — Collecte de données RF sous budget strict",
            mission_type="telecom_radio",
            max_budget_meur=1.6,
            target_lifetime_years=2.5,
            min_trl=8,
            context=(
                "Un consortium universitaire dispose d'un budget strictement plafonné à 1,60 M€ pour déployer un "
                "nanosatellite CubeSat dédié à la collecte de données maritimes."
            ),
            primary_objective=(
                "Établir une liaison descendante RF d'au moins 15 Mbit/s avec une marge >= 3,0 dB sous 1,60 M€."
            ),
            secondary_objectives=[
                "Contenir la masse dans un déployeur CubeSat <= 32 kg.",
            ],
            scientific_or_operational_need=(
                "Ingénierie spatiale sous forte contrainte de coût."
            ),
            orbit_constraints_description=(
                "Orbite héliosynchrone standard 500–550 km en covoiturage."
            ),
            conops_guidance=(
                "Collecte permanente et vidage lors des passages station."
            ),
            deliverables_expected=[
                "Démontrer le respect du plafond de 1,60 M€.",
            ],
            requirements=[
                dict(
                    id="REQ-RF-RATE-01",
                    title="Débit de données RF descendant",
                    description="Le débit maximal RF doit être >= 15,0 Mbit/s.",
                    req_type="payload_perf",
                    parameter="max_data_rate_mbps",
                    operator=">=",
                    threshold=15.0,
                    goal=35.0,
                    unit="Mbps",
                    weight=1.5,
                ),
                dict(
                    id="REQ-RF-MARGIN-01",
                    title="Marge du bilan de liaison RF",
                    description="La marge Eb/N0 doit être >= 3,0 dB.",
                    req_type="payload_perf",
                    parameter="link_margin_db",
                    operator=">=",
                    threshold=3.0,
                    goal=6.0,
                    unit="dB",
                    weight=1.0,
                ),
            ],
            ground_stations=[
                dict(
                    id="sta_brest",
                    name="Station Universitaire de Brest",
                    latitude_deg=48.39,
                    longitude_deg=-4.49,
                    altitude_m=50.0,
                    min_elevation_deg=10.0,
                    bands_supported=["UHF", "S", "X"],
                    cost_per_pass_eur=40.0,
                )
            ],
            target_zones=[],
        ),
    ),
]


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    MISSIONS_DIR.mkdir(parents=True, exist_ok=True)
    for fname, data in MISSIONS:
        spec = MissionSpecification.model_validate(data)
        out = MISSIONS_DIR / fname
        out.write_text(spec.model_dump_json(indent=2), encoding="utf-8")
        print(f"Wrote {fname}: {spec.id} — {spec.title} (budget {spec.max_budget_meur} M€, {len(spec.requirements)} reqs)")


if __name__ == "__main__":
    main()
