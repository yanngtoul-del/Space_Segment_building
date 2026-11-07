"""Equipment catalog source: overlays for existing items + new items."""

from common import base

IMG_PROP_E = "equip_propulsion_electric.jpg"
IMG_PROP_C = "equip_propulsion_chemical.jpg"
IMG_PROP_M = "equip_propulsion_micro.jpg"
IMG_ELEC = "equip_electronics.jpg"
IMG_ADCS = "equip_adcs.jpg"

# ---------------------------------------------------------------- overlays (existing items)
OVERLAY = {
    "prop_coldgas_10u": dict(
        image=IMG_PROP_M, dimensions_mm=(200, 100, 100),
        long_description="Système de propulsion à gaz froid miniaturisé utilisant du R236fa liquide stocké sous faible pression et détendu dans des micro-tuyères. Il fournit de petites impulsions précises pour les corrections d'orbite, le maintien de formation et la désorbitation des nanosatellites. Faible poussée, très faible consommation et aucune contamination : idéal quand la charge utile est sensible.",
        key_features=["Propergol R236fa non toxique", "Poussée 25 mN, Isp 65 s", "Aucun risque de contamination optique", "Tank intégré au châssis 1U-2U"],
        interfaces=["Alimentation 5 V / 12 V", "Commande par RS-422 / CAN", "Interface mécanique CubeSat 10U"]),
    "prop_electric_hall_100w": dict(
        image=IMG_PROP_E, dimensions_mm=(250, 180, 120),
        long_description="Propulseur à effet Hall de 100 W, doté d'une unité de conditionnement de puissance (PPU) intégrée et d'un réservoir de xénon. Il permet la remontée d'orbite, le maintien d'altitude et la désorbitation active en fin de vie de satellites de 50 à 200 kg. L'impulsion spécifique élevée réduit fortement la masse de propergol par rapport à la propulsion chimique, au prix d'une poussée faible (manœuvres lentes).",
        key_features=["Isp 1400 s, poussée 8 mN", "PPU intégrée, xénon 4 kg", "Allumage < 30 s", "Durée de vie > 4000 h"],
        interfaces=["Bus 28 V / 100 V", "Commande CAN / SpaceWire", "Interface de fixation 4 x M6"]),
    "prop_electric_hall_1kw": dict(
        image=IMG_PROP_E, dimensions_mm=(420, 330, 260),
        long_description="Module de propulsion électrique de forte puissance (1 kW) à base de krypton ou de xénon, pour satellites de classe 500 kg et au-delà. Il assure la montée en orbite complète depuis une orbite basse d'injection, le maintien de constellation et la désorbitation contrôlée. Sa consommation importante doit être couverte par les panneaux solaires de la plateforme.",
        key_features=["Isp 1850 s, poussée 65 mN", "Krypton ou xénon, 25 kg de propergol", "Poussée dirigeable (gimbal)", "Qualifié 15 000 h"],
        interfaces=["Bus 100 V régulé", "Commande SpaceWire / MIL-1553", "Interface mécanique sur poussée centrale"]),
    "prop_monoprop_1n": dict(
        image=IMG_PROP_C, dimensions_mm=(300, 300, 260),
        long_description="Module monergol à l'hydrazine avec réservoir à diaphragme et propulseur catalytique de 1 N. Technologie éprouvée depuis des décennies, offrant une réponse immédiate et une grande fiabilité pour les manœuvres d'évitement, les changements d'altitude et la désorbitation en fin de vie. Impulsion spécifique modérée mais poussée instantanée sans phase de chauffe longue.",
        key_features=["Poussée 1 N, Isp 225 s", "10 kg d'hydrazine", "Héritage > 500 satellites", "Réponse immédiate"],
        interfaces=["Alimentation 28 V", "Commande MIL-1553 / CAN", "Vannes de remplissage au sol (sécurité pyrotechnique)"]),
    "prop_biprop_400n": dict(
        image=IMG_PROP_C, dimensions_mm=(550, 450, 420),
        long_description="Moteur apogée biergol MMH/NTO de 400 N pour injection en orbite, relèvement d'apogée et désorbitation rapide de satellites de plus de 500 kg. C'est la solution à forte poussée de la gamme : les manœuvres sont courtes, mais la masse totale et le coût sont élevés et la manipulation du propergol toxique impose des contraintes au sol.",
        key_features=["Poussée 400 N, Isp 320 s", "120 kg de propergol MMH/NTO", "Manœuvres d'orbite en quelques minutes", "Héritage GEO et LEO lourd"],
        interfaces=["Alimentation 28 V", "Commande MIL-1553", "Interface lourde sur cône de lanceur"]),
    "ttc_sband_transceiver": dict(
        image=IMG_ELEC, dimensions_mm=(110, 95, 40),
        long_description="Transpondeur TT&C en bande S, full duplex, conforme aux standards CCSDS et ECSS. Il assure la télémesure, la télécommande et la mesure de distance du satellite depuis une station sol. Sa sensibilité et sa fiabilité en font l'équipement de contrôle incontournable de la quasi-totalité des plateformes.",
        key_features=["S-band 2,2 / 2,0 GHz", "Débit descendant 1 Mbit/s", "Conforme CCSDS", "Diplexeur et antenne patch intégrés"],
        interfaces=["Alimentation 12 V", "Interface OBC CAN / UART", "Connecteur SMA"]),
    "downlink_xband_tx": dict(
        image=IMG_ELEC, dimensions_mm=(180, 120, 60),
        long_description="Émetteur de charge utile en bande X à modulation DVB-S2X, capable de 500 Mbit/s vers une station sol à 8 GHz. C'est la solution standard pour le transfert des images d'observation de la Terre, avec une très bonne disponibilité des stations commerciales en bande X.",
        key_features=["Jusqu'à 500 Mbit/s (DVB-S2X)", "RF 10 W, 8,2 GHz", "Antenne cornet fournie", "Chiffrement des données en option"],
        interfaces=["Alimentation 28 V", "Données SpaceWire / SpaceFibre / LVDS", "Sortie RF guide d'onde WR-112"]),
    "downlink_kaband_tx_2gbps": dict(
        image=IMG_ELEC, dimensions_mm=(250, 180, 100),
        long_description="Émetteur très haut débit en bande Ka (26 GHz) avec antenne cornet orientable, pour les charges utiles à forte production de données comme le SAR ou l'hyperspectral. Il atteint 2 Gbit/s mais requiert des stations sol dédiées et subit l'atténuation atmosphérique (pluie).",
        key_features=["Jusqu'à 2 Gbit/s", "Ka-band 26,5 GHz, RF 20 W", "Antenne orientable 2 axes", "Modulation adaptative"],
        interfaces=["Alimentation 28 V", "Données SpaceFibre 6,25 Gbit/s", "Mécanisme d'antenne SpaceWire"]),
    "mass_mem_512gb": dict(
        image=IMG_ELEC, dimensions_mm=(120, 100, 50),
        long_description="Mémoire de masse NAND flash tolérante aux radiations avec codes correcteurs d'erreurs (EDAC) et interfaces haut débit. Elle tamponne les images acquises avant leur transfert vers le sol pendant les passages sur station. La capacité en fin de vie est inférieure à la capacité nominale en raison de la dégradation des cellules.",
        key_features=["512 Go début de vie, 460 Go fin de vie", "Écriture 1,6 Gbit/s", "EDAC et gestion des blocs défectueux", "Conception tolérante aux SEU"],
        interfaces=["SpaceWire / SpaceFibre", "Alimentation 28 V", "Télémesure CAN"]),
    "mass_mem_2tb_highrel": dict(
        image=IMG_ELEC, dimensions_mm=(200, 160, 80),
        long_description="Enregistreur à état solide de 2 To de classe entreprise, durci pour la tenue aux radiations. Il est conçu pour les missions de constellation, SAR et hyperspectrales qui accumulent de très gros volumes de données entre deux passages sol.",
        key_features=["2 To début de vie, 1,85 To fin de vie", "Écriture 4 Gbit/s", "Redondance interne", "TRL 9"],
        interfaces=["SpaceFibre 4 x 6,25 Gbit/s", "Alimentation 28 V", "Télémesure MIL-1553"]),
    "adcs_high_accuracy_pack": dict(
        image=IMG_ADCS, dimensions_mm=(260, 220, 180),
        long_description="Suite de contrôle d'attitude de précision : deux viseurs d'étoiles pour la mesure absolue et quatre roues à réaction pour l'actionnement fin. Elle fait passer la précision de pointage sous 0,01° et la stabilité sous 1 arcsec/s, ce qui est indispensable pour les télescopes sub-métriques.",
        key_features=["Précision 0,005°", "Stabilité 0,5 arcsec/s", "Double viseur d'étoiles", "4 roues, 1,5 N·m·s"],
        interfaces=["Alimentation 28 V", "Bus CAN / SpaceWire", "Montage rigide sur plateau structurel"]),
    "adcs_cmg_agility_pack": dict(
        image=IMG_ADCS, dimensions_mm=(420, 380, 300),
        long_description="Suite de quatre gyroscopes de contrôle (CMG) en pyramide. Elle offre une agilité exceptionnelle (plus de 5°/s) pour imager de nombreuses cibles par passage, ou suivre un objectif en mouvement. Sa masse et sa consommation sont élevées, et les CMG génèrent des micro-vibrations à prendre en compte pour la stabilité.",
        key_features=["Agilité 6,5°/s", "Précision 0,003°", "4 CMG en pyramide", "Imagerie multi-cibles et stéréo"],
        interfaces=["Alimentation 28 V (pic 180 W)", "Commande SpaceWire", "Montage sur plateforme dédiée"]),
}

