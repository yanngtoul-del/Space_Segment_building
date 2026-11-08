"""Structured French datasheet builder for any catalog item."""

from dataclasses import dataclass, field
from typing import Any
from ssb.core.orbit import OrbitDefinition
from ssb.core.platform import PlatformBase, Equipment, SubsystemFunction
from ssb.core.payload import (
    BasePayload,
    OpticalImagerPayload,
    SpectrometerPayload,
    SarPayload,
    OpticalCommPayload,
    QkdPayload,
    RadioCommPayload,
    PayloadType,
)
from ssb.core.project import Launcher
from ssb.payload.optical_model import OpticalImagerModel
from ssb.payload.spectrometer_model import SpectrometerModel
from ssb.payload.sar_model import SarModel
from ssb.payload.comm_model import OpticalCommModel, RadioCommModel
from ssb.payload.qkd_model import QkdModel


FUNCTION_LABELS_FR = {
    SubsystemFunction.PROPULSION.value: "Propulsion",
    SubsystemFunction.TTC.value: "Télémesure / Télécommande (TT&C)",
    SubsystemFunction.PAYLOAD_DOWNLINK.value: "Émetteur de descente charge utile",
    SubsystemFunction.MASS_MEMORY.value: "Mémoire de masse",
    SubsystemFunction.ADCS.value: "Contrôle d'attitude (ADCS)",
    SubsystemFunction.EPS_SOLAR.value: "Génération solaire",
    SubsystemFunction.EPS_BATTERY.value: "Batterie",
    SubsystemFunction.OBC.value: "Calculateur de bord",
    SubsystemFunction.THERMAL.value: "Contrôle thermique",
    SubsystemFunction.DEORBIT_DEVICE.value: "Dispositif de désorbitation",
    SubsystemFunction.OPTICAL_INTERFACE.value: "Interface Optique / Fente Spectrométrique",
}

PAYLOAD_TYPE_LABELS_FR = {
    PayloadType.OPTICAL_IMAGER.value: "Imageur optique / Télescope",
    PayloadType.SPECTROMETER.value: "Spectromètre imageur / Hyperspectral",
    PayloadType.SAR.value: "Radar à synthèse d'ouverture (SAR)",
    PayloadType.OPTICAL_COMM.value: "Terminal de télécommunication optique laser",
    PayloadType.QKD.value: "Terminal de distribution quantique de clés (QKD)",
    PayloadType.RADIO_COMM.value: "Charge utile radio-fréquence (RF)",
}


@dataclass
class DatasheetSection:
    title: str
    rows: list[tuple[str, str]] = field(default_factory=list)


@dataclass
class DatasheetData:
    item_id: str
    name: str
    supplier_name: str
    category_label: str
    short_description: str
    long_description: str
    image: str
    price_label: str
    dimensions_mm: tuple[float, float, float]
    volume_label: str
    mass_label: str
    key_features: list[str]
    interfaces: list[str]
    sections: list[DatasheetSection]


def _fmt_dims(dims: tuple[float, float, float]) -> str:
    if not dims or dims == (0.0, 0.0, 0.0):
        return "Non spécifié"
    return f"{dims[0]:.0f} × {dims[1]:.0f} × {dims[2]:.0f} mm"


def build_datasheet(item: Any, ref_orbit: OrbitDefinition | None = None) -> DatasheetData:
    """Build a complete French datasheet for a Platform, Payload, Equipment, or Launcher."""
    orbit = ref_orbit or OrbitDefinition(altitude_km=500.0, inclination_deg=97.4)

    if isinstance(item, PlatformBase):
        return _from_platform(item)
    if isinstance(item, BasePayload):
        return _from_payload(item, orbit)
    if isinstance(item, Equipment):
        return _from_equipment(item)
    if isinstance(item, Launcher):
        return _from_launcher(item)
    raise TypeError(f"Unsupported item type for datasheet: {type(item)}")


