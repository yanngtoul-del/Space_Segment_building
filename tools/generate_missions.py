"""Generate the official set of mission specification sheets (fiches de spécification mission) in data/missions/."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ssb.core.mission import MissionSpecification  # noqa: E402

MISSIONS_DIR = ROOT / "data" / "missions"


MISSIONS: list[tuple[str, dict]] = [
    # ------------------------------------------------------------------ 1. Observation de la Terre Optique HR
    (
        "exam_optical_earth_observation.mission.json",
        dict(
            schema_version="1.0.0",
            id="EXAM-2026-EO-OPT",
            title="Mission Sentinel-Vision — Observation de la Terre Haute Résolution",
            client_agency="Agence Européenne d'Observation Civile & Sécurité (AEOCS)",
            domain_label="Observation de la Terre — Imagerie optique sub-métrique",
            mission_type="optical_eo",
            max_budget_meur=18.0,
            target_lifetime_years=5.0,
            min_trl=8,
            context=(
                "L'agence souhaite déployer un microsatellite d'observation optique sub-métrique en orbite héliosynchrone "
                "pour le suivi quotidien des infrastructures critiques, la cartographie urbaine fine et l'évaluation rapide "
                "des dommages après catastrophe naturelle."
            ),
            primary_objective=(
                "Fournir des images optiques panchromatiques et multispectrales (VNIR) avec une résolution au sol au nadir "
                "inférieure ou égale à 1,0 m (objectif 0,80 m) et une fauchée d'au moins 10 km, tout en garantissant un rapport "
                "signal-sur-bruit supérieur à 80 et le vidage quotidien d'au moins 25 scènes vers la station polaire de Svalbard."
            ),
            secondary_objectives=[
                "Permettre des prises de vue dépointées (agilité latérale) pour réduire le temps de revisite sur une zone d'intérêt européenne.",
                "Maintenir une marge de puissance moyenne d'au moins 15 % sur l'orbite héliosynchrone choisie.",
                "Contenir le coût complet (plateforme + options + instrument + lancement) sous 18,0 M€.",
            ],
            scientific_or_operational_need=(
                "Les services de protection civile et d'aménagement du territoire ont besoin d'une résolution sub-métrique "
                "pour distinguer les véhicules, l'état des ponts et des digues, ainsi que de bandes proche-infrarouge pour "
                "qualifier le stress hydrique péri-urbain. Le segment spatial doit être livrable en moins de 18 mois."
            ),
            orbit_constraints_description=(
                "Orbite basse héliosynchrone (SSO) recommandée entre 450 km et 600 km d'altitude (LTAN ~ 10h30) afin de concilier "
                "résolution géométrique (GSD proportionnel à l'altitude), éclairement solaire constant et durée de vie orbitale."
            ),
            conops_guidance=(
                "Acquisition sur les terres émergées éclairées (facteur de marche charge utile ~15–25 %), stockage dans la mémoire "
                "de masse embarquée, puis téléchargement haut débit en bande X ou par lien optique lors des passages à haute "
                "élévation sur la station de Svalbard. Gestion de la charge batterie pendant les ~35 minutes d'éclipse par orbite."
            ),
            deliverables_expected=[
                "Justifier le choix du couple (altitude orbitale, télescope) vis-à-vis du compromis résolution GSD / largeur de fauchée.",
                "Justifier la sélection de la plateforme et du pack ADCS au regard de l'exigence de pointage de l'instrument.",
                "Dimensionner la chaîne mémoire de masse + émetteur de télémesure charge utile pour écouler le débit généré.",
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
                    description="Le SNR au nadir sur cible d'albédo 0,3 doit être >= 80.",
                    req_type="payload_perf",
                    parameter="snr_nadir_estimate",
                    operator=">=",
                    threshold=80.0,
                    goal=120.0,
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
                ),
                dict(
                    id="toulouse",
                    name="Station Réception Toulouse",
                    latitude_deg=43.60,
                    longitude_deg=1.44,
                    altitude_m=150.0,
                    min_elevation_deg=10.0,
                    bands_supported=["S", "X"],
                    cost_per_pass_eur=180.0,
                ),
            ],
            target_zones=[
                dict(
                    id="zone_med",
                    name="Arc Méditerranéen & Europe de l'Ouest",
                    points_lat_lon=[(36.0, -5.0), (48.0, 2.0), (43.0, 15.0)],
                    priority=1,
                )
            ],
        ),
    ),

    # ------------------------------------------------------------------ 2. Observation Radar SAR (preserved IDs for unit test)
    (
        "exam_sar_surveillance.mission.json",
        dict(
            schema_version="1.0.0",
            id="EXAM-2026-SAR",
            title="Mission RadarGuard — Surveillance Maritime & Terrestre Tout-Temps",
            client_agency="Direction de la Surveillance Maritime & Polaire",
            domain_label="Observation de la Terre — Imagerie Radar SAR tout-temps",
            mission_type="sar_eo",
            max_budget_meur=25.0,
            target_lifetime_years=5.0,
            min_trl=8,
            context=(
                "Concevoir un satellite d'observation radar à synthèse d'ouverture (SAR) capable d'imager les zones côtières, "
                "les détroits stratégiques et les glaces arctiques de jour comme de nuit, indépendamment de la couverture nuageuse."
            ),
            primary_objective=(
                "Assurer l'imagerie radar tout-temps en mode Stripmap avec une résolution azimutale meilleure que 2,0 m, "
                "une fauchée au sol d'au moins 15 km et une sensibilité radiométrique (NESZ) meilleure que -15,0 dB afin de "
                "détecter les navires non coopératifs, les nappes d'hydrocarbures et la dérive des glaces."
            ),
            secondary_objectives=[
                "Dimensionner l'alimentation électrique et la batterie pour encaisser les forts appels de puissance RF durant les prises de vue radar.",
                "Embarquer optionnellement un récepteur AIS/ADS-B en charge utile secondaire si les marges de masse et de budget le permettent.",
            ],
            scientific_or_operational_need=(
                "Les zones arctiques et nord-européennes sont couvertes de nuages plus de 70 % du temps et plongées dans la nuit "
                "polaire plusieurs mois par an : seule une charge utile active micro-ondes (SAR) garantit la continuité de surveillance."
            ),
            orbit_constraints_description=(
                "Orbite polaire ou héliosynchrone (SSO crépusculaire 06h00/18h00 recommandée pour maximiser l'ensoleillement des panneaux "
                "solaires et alimenter le radar) à une altitude comprise entre 450 km et 580 km."
            ),
            conops_guidance=(
                "Prises de vue radar programmées de 60 à 120 secondes par orbite au-dessus des zones maritimes d'intérêt. "
                "Le débit brut élevé (plusieurs Gbit/s) impose une mémoire de masse d'au moins 1 à 2 To et une liaison descendante "
                "en bande X large bande ou bande Ka."
            ),
            deliverables_expected=[
                "Expliquer l'influence de l'altitude orbitale et de la longueur d'antenne sur la résolution azimutale et le bilan NESZ.",
                "Vérifier la tenue du bilan de puissance moyenne et crête de la plateforme face à la consommation du radar.",
                "Justifier le choix du lanceur au regard de la masse humide avec marge de 20 %.",
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

    # ------------------------------------------------------------------ 3. Atmosphère Terrestre & Gaz à Effet de Serre
    (
        "exam_atmosphere_greenhouse_gas.mission.json",
        dict(
            schema_version="1.0.0",
            id="EXAM-2026-ATMO-GHG",
            title="Mission AtmoWatch — Chimie de l'Atmosphère Terrestre & Panaches de Méthane",
            client_agency="Institut Spatial du Climat & de l'Atmosphère (ISCA)",
            domain_label="Connaissance de l'Atmosphère Terrestre — Spectrométrie gaz à effet de serre",
            mission_type="atmosphere",
            max_budget_meur=16.5,
            target_lifetime_years=5.0,
            min_trl=8,
            context=(
                "Dans le cadre du suivi international des émissions anthropiques, l'ISCA lance une mission spatiale dédiée à la "
                "connaissance fine de la composition de l'atmosphère terrestre et à la détection des super-émetteurs de méthane (CH4) "
                "et de dioxyde de carbone (CO2)."
            ),
            primary_objective=(
                "Mesurer par spectrométrie imageuse dans le proche infrarouge et l'infrarouge à ondes courtes (SWIR, autour de 1,65 µm) "
                "les colonnes d'absorption de CH4 et de CO2 avec une résolution spectrale meilleure ou égale à 1,0 nm (objectif 0,3 nm), "
                "une résolution spatiale au sol <= 10 m permettant d'attribuer les panaches aux installations industrielles, et un SNR >= 50."
            ),
            secondary_objectives=[
                "Caractériser les aérosols atmosphériques et les panaches urbains sur l'ensemble des bassins industriels mondiaux.",
                "Maintenir le budget global du segment spatial sous 16,5 M€ grâce à une plateforme microsatellite optimisée.",
            ],
            scientific_or_operational_need=(
                "Les inventaires climatiques souffrent d'une forte incertitude sur les fuites ponctuelles de méthane (puits gaziers, "
                "décharges, mines, pipelines). Seul un spectromètre à très haute finesse spectrale dans la bande SWIR (> 1600 nm) "
                "permet de séparer les raies rovibrationnelles du CH4 et du CO2 du fond d'albédo terrestre."
            ),
            orbit_constraints_description=(
                "Orbite héliosynchrone (SSO) vers 500–650 km d'altitude avec passage en milieu de journée (LTAN 11h00–13h00) "
                "pour maximiser le flux solaire réfléchi dans le SWIR et réduire l'angle zénithal solaire."
            ),
            conops_guidance=(
                "Observation systématique au nadir des zones continentales et des sites d'extraction. Refroidissement actif du "
                "plan focal SWIR maintenu en permanence ; étalonnage spectral sur diffuseur solaire une fois par jour au passage polaire."
            ),
            deliverables_expected=[
                "Justifier le choix du spectromètre (domaine spectral SWIR >= 1650 nm et finesse spectrale <= 1 nm) par rapport aux spectromètres VNIR classiques.",
                "Vérifier la compatibilité de pointage et de dissipation thermique entre le sondeur refroidi et la plateforme choisie.",
                "Décrire le plan d'opérations (calibration, acquisition, vidage mémoire).",
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

    # ------------------------------------------------------------------ 4. Cosmologie & Astrométrie Champ Profond
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
                "Pour cartographier la distribution de matière noire par cisaillement gravitationnel faible (weak lensing) "
                "et suivre les supernovæ distantes, le consortium souhaite placer en orbite basse un télescope optique à grand "
                "diamètre primaire et très haute stabilité de pointage."
            ),
            primary_objective=(
                "Disposer d'un télescope spatial d'au moins 0,60 m d'ouverture primaire (objectif 0,70 m) limité par la diffraction "
                "(tache de diffraction équivalente <= 0,65 m projetée à l'échelle de référence), monté sur une plateforme garantissant "
                "une précision de pointage meilleure ou égale à 0,004° afin d'éviter tout flou d'étalement de la fonction d'étalement "
                "du point (PSF) lors des poses longues sur le ciel profond."
            ),
            secondary_objectives=[
                "Assurer un stockage bord d'au moins 1 à 2 To pour accumuler les mosaïques du relevé cosmologique.",
                "Privilégier un contrôle d'attitude à très faibles micro-vibrations (roues agiles ou suite ultra-stable).",
            ],
            scientific_or_operational_need=(
                "La mesure de la déformation cohérente de millions de galaxies lointaines par la matière noire exige une qualité "
                "d'image affranchie de la turbulence atmosphérique terrestre, un grand diamètre collecteur de photons et une "
                "stabilité d'attitude sub-arcseconde."
            ),
            orbit_constraints_description=(
                "Orbite héliosynchrone crépusculaire (dawn-dusk, 550–700 km) maintenant le télescope à l'ombre du pare-soleil "
                "et permettant de pointer à l'opposé de la Terre et du Soleil avec un minimum d'interruptions d'occultation."
            ),
            conops_guidance=(
                "Pointage inertiel prolongé (poses de 300 à 600 s par champ cosmologique) suivi d'un basculement fin vers le champ "
                "suivant. Vidage quotidien des images scientifiques non destructivement compressées en bande X ou Ka."
            ),
            deliverables_expected=[
                "Justifier le diamètre du miroir primaire choisi vis-à-vis de la limite de diffraction et de la collecte de photons.",
                "Démontrer que l'association (plateforme + option ADCS) respecte l'exigence stricte de pointage <= 0,004°.",
                "Présenter le bilan de masse et le choix du lanceur (rideshare lourd ESPA Grande ou lanceur dédié).",
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
                    description="La tache de diffraction de référence doit être <= 0,65 m.",
                    req_type="payload_perf",
                    parameter="diffraction_ground_spot_m",
                    operator="<=",
                    threshold=0.65,
                    goal=0.50,
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
                ),
                dict(
                    id="svalbard_cosmo",
                    name="Svalbard Polar Station",
                    latitude_deg=78.22,
                    longitude_deg=15.40,
                    altitude_m=450.0,
                    min_elevation_deg=5.0,
                    bands_supported=["S", "X", "Ka"],
                    cost_per_pass_eur=250.0,
                ),
            ],
            target_zones=[],
        ),
    ),

    # ------------------------------------------------------------------ 5. Télécommunications & Haut Débit de Données (Laser / RF)
    (
        "exam_high_throughput_datalink.mission.json",
        dict(
            schema_version="1.0.0",
            id="EXAM-2026-DATARATE",
            title="Mission TeraRelay — Établissement d'une Liaison Spatiale Très Haut Débit (≥ 25 Gbit/s)",
            client_agency="Opérateur Européen de Dorsale Spatiale Souveraine",
            domain_label="Télécommunications Spatiales — Établir un très haut débit de données optique",
            mission_type="telecom_opt",
            max_budget_meur=15.0,
            target_lifetime_years=6.0,
            min_trl=8,
            context=(
                "Pour désengorger les liaisons radio-fréquence saturées et rapatrier en temps quasi-réel des téraoctets de données "
                "issues de satellites d'observation ou de centres isolés, l'opérateur souhaite déployer un nœud orbital capable "
                "d'établir une liaison optique directe vers le sol à au moins 25 Gbit/s."
            ),
            primary_objective=(
                "Établir une liaison descendante laser à 1550 nm délivrant un débit effectif supérieur ou égal à 25 Gbit/s "
                "(objectif 100 Gbit/s) vers des stations sol optiques de 80 cm de diamètre, avec une marge de liaison d'au moins "
                "6,0 dB en ciel clair et une précision de pointage plateforme <= 0,008° pour assurer l'acquisition rapide du faisceau."
            ),
            secondary_objectives=[
                "Minimiser le coût du segment spatial (plafond strict de 15,0 M€) pour permettre le déploiement futur d'une constellation.",
                "Embarquer optionnellement un transpondeur RF bande X/Ka de secours pour la continuité de service par temps couvert.",
            ],
            scientific_or_operational_need=(
                "Les capteurs modernes génèrent plusieurs gigabits par seconde alors que les passages au-dessus d'une station sol "
                "en orbite basse ne durent que 6 à 10 minutes. Établir un débit de 25 Gbit/s permet de transférer plus de "
                "1,5 téraoctet de données utiles en un seul passage de 8 minutes."
            ),
            orbit_constraints_description=(
                "Orbite basse entre 500 km et 750 km d'altitude. Une altitude trop élevée dégrade le bilan de liaison en 1/R², "
                "tandis qu'une altitude trop basse raccourcit la durée de visibilité géométrique des stations optiques."
            ),
            conops_guidance=(
                "Pointage grossier du satellite vers la station sol optique, acquisition du phare montant (beacon) par le miroir "
                "de pointage fin (PAT) du terminal laser, verrouillage en boucle fermée (< 1,5 µrad) et vidage à très haut débit "
                "de la mémoire de masse."
            ),
            deliverables_expected=[
                "Calculer le volume total de données (en Go ou To) transférable lors d'un passage de 6 minutes au débit retenu.",
                "Démontrer la fermeture du bilan de liaison optique (puissance laser, diamètre télescope, pertes de pointage, marge >= 6 dB).",
                "Discuter la sensibilité aux nuages et l'intérêt de la diversité géographique des stations optiques (Calern, Tenerife, Athènes).",
            ],
            requirements=[
                dict(
                    id="REQ-DATA-RATE-01",
                    title="Débit de données optique atteignable",
                    description="Le débit de données effectif sur la liaison LEO-sol doit être >= 25,0 Gbit/s.",
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
                    title="Marge de bilan de liaison optique",
                    description="La marge du lien optique à 1550 nm doit être >= 6,0 dB.",
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
                dict(
                    id="ogs_helmos",
                    name="Helmos Optical Ground Station (Grèce)",
                    latitude_deg=37.98,
                    longitude_deg=22.20,
                    altitude_m=2340.0,
                    min_elevation_deg=15.0,
                    bands_supported=["Optical"],
                    cost_per_pass_eur=320.0,
                ),
            ],
            target_zones=[],
        ),
    ),

    # ------------------------------------------------------------------ 6. Distribution Quantique de Clés (QKD, preserved IDs for unit test)
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
                "de calcul souverains et les ambassades en clés cryptographiques inviolables par injection laser nocturne."
            ),
            primary_objective=(
                "Générer et distribuer des clés cryptographiques quantiques selon le protocole BB84 à états leurres à 850 nm "
                "vers des stations sol optiques de 1 m, avec un taux d'erreur quantique (QBER) <= 6,0 % et un débit asymptotique "
                "de clé secrète >= 1 000 bit/s lors des passages nocturnes."
            ),
            secondary_objectives=[
                "Garantir un pointage plateforme <= 0,008° afin de permettre au système de suivi fin sub-microradian d'accrocher la station sol.",
                "Assurer l'authentification et la distillation des clés via un canal classique radio S ou X redondé.",
            ],
            scientific_or_operational_need=(
                "Face à la menace des calculateurs quantiques sur les algorithmes asymétriques classiques (RSA/ECC), la distribution "
                "quantique de clés par satellite permet d'échanger à l'échelle intercontinentale des clés à usage unique dont la "
                "sécurité repose sur les lois de la mécanique quantique."
            ),
            orbit_constraints_description=(
                "Orbite héliosynchrone (LTAN ~ 22h30 / 10h30) à une altitude modérée (450–550 km) pour maximiser le nombre de "
                "passages de nuit au-dessus de l'Europe et minimiser l'atténuation géométrique du canal quantique."
            ),
            conops_guidance=(
                "Émission quantique exclusivement de nuit sur les stations sol dégagées de nuages. Synchronisation temporelle "
                "sub-nanoseconde et post-traitement (tamisage, correction d'erreurs, amplification de confidentialité) sur le "
                "canal classique S/X."
            ),
            deliverables_expected=[
                "Analyser le compromis entre l'altitude orbitale, les pertes géométriques du canal (en dB) et le débit de clé secrète.",
                "Justifier le choix du terminal QKD et du pack ADCS pour tenir le budget de pointage.",
                "Évaluer la quantité de clés de 256 bits produite par passage utile.",
            ],
            requirements=[
                dict(
                    id="REQ-QKD-QBER-01",
                    title="Taux d'Erreur Quantique (QBER)",
                    description="Quantum Bit Error Rate <= 6.0 % pour garantir la distillation de clé",
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
                    description="Secret Key Rate moyen >= 1000 bps lors des contacts",
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
                ),
                dict(
                    id="sta_tenerife_ogs",
                    name="Teide Optical Ground Station (IAC)",
                    latitude_deg=28.30,
                    longitude_deg=-16.51,
                    altitude_m=2390.0,
                    min_elevation_deg=15.0,
                    bands_supported=["Optical", "S"],
                    cost_per_pass_eur=450.0,
                ),
            ],
            target_zones=[],
        ),
    ),

    # ------------------------------------------------------------------ 7. CubeSat Bas Coût Surveillance Maritime & Débit RF
    (
        "exam_cubesat_maritime_iot.mission.json",
        dict(
            schema_version="1.0.0",
            id="EXAM-2026-CUBESAT-RF",
            title="Mission NanoSentinel — CubeSat Bas-Coût de Collecte IoT/AIS & Imagerie Côtière",
            client_agency="Pôle Universitaire & Maritime NewSpace",
            domain_label="Nanosatellite Bas-Coût — Établir un service de collecte de données RF sous très faible budget",
            mission_type="telecom_radio",
            max_budget_meur=1.6,
            target_lifetime_years=2.5,
            min_trl=8,
            context=(
                "Un consortium universitaire et portuaire dispose d'un budget strictement plafonné à 1,60 M€ (lancement compris) "
                "pour démontrer en orbite un service de collecte de données maritimes/IoT par radio-fréquence, éventuellement "
                "complété par une nano-caméra côtière."
            ),
            primary_objective=(
                "Établir une liaison descendante radio-fréquence d'au moins 15 Mbit/s avec une marge de liaison >= 3,0 dB "
                "depuis un nanosatellite (CubeSat 6U, 12U ou 16U) lancé en déployeur partagé, sans dépasser l'enveloppe budgétaire "
                "totale de 1,60 M€."
            ),
            secondary_objectives=[
                "Ajouter une seconde charge utile (ex. caméra optique 6 cm) si la plateforme CubeSat et le budget le permettent.",
                "Maintenir une masse au lancement compatible avec le service de déployeur CubeSat (<= 32 kg).",
            ],
            scientific_or_operational_need=(
                "Ce sujet met l'accent sur l'ingénierie NewSpace sous forte contrainte de coût : l'étudiant doit éviter tout "
                "sur-dimensionnement (plateformes de 50 kg ou lanceurs dédiés hors budget) et sélectionner uniquement les "
                "équipements strictement nécessaires."
            ),
            orbit_constraints_description=(
                "Orbite héliosynchrone de covoiturage standard entre 500 km et 550 km d'altitude, imposée par le vol partagé."
            ),
            conops_guidance=(
                "Réception permanente des balises AIS/IoT à faible consommation, vidage en bande S lors des passages sur la "
                "station universitaire."
            ),
            deliverables_expected=[
                "Démontrer le respect strict du plafond de 1,60 M€ (arbitrage 6U vs 12U vs 16U et choix du lanceur déployeur).",
                "Vérifier le bilan de masse, de volume (en U/litres) et de puissance du CubeSat.",
            ],
            requirements=[
                dict(
                    id="REQ-RF-RATE-01",
                    title="Débit de données RF descendant",
                    description="Le débit maximal de la charge utile RF doit être >= 15,0 Mbit/s.",
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
                    description="La marge Eb/N0 sur la liaison descendante doit être >= 3,0 dB.",
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
                    name="Station Universitaire Maritime de Brest",
                    latitude_deg=48.39,
                    longitude_deg=-4.49,
                    altitude_m=50.0,
                    min_elevation_deg=10.0,
                    bands_supported=["UHF", "S", "X"],
                    cost_per_pass_eur=40.0,
                )
            ],
            target_zones=[
                dict(
                    id="zone_atlantic",
                    name="Façade Atlantique & Manche",
                    points_lat_lon=[(43.0, -10.0), (50.0, -5.0), (51.0, 2.0)],
                    priority=1,
                )
            ],
        ),
    ),
]


def main() -> None:
    MISSIONS_DIR.mkdir(parents=True, exist_ok=True)
    for fname, data in MISSIONS:
        spec = MissionSpecification.model_validate(data)
        out = MISSIONS_DIR / fname
        out.write_text(spec.model_dump_json(indent=2), encoding="utf-8")
        print(f"Wrote {fname}: {spec.id} — {spec.title} (budget {spec.max_budget_meur} M€, {len(spec.requirements)} reqs)")


if __name__ == "__main__":
    main()