# ---------------------------------------------------------------- new items


def eq(item_id, sup, fn, name, mass, power, price, vol, dims, desc, long, feats, ifaces, image, specs,
       trl=9, peak=None, standby=None, heritage=""):
    return base(
        item_id, sup, name=name, function=fn, description=desc, mass_kg=mass, power_w=power,
        peak_power_w=peak if peak is not None else round(power * 1.3, 2),
        standby_power_w=standby if standby is not None else round(power * 0.1, 2),
        volume_liters=vol, dimensions_mm=dims, price_meur=price, trl=trl, flight_heritage=heritage,
        image=image, long_description=long, key_features=feats, interfaces=ifaces, specs=specs,
    )


NEW = [
    # ---- propulsion
    eq("prop_coldgas_1u", "newspace_micro", "propulsion", "CG-1U Cold Gas Thruster Module", 0.6, 1.0, 0.06, 0.5,
       (100, 100, 50), "Module gaz froid 1U pour CubeSats",
       "Module de propulsion gaz froid de format 1U destiné aux CubeSats 6U à 12U. Il délivre de petites impulsions pour la désaturation des roues, les corrections de phasage et une désorbitation lente. Sa simplicité et son absence de composants toxiques en font la solution de propulsion la plus économique du catalogue.",
       ["Format 1U", "Poussée 10 mN, Isp 60 s", "Sans entretien, non toxique", "Qualifié pour lancement en dispenser"],
       ["Alimentation 5 V", "Commande I2C / UART", "Interface CubeSat PC104"], IMG_PROP_M,
       {"isp_s": 60.0, "propellant_mass_kg": 0.12, "thrust_mn": 10.0}, standby=0.1, heritage="12 vols"),
    eq("prop_pptt_micro", "newspace_micro", "propulsion", "PPT-μ Pulsed Plasma Thruster", 1.4, 15.0, 0.22, 1.0,
       (100, 100, 100), "Propulseur plasma pulsé à propergol solide",
       "Propulseur à plasma pulsé utilisant un barreau de PTFE comme propergol solide. Les impulsions successives délivrent une poussée très faible mais une impulsion spécifique très élevée, avec un système sans réservoir sous pression. Adapté aux corrections fines d'orbite et au contrôle d'attitude de CubeSats et de microsatellites.",
       ["Isp 600 s, poussée 0,5 mN", "Propergol solide sans pression", "Pas de risque de fuite", "Précision de manœuvre élevée"],
       ["Alimentation 12 V", "Commande CAN", "Format 1U"], IMG_PROP_M,
       {"isp_s": 600.0, "propellant_mass_kg": 0.3, "thrust_mn": 0.5}, trl=8, standby=0.2),
    eq("prop_electric_hall_300w", "orbital_prop", "propulsion", "HET-300 Hall Effect Thruster", 11.0, 320.0, 0.85, 8.0,
       (320, 220, 180), "Propulseur Hall 300 W pour microsatellites",
       "Propulseur à effet Hall de 300 W pour microsatellites de 100 à 400 kg. Son compromis poussée/consommation en fait le choix usuel pour la remontée d'orbite après un lancement partagé et le maintien d'altitude en orbite basse. Il nécessite une puissance électrique conséquente, à comparer à celle de la plateforme.",
       ["Isp 1600 s, poussée 17 mN", "PPU et régulateur de débit inclus", "Xénon 8 kg", "Cathode creuse intégrée"],
       ["Bus 28 V / 70 V", "Commande CAN / SpaceWire", "Alimentation PPU dédiée"], IMG_PROP_E,
       {"isp_s": 1600.0, "propellant_mass_kg": 8.0, "thrust_mn": 17.0}, trl=9, standby=3.0, heritage="40 vols"),
    eq("prop_ion_500w", "orbital_prop", "propulsion", "GIT-500 Gridded Ion Thruster", 15.0, 520.0, 1.3, 11.0,
       (360, 260, 200), "Propulseur ionique à grille 500 W",
       "Propulseur ionique à grille offrant la plus haute impulsion spécifique du catalogue. Sa poussée est faible, ce qui impose de longues phases de propulsion, mais la masse de propergol est minimale : intéressant pour les missions à fort delta-V (montée en altitude, changement de plan, désorbitation précise).",
       ["Isp 2800 s, poussée 20 mN", "Rendement > 60 %", "Xénon 14 kg", "Durée de vie > 20 000 h"],
       ["Bus 100 V", "Commande SpaceWire", "Gimbal optionnel"], IMG_PROP_E,
       {"isp_s": 2800.0, "propellant_mass_kg": 14.0, "thrust_mn": 20.0}, trl=8, standby=6.0),
    eq("prop_green_5n", "heritage_aero", "propulsion", "GreenProp-5N Green Monopropellant", 4.5, 20.0, 0.7, 6.0,
       (250, 220, 200), "Monergol vert 5 N (type LMP-103S)",
       "Module de propulsion à ergol « vert » ADN (type LMP-103S), moins toxique que l'hydrazine et à meilleure impulsion volumique. Il remplace avantageusement la propulsion monergol classique pour les microsatellites, avec un manipulation au sol simplifiée et des performances supérieures de 6 %.",
       ["Poussée 5 N, Isp 235 s", "Ergol peu toxique", "Chauffage du catalyseur requis (10 min)", "Héritage PRISMA et SkySat"],
       ["Alimentation 28 V", "Commande CAN", "Interface mécanique 4 x M6"], IMG_PROP_C,
       {"isp_s": 235.0, "propellant_mass_kg": 6.0, "thrust_mn": 5000.0}, standby=4.0, heritage="25 vols"),
    # ---- TT&C
    eq("ttc_uhf_cubesat", "newspace_micro", "ttc", "UHF/VHF CubeSat Transceiver", 0.15, 2.0, 0.03, 0.15,
       (96, 90, 15), "Transpondeur UHF/VHF pour CubeSats",
       "Transpondeur radioamateur/UHF léger pour le contrôle de nanosatellites. Faible débit, mais très économique et compatible avec des stations sol bon marché. Convient aux missions de démonstration qui n'exigent pas de forte disponibilité.",
       ["Bande 437 MHz", "Débit 9,6 kbit/s", "Masse 150 g", "Compatible stations radioamateurs"],
       ["Alimentation 5 V", "Commande UART", "Antenne dipôle déployable"], IMG_ELEC,
       {"tx_rf_power_w": 1.0, "downlink_rate_kbps": 9.6, "uplink_rate_kbps": 9.6}, standby=0.4, heritage="80 vols"),
    eq("ttc_xband_tmtc", "comms_euro", "ttc", "X-Band TT&C Transponder", 2.4, 20.0, 0.45, 1.6,
       (160, 110, 50), "Transpondeur TT&C bande X",
       "Transpondeur TT&C en bande X permettant de réutiliser les mêmes stations que la liaison de charge utile et d'obtenir un meilleur débit de télémesure. Il mesure aussi la distance avec une grande précision, utile pour la détermination d'orbite.",
       ["Bande X 7,2 / 8,4 GHz", "Débit descendant 2 Mbit/s", "Ranging ESA/NASA", "Bonne résilience aux interférences"],
       ["Alimentation 28 V", "Commande MIL-1553 / CAN", "Sortie RF guide d'onde"], IMG_ELEC,
       {"tx_rf_power_w": 5.0, "downlink_rate_kbps": 2000.0, "uplink_rate_kbps": 256.0}, standby=3.0, heritage="60 vols"),
    eq("ttc_sband_dual_redundant", "comms_euro", "ttc", "S-Band Dual Redundant TT&C Unit", 2.6, 20.0, 0.38, 1.8,
       (170, 120, 55), "Transpondeur S-band en redondance chaude",
       "Ensemble TT&C en bande S avec deux chaînes complètes en redondance, pour les satellites institutionnels et les missions critiques. Aucune panne simple ne peut priver le sol du contrôle du satellite.",
       ["Redondance chaude 2 x 2 W", "Débit 2 Mbit/s", "Conforme ECSS/CCSDS", "Mode sécurisé (chiffrement)"],
       ["Alimentation 28 V", "MIL-1553", "Deux sorties RF + hybride"], IMG_ELEC,
       {"tx_rf_power_w": 4.0, "downlink_rate_kbps": 2000.0, "uplink_rate_kbps": 256.0}, standby=4.0, heritage="120 vols"),
    # ---- Payload downlinks
    eq("downlink_sband_hr", "newspace_micro", "payload_downlink", "S-Band High-Rate Transmitter 20 Mbps", 0.4, 8.0, 0.08, 0.4,
       (95, 90, 25), "Émetteur S-band 20 Mbit/s",
       "Émetteur de charge utile en bande S pour CubeSats, permettant d'atteindre 20 Mbit/s avec une petite antenne patch. Convient aux faibles volumes de données comme les images compressées ou les mesures de capteurs.",
       ["20 Mbit/s en bande S", "RF 2 W", "Antenne patch intégrée", "Masse 400 g"],
       ["Alimentation 5-12 V", "Données LVDS / SPI", "Sortie SMA"], IMG_ELEC,
       {"rf_frequency_ghz": 2.25, "rf_power_w": 2.0, "max_data_rate_mbps": 20.0}, standby=0.4),
    eq("downlink_xband_tx_50mbps", "newspace_micro", "payload_downlink", "X-Band CubeSat Transmitter 50 Mbps", 0.7, 12.0, 0.12, 0.6,
       (95, 90, 45), "Émetteur X-band 50 Mbit/s pour CubeSats",
       "Émetteur bande X de format CubeSat à 50 Mbit/s, avec antenne patch réseau. Compromis entre débit et simplicité pour les CubeSats d'imagerie.",
       ["50 Mbit/s en bande X", "RF 3 W", "Modulation QPSK/8PSK", "Antenne patch 8 dBi"],
       ["Alimentation 12 V", "LVDS / SpaceWire", "Sortie SMA"], IMG_ELEC,
       {"rf_frequency_ghz": 8.2, "rf_power_w": 3.0, "max_data_rate_mbps": 50.0}, standby=0.6, heritage="30 vols"),
    eq("downlink_xband_tx_150mbps", "comms_euro", "payload_downlink", "X-Band Transmitter 150 Mbps", 1.1, 18.0, 0.2, 1.0,
       (130, 100, 55), "Émetteur X-band 150 Mbit/s",
       "Émetteur bande X de 150 Mbit/s adapté aux microsatellites d'observation de la Terre. Solution intermédiaire entre le CubeSat et la classe 500 Mbit/s.",
       ["150 Mbit/s en bande X", "RF 5 W", "DVB-S2", "Antenne cornet 14 dBi"],
       ["Alimentation 28 V", "SpaceWire / LVDS", "Guide d'onde WR-112"], IMG_ELEC,
       {"rf_frequency_ghz": 8.2, "rf_power_w": 5.0, "max_data_rate_mbps": 150.0}, standby=1.2, heritage="45 vols"),
    eq("downlink_xband_tx_1200mbps", "comms_euro", "payload_downlink", "X-Band Wideband Transmitter 1.2 Gbps", 4.2, 55.0, 0.6, 3.2,
       (220, 160, 90), "Émetteur X-band 1,2 Gbit/s large bande",
       "Émetteur de la dernière génération en bande X (2 canaux de 375 MHz) délivrant jusqu'à 1,2 Gbit/s. Plus économe en stations sol que la bande Ka et moins sensible aux conditions météo, mais avec des exigences de coordination de fréquence.",
       ["1,2 Gbit/s (2 canaux polarisés)", "RF 15 W", "DVB-S2X, 16APSK/32APSK", "Antenne orientable en option"],
       ["Alimentation 28 V", "SpaceFibre", "Guide d'onde WR-112"], IMG_ELEC,
       {"rf_frequency_ghz": 8.2, "rf_power_w": 15.0, "max_data_rate_mbps": 1200.0}, standby=3.0, heritage="12 vols"),
    # ---- Mass memory
    eq("mass_mem_64gb", "newspace_micro", "mass_memory", "Flash Memory Module 64 GB", 0.05, 1.5, 0.03, 0.05,
       (90, 90, 10), "Mémoire flash 64 Go pour CubeSats",
       "Module mémoire flash COTS de 64 Go avec contrôle d'erreurs logiciel. Capacité suffisante pour quelques centaines d'images ou plusieurs heures de télémesure.",
       ["64 Go début de vie", "Format PC104", "EDAC logiciel", "Masse 50 g"],
       ["SPI / SATA", "Alimentation 5 V"], IMG_ELEC,
       {"capacity_bol_gb": 64.0, "capacity_eol_gb": 56.0, "write_speed_mbps": 400.0, "read_speed_mbps": 300.0}, standby=0.2),
    eq("mass_mem_1tb", "space_avionics", "mass_memory", "Solid State Recorder 1 TB", 1.4, 8.0, 0.26, 1.0,
       (160, 130, 50), "Enregistreur à état solide 1 To",
       "Enregistreur à état solide de 1 To pour microsatellites d'observation. Écriture rapide et interfaces SpaceFibre, avec un excellent compromis capacité/coût/masse pour les missions optiques à haute résolution.",
       ["1 To début de vie, 920 Go fin de vie", "Écriture 2,5 Gbit/s", "EDAC matériel", "Redondance partielle"],
       ["SpaceFibre", "Alimentation 28 V"], IMG_ELEC,
       {"capacity_bol_gb": 1024.0, "capacity_eol_gb": 920.0, "write_speed_mbps": 2500.0, "read_speed_mbps": 1600.0}, standby=1.5),
    eq("mass_mem_8tb", "space_avionics", "mass_memory", "High-Capacity Recorder 8 TB", 4.8, 28.0, 0.95, 3.8,
       (230, 190, 100), "Enregistreur très grande capacité 8 To",
       "Enregistreur de très grande capacité pour les missions SAR haute résolution et hyperspectrales qui produisent des volumes énormes entre deux passages sol. Conçu avec une redondance complète et une protection des données contre les radiations.",
       ["8 To début de vie, 7,3 To fin de vie", "Écriture 8 Gbit/s", "Redondance complète", "Chiffrement intégré"],
       ["SpaceFibre 8 x 6,25 Gbit/s", "Alimentation 28 V"], IMG_ELEC,
       {"capacity_bol_gb": 8192.0, "capacity_eol_gb": 7300.0, "write_speed_mbps": 8000.0, "read_speed_mbps": 6000.0}, standby=4.0),
    # ---- ADCS
    eq("adcs_cubesat_basic", "newspace_micro", "adcs", "CubeADCS Basic (Magnetorquers + Sun Sensors)", 0.4, 1.2, 0.05, 0.3,
       (90, 90, 25), "ADCS de base pour CubeSats",
       "Ensemble de base comportant trois magnétocoupleurs, des capteurs solaires et un magnétomètre. Il permet une stabilisation grossière et le détumbling, mais pas de pointage précis. Suffisant pour des charges utiles non imageuses.",
       ["Précision 1°", "Magnétocoupleurs 3 axes", "Capteurs solaires 6 faces", "Masse 400 g"],
       ["Alimentation 5 V", "I2C / UART"], IMG_ADCS,
       {"pointing_accuracy_deg": 1.0, "pointing_stability_arcsec_s": 120.0, "slew_rate_deg_s": 1.0}, standby=0.2, heritage="60 vols"),
    eq("adcs_cubesat_precision", "newspace_micro", "adcs", "CubeADCS Precision (Star Tracker + 3 Reaction Wheels)", 0.9, 3.0, 0.18, 0.6,
       (90, 90, 55), "ADCS de précision pour CubeSats",
       "ADCS 3 axes complet pour CubeSats, avec un viseur d'étoiles miniature et trois roues à réaction. Il atteint 0,05° de précision, suffisant pour les caméras compactes de résolution métrique.",
       ["Précision 0,05°", "Viseur d'étoiles 6 arcsec", "3 roues 1 mN·m", "Masse 900 g"],
       ["Alimentation 5-12 V", "CAN / UART"], IMG_ADCS,
       {"pointing_accuracy_deg": 0.05, "pointing_stability_arcsec_s": 8.0, "slew_rate_deg_s": 2.0}, standby=0.6, heritage="35 vols"),
    eq("adcs_agile_wheels_medium", "gyro_dyn", "adcs", "AgileWheel Medium ADCS (4 Wheels + Star Trackers)", 12.0, 35.0, 0.95, 9.0,
       (300, 250, 200), "ADCS à roues agiles pour plateformes moyennes",
       "Ensemble de quatre roues à réaction à grand couple et de deux viseurs d'étoiles, pour les satellites de 150 à 600 kg. Offre un bon compromis entre précision de pointage et agilité, sans les contraintes des CMG.",
       ["Précision 0,004°", "Agilité 3°/s", "4 roues 4 mN·m", "Stabilité 0,35 arcsec/s"],
       ["Alimentation 28 V", "CAN / SpaceWire"], IMG_ADCS,
       {"pointing_accuracy_deg": 0.004, "pointing_stability_arcsec_s": 0.35, "slew_rate_deg_s": 3.0}, standby=6.0, heritage="20 vols"),
    eq("adcs_ultra_stable", "gyro_dyn", "adcs", "UltraStable Pointing Suite (Fine Stellar Gyro)", 18.0, 40.0, 1.6, 14.0,
       (350, 300, 240), "ADCS ultra-stable pour télescopes très haute résolution",
       "Suite de pointage ultra-stable avec gyroscope stellaire de précision, roues à très faibles vibrations et amortisseurs. Conçue pour les télescopes de 1 m de résolution et les instruments très sensibles aux micro-vibrations. Faible agilité mais excellente stabilité.",
       ["Précision 0,001°", "Stabilité 0,05 arcsec/s", "Roues à très faibles vibrations", "Agilité 0,8°/s"],
       ["Alimentation 28 V", "SpaceWire / MIL-1553"], IMG_ADCS,
       {"pointing_accuracy_deg": 0.001, "pointing_stability_arcsec_s": 0.05, "slew_rate_deg_s": 0.8}, trl=8, standby=8.0),
]