def _from_platform(p: PlatformBase) -> DatasheetData:
    phys = DatasheetSection(
        "Caractéristiques physiques & mécaniques",
        [
            ("Catégorie de bus", p.category),
            ("Masse sèche de la plateforme (sans options)", f"{p.dry_mass_kg:.1f} kg"),
            ("Masse maximale de charge utile", f"{p.max_payload_mass_kg:.1f} kg"),
            ("Masse maximale au lancement (humide)", f"{p.max_launch_mass_kg:.1f} kg"),
            ("Volume de la baie charge utile", f"{p.payload_volume_liters:.1f} L"),
            ("Dimensions repliées (L × l × H)", _fmt_dims(p.dimensions_mm)),
            ("Envergure panneaux déployés", f"{p.deployed_span_m:.1f} m"),
            ("Dissipation thermique charge utile max.", f"{p.payload_thermal_dissipation_w:.0f} W"),
            ("Environnements lanceur compatibles", ", ".join(p.launch_environment_compatible) or "—"),
        ],
    )
    elec = DatasheetSection(
        "Sous-système électrique (EPS)",
        [
            ("Puissance moyenne générée en orbite", f"{p.orbit_avg_power_w:.0f} W"),
            ("Puissance moyenne disponible pour CU + options", f"{p.payload_avg_power_w:.0f} W"),
            ("Puissance crête disponible pour CU", f"{p.payload_peak_power_w:.0f} W"),
            ("Tension de bus primaire", f"{p.bus_voltage_v:.0f} V"),
            ("Capacité batterie", f"{p.battery_capacity_wh:.0f} Wh"),
            ("Profondeur de décharge max. (DoD)", f"{p.battery_max_dod * 100:.0f} %"),
        ],
    )
    adcs = DatasheetSection(
        "Contrôle d'attitude de base (ADCS)",
        [
            ("Précision de pointage (3σ)", f"{p.pointing_accuracy_deg:.4f} °"),
            ("Stabilité de pointage (dérive)", f"{p.pointing_stability_arcsec_s:.2f} arcsec/s"),
            ("Agilité (vitesse de basculement)", f"{p.slew_rate_deg_s:.1f} °/s"),
            ("Jitter résiduel", f"{p.jitter_arcsec:.2f} arcsec"),
        ],
    )
    slots_rows: list[tuple[str, str]] = []
    for s in p.slots:
        fn_lbl = FUNCTION_LABELS_FR.get(s.function.value, s.function.value)
        inc = ", ".join(s.included_equipment_ids) if s.included_equipment_ids else "aucun inclus"
        surch = ""
        if s.integration_cost_fixed_meur or s.integration_cost_pct:
            surch = f" | surcoût intégration {s.integration_cost_fixed_meur:.2f} M€ + {s.integration_cost_pct:.0f}%"
        slots_rows.append(
            (fn_lbl, f"qté {s.min_qty}..{s.max_qty} | {len(s.allowed_equipment_ids)} choix | inclus : {inc}{surch}")
        )
    slots_sec = DatasheetSection("Emplacements d'options (Slots)", slots_rows)
    comm = DatasheetSection(
        "Fiabilité, héritage & conditions commerciales",
        [
            ("Fournisseur", p.supplier_name),
            ("Prix de base (hors options payantes)", f"{p.base_price_meur:.2f} M€"),
            ("Délai de livraison nominal", f"{p.base_lead_time_months} mois"),
            ("Durée de vie nominale", f"{p.design_lifetime_years:.1f} ans"),
            ("Tolérance aux radiations (TID)", f"{p.rad_tolerance_krad:.0f} krad"),
            ("Niveau de maturité (TRL)", f"TRL {p.trl}"),
        ],
    )
    return DatasheetData(
        item_id=p.id,
        name=p.name,
        supplier_name=p.supplier_name,
        category_label=f"Plateforme — {p.category}",
        short_description=p.description,
        long_description=p.long_description or p.description,
        image=p.image,
        price_label=f"{p.base_price_meur:.2f} M€ (base)",
        dimensions_mm=p.dimensions_mm,
        volume_label=f"Baie CU : {p.payload_volume_liters:.0f} L",
        mass_label=f"{p.dry_mass_kg:.0f} kg sec (CU max {p.max_payload_mass_kg:.0f} kg)",
        key_features=p.key_features,
        interfaces=p.interfaces,
        sections=[phys, elec, adcs, slots_sec, comm],
    )


