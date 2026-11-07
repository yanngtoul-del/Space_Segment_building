"""Launcher catalog source: overlays for the 4 existing launchers + 4 new launchers."""

from common import base

IMG_RIDE = "launcher_rideshare.jpg"
IMG_ROCK = "launcher_rocket.jpg"
IMG_HEAVY = "launcher_heavy.jpg"


def cap(orbit_type, mass, d, h):
    return dict(orbit_type=orbit_type, max_payload_mass_kg=mass, fairing_diameter_m=d, fairing_height_m=h)


OVERLAY = {
    "ln_rideshare_sso": dict(
        image=IMG_RIDE, fairing_volume_m3=2.0,
        description="Covoiturage régulier vers l'orbite héliosynchrone sur port ESPA ou plateau partagé",
        long_description="Service de lancement partagé (rideshare) sur lanceur moyen réutilisable, avec départs trimestriels vers une orbite héliosynchrone à 500–600 km. Le tarif comprend un prix d'entrée fixe et un coût au kilogramme : c'est la solution la plus économique pour un microsatellite jusqu'à 350–450 kg, mais l'orbite d'injection est imposée par le passager principal.",
        key_features=["Départs tous les 3 mois vers SSO", "0,25 M€ + 15 k€/kg", "Jusqu'à 350 kg en SSO 500 km", "Ports ESPA 15\" et 24\""],
        interfaces=["Anneau ESPA 15 ou 24 pouces", "Connecteur ombilical standard", "Enveloppe mécanique 1,2 x 1,8 m"]),
    "ln_dedicated_light": dict(
        image=IMG_ROCK, fairing_volume_m3=2.2,
        description="Petit lanceur dédié pour l'injection directe d'un microsatellite sur orbite sur mesure",
        long_description="Petit lanceur orbital dédié (classe 250 kg en orbite basse). Contrairement au rideshare, l'étudiant choisit librement l'altitude et l'inclinaison d'injection sans avoir à dépenser du propergol pour rejoindre l'orbite opérationnelle. Le coût fixe (5,5 M€) est en revanche bien supérieur à un lancement partagé.",
        key_features=["Orbite d'injection sur mesure", "220 kg en SSO 500 km, 180 kg à 700 km", "Coiffe Ø 1,2 m x 2,0 m", "Étage supérieur réallumable"],
        interfaces=["Adaptateur 15 ou 24 pouces", "Coiffe 1,2 m"]),
    "ln_dedicated_medium": dict(
        image=IMG_ROCK, fairing_volume_m3=18.0,
        description="Lanceur médium dédié pour satellites de 300 à 1500 kg",
        long_description="Lanceur dédié de classe moyenne (inspiré de Vega-C / Firefly Alpha+), capable de placer plus d'une tonne en orbite héliosynchrone. Il dispose d'une coiffe de 2,6 m de diamètre permettant d'embarquer des télescopes sub-métriques ou des antennes radar repliées.",
        key_features=["1 350 kg en SSO 500 km", "Coiffe Ø 2,6 m x 3,5 m", "Haute précision d'injection", "Adaptateur double lancement possible"],
        interfaces=["Adaptateur 937 mm ou 1194 mm", "Coiffe 2,6 m"]),
    "ln_heavy_institutional": dict(
        image=IMG_HEAVY, fairing_volume_m3=85.0,
        description="Lanceur lourd institutionnel pour grands satellites ou grappes multi-tonnes",
        long_description="Lanceur lourd européen/américain (classe Ariane 6 / Falcon 9 dédié) offrant plusieurs tonnes de capacité en orbite héliosynchrone et une coiffe de grand volume (4,5 m de diamètre). Indispensable pour les plateformes de plus de 1,5 tonne, mais son coût très élevé pénalise fortement le budget global si le satellite est léger.",
        key_features=["5 000 kg en SSO 500 km", "Coiffe Ø 4,5 m x 6,0 m", "Fiabilité institutionnelle", "Injection directe toute inclinaison"],
        interfaces=["Adaptateur 1194 mm ou 1666 mm", "Coiffe 4,5 m"]),
}


def ln(item_id, sup, name, ltype, pbase, ppkg, mMax, lead, trl, her, vol, img, desc, long, feats, ifaces, caps):
    return base(
        item_id, sup, name=name, launcher_type=ltype, description=desc, fairing_volume_m3=vol,
        price_base_meur=pbase, price_per_kg_meur=ppkg, max_total_mass_kg=mMax, lead_time_months=lead,
        trl=trl, flight_heritage=her, image=img, long_description=long, key_features=feats,
        interfaces=ifaces, capacities=caps,
    )


