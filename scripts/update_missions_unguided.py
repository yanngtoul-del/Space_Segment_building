"""Rewrite all 10 mission specification sheets to be authentic, non-guided engineering Statements of Work."""

import json
from pathlib import Path

MISSIONS_DIR = Path(r"C:\Users\Lapto\PycharmProjects\Space_Segment_building\data\missions")


MISSIONS_UPDATES = {
    "exam_optical_light_lowcost.mission.json": {
        "context": (
            "Une jeune pousse européenne d'agriculture de précision souhaite déployer le premier satellite démonstrateur tête de série "
            "d'une future constellation de suivi hydrique et parcellaire. Le budget d'investissement (CAPEX) est strictement plafonné à "
            "2.35 M€ tout compris (plateforme, charge utile, options sous-systèmes, campagne d'étalonnage au sol et lancement). "
            "Ce cahier des charges place l'architecte devant les compromis fondamentaux du NewSpace : arbitrer entre résolution spatiale "
            "au nadir (seuil GSD ≤ 2.80 m, objectif ≤ 1.60 m), largeur de fauchée au sol (seuil ≥ 18.0 km, objectif ≥ 45.0 km), "
            "rapport signal-sur-bruit (seuil SNR ≥ 80, objectif ≥ 120), précision de pointage ADCS (≤ 0.06°, objectif ≤ 0.03°), "
            "qualité d'étalonnage radiométrique au sol (≤ 2.0 % en vide thermique, objectif ≤ 1.8 %) et durée de vie nominale "
            "(seuil ≥ 3.0 ans, objectif ≥ 4.0 ans)."
        ),
        "primary_objective": (
            "Concevoir un nanosatellite ou microsatellite d'observation optique multispectrale en orbite héliosynchrone (SSO) respectant "
            "l'ensemble des exigences techniques et programmatiques : résolution spatiale au nadir GSD ≤ 2.80 m (objectif ≤ 1.60 m), "
            "largeur de fauchée au sol ≥ 18.0 km (objectif ≥ 45.0 km), rapport signal-sur-bruit SNR ≥ 80 (objectif ≥ 120), "
            "précision de pointage ADCS ≤ 0.06° (objectif ≤ 0.03°), incertitude d'étalonnage radiométrique ≤ 2.0 % (objectif ≤ 1.8 %) "
            "et durée de vie plateforme ≥ 3.0 ans (objectif ≥ 4.0 ans), sous une enveloppe globale ≤ 2.35 M€ TTC."
        ),
        "secondary_objectives": [
            "Étudier le compromis géométrique lié au choix de l'altitude orbitale SSO et des paramètres optiques (focale, pas de pixel, nombre de pixels cross-track) entre résolution spatiale au nadir et largeur de fauchée au sol.",
            "Analyser le mode d'acquisition du plan focal (capteur matriciel 2D Frame vs barrette linéaire Push-Broom avec ou sans TDI) et ses conséquences sur les exigences de stabilité d'attitude ADCS et sur le rapport signal-sur-bruit.",
            "Évaluer la tension entre la classe de plateforme (nanosatellite CubeSat vs microsatellite), les objectifs étendus de performance (résolution sub-2 m, très large fauchée ou durée de vie ≥ 4 ans), le bilan de puissance électrique en orbite et le plafond budgétaire.",
            "Arbitrer la stratégie d'étalonnage radiométrique au sol (campagne en cuve à vide thermique TVAC vs étalonnage en salle blanche à pression ambiante) au regard de la dérive thermo-élastique en orbite et du budget disponible."
        ],
        "scientific_or_operational_need": (
            "Fournir des cartes hebdomadaires d'indice de végétation (NDVI) et de stress hydrique à l'échelle intra-parcellaire (GSD ≤ 2.80 m) "
            "sur les grandes plaines céréalières européennes avec une fauchée minimale de 18.0 km et une radiométrie absolue maîtrisée (≤ 2.0 %), "
            "à un coût unitaire compatible avec le déploiement ultérieur d'une constellation commerciale."
        ),
        "orbit_constraints_description": (
            "Orbite basse héliosynchrone (SSO) recommandée entre 400 km et 600 km d'altitude pour garantir un éclairement solaire constant "
            "lors des prises de vue agronomiques. L'architecte devra déterminer la fenêtre d'altitude optimale permettant de concilier "
            "le seuil de résolution spatiale (GSD proportionnel à H/f) et la largeur de fauchée minimale (proportionnelle à N_pix × GSD)."
        ),
        "conops_guidance": (
            "Décrire le profil opérationnel sur une orbite type : programmation des prises de vue diurnes au nadir sur les bassins agricoles, "
            "mode de balayage du capteur (Push-Broom ou clichés matriciels), gestion de la profondeur de décharge batterie en éclipse, "
            "stockage bord sur mémoire flash et téléchargement des scènes compressées lors des passages au-dessus des stations sol de Toulouse et Delft."
        ),
        "deliverables_expected": [
            "Justification paramétrique du choix de l'altitude SSO et de la charge utile optique retenue (analyse croisée GSD, fauchée, SNR, architecture capteur Push-Broom/Matriciel et bilan SWaP).",
            "Dimensionnement de la plateforme et des équipements sous-systèmes (ADCS, mémoire de masse, télémesure/descente de données, propulsion éventuelle) avec vérification des marges de masse et de puissance électrique.",
            "Justification technico-économique de la campagne d'étalonnage au sol et du service de lancement retenus dans l'enveloppe de 2.35 M€.",
            "En cas de non-conformité résiduelle résultant d'un arbitrage délibéré (dépassement budgétaire pour viser un objectif étendu, compromis sur la fauchée ou sur le protocole d'étalonnage sol), rédaction d'une Demande de Dérogation (Request for Waiver) argumentée à l'Onglet 9."
        ],
        "req_descriptions": {
            "REQ-LIGHT-GSD": "La distance d'échantillonnage au sol (GSD) au nadir doit être ≤ 2.80 m (objectif ≤ 1.60 m) afin de résoudre l'hétérogénéité intra-parcellaire.",
            "REQ-LIGHT-SWATH": "La largeur de fauchée au nadir doit être ≥ 18.0 km (objectif ≥ 45.0 km) pour assurer la couverture hebdomadaire des bassins agricoles.",
            "REQ-LIGHT-SNR": "Le rapport signal-sur-bruit au nadir doit être ≥ 80 (objectif ≥ 120) pour garantir la qualité radiométrique des indices végétatifs.",
            "REQ-LIGHT-POINT": "La précision de pointage 3 axes du système ADCS doit être ≤ 0.06° (objectif ≤ 0.03°) et sa stabilité compatible avec le temps d'intégration du capteur.",
            "REQ-LIGHT-CALIB": "L'incertitude radiométrique absolue certifiée au sol doit être ≤ 2.0 % (objectif ≤ 1.8 %) afin d'assurer la comparabilité multi-temporelle des mesures.",
            "REQ-LIGHT-LIFE": "La durée de vie nominale de la plateforme doit être ≥ 3.0 ans (objectif ≥ 4.0 ans)."
        }
    },

    "exam_optical_earth_observation.mission.json": {
        "context": (
            "Dans le cadre du renouvellement des capacités européennes de cartographie rapide et de surveillance environnementale et côtière, "
            "l'Agence souhaite déployer un satellite d'observation optique sub-métrique agile en orbite héliosynchrone (SSO). "
            "Le cahier des charges comporte une tension physique, industrielle et budgétaire entre six exigences simultanées : "
            "(1) une résolution spatiale au nadir sub-métrique (seuil GSD ≤ 0.88 m, objectif ≤ 0.70 m), "
            "(2) une largeur de fauchée au nadir ≥ 17.0 km (objectif ≥ 20.0 km), "
            "(3) un rapport signal-sur-bruit SNR ≥ 58 (objectif ≥ 75), "
            "(4) une incertitude radiométrique absolue caractérisée au sol ≤ 2.0 % (objectif ≤ 1.5 %), "
            "(5) une précision de pointage ADCS ≤ 0.005° (objectif ≤ 0.003°) et "
            "(6) une durée de vie ≥ 5.0 ans (objectif ≥ 7.0 ans), tout en respectant les règles de retour géographique ESA entre la France, "
            "l'Italie et l'Allemagne sous un plafond global de 15.20 M€."
        ),
        "primary_objective": (
            "Acquérir des images optiques sub-métriques sur les zones d'intérêt européennes et méditerranéennes en respectant les seuils "
            "techniques du cahier des charges : GSD au nadir ≤ 0.88 m (objectif ≤ 0.70 m), fauchée au nadir ≥ 17.0 km (objectif ≥ 20.0 km), "
            "SNR au nadir ≥ 58 (objectif ≥ 75), étalonnage radiométrique sous vide thermique ≤ 2.0 % (objectif ≤ 1.5 %), "
            "précision de pointage ≤ 0.005° (objectif ≤ 0.003°) et durée de vie ≥ 5.0 ans (objectif ≥ 7.0 ans), pour un coût consolidé ≤ 15.20 M€ TTC."
        ),
        "secondary_objectives": [
            "Étudier le couplage entre l'altitude orbitale SSO et les caractéristiques du télescope (diamètre de pupille, distance focale, format du détecteur) face à l'antagonisme géométrique entre résolution au sol (GSD) et largeur de fauchée.",
            "Analyser les contraintes imposées par l'acquisition Push-Broom à intégration TDI (nombre d'étages TDI, fréquence ligne, tolérance à la dérive angulaire et au jitter) sur le dimensionnement du sous-système de contrôle d'attitude (ADCS).",
            "Arbitrer l'allocation budgétaire et industrielle entre la plateforme, l'instrument optique, les équipements de servitudes et la campagne d'essais en vide thermique (TVAC) afin de respecter simultanément le plafond de 15.20 M€ et les quotas de retour géographique ESA (France 35–60 %, Italie 25–45 %, Allemagne 8–25 %)."
        ],
        "scientific_or_operational_need": (
            "Les services de sécurité civile, d'urbanisme et de surveillance côtière requièrent une résolution spatiale sub-métrique "
            "(GSD ≤ 0.88 m) pour identifier la voirie, le bâti et l'érosion du trait de côte, tandis que les applications hydrologiques "
            "et agricoles exigent une fauchée large (≥ 17.0 km) et une incertitude radiométrique absolue ≤ 2.0 % pour le suivi quantitatif des surfaces."
        ),
        "orbit_constraints_description": (
            "Orbite basse héliosynchrone (SSO) à définir dans la plage 400–600 km. Le choix de l'altitude doit résulter d'une analyse "
            "quantitative du compromis entre la finesse d'échantillonnage spatial (GSD), le maintien de la fauchée au-dessus de 17.0 km "
            "et la compensation de la traînée atmosphérique sur la durée de vie de la mission."
        ),
        "conops_guidance": (
            "Préciser le profil opérationnel : prises de vue diurnes sur l'arc descendant (vers 10h30 heure solaire locale), basculement "
            "d'attitude agile hors-nadir pour revisiter les zones prioritaires, synchronisation du défilement au sol pour l'intégration TDI, "
            "stockage bord sur mémoire de masse haute capacité, vidage en bande X lors des passages sur Kiruna et Toulouse, et maintien d'orbite."
        ),
        "deliverables_expected": [
            "Analyse du compromis d'altitude orbitale (GSD vs Fauchée vs SNR vs maintien à poste) et justification de l'orbite SSO retenue.",
            "Justification du choix de l'instrument optique (diamètre, focale, architecture Push-Broom TDI vs matricielle), de la plateforme et de la chaîne ADCS associée.",
            "Validation de la campagne d'étalonnage optique sous vide thermique et démonstration de la conformité aux quotas de retour géographique ESA (France, Italie, Allemagne) et au plafond hors-ESA (≤ 15 %).",
            "En cas de non-conformité résiduelle résultant d'un choix architectural (recherche de l'objectif GSD ≤ 0.70 m, arbitrage budgétaire ou industriel), rédaction d'une Demande de Dérogation (Request for Waiver) argumentée à l'Onglet 9."
        ],
        "req_descriptions": {
            "REQ-OPT-GSD": "La distance d'échantillonnage au sol (GSD) au nadir doit être ≤ 0.88 m (objectif ≤ 0.70 m) pour permettre l'analyse fine des infrastructures urbaines et côtières.",
            "REQ-OPT-SWATH": "La fauchée au sol doit couvrir au minimum 17.0 km au nadir (objectif ≥ 20.0 km), exigence directement antagoniste avec l'abaissement de l'altitude orbitale ou l'augmentation de la focale.",
            "REQ-OPT-SNR": "Le rapport signal-sur-bruit dans la bande panchromatique au nadir doit être ≥ 58 (objectif ≥ 75).",
            "REQ-OPT-CALIB": "L'incertitude radiométrique absolue certifiée au sol doit être ≤ 2.0 % (objectif ≤ 1.5 %), nécessitant une caractérisation représentative de l'environnement radiatif et thermique orbital.",
            "REQ-SYS-POINT": "La précision de pointage 3 axes (plateforme et/ou suite ADCS) doit être ≤ 0.005° (objectif ≤ 0.003°) avec une stabilité compatible avec l'intégration TDI.",
            "REQ-SYS-LIFE": "La plateforme sélectionnée doit être qualifiée pour au moins 5.0 ans en orbite LEO (objectif ≥ 7.0 ans)."
        }
    },

    "exam_optical_highperf.mission.json": {
        "context": (
            "Pour les besoins de renseignement stratégique, de sécurité européenne et d'évaluation précise des dommages sur infrastructures critiques, "
            "ce programme vise le déploiement d'un satellite d'observation optique de Très Haute Résolution (THR, classe 30–40 cm) doté d'une forte agilité "
            "de re-pointage. L'architecte doit résoudre l'équation technico-économique d'un système optique à grande pupille (seuil D ≥ 0.70 m, objectif ≥ 1.00 m) "
            "soumis simultanément à une exigence de résolution GSD ≤ 0.40 m (objectif ≤ 0.30 m) et à une exigence de fauchée minimale ≥ 13.8 km (objectif ≥ 16.0 km), "
            "sous un plafond budgétaire strict de 33.50 M€ et des contraintes de souveraineté industrielle franco-allemande."
        ),
        "primary_objective": (
            "Déployer un satellite d'observation optique Très Haute Résolution en orbite SSO délivrant un GSD au nadir ≤ 0.40 m (objectif ≤ 0.30 m), "
            "un diamètre d'ouverture du télescope ≥ 0.70 m (objectif ≥ 1.00 m), une largeur de fauchée au nadir ≥ 13.8 km (objectif ≥ 16.0 km), "
            "une précision de pointage ADCS ≤ 0.004° (objectif ≤ 0.003°), une qualification opto-mécanique en vide thermique ≤ 2.0 % (objectif ≤ 0.9 %) "
            "et une durée de vie ≥ 8.0 ans (objectif ≥ 10.0 ans) sous un plafond global de 33.50 M€ TTC."
        ),
        "secondary_objectives": [
            "Déterminer par le calcul la plage d'altitude orbitale SSO permettant de satisfaire simultanément la contrainte de résolution au nadir (GSD ≤ 0.40 m) et la contrainte de largeur de fauchée (≥ 13.8 km).",
            "Analyser le saut d'échelle physique et financier (masse de l'instrument, classe de plateforme, capacité lanceur et coût global) entre un télescope de classe 70 cm et un instrument de classe métrique (1.00 m).",
            "Dimensionner la chaîne cinématique de contrôle d'attitude (roues de réaction haute capacité vs actionneurs gyroscopiques CMG) au regard des exigences de stabilité d'intégration Push-Broom TDI multi-étages (64 à 128 étages) et d'agilité de basculement hors-nadir.",
            "Assurer la cohérence de la chaîne bord-sol très haut débit (mémoire de masse et émetteur bande X large bande ou bande Ka) et le respect des quotas de retour géographique (France 70–98 %, Allemagne 2–25 %)."
        ],
        "scientific_or_operational_need": (
            "L'identification formelle de véhicules, d'aéronefs sur tarmac et d'ouvrages d'art exige un GSD ≤ 0.40 m (idéalement ≤ 0.30 m) "
            "associé à une fauchée d'au moins 13.8 km et à une haute agilité de dépointage pour acquérir plusieurs cibles ponctuelles "
            "lors d'un même passage au-dessus d'un théâtre d'opérations."
        ),
        "orbit_constraints_description": (
            "Orbite héliosynchrone (SSO) en basse altitude. En raison de l'antagonisme direct entre GSD et largeur de fauchée à géométrie "
            "focale fixée, la fenêtre d'altitude admissible sans dérogation est particulièrement étroite et doit être rigoureusement identifiée par l'architecte."
        ),
        "conops_guidance": (
            "Détailler le mode d'acquisition agile : programmation sécurisée en bande S, basculement rapide hors-nadir entre cibles ponctuelles, "
            "asservissement gyroscopique du défilement au sol pour l'intégration TDI à grand nombre d'étages, chiffrement et stockage sur mémoire "
            "de masse haute capacité, puis vidage très haut débit en bande X ou Ka vers les stations de Toulouse/Creil et Kiruna."
        ),
        "deliverables_expected": [
            "Détermination analytique de la fenêtre d'altitude SSO compatible à la fois avec GSD ≤ 0.40 m et Fauchée ≥ 13.8 km.",
            "Étude comparative des architectures instrumentales et plateformes candidates (compromis ouverture/résolution vs masse, coût de lancement et plafond budgétaire de 33.50 M€).",
            "Justification du sous-système ADCS (stabilité durant l'intégration TDI multi-étages et agilité de re-pointage), de la chaîne de télémesure haut débit et de la qualification TVAC optique.",
            "Validation de la répartition industrielle franco-allemande et, si un objectif étendu (GSD ≤ 0.30 m ou fauchée ≥ 16.0 km) est privilégié au prix d'un écart sur un autre critère, rédaction d'une Demande de Dérogation argumentée à l'Onglet 9."
        ],
        "req_descriptions": {
            "REQ-HP-GSD": "La distance d'échantillonnage au sol (GSD) au nadir doit être ≤ 0.40 m (objectif ≤ 0.30 m) pour permettre l'identification tactique fine.",
            "REQ-HP-APERTURE": "Le diamètre du miroir primaire du télescope doit être ≥ 0.70 m (objectif ≥ 1.00 m) afin de limiter la tache de diffraction et de maximiser le flux photonique.",
            "REQ-HP-SWATH": "La largeur de fauchée au nadir doit être ≥ 13.8 km (objectif ≥ 16.0 km) pour couvrir une agglomération ou une base étendue en une seule trace.",
            "REQ-HP-POINT": "La précision de pointage 3 axes doit être ≤ 0.004° (objectif ≤ 0.003°) avec une dérive et un jitter compatibles avec un plan focal Push-Broom TDI à haute cadence.",
            "REQ-HP-CALIB": "La campagne d'étalonnage interférométrique et radiométrique sous vide thermique doit certifier une incertitude ≤ 2.0 % (objectif ≤ 0.9 %).",
            "REQ-HP-LIFE": "La plateforme doit être qualifiée pour au moins 8.0 ans d'opérations en orbite basse (objectif ≥ 10.0 ans)."
        }
    },

    "exam_atmosphere_greenhouse_gas.mission.json": {
        "context": (
            "La détection et la quantification des panaches ponctuels de méthane (CH₄ vers 1 650 nm) et de dioxyde de carbone (CO₂ vers 1 600–2 050 nm) "
            "issus des sites industriels, pipelines et bassins d'extraction exigent une chaîne instrumentale dispersive complète couplant : "
            "(1) un télescope collecteur avant, (2) une fente spectrométrique d'interface au plan focal (sous-système « Interface Optique ») et "
            "(3) un banc spectromètre infrarouge à ondes courtes (SWIR). Ce cahier des charges confronte l'architecte à un trilemme optique "
            "entre résolution spatiale spectrométrique au nadir (seuil ≤ 6.80 m, objectif ≤ 3.50 m), largeur de fauchée spectrométrique "
            "(seuil ≥ 9.5 km, objectif ≥ 15.0 km), pouvoir de résolution spectrale fine (seuil FWHM ≤ 0.50 nm, objectif ≤ 0.25 nm) et "
            "rapport signal-sur-bruit moyen (seuil SNR ≥ 70, objectif ≥ 120), sous un plafond global de 19.20 M€."
        ),
        "primary_objective": (
            "Assembler et qualifier une chaîne spectrométrique SWIR complète (Télescope collecteur avant + Fente spectrométrique + Spectromètre SWIR "
            "couvrant au-delà de 1 650 nm) en orbite SSO permettant de résoudre les raies d'absorption fines du CH₄ et du CO₂ : extension spectrale "
            "≥ 1 650 nm (objectif ≥ 2 000 nm), résolution spectrale FWHM ≤ 0.50 nm (objectif ≤ 0.25 nm), GSD spatial spectrométrique ≤ 6.80 m "
            "(objectif ≤ 3.50 m), fauchée du banc spectrométrique ≥ 9.5 km (objectif ≥ 15.0 km), SNR moyen ≥ 70 (objectif ≥ 120), "
            "étalonnage cryo-vide ≤ 1.0 % (objectif ≤ 0.9 %) et durée de vie ≥ 5.0 ans (objectif ≥ 7.0 ans), sous 19.20 M€ TTC."
        ),
        "secondary_objectives": [
            "Maîtriser le couplage opto-mécanique à trois étages [Télescope avant → Fente spectrométrique → Banc spectromètre] : le banc dispersif ne possédant pas d'optique frontale propre, son échantillonnage spatial (GSD), sa fauchée et son flux lumineux incident (via l'ouverture numérique F/#) dépendent directement du télescope collecteur auquel il est associé.",
            "Analyser l'effet de la longueur focale et du nombre d'ouverture (F/#) du télescope collecteur avant sur l'équilibre entre résolution spatiale (GSD ≤ 6.80 m), largeur de fauchée (≥ 9.5 km) et rapport signal-sur-bruit (SNR ≥ 70).",
            "Comparer les spectromètres du catalogue selon leur pouvoir séparateur spectral (FWHM requis ≤ 0.50 nm pour isoler les raies rovibrationnelles des gaz traces contre quelques nanomètres pour l'imagerie minéralogique) et leur origine industrielle.",
            "Intégrer une campagne d'étalonnage spectral et radiométrique sous vide cryogénique (incertitude ≤ 1.0 %) tout en respectant les quotas de retour géographique ESA (France 30–60 %, Allemagne 10–35 %, Espagne 5–20 %)."
        ],
        "scientific_or_operational_need": (
            "Pour inverser les colonnes intégrées XCO₂ et XCH₄ avec une précision inférieure à 1 % sans biais systématique et attribuer un panache "
            "à une installation précise, il est indispensable de séparer les raies d'absorption individuelles (FWHM ≤ 0.50 nm), de maintenir "
            "un SNR moyen ≥ 70 dans le SWIR et d'étalonner la fonction d'appareil spectrale (ISRF) sous vide cryogénique (incertitude ≤ 1.0 %)."
        ),
        "orbit_constraints_description": (
            "Orbite héliosynchrone (SSO) autour de 450–550 km d'altitude avec passage à l'équateur en début d'après-midi (~13h00 heure solaire locale) "
            "afin de maximiser le rayonnement solaire réfléchi en bande SWIR et le mélange convectif de la couche limite atmosphérique."
        ),
        "conops_guidance": (
            "Décrire le fonctionnement couplé Télescope + Fente + Spectromètre : régulation cryogénique du plan focal SWIR, acquisitions Push-Broom "
            "au nadir au-dessus des bassins industriels et miniers, séquences d'étalonnage spectral en vol (visées solaires via diffuseur et visées lunaires), "
            "stockage bord et vidage en bande X sur les stations de Kiruna et Maspalomas."
        ),
        "deliverables_expected": [
            "Justification physique et optique de l'assemblage à 3 étages retenu : choix du télescope collecteur avant (focale f, ouverture D et F/#), de l'interface fente spectrométrique et du banc spectromètre SWIR.",
            "Analyse quantitative du compromis entre résolution spatiale spectrométrique (GSD), largeur de fauchée et rapport signal-sur-bruit en fonction du télescope collecteur sélectionné.",
            "Validation du bilan énergétique et thermique de la plateforme (dissipation du cryorefroidisseur SWIR), de la campagne d'essais cryo-vide et des quotas de retour géographique ESA (France, Allemagne, Espagne).",
            "En cas de choix privilégiant l'objectif étendu de résolution spatiale (≤ 3.50 m) ou un équipement hors quota, présentation d'une Demande de Dérogation (Waiver) argumentée à l'Onglet 9."
        ],
        "req_descriptions": {
            "REQ-ATMO-SWIR-RANGE": "Le spectromètre doit couvrir le domaine SWIR au-delà de 1 650 nm (objectif ≥ 2 000 nm) pour observer les bandes d'absorption rovibrationnelles du CH₄ et du CO₂.",
            "REQ-ATMO-SPEC-RES": "La largeur à mi-hauteur de la fonction d'appareil spectrale (FWHM) doit être ≤ 0.50 nm (objectif ≤ 0.25 nm) afin de séparer les raies individuelles des gaz à effet de serre.",
            "REQ-ATMO-GSD": "Le pas d'échantillonnage spatial du spectromètre au nadir (déterminé par la focale du télescope collecteur avant) doit être ≤ 6.80 m (objectif ≤ 3.50 m).",
            "REQ-ATMO-SWATH": "La largeur de fauchée couverte par la fente du spectromètre doit être ≥ 9.5 km (objectif ≥ 15.0 km), exigence antagoniste avec l'emploi d'une longue focale.",
            "REQ-ATMO-SNR": "Le rapport signal-sur-bruit moyen sur les canaux spectraux doit être ≥ 70 (objectif ≥ 120), ce qui requiert un collecteur avant suffisamment ouvert (faible F/#).",
            "REQ-ATMO-CALIB": "L'incertitude radiométrique et spectrale certifiée au sol sous vide cryogénique doit être ≤ 1.0 % (objectif ≤ 0.9 %).",
            "REQ-ATMO-LIFE": "La plateforme doit assurer une durée de vie nominale ≥ 5.0 ans (objectif ≥ 7.0 ans) pour le suivi pluriannuel des émissions."
        }
    },

    "exam_sar_surveillance.mission.json": {
        "context": (
            "Pour surveiller le trafic maritime non-coopératif, les dégazages illicites d'hydrocarbures et la dérive des glaces dans l'Arctique "
            "indépendamment de la couverture nuageuse et de l'éclairement solaire, l'EMSA et l'ESA lancent le programme RadarGuard-SAR. "
            "Cette mission met en jeu le compromis physique fondamental des radars à synthèse d'ouverture (SAR) : en mode Stripmap, "
            "la résolution azimutale théorique vaut d_az = L_a / 2 (où L_a est la longueur d'antenne), tandis que la sensibilité radiométrique "
            "au bruit (NESZ ≤ -21.0 dB, objectif ≤ -24.0 dB) exige un produit Puissance × Surface d'antenne élevé, sous un plafond global de 24.50 M€."
        ),
        "primary_objective": (
            "Déployer un satellite SAR en orbite héliosynchrone (SSO) capable d'acquérir des scènes radar Stripmap avec une résolution azimutale "
            "≤ 1.80 m (objectif ≤ 1.30 m), une résolution distance au sol ≤ 1.00 m (objectif ≤ 0.65 m), une largeur de fauchée radar ≥ 30.0 km "
            "(objectif ≥ 50.0 km), une sensibilité radiométrique NESZ ≤ -21.0 dB (objectif ≤ -24.0 dB), une qualification antenne/Multipactor "
            "en base compacte sous vide thermique ≤ 2.1 % (objectif ≤ 1.8 %) et une durée de vie ≥ 6.0 ans (objectif ≥ 8.0 ans) sous 24.50 M€ TTC."
        ),
        "secondary_objectives": [
            "Analyser l'antagonisme physique SAR entre la finesse de résolution azimutale en mode Stripmap (qui favorise une antenne courte) et la sensibilité radiométrique NESZ (qui exige un grand gain d'antenne et une forte puissance RF émise).",
            "Dimensionner le sous-système électrique (génération solaire, capacité batterie et bus haute puissance) et le contrôle thermique de la plateforme pour supporter les appels de puissance crête et la dissipation thermique de l'antenne radar active.",
            "Optimiser la chaîne d'enregistrement et de télémesure descendante haut débit (bande X ou Ka) ainsi que la qualification radiofréquence sous vide thermique (étalonnage diagramme d'antenne CATR et tenue Multipactor).",
            "Respecter l'équilibre industriel des États participants (Allemagne 40–65 %, France 30–50 %, Italie 3–15 %) et la limite de dépenses hors-ESA (≤ 15 %)."
        ],
        "scientific_or_operational_need": (
            "La détection des pollutions marines par hydrocarbures (amortissement des vagues capillaires de Bragg produisant des zones sombres à très faible "
            "rétrodiffusion) exige impérativement un plancher de bruit radar NESZ ≤ -21.0 dB, tandis que la détection des navires et icebergs "
            "requiert une résolution azimutale ≤ 1.80 m et une résolution distance ≤ 1.00 m sur une fauchée minimale de 30 km."
        ),
        "orbit_constraints_description": (
            "Orbite héliosynchrone (SSO) entre 450 km et 550 km d'altitude. Une orbite crépusculaire (« Dawn-Dusk », 06h00 / 18h00 heure solaire locale) "
            "est privilégiée pour maximiser l'ensoleillement des panneaux solaires et alimenter l'émetteur radar. L'architecte étudiera l'influence "
            "de l'altitude orbitale sur le bilan NESZ (loi en R³) et sur la largeur de fauchée au sol."
        ),
        "conops_guidance": (
            "Justifier le cycle d'utilisation radar (duty cycle par orbite) : préchauffage des modules T/R, prises de vue radar par salves sur les "
            "corridors maritimes arctiques et méditerranéens, stockage sur enregistreur SSD haute vitesse, vidage rapide sur les stations de "
            "Svalbard (SvalSat) et Matera, et gestion thermique du panneau rayonnant."
        ),
        "deliverables_expected": [
            "Analyse comparative des charges utiles SAR du catalogue (compromis longueur d'antenne / résolution azimutale / sensibilité NESZ / puissance RF / origine géographique).",
            "Justification du choix de la plateforme (capacité de puissance moyenne et crête, dissipation thermique, durée de vie) et de l'orbite SSO Dawn-Dusk.",
            "Dimensionnement de la mémoire de masse, du lien descendant haut débit et justification de la campagne d'essais antenne/Multipactor en vide thermique.",
            "Démonstration de la conformité au plafond de 24.50 M€ et aux quotas ESA (Allemagne, France, Italie), ou rédaction d'une Demande de Dérogation argumentée à l'Onglet 9."
        ],
        "req_descriptions": {
            "REQ-SAR-AZ-01": "La résolution azimutale en mode Stripmap (L_a / 2) doit être ≤ 1.80 m (objectif ≤ 1.30 m). Réduire la longueur d'antenne améliore la résolution azimutale mais réduit la surface collectrice et dégrade le NESZ.",
            "REQ-SAR-RG-01": "La résolution distance projetée au sol (liée à la bande passante du chirp radar) doit être ≤ 1.00 m (objectif ≤ 0.65 m).",
            "REQ-SAR-SWATH-01": "La largeur de fauchée radar au sol en mode Stripmap doit être ≥ 30.0 km (objectif ≥ 50.0 km).",
            "REQ-SAR-NESZ-01": "Le niveau de bruit équivalent radar (NESZ) doit être ≤ -21.0 dB (objectif ≤ -24.0 dB) pour permettre la détection des nappes d'hydrocarbures en mer.",
            "REQ-SAR-CALIB": "L'antenne SAR doit être étalonnée en base compacte sous vide thermique avec une incertitude radiométrique ≤ 2.1 % (objectif ≤ 1.8 %) et une qualification Multipactor.",
            "REQ-SAR-LIFE": "La plateforme doit être qualifiée pour au moins 6.0 ans d'opérations en orbite basse (objectif ≥ 8.0 ans)."
        }
    },

    "exam_high_throughput_datalink.mission.json": {
        "context": (
            "Face à la saturation du spectre radiofréquence (bandes X et Ka) et à l'explosion des volumes de données générés par les systèmes "
            "d'observation de nouvelle génération, l'ESA développe le démonstrateur de relais optique OptiRelay-Laser en orbite basse. "
            "Ce cahier des charges confronte l'architecte à l'ingénierie des liaisons laser en espace libre (FSO à 1 550 nm) : atteindre "
            "un débit descendant ≥ 25.0 Gbps (objectif ≥ 40.0 Gbps) avec une marge de liaison ≥ 15.0 dB (objectif ≥ 35.0 dB), "
            "un cône de pré-pointage plateforme ≤ 0.003° (objectif ≤ 0.002°) et une qualification du mécanisme de pointage fin (PAT) "
            "sous vide thermique ≤ 2.6 % (objectif ≤ 2.0 %), tout en respectant l'équilibre industriel entre la France, l'Allemagne et la Suisse "
            "sous un plafond de 14.50 M€."
        ),
        "primary_objective": (
            "Déployer un satellite relais équipé d'un terminal de télécommunication optique laser (1 550 nm) garantissant un débit descendant "
            "≥ 25.0 Gbps (objectif ≥ 40.0 Gbps) vers les stations sol optiques européennes (Tenerife et Plateau de Calern), avec une marge de liaison "
            "≥ 15.0 dB (objectif ≥ 35.0 dB), un pré-pointage ADCS ≤ 0.003° (objectif ≤ 0.002°), une qualification PAT-TVAC ≤ 2.6 % (objectif ≤ 2.0 %) "
            "et une durée de vie ≥ 6.0 ans (objectif ≥ 7.0 ans) sous 14.50 M€ TTC."
        ),
        "secondary_objectives": [
            "Analyser le bilan de liaison optique espace-sol (puissance laser émise, diamètre du télescope, divergence du faisceau limité par la diffraction et pertes de pointage) en fonction de l'altitude orbitale.",
            "Concevoir l'architecture de pointage hiérarchique associant le pré-pointage 3 axes de la plateforme (≤ 0.003°) et la boucle d'asservissement fin (PAT) du terminal optique.",
            "Dimensionner la mémoire tampon embarquée (Mass Memory) pour stocker les téraoctets de données en cas d'indisponibilité météorologique (couverture nuageuse) au-dessus d'une station sol optique.",
            "Arbitrer la sélection de la plateforme, du terminal laser et des équipements vis-à-vis du plafond budgétaire de 14.50 M€ et des quotas de retour géographique ESA (France 35–60 %, Allemagne 30–55 %, Suisse 2–12 %)."
        ],
        "scientific_or_operational_need": (
            "Permettre le rapatriement de plusieurs téraoctets de données en quelques minutes lors d'un passage unique au-dessus d'une station "
            "sol optique européenne équipée d'un télescope récepteur de 80 cm avec optique adaptative."
        ),
        "orbit_constraints_description": (
            "Orbite basse (LEO / SSO) entre 450 km et 650 km d'altitude. Une altitude plus élevée augmente la durée de visibilité par passage "
            "au-dessus des stations de Tenerife et Calern, mais accroît l'affaiblissement géométrique en 1/R² sur le bilan de liaison optique."
        ),
        "conops_guidance": (
            "Détailler la séquence opérationnelle « Acquisition, Pointing & Tracking » (APT) : pré-pointage de la plateforme vers la station sol, "
            "détection de la balise laser montante, verrouillage du miroir de pointage fin (FSM) à haute bande passante, transmission cohérente "
            "à 1 550 nm et stratégie de diversité de sites (basculement Tenerife / Calern selon la nébulosité)."
        ),
        "deliverables_expected": [
            "Étude comparative des terminaux optiques laser du catalogue (débit, marge de liaison, masse/consommation, coût et nationalité industrielle).",
            "Justification du couplage ADCS plateforme / pointage fin PAT, du dimensionnement de la mémoire tampon et de la campagne de qualification en vide thermique.",
            "Vérification de la conformité budgétaire (≤ 14.50 M€) et des quotas de retour géographique ESA (France, Allemagne, Suisse).",
            "En cas de choix privilégiant un objectif étendu de débit (≥ 40 Gbps) au prix d'un dépassement budgétaire ou d'un déséquilibre géographique, rédaction d'une Demande de Dérogation argumentée à l'Onglet 9."
        ],
        "req_descriptions": {
            "REQ-LASER-RATE": "Le débit utile de la liaison laser espace-sol doit être ≥ 25.0 Gbps (objectif ≥ 40.0 Gbps).",
            "REQ-LASER-MARGIN": "La marge du bilan de liaison optique à 1 550 nm doit être ≥ 15.0 dB (objectif ≥ 35.0 dB) pour absorber la scintillation atmosphérique et les cirrus fins.",
            "REQ-LASER-POINTING": "Le système ADCS du satellite doit assurer un pré-pointage ≤ 0.003° (objectif ≤ 0.002°) afin de placer la station sol dans le cône d'acquisition du terminal optique.",
            "REQ-LASER-CALIB": "Le terminal optique et son mécanisme de pointage fin (PAT) doivent être qualifiés en vide thermique avec une incertitude ≤ 2.6 % (objectif ≤ 2.0 %) pour garantir la co-axialité émission/réception.",
            "REQ-LASER-LIFE": "La plateforme doit présenter une durée de vie nominale ≥ 6.0 ans (objectif ≥ 7.0 ans)."
        }
    },

    "exam_qkd_secure_links.mission.json": {
        "context": (
            "Dans le cadre de l'infrastructure européenne de communication quantique (EuroQCI / SAGA), l'Union Européenne et l'ESA souhaitent "
            "déployer un satellite de Distribution Quantique de Clés (QKD) en orbite basse héliosynchrone afin d'établir des clés cryptographiques "
            "inconditionnellement sûres entre les chancelleries et centres de données européens. Ce cahier des charges confronte l'architecte "
            "aux exigences physiques de la photonique quantique spatiale : garantir un taux d'erreur binaire quantique QBER ≤ 2.0 % (objectif ≤ 1.60 %) "
            "et un débit asymptotique de clé secrète SKR ≥ 20 000 bps (objectif ≥ 80 000 bps), tout en maîtrisant le pointage plateforme (≤ 0.005°), "
            "la tenue en polarisation sous vide thermique (≤ 2.6 %) et le retour géographique franco-allemand sous un plafond de 14.50 M€."
        ),
        "primary_objective": (
            "Déployer un satellite QKD en orbite SSO garantissant un taux d'erreur binaire quantique QBER ≤ 2.0 % (objectif ≤ 1.60 %), "
            "un débit asymptotique de clé secrète SKR ≥ 20 000 bps (objectif ≥ 80 000 bps), une précision de pré-pointage plateforme/ADCS "
            "≤ 0.005° (objectif ≤ 0.003°), une qualification PAT-TVAC ≤ 2.6 % (objectif ≤ 2.0 %) et une durée de vie opérationnelle ≥ 5.0 ans "
            "(objectif ≥ 7.0 ans) sous un plafond global de 14.50 M€ TTC."
        ),
        "secondary_objectives": [
            "Comparer les protocoles et architectures de sources quantiques (BB84 à états leurres vs BBM92 à paires de photons intriqués, diamètre du télescope d'émission et cadence de source) vis-à-vis du compromis entre débit de clé secrète (SKR) et taux d'erreur (QBER).",
            "Étudier l'influence de l'altitude orbitale sur l'atténuation géométrique du canal quantique (en dB), sur le taux de comptage des détecteurs à photons uniques au sol et sur le QBER résultant.",
            "Dimensionner la chaîne de pointage et qualifier l'absence de biréfringence thermo-élastique en vide thermique afin de préserver la fidélité des états de polarisation.",
            "Respecter le plafond budgétaire de 14.50 M€ et les contraintes de retour géographique ESA (France 35–70 %, Allemagne 2–45 %)."
        ],
        "scientific_or_operational_need": (
            "Protéger les réseaux diplomatiques et gouvernementaux européens contre la menace des futurs calculateurs quantiques grâce "
            "à la distribution spatiale de clés cryptographiques renouvelées à chaque passage nocturne (SKR ≥ 20 kbps, QBER ≤ 2.0 %)."
        ),
        "orbit_constraints_description": (
            "Orbite héliosynchrone (SSO) autour de 400–550 km avec passage à minuit/midi (22h30–01h30 heure solaire locale) pour maximiser "
            "les passages nocturnes au-dessus de l'Europe (le rayonnement solaire diffusé de jour augmentant le bruit de fond des détecteurs "
            "de photons uniques au sol et dégradant le QBER)."
        ),
        "conops_guidance": (
            "Expliquer le protocole opérationnel QKD en orbite : pré-pointage ADCS puis accrochage fin sur la balise laser de la station sol "
            "quantique (Tenerife, Graz ou Matera), transmission du flux d'impulsions quantiques de nuit, échange concomitant sur le canal "
            "radio classique authentifié (bande S/X) pour la réconciliation des bases (sifting), la correction d'erreurs et l'amplification de confidentialité."
        ),
        "deliverables_expected": [
            "Analyse comparative des terminaux QKD disponibles (protocole, diamètre optique, SKR, QBER, masse et coût) et justification de l'altitude SSO retenue.",
            "Justification de la plateforme, de la suite ADCS et de la chaîne radiofréquence classique associée pour le post-traitement cryptographique.",
            "Validation de la qualification thermique sous vide (stabilité de polarisation et d'alignement PAT) et du retour géographique franco-allemand.",
            "En cas de dépassement budgétaire ou de dérogation sur une exigence pour maximiser le débit de clé secrète, rédaction d'une Demande de Dérogation argumentée à l'Onglet 9."
        ],
        "req_descriptions": {
            "REQ-QKD-QBER-01": "Le taux d'erreur binaire quantique (QBER) sur la liaison espace-sol doit être ≤ 2.0 % (objectif ≤ 1.60 %) afin de garantir la sécurité inconditionnelle de la distillation de clé.",
            "REQ-QKD-SKR-01": "Le débit asymptotique de clé secrète (SKR) après réconciliation et amplification de confidentialité doit être ≥ 20 000 bps (objectif ≥ 80 000 bps).",
            "REQ-POINTING-QKD": "La précision de pré-pointage plateforme/ADCS doit être ≤ 0.005° (objectif ≤ 0.003°) pour permettre l'acquisition rapide de la balise sol par le suivi fin.",
            "REQ-QKD-CALIB": "Le terminal quantique doit être qualifié en vide thermique avec une incertitude ≤ 2.6 % (objectif ≤ 2.0 %) afin de vérifier la stabilité des états de polarisation face aux gradients thermiques.",
            "REQ-QKD-LIFE": "La plateforme doit assurer une durée de vie nominale ≥ 5.0 ans (objectif ≥ 7.0 ans)."
        }
    },

    "exam_cosmology_deep_field.mission.json": {
        "context": (
            "L'étude de l'énergie noire et de la distribution de matière noire par mesure du cisaillement gravitationnel faible (weak lensing) "
            "requiert un télescope spatial à grande ouverture dont la fonction d'étalement du point (PSF) est strictement limitée par la diffraction "
            "et thermiquement ultra-stable. Ce cahier des charges confronte l'architecte à un arbitrage système de classe scientifique : "
            "sélectionner un grand télescope (diamètre primaire ≥ 0.60 m, objectif ≥ 0.70 m ; tache de diffraction projetée ≤ 0.70 m, objectif ≤ 0.58 m), "
            "évaluer l'opportunité d'un couplage spectroscopique proche infrarouge pour la mesure des redshifts, garantir une stabilité de pointage "
            "astrométrique ≤ 0.004° (objectif ≤ 0.001°) et une qualification cryo-vide ≤ 1.0 %, tout en respectant la souscription industrielle "
            "Italie / France / Allemagne sous un plafond de 30.00 M€."
        ),
        "primary_objective": (
            "Concevoir un observatoire spatial équipé d'un télescope de diamètre d'ouverture ≥ 0.60 m (objectif ≥ 0.70 m) présentant une tache "
            "de diffraction projetée de référence ≤ 0.70 m (objectif ≤ 0.58 m), une précision de pointage astrométrique ≤ 0.004° (objectif ≤ 0.001°), "
            "un étalonnage cryo-vide ≤ 1.0 % (objectif ≤ 0.9 %) et une durée de vie scientifique ≥ 7.0 ans (objectif ≥ 10.0 ans) sous un plafond "
            "global de 30.00 M€ TTC."
        ),
        "secondary_objectives": [
            "Arbitrer le dimensionnement du télescope primaire (diamètre de pupille ≥ 0.60 m vs objectif ≥ 0.70 m, architecture du plan focal pour les poses longues « Step-and-Stare ») au regard du plafond budgétaire de 30.00 M€ et de la répartition géographique (Italie 40–65 %, France 25–50 %, Allemagne 4–20 %).",
            "Étudier la faisabilité et la valeur ajoutée scientifique d'une architecture bi-instrumentale couplant le télescope principal, une fente spectrométrique grand champ et un spectromètre VNIR/SWIR pour déterminer les redshifts galactiques.",
            "Sélectionner une plateforme haute stabilité (durée de vie ≥ 7.0 ans) et une suite ADCS ultra-stable permettant de maintenir le flou de bougé bien en deçà de la tache d'Airy durant des poses de plusieurs centaines de secondes.",
            "Justifier le protocole d'étalonnage optique et de front d'onde (WFE/PSF) sous vide cryogénique."
        ],
        "scientific_or_operational_need": (
            "La mesure sans biais de l'ellipticité apparente de centaines de millions de galaxies lointaines exige une optique limitée par la diffraction, "
            "dépourvue de distorsion thermo-élastique (qualifiée en cuve Cryo-TVAC ≤ 1.0 %) et associée à une dérive de pointage inférieure "
            "à une fraction de pixel durant des poses longues de 500 secondes."
        ),
        "orbit_constraints_description": (
            "Orbite héliosynchrone (SSO) crépusculaire (Dawn-Dusk, 06h00 / 18h00) autour de 500–600 km pour éliminer les chocs thermiques "
            "d'entrée/sortie d'éclipse, maximiser la stabilité thermo-élastique passive du banc optique en carbure de silicium (SiC) et viser "
            "les champs profonds à l'opposé du Soleil et de la Terre."
        ),
        "conops_guidance": (
            "Détailler la séquence d'observation cosmologique (« Step-and-Stare ») : ralliement vers un champ extragalactique profond hors du plan "
            "galactique, amortissement des micro-vibrations avant ouverture de l'obturateur, pose longue stabilisée de 500 s sur matrice focale, "
            "calibration périodique de la PSF sur champs stellaires de référence, compression sans perte et vidage quotidien vers Cebreros et Kiruna."
        ),
        "deliverables_expected": [
            "Analyse comparative des grands télescopes et des plateformes de classe moyenne/lourde disponibles vis-à-vis de la limite de diffraction, de la stabilité de pointage, de la durée de vie (≥ 7.0 ans) et des quotas ESA (Italie, France, Allemagne).",
            "Évaluation technique et budgétaire de l'option de couplage spectroscopique (ajout d'une fente et d'un spectromètre proche infrarouge).",
            "Justification de la chaîne ADCS ultra-stable et de la campagne d'essais sous vide cryogénique (≤ 1.0 %).",
            "En cas de choix privilégiant l'objectif d'ouverture ≥ 0.70 m au détriment du plafond budgétaire ou des quotas industriels, rédaction d'une Demande de Dérogation argumentée à l'Onglet 9."
        ],
        "req_descriptions": {
            "REQ-COSMO-APERTURE": "Le diamètre de la pupille d'entrée du télescope doit être ≥ 0.60 m (objectif ≥ 0.70 m) pour maximiser la collecte de photons des galaxies à haut redshift.",
            "REQ-COSMO-DIFF": "La tache de diffraction optique projetée de référence doit être ≤ 0.70 m (objectif ≤ 0.58 m) afin de garantir la finesse angulaire de la PSF.",
            "REQ-COSMO-POINTING": "La précision de pointage 3 axes doit être ≤ 0.004° (objectif ≤ 0.001°) avec un jitter et une dérive minimaux durant les poses longues.",
            "REQ-COSMO-CALIB": "L'incertitude d'étalonnage radiométrique et de qualité d'onde (WFE/PSF) sous vide cryogénique doit être ≤ 1.0 % (objectif ≤ 0.9 %).",
            "REQ-COSMO-LIFE": "La plateforme doit assurer une durée de vie nominale ≥ 7.0 ans (objectif ≥ 10.0 ans) pour couvrir l'intégralité du relevé extragalactique."
        }
    },

    "exam_cubesat_maritime_iot.mission.json": {
        "context": (
            "Un opérateur européen de services maritimes souhaite lancer un démonstrateur nanosatellite (classe CubeSat) en orbite basse "
            "héliosynchrone pour collecter les balises AIS des navires, les messages ADS-B aéronautiques et les capteurs IoT déportés en haute mer. "
            "Le défi d'ingénierie réside dans l'extrême sévérité de l'enveloppe SWaP-C (Size, Weight, Power and Cost) : sous un plafond strict "
            "de 1.95 M€ tout compris (satellite, options, étalonnage sol et lancement), l'architecte doit concevoir un système assurant un débit "
            "descendant ≥ 15.0 Mbps (objectif ≥ 35.0 Mbps), une marge de liaison RF ≥ 10.0 dB (objectif ≥ 14.0 dB), un pointage ≤ 0.10° "
            "(objectif ≤ 0.05°), une qualification RF en vide thermique ≤ 2.5 % et une durée de vie ≥ 2.5 ans (objectif ≥ 3.0 ans)."
        ),
        "primary_objective": (
            "Concevoir un nanosatellite de collecte RF en orbite SSO capable d'assurer un débit descendant de collecte ≥ 15.0 Mbps "
            "(objectif ≥ 35.0 Mbps) avec une marge du bilan de liaison RF ≥ 10.0 dB (objectif ≥ 14.0 dB), une précision de pointage CubeSat "
            "≤ 0.10° (objectif ≤ 0.05°), une qualification RF en vide thermique ≤ 2.5 % (objectif ≤ 2.2 %) et une durée de vie nominale "
            "≥ 2.5 ans (objectif ≥ 3.0 ans) pour un coût total ≤ 1.95 M€ TTC."
        ),
        "secondary_objectives": [
            "Comparer les différentes plateformes nanosatellites du catalogue (formats 3U, 6U, 12U standard ou haute puissance) vis-à-vis de la masse utile admissible, de la puissance électrique disponible en orbite, de la durée de vie nominale et du coût.",
            "Analyser le compromis entre les différentes charges utiles de collecte RF / IoT (débit de données, masse, consommation électrique et prix) et évaluer la faisabilité d'embarquer un micro-imageur optique secondaire à capteur matriciel pour la levée de doute visuelle sur les navires non-coopératifs.",
            "Vérifier l'équilibre du bilan énergétique du nanosatellite (génération solaire vs consommation moyenne de la charge utile et des équipements TT&C / ADCS) en tenant compte de la marge système recommandée.",
            "Intégrer une qualification radiofréquence en vide thermique (≤ 2.5 %) tout en respectant l'enveloppe globale de 1.95 M€."
        ],
        "scientific_or_operational_need": (
            "Assurer le suivi quasi-temps réel des flottes marchandes et des bouées océanographiques dans les zones blanches océaniques "
            "et arctiques (débit ≥ 15.0 Mbps, marge RF ≥ 10.0 dB), avec capacité optionnelle de vérification optique sur alerte AIS."
        ),
        "orbit_constraints_description": (
            "Orbite héliosynchrone (SSO) autour de 500–550 km d'altitude, injectable à bas coût via un service de lancement partagé "
            "en déployeur CubeSat standardisé."
        ),
        "conops_guidance": (
            "Préciser la gestion de l'énergie à bord du nanosatellite : écoute AIS/ADS-B/IoT continue à faible consommation au-dessus des "
            "bassins océaniques, déclenchement ponctuel d'une éventuelle prise de vue secondaire uniquement sur alerte diurne, stockage "
            "sur mémoire flash embarquée et vidage rapide en bande S sur les stations de Redu et Kiruna."
        ),
        "deliverables_expected": [
            "Comparaison chiffrée des architectures nanosatellites candidates (choix du format de bus CubeSat, de la charge utile RF et opportunité d'une charge utile secondaire) au regard du plafond de 1.95 M€.",
            "Analyse détaillée des marges de masse, de volume et surtout de puissance électrique moyenne en orbite.",
            "Validation du bilan de liaison RF descendant (≥ 10.0 dB) et justification de la campagne de qualification RF sous vide thermique.",
            "En cas de choix privilégiant l'objectif étendu de débit (≥ 35.0 Mbps) ou une plateforme plus lourde dépassant le budget, rédaction d'une Demande de Dérogation argumentée à l'Onglet 9."
        ],
        "req_descriptions": {
            "REQ-CUBE-RATE": "Le débit maximal de la charge utile RF de collecte doit être ≥ 15.0 Mbps (objectif ≥ 35.0 Mbps).",
            "REQ-CUBE-MARGIN": "La marge du bilan de liaison RF descendant doit être ≥ 10.0 dB (objectif ≥ 14.0 dB) pour garantir la robustesse des téléchargements à faible angle d'élévation.",
            "REQ-CUBE-POINT": "La précision de pointage 3 axes doit être ≤ 0.10° (objectif ≤ 0.05°) pour orienter les antennes directives et permettre une éventuelle prise de vue secondaire.",
            "REQ-CUBE-CALIB": "La charge utile RF doit subir une qualification en vide thermique certifiant une précision radiométrique/RF ≤ 2.5 % (objectif ≤ 2.2 %).",
            "REQ-CUBE-LIFE": "La plateforme nanosatellite doit présenter une durée de vie nominale ≥ 2.5 ans (objectif ≥ 3.0 ans)."
        }
    },

    "exam_geo_telecom_classical.mission.json": {
        "context": (
            "Pour assurer une couverture permanente 24h/24 de l'Europe, de la Méditerranée et de l'Afrique subsaharienne, un opérateur "
            "institutionnel et commercial souhaite déployer un satellite de télécommunications en orbite géostationnaire (GEO, altitude 35 786 km, "
            "inclinaison 0°). À cette distance, l'affaiblissement d'espace libre dépasse 205 dB, imposant des charges utiles à forte PIRE "
            "et des plateformes qualifiées pour 15 ans dans l'environnement radiatif sévère de la ceinture externe. L'architecte doit "
            "arbitrer entre la capacité de débit du répéteur (seuil ≥ 700 Mbps, objectif ≥ 1 500 Mbps), la classe de plateforme GEO et "
            "le mode de lancement (créneau partagé GTO vs lanceur lourd dédié), tout en respectant les quotas de retour géographique "
            "France / Suisse / Allemagne sous un plafond global de 46.00 M€."
        ),
        "primary_objective": (
            "Concevoir un satellite de télécommunications en orbite géostationnaire (GEO, 35 786 km) délivrant une capacité de débit total "
            "≥ 700.0 Mbps (objectif ≥ 1 500.0 Mbps) avec une marge de liaison descendante ≥ 8.0 dB (objectif ≥ 11.0 dB), une précision de pointage "
            "des faisceaux ≤ 0.01° (objectif ≤ 0.004°), une qualification RF en vide thermique ≤ 2.5 % (objectif ≤ 2.0 %) et une durée de vie "
            "opérationnelle ≥ 15.0 ans sous un plafond global de 46.00 M€ TTC."
        ),
        "secondary_objectives": [
            "Configurer l'orbite Géostationnaire (35 786 km, inclinaison 0°) et analyser le bilan de liaison descendant en bande Ku/Ka face aux pertes d'espace libre (> 205 dB) et à l'affaiblissement atmosphérique.",
            "Comparer les architectures de plateformes géostationnaires compactes (classe SmallGEO compatible lancement partagé GTO ≤ 1 400 kg) et lourdes (classe VHTS nécessitant un lanceur dédié) en termes de puissance électrique disponible, de masse injectable et de coût global.",
            "Arbitrer la stratégie de propulsion pour le transfert GTO → GEO et le maintien à poste Nord-Sud / Est-Ouest sur 15 ans (propulsion chimique bi-ergol 400 N à mise à poste rapide vs propulsion électrique à effet Hall / ionique à forte impulsion spécifique).",
            "Garantir la qualification RF haute puissance sous vide thermique (effets Multipactor et intermodulation passive PIM) et le respect des quotas industriels (France 45–75 %, Suisse 20–40 %, Allemagne 3–18 %)."
        ],
        "scientific_or_operational_need": (
            "Fournir une capacité souveraine de télédiffusion, d'interconnexion de réseaux gouvernementaux et de désenclavement numérique "
            "à haute disponibilité (≥ 99.9 %, marge pluie ≥ 8.0 dB) pendant 15 ans sur toute la zone Europe-Méditerranée-Afrique depuis la position 13° Est."
        ),
        "orbit_constraints_description": (
            "Orbite Géostationnaire équatoriale stricte (altitude = 35 786 km, inclinaison = 0.0°, période = 24h00). L'architecte devra "
            "vérifier la compatibilité de la masse totale au lancement avec l'option de lanceur GTO retenue."
        ),
        "conops_guidance": (
            "Détailler la phase de mise à poste depuis l'orbite de transfert géostationnaire (manœuvres d'apogée impulsives ou remontée "
            "d'orbite électrique EOR sur plusieurs mois), le maintien dans la fenêtre de stationnement ±0.05° pendant 15 ans, la gestion "
            "thermique et énergétique lors des éclipses d'équinoxe, et le télécontrôle depuis Redu et Fucino."
        ),
        "deliverables_expected": [
            "Justification du bilan de liaison GEO à 35 786 km (PIRE, pertes de propagation, marge ≥ 8.0 dB) et du choix du répéteur télécom.",
            "Analyse comparative des plateformes GEO et des options de lancement vis-à-vis de la masse humide, du bilan électrique, du plafond de 46.00 M€ et de la souscription franco-germano-suisse.",
            "Justification du sous-système de propulsion (chimique vs électrique) et de la campagne d'essais RF-TVAC (Multipactor / PIM).",
            "En cas de choix privilégiant l'objectif étendu de capacité (≥ 1 500 Mbps) au prix d'un dépassement budgétaire ou d'un écart sur les quotas géographiques, rédaction d'une Demande de Dérogation argumentée à l'Onglet 9."
        ],
        "req_descriptions": {
            "REQ-GEO-RATE": "La capacité de débit agrégé de la charge utile télécom GEO doit être ≥ 700.0 Mbps (objectif ≥ 1 500.0 Mbps).",
            "REQ-GEO-MARGIN": "La marge du bilan de liaison descendant depuis 35 786 km doit être ≥ 8.0 dB (objectif ≥ 11.0 dB) pour compenser l'affaiblissement de pluie en bande Ku/Ka.",
            "REQ-GEO-POINT": "La précision de maintien d'attitude 3 axes doit être ≤ 0.01° (objectif ≤ 0.004°) afin de stabiliser l'empreinte au sol des faisceaux.",
            "REQ-GEO-CALIB": "Le répéteur doit être qualifié en vide thermique avec une incertitude ≤ 2.5 % (objectif ≤ 2.0 %) incluant les essais de tenue Multipactor et d'intermodulation passive (PIM).",
            "REQ-GEO-LIFE": "La plateforme doit être certifiée pour ≥ 15.0 ans de service continu en environnement radiatif géostationnaire."
        }
    }
}


def apply_updates() -> None:
    for filename, upd in MISSIONS_UPDATES.items():
        fpath = MISSIONS_DIR / filename
        data = json.loads(fpath.read_text(encoding="utf-8"))
        data["context"] = upd["context"]
        data["primary_objective"] = upd["primary_objective"]
        data["secondary_objectives"] = upd["secondary_objectives"]
        data["scientific_or_operational_need"] = upd["scientific_or_operational_need"]
        data["orbit_constraints_description"] = upd["orbit_constraints_description"]
        data["conops_guidance"] = upd["conops_guidance"]
        data["deliverables_expected"] = upd["deliverables_expected"]

        req_map = upd["req_descriptions"]
        for req in data.get("requirements", []):
            rid = req["id"]
            if rid in req_map:
                req["description"] = req_map[rid]

        fpath.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Updated mission sheet: {filename}")


if __name__ == "__main__":
    apply_updates()