def _from_payload(pl: BasePayload, orbit: OrbitDefinition) -> DatasheetData:
    ptype_label = PAYLOAD_TYPE_LABELS_FR.get(pl.payload_type.value, pl.payload_type.value)
    phys = DatasheetSection(
        "Masse, volume, puissance & interfaces",
        [
            ("Type d'instrument", ptype_label),
            ("Masse de l'instrument", f"{pl.mass_kg:.1f} kg"),
            ("Volume enveloppe", f"{pl.volume_liters:.1f} L"),
            ("Dimensions (L × l × H)", _fmt_dims(pl.dimensions_mm)),
            ("Puissance en opération", f"{pl.operational_power_w:.1f} W"),
            ("Puissance crête", f"{pl.peak_power_w:.1f} W"),
            ("Puissance en veille (standby)", f"{pl.standby_power_w:.1f} W"),
            ("Dissipation thermique à évacuer", f"{pl.thermal_dissipation_w:.1f} W"),
            ("Débit de données brut", f"{pl.raw_data_rate_mbps:.1f} Mbit/s"),
            ("Débit de données compressé", f"{pl.compressed_data_rate_mbps:.1f} Mbit/s"),
        ],
    )
    point = DatasheetSection(
        "Exigences de pointage imposées à la plateforme",
        [
            ("Précision de pointage requise (≤)", f"{pl.required_pointing_accuracy_deg:.4f} °"),
            ("Stabilité de pointage requise (≤)", f"{pl.required_pointing_stability_arcsec_s:.2f} arcsec/s"),
            ("Jitter maximal toléré (≤)", f"{pl.max_tolerated_jitter_arcsec:.2f} arcsec"),
        ],
    )

    spec_rows: list[tuple[str, str]] = []
    perf_rows: list[tuple[str, str]] = []
    h = orbit.altitude_km

    if isinstance(pl, OpticalImagerPayload):
        spec_rows = [
            ("Diamètre de pupille / miroir primaire", f"{pl.aperture_diameter_m * 100:.1f} cm ({pl.aperture_diameter_m:.2f} m)"),
            ("Longueur focale", f"{pl.focal_length_m:.2f} m (f/{pl.f_number:.1f})"),
            ("Pas des pixels (pitch)", f"{pl.pixel_pitch_um:.2f} µm"),
            ("Nombre de pixels fauchée (cross-track)", f"{pl.detector_pixels_cross_track:,}".replace(",", " ")),
            ("Bandes spectrales", f"{len(pl.spectral_bands)} bandes : {', '.join(pl.spectral_bands)}"),
            ("Domaine spectral", f"{pl.min_wavelength_nm:.0f} – {pl.max_wavelength_nm:.0f} nm"),
            ("Rendement quantique moyen (QE)", f"{pl.quantum_efficiency_avg * 100:.0f} %"),
            ("Bruit de lecture / pleine capacité", f"{pl.read_noise_electrons:.1f} e⁻ / {pl.full_well_capacity_electrons:.0f} e⁻"),
            ("Transmission optique / MTF Nyquist", f"{pl.optics_transmission * 100:.0f} % / {pl.optics_mtf_at_nyquist:.2f}"),
            ("Quantification", f"{pl.quantization_bits} bits"),
        ]
        perf = OpticalImagerModel.compute(pl, orbit)
        perf_rows = [
            (f"Résolution au sol nadir (GSD @ {h:.0f} km)", f"{perf.gsd_nadir_m:.2f} m"),
            (f"Largeur de fauchée (@ {h:.0f} km)", f"{perf.swath_width_km:.1f} km (FOV {perf.field_of_view_deg:.2f}°)"),
            ("Tache de diffraction au sol", f"{perf.diffraction_ground_spot_m:.2f} m"),
            ("Rapport signal/bruit estimé (SNR nadir)", f"{perf.snr_nadir_estimate:.1f}"),
            ("Indice de qualité d'image estimé (NIIRS)", f"{perf.niirs_estimate:.1f}"),
        ]
    elif isinstance(pl, SpectrometerPayload):
        spec_rows = [
            ("Architecture instrumentale", "Banc dispersif (fente + réseau/prisme + matrice détecteur)"),
            ("Optique collectrice requise", "Télescope avant (Charge utile optique)"),
            ("Interface mécanique/optique", "Option « Interface Optique / Fente Spectrométrique »"),
            ("Pas des pixels", f"{pl.pixel_pitch_um:.2f} µm"),
            ("Pixels spatiaux (fauchée)", f"{pl.detector_spatial_pixels}"),
            ("Domaine spectral", f"{pl.spectral_range_min_nm:.0f} – {pl.spectral_range_max_nm:.0f} nm"),
            ("Nombre de bandes spectrales", f"{pl.number_of_spectral_bands}"),
            ("Résolution spectrale (FWHM)", f"{pl.spectral_resolution_nm:.2f} nm"),
            ("Quantification", f"{pl.quantization_bits} bits"),
        ]
        perf = SpectrometerModel.compute(pl, orbit)
        if perf.gsd_spatial_nadir_m > 0:
            perf_rows = [
                (f"GSD spatial au nadir (@ {h:.0f} km)", f"{perf.gsd_spatial_nadir_m:.2f} m"),
                (f"Fauchée (@ {h:.0f} km)", f"{perf.swath_width_km:.1f} km"),
                ("SNR moyen par bande (TDI)", f"{perf.mean_snr_estimate:.1f}"),
                ("Débit brut / compressé calculé", f"{perf.data_rate_raw_mbps:.0f} / {perf.data_rate_compressed_mbps:.0f} Mbit/s"),
            ]
        else:
            perf_rows = [
                ("Échantillonnage spectral", f"{perf.spectral_sampling_nm:.2f} nm"),
                ("Nombre de canaux spectraux", f"{perf.spectral_bands_count}"),
                ("Résolution spatiale (GSD)", "Couplage requis (dépend de la focale f du télescope avant)"),
                ("SNR radiométrique", "Couplage requis (dépend de la pupille D du télescope avant)"),
                ("Chaîne optomécanique", "[Télescope CU] -> [Option Fente] -> [Spectromètre CU]"),
            ]
    elif isinstance(pl, SarPayload):
        spec_rows = [
            ("Bande radar & fréquence centrale", f"Bande {pl.band_name} ({pl.frequency_ghz:.3f} GHz)"),
            ("Type d'antenne", pl.antenna_type),
            ("Dimensions d'antenne (L × l)", f"{pl.antenna_length_m:.2f} m × {pl.antenna_width_m:.2f} m"),
            ("Puissance crête RF émise", f"{pl.rf_peak_power_w:.0f} W"),
            ("Rapport cyclique max. (duty cycle)", f"{pl.duty_cycle_max_pct:.1f} %"),
            ("Bande passante du chirp", f"{pl.chirp_bandwidth_mhz:.0f} MHz"),
            ("Facteur de bruit récepteur (NF)", f"{pl.system_noise_figure_db:.1f} dB"),
            ("Plage d'angles d'incidence", f"{pl.incidence_angle_min_deg:.0f}° – {pl.incidence_angle_max_deg:.0f}°"),
        ]
        perf = SarModel.compute(pl, orbit)
        perf_rows = [
            (f"Résolution distance au sol (@ {h:.0f} km, 35°)", f"{perf.ground_range_resolution_m:.2f} m"),
            ("Résolution azimut (stripmap)", f"{perf.azimuth_resolution_stripmap_m:.2f} m"),
            (f"Fauchée stripmap (@ {h:.0f} km)", f"{perf.swath_width_ground_km:.1f} km"),
            (f"Sensibilité NESZ (@ {h:.0f} km)", f"{perf.nesz_db:.1f} dB"),
        ]
    elif isinstance(pl, OpticalCommPayload):
        spec_rows = [
            ("Diamètre du télescope optique", f"{pl.telescope_aperture_m * 100:.1f} cm"),
            ("Longueur d'onde laser", f"{pl.wavelength_nm:.0f} nm"),
            ("Puissance optique émise", f"{pl.tx_optical_power_w:.2f} W"),
            ("Débit maximal", f"{pl.max_data_rate_gbps:.1f} Gbit/s"),
            ("Divergence du faisceau", f"{pl.beam_divergence_urad:.1f} µrad"),
            ("Précision du suivi fin (PAT)", f"{pl.pointing_tracking_accuracy_urad:.2f} µrad"),
            ("Standards supportés", ", ".join(pl.compatible_standards)),
        ]
        perf = OpticalCommModel.compute_leo_to_ground_link(
            tx_power_w=pl.tx_optical_power_w,
            tx_aperture_m=pl.telescope_aperture_m,
            rx_aperture_m=0.80,
            wavelength_nm=pl.wavelength_nm,
            slant_range_km=h * 1.5,
            pointing_error_urad=pl.pointing_tracking_accuracy_urad,
            target_data_rate_gbps=pl.max_data_rate_gbps,
        )
        perf_rows = [
            (f"Marge de liaison vers télescope sol 80 cm (@ {h:.0f} km)", f"{perf.margin_db:.1f} dB"),
            ("Puissance optique reçue au sol", f"{perf.received_optical_power_dbm:.1f} dBm ({perf.received_optical_power_nw:.1f} nW)"),
            ("Débit atteignable sur ce lien", f"{perf.achievable_data_rate_gbps:.1f} Gbit/s"),
        ]
    elif isinstance(pl, QkdPayload):
        spec_rows = [
            ("Protocole quantique", pl.protocol),
            ("Diamètre du télescope d'émission", f"{pl.telescope_aperture_m * 100:.1f} cm"),
            ("Cadence de la source de photons", f"{pl.source_rate_mhz:.0f} MHz"),
            ("Longueur d'onde", f"{pl.wavelength_nm:.0f} nm"),
            ("Précision de pointage fin", f"{pl.pointing_accuracy_urad:.2f} µrad"),
            ("Opération nocturne uniquement", "Oui" if pl.night_only_operation else "Jour et nuit"),
        ]
        perf = QkdModel.compute(
            telescope_aperture_m=pl.telescope_aperture_m,
            source_rate_mhz=pl.source_rate_mhz,
            wavelength_nm=pl.wavelength_nm,
            ground_telescope_aperture_m=1.0,
            slant_range_km=h * 1.3,
            pointing_jitter_urad=pl.pointing_accuracy_urad,
        )
        perf_rows = [
            (f"Pertes totales du canal (@ {h:.0f} km → station 1 m)", f"{perf.total_channel_loss_db:.1f} dB"),
            ("Photons détectés au sol", f"{perf.detected_count_rate_cps:.0f} cps"),
            ("Taux d'erreur quantique (QBER)", f"{perf.quantum_bit_error_rate_pct:.2f} %"),
            ("Débit de clé secrète asymptotique", f"{perf.asymptotic_secret_key_rate_bps / 1000.0:.2f} kbit/s ({perf.secret_bits_per_pass / 1000.0:.1f} kbits/passage)"),
        ]
    elif isinstance(pl, RadioCommPayload):
        spec_rows = [
            ("Fréquence montante (uplink)", f"{pl.uplink_frequency_ghz:.3f} GHz"),
            ("Fréquence descendante (downlink)", f"{pl.downlink_frequency_ghz:.3f} GHz"),
            ("Puissance RF de sortie", f"{pl.rf_output_power_w:.1f} W"),
            ("Gain d'antenne émission / réception", f"{pl.antenna_gain_tx_dbi:.1f} dBi / {pl.antenna_gain_rx_dbi:.1f} dBi"),
            ("Bande passante RF", f"{pl.bandwidth_mhz:.1f} MHz"),
            ("Débit maximal de données", f"{pl.max_data_rate_mbps:.1f} Mbit/s"),
        ]
        perf = RadioCommModel.compute_downlink_budget(
            rf_power_w=pl.rf_output_power_w,
            carrier_freq_ghz=pl.downlink_frequency_ghz,
            satellite_antenna_gain_dbi=pl.antenna_gain_tx_dbi,
            ground_antenna_diameter_m=5.0,
            data_rate_mbps=pl.max_data_rate_mbps,
            slant_range_km=h * 1.5,
        )
        perf_rows = [
            ("PIRE (EIRP)", f"{perf.eirp_dbw:.1f} dBW"),
            (f"Eb/N0 vers antenne sol 5 m (@ {h:.0f} km)", f"{perf.eb_over_n0_db:.1f} dB"),
            ("Marge de liaison", f"{perf.link_margin_db:.1f} dB"),
        ]

    spec_sec = DatasheetSection("Spécifications fonctionnelles de l'instrument", spec_rows)
    perf_sec = DatasheetSection("Performances en mission (modèle analytique)", perf_rows)
    comm = DatasheetSection(
        "Maturité, héritage & conditions commerciales",
        [
            ("Fournisseur", pl.supplier_name),
            ("Prix catalogue de l'instrument", f"{pl.price_meur:.2f} M€"),
            ("Niveau de maturité (TRL)", f"TRL {pl.trl}"),
            ("Héritage en vol", pl.flight_heritage or "Nouveau développement"),
        ],
    )
    sections = [phys, point, spec_sec, perf_sec, comm]
    return DatasheetData(
        item_id=pl.id,
        name=pl.name,
        supplier_name=pl.supplier_name,
        category_label=f"Charge utile — {ptype_label}",
        short_description=pl.description,
        long_description=pl.long_description or pl.description,
        image=pl.image,
        price_label=f"{pl.price_meur:.2f} M€",
        dimensions_mm=pl.dimensions_mm,
        volume_label=f"{pl.volume_liters:.1f} L",
        mass_label=f"{pl.mass_kg:.1f} kg | {pl.operational_power_w:.0f} W",
        key_features=pl.key_features,
        interfaces=pl.interfaces,
        sections=sections,
    )