NEW = [
    ln("ln_cubesat_deployer", "launch_global", "CubePod SSO Dispenser Service", "rideshare",
       0.08, 0.025, 32.0, 6, 9, ">120 CubeSats déployés", 0.05, IMG_RIDE,
       "Déployeur CubeSat (6U à 16U) en covoiturage SSO",
       "Service d'intégration et d'éjection en déployeur containerisé (6U, 12U ou 16U) sur un vol partagé. C'est le mode de lancement le moins cher du catalogue, réservé aux nanosatellites de moins de 32 kg. Le satellite est protégé dans son pod jusqu'à l'éjection en orbite.",
       ["Pour CubeSats 6U, 12U, 16U (max 32 kg)", "Mise de départ très faible (80 k€)", "Délai 6 mois", "Démarches de sécurité simplifiées"],
       ["Rails CubeSat conformes CDS", "Volume max 0,45 x 0,25 x 0,25 m"],
       [cap("sso_500km", 32.0, 0.50, 0.55), cap("sso_700km", 26.0, 0.50, 0.55), cap("leo_inclined", 32.0, 0.50, 0.55)]),

    ln("ln_espa_heavy_rideshare", "launch_global", "OrbitalShare XL (ESPA Grande)", "rideshare",
       0.65, 0.012, 850.0, 12, 9, ">25 vols", 5.5, IMG_RIDE,
       "Emplacement ESPA Grande / plateau supérieur pour satellites jusqu'à 800 kg",
       "Emplacement de covoiturage de grande capacité sur port ESPA Grande (24 pouces) ou adaptateur supérieur, acceptant des satellites jusqu'à 800 kg en SSO. Permet de lancer des plateformes de 300 à 700 kg à une fraction du prix d'un lanceur dédié, avec la contrainte d'une orbite partagée.",
       ["Jusqu'à 800 kg en SSO 500 km", "0,65 M€ + 12 k€/kg", "Volume 1,6 x 2,2 m", "Idéal pour classes 300–700 kg"],
       ["Anneau 24 pouces ou adaptateur 937 mm", "Enveloppe 1,6 x 2,2 m"],
       [cap("sso_500km", 800.0, 1.6, 2.2), cap("sso_700km", 650.0, 1.6, 2.2), cap("leo_inclined", 850.0, 1.6, 2.2)]),

    ln("ln_polar_dedicated_micro", "polar_launch", "Aurora-1 Polar Micro Launcher", "dedicated",
       3.8, 0.0, 130.0, 10, 8, "6 vols", 1.3, IMG_ROCK,
       "Micro-lanceur dédié tiré depuis un cosmodrome polaire européen",
       "Micro-lanceur dédié de Borealis Launch Systems, opéré depuis la Scandinavie pour un accès direct aux orbites polaires et héliosynchrones. Il cible les satellites de 50 à 120 kg qui ont besoin d'une orbite précise (inclinaison, heure locale) sans payer un lanceur de 250 kg.",
       ["115 kg en SSO 500 km", "Prix dédié 3,8 M€", "Tir direct vers inclinaisons polaires", "Délai 10 mois"],
       ["Adaptateur 15 pouces / déployeur 16U", "Coiffe Ø 1,0 m x 1,6 m"],
       [cap("sso_500km", 115.0, 1.0, 1.6), cap("sso_700km", 90.0, 1.0, 1.6), cap("leo_inclined", 130.0, 1.0, 1.6)]),

    ln("ln_polar_medium_500", "polar_launch", "Aurora-5 Small-Medium Launcher", "dedicated",
       11.5, 0.0, 650.0, 15, 8, "4 vols", 7.5, IMG_ROCK,
       "Lanceur dédié de classe 600 kg positionné entre le micro-lanceur et le médium",
       "Lanceur à deux étages au méthane liquide capable de placer 550 kg en orbite héliosynchrone pour 11,5 M€. Il comble le trou tarifaire entre les petits lanceurs (250 kg, 5,5 M€) et les lanceurs moyens (1 500 kg, 18 M€) pour les satellites de 250 à 550 kg.",
       ["550 kg en SSO 500 km", "11,5 M€ en lancement dédié", "Coiffe Ø 2,0 m x 2,8 m", "Étage supérieur réallumable"],
       ["Adaptateur 24 pouces ou 937 mm", "Coiffe 2,0 m"],
       [cap("sso_500km", 550.0, 2.0, 2.8), cap("sso_700km", 440.0, 2.0, 2.8), cap("leo_inclined", 650.0, 2.0, 2.8)]),
]