def _from_equipment(eq: Equipment) -> DatasheetData:
    fn_label = FUNCTION_LABELS_FR.get(eq.function.value, eq.function.value)
    phys = DatasheetSection(
        "Masse, volume & bilan électrique",
        [
            ("Fonction sous-système", fn_label),
            ("Masse de l'équipement", f"{eq.mass_kg:.2f} kg"),
            ("Volume enveloppe", f"{eq.volume_liters:.2f} L"),
            ("Dimensions (L × l × H)", _fmt_dims(eq.dimensions_mm)),
            ("Consommation moyenne en opération", f"{eq.power_w:.1f} W"),
            ("Consommation crête", f"{eq.peak_power_w:.1f} W"),
            ("Consommation en veille", f"{eq.standby_power_w:.1f} W"),
        ],
    )
    spec_labels = {
        "isp_s": ("Impulsion spécifique (Isp)", "s"),
        "propellant_mass_kg": ("Masse de propergol embarquée", "kg"),
        "thrust_mn": ("Poussée nominale", "mN"),
        "tx_rf_power_w": ("Puissance RF émission", "W"),
        "downlink_rate_kbps": ("Débit descendant TT&C", "kbit/s"),
        "uplink_rate_kbps": ("Débit montant TT&C", "kbit/s"),
        "rf_frequency_ghz": ("Fréquence porteuse RF", "GHz"),
        "rf_power_w": ("Puissance RF de sortie", "W"),
        "max_data_rate_mbps": ("Débit maximal de données", "Mbit/s"),
        "capacity_bol_gb": ("Capacité début de vie (BOL)", "Go"),
        "capacity_eol_gb": ("Capacité fin de vie (EOL)", "Go"),
        "write_speed_mbps": ("Vitesse d'écriture", "Mbit/s"),
        "read_speed_mbps": ("Vitesse de lecture", "Mbit/s"),
        "pointing_accuracy_deg": ("Précision de pointage (3σ)", "°"),
        "pointing_stability_arcsec_s": ("Stabilité de pointage", "arcsec/s"),
        "slew_rate_deg_s": ("Vitesse de basculement (agilité)", "°/s"),
        "wheel_momentum_nms": ("Moment cinétique des roues", "N·m·s"),
    }
    srows: list[tuple[str, str]] = []
    for k, v in eq.specs.items():
        lbl, unit = spec_labels.get(k, (k, ""))
        srows.append((lbl, f"{v} {unit}".strip()))
    spec_sec = DatasheetSection("Spécifications fonctionnelles", srows)
    comm = DatasheetSection(
        "Conditions commerciales & maturité",
        [
            ("Fournisseur", eq.supplier_name),
            ("Prix catalogue de base (hors intégration plateforme)", f"{eq.price_meur:.2f} M€"),
            ("Niveau de maturité (TRL)", f"TRL {eq.trl}"),
            ("Héritage en vol", eq.flight_heritage or "Qualifié"),
        ],
    )
    return DatasheetData(
        item_id=eq.id,
        name=eq.name,
        supplier_name=eq.supplier_name,
        category_label=f"Équipement — {fn_label}",
        short_description=eq.description,
        long_description=eq.long_description or eq.description,
        image=eq.image,
        price_label=f"{eq.price_meur:.2f} M€ (catalogue)",
        dimensions_mm=eq.dimensions_mm,
        volume_label=f"{eq.volume_liters:.2f} L",
        mass_label=f"{eq.mass_kg:.2f} kg | {eq.power_w:.0f} W",
        key_features=eq.key_features,
        interfaces=eq.interfaces,
        sections=[phys, spec_sec, comm],
    )


def _from_launcher(ln: Launcher) -> DatasheetData:
    ltype = "Lancement partagé (Rideshare)" if ln.launcher_type == "rideshare" else "Lanceur dédié"
    cap_rows = [
        (
            f"Orbite {c.orbit_type}",
            f"max {c.max_payload_mass_kg:.0f} kg — coiffe/volume Ø {c.fairing_diameter_m:.2f} m × H {c.fairing_height_m:.2f} m",
        )
        for c in ln.capacities
    ]
    c0 = ln.capacities[0] if ln.capacities else None
    dims = (
        (c0.fairing_diameter_m * 1000, c0.fairing_diameter_m * 1000, c0.fairing_height_m * 1000)
        if c0
        else (1000.0, 1000.0, 2000.0)
    )
    price_str = (
        f"{ln.price_base_meur:.2f} M€ + {ln.price_per_kg_meur * 1000:.0f} k€/kg"
        if ln.price_per_kg_meur > 0
        else f"{ln.price_base_meur:.2f} M€ (dédié)"
    )
    gen = DatasheetSection(
        "Caractéristiques du service de lancement",
        [
            ("Type de service", ltype),
            ("Opérateur", ln.supplier_name),
            ("Masse maximale injectable", f"{ln.max_total_mass_kg:.0f} kg"),
            ("Volume sous coiffe / enveloppe", f"{ln.fairing_volume_m3:.2f} m³"),
            ("Formule tarifaire", price_str),
            ("Délai de réservation (lead time)", f"{ln.lead_time_months} mois"),
            ("Maturité & historique", f"TRL {ln.trl} ({ln.flight_heritage or 'opérationnel'})"),
        ],
    )
    caps_sec = DatasheetSection("Capacités par orbite de référence & enveloppe sous coiffe", cap_rows)
    return DatasheetData(
        item_id=ln.id,
        name=ln.name,
        supplier_name=ln.supplier_name,
        category_label=f"Lanceur — {ltype}",
        short_description=ln.description,
        long_description=ln.long_description or ln.description,
        image=ln.image,
        price_label=price_str,
        dimensions_mm=dims,
        volume_label=f"Coiffe {ln.fairing_volume_m3:.2f} m³",
        mass_label=f"Capacité max {ln.max_total_mass_kg:.0f} kg",
        key_features=ln.key_features,
        interfaces=ln.interfaces,
        sections=[gen, caps_sec],
    )
