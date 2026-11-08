"""Overall system budget calculations and rule verification."""

from dataclasses import dataclass, field
from typing import Any
from ssb.core.orbit import OrbitDefinition
from ssb.core.project import SystemConfiguration, Launcher
from ssb.core.mission import MissionSpecification, RequirementOperator
from ssb.core.payload import BasePayload
from ssb.catalog.database import CatalogDatabase
from ssb.core.catalog_meta import ESA_MEMBER_STATES
from ssb.system.configurator import PlatformConfigurator, ConfiguredPlatform
from ssb.system.checks import CheckStatus, RuleCheckResult
from ssb.system.payload_evaluator import evaluate_payload_requirements


@dataclass
class MassBudget:
    platform_dry_kg: float
    options_mass_kg: float
    payloads_mass_kg: float
    system_dry_mass_kg: float
    propellant_mass_kg: float
    system_wet_mass_kg: float
    margin_pct: float
    launch_mass_with_margin_kg: float
    platform_capacity_kg: float


@dataclass
class PowerBudget:
    platform_avg_power_w: float
    options_avg_power_w: float
    payloads_avg_power_w: float
    total_avg_consumption_w: float
    platform_generation_w: float
    power_margin_w: float
    power_margin_pct: float
    peak_consumption_w: float


@dataclass
class CostBudget:
    platform_base_meur: float
    options_total_meur: float
    payloads_total_meur: float
    launcher_meur: float
    space_segment_total_meur: float
    mission_budget_limit_meur: float
    cost_margin_meur: float
    satellite_cost_meur: float = 0.0
    calibration_total_meur: float = 0.0
    cost_by_country_meur: dict[str, float] = field(default_factory=dict)
    cost_by_country_pct: dict[str, float] = field(default_factory=dict)


@dataclass
class SystemBudgets:
    configured_platform: ConfiguredPlatform
    mass: MassBudget
    power: PowerBudget
    cost: CostBudget
    payload_performances: dict[str, Any] = field(default_factory=dict)
    rule_checks: list[RuleCheckResult] = field(default_factory=list)
    compliance_checks: list[RuleCheckResult] = field(default_factory=list)

    @property
    def has_blocking_errors(self) -> bool:
        return any(
            c.status == CheckStatus.FAIL
            for c in (self.rule_checks + self.compliance_checks)
        )


def launcher_capacity_for_orbit(ln: Launcher, orbit: OrbitDefinition) -> float:
    """Return launcher mass capacity (kg) for the requested orbit."""
    if not ln.capacities:
        return ln.max_total_mass_kg
    by_type = {c.orbit_type: c.max_payload_mass_kg for c in ln.capacities}

    # GEO orbit
    if orbit.is_geo or orbit.orbit_type.value == "geo" or orbit.altitude_km >= 30000.0:
        if "geo" in by_type:
            return by_type["geo"]
        if "gto" in by_type:
            return by_type["gto"]
        return 0.0

    # MEO orbit
    if orbit.is_meo or orbit.orbit_type.value == "meo" or (2000.0 <= orbit.altitude_km < 30000.0):
        if "meo" in by_type:
            return by_type["meo"]
        if "gto" in by_type:
            return by_type["gto"]
        if "sso_500km" in by_type:
            return by_type["sso_500km"] * 0.4
        return 0.0

    # SSO LEO
    if orbit.is_sso or orbit.orbit_type.value == "sso" or orbit.inclination_deg >= 95.0:
        if orbit.altitude_km <= 600.0 and "sso_500km" in by_type:
            return by_type["sso_500km"]
        if "sso_700km" in by_type:
            return by_type["sso_700km"]
        if "sso_500km" in by_type:
            return by_type["sso_500km"]

    if "leo_inclined" in by_type:
        return by_type["leo_inclined"]
    return ln.max_total_mass_kg


class SystemEvaluator:
    """Evaluates the complete satellite architecture against physics, platform limits, and mission specs."""

    def __init__(self, catalog: CatalogDatabase) -> None:
        self.catalog = catalog
        self.configurator = PlatformConfigurator(catalog)

    def evaluate(
        self, config: SystemConfiguration, mission: MissionSpecification
    ) -> SystemBudgets:
        rule_checks: list[RuleCheckResult] = []
        compliance_checks: list[RuleCheckResult] = []

        if not config.platform_id or config.platform_id not in self.catalog.platforms:
            raise ValueError("No valid platform selected in configuration")

        conf_plat = self.configurator.configure(
            config.platform_id, config.selected_options
        )
        for err in conf_plat.validation_errors:
            rule_checks.append(
                RuleCheckResult(
                    rule_id="RULE_PLAT_CONFIG",
                    category="Platform Configuration",
                    status=CheckStatus.FAIL,
                    message=err,
                )
            )

        plat_base = conf_plat.base

        # Resolve selected payloads
        payloads: list[BasePayload] = []
        for pid in config.selected_payload_ids:
            if pid in self.catalog.payloads:
                payloads.append(self.catalog.payloads[pid])
            else:
                rule_checks.append(
                    RuleCheckResult(
                        rule_id="RULE_PAYLOAD_MISSING",
                        category="Payload",
                        status=CheckStatus.FAIL,
                        message=f"Selected payload '{pid}' not found in catalog",
                    )
                )

        # 1. Mass & Volume Budget
        pl_mass = sum(p.mass_kg for p in payloads)
        pl_vol = sum(p.volume_liters for p in payloads)
        opt_mass = sum(opt.final_mass_kg for opt in conf_plat.resolved_options)

        prop_mass = 0.0
        for opt in conf_plat.resolved_options:
            if opt.equipment.function.value == "propulsion":
                prop_mass += opt.equipment.specs.get("propellant_mass_kg", 0.0)

        sys_dry_kg = plat_base.dry_mass_kg + opt_mass + pl_mass
        wet_mass_kg = sys_dry_kg + prop_mass
        margin_pct = 20.0
        launch_mass_with_margin_kg = wet_mass_kg * (1.0 + margin_pct / 100.0)

        mass_b = MassBudget(
            platform_dry_kg=plat_base.dry_mass_kg,
            options_mass_kg=round(opt_mass, 2),
            payloads_mass_kg=round(pl_mass, 2),
            system_dry_mass_kg=round(sys_dry_kg, 2),
            propellant_mass_kg=round(prop_mass, 2),
            system_wet_mass_kg=round(wet_mass_kg, 2),
            margin_pct=margin_pct,
            launch_mass_with_margin_kg=round(launch_mass_with_margin_kg, 2),
            platform_capacity_kg=plat_base.max_payload_mass_kg,
        )

        # Rule checks on Mass & Volume
        if pl_mass > plat_base.max_payload_mass_kg:
            rule_checks.append(
                RuleCheckResult(
                    rule_id="RULE_MASS_PAYLOAD_MAX",
                    category="Mass",
                    status=CheckStatus.FAIL,
                    message=f"Payload mass ({pl_mass:.1f} kg) exceeds platform payload capacity ({plat_base.max_payload_mass_kg:.1f} kg)",
                    current_value=pl_mass,
                    target_value=plat_base.max_payload_mass_kg,
                    unit="kg",
                )
            )
        else:
            rule_checks.append(
                RuleCheckResult(
                    rule_id="RULE_MASS_PAYLOAD_MAX",
                    category="Mass",
                    status=CheckStatus.PASS,
                    message=f"Payload mass ({pl_mass:.1f} kg) within platform capability ({plat_base.max_payload_mass_kg:.1f} kg)",
                    current_value=pl_mass,
                    target_value=plat_base.max_payload_mass_kg,
                    unit="kg",
                )
            )

        if pl_vol > plat_base.payload_volume_liters:
            rule_checks.append(
                RuleCheckResult(
                    rule_id="RULE_PLAT_PAYLOAD_VOL",
                    category="Volume",
                    status=CheckStatus.FAIL,
                    message=f"Payload volume ({pl_vol:.1f} L) exceeds platform volume ({plat_base.payload_volume_liters:.1f} L)",
                    current_value=pl_vol,
                    target_value=plat_base.payload_volume_liters,
                    unit="L",
                )
            )
        else:
            rule_checks.append(
                RuleCheckResult(
                    rule_id="RULE_PLAT_PAYLOAD_VOL",
                    category="Volume",
                    status=CheckStatus.PASS,
                    message=f"Payload volume ({pl_vol:.1f} L) within platform bay ({plat_base.payload_volume_liters:.1f} L)",
                    current_value=pl_vol,
                    target_value=plat_base.payload_volume_liters,
                    unit="L",
                )
            )

        if wet_mass_kg > plat_base.max_launch_mass_kg:
            rule_checks.append(
                RuleCheckResult(
                    rule_id="RULE_PLAT_LAUNCH_MASS",
                    category="Mass",
                    status=CheckStatus.FAIL,
                    message=f"Wet mass ({wet_mass_kg:.1f} kg) exceeds platform structural limit ({plat_base.max_launch_mass_kg:.1f} kg)",
                    current_value=wet_mass_kg,
                    target_value=plat_base.max_launch_mass_kg,
                    unit="kg",
                )
            )

        # 2. Power Budget
        pl_power_avg = sum(p.operational_power_w for p in payloads) * 0.25

        opt_power_avg = 0.0
        for opt in conf_plat.resolved_options:
            if opt.equipment.function.value == "propulsion":
                opt_power_avg += opt.equipment.standby_power_w
            else:
                opt_power_avg += opt.equipment.power_w

        total_cons_avg = opt_power_avg + pl_power_avg
        power_margin_w = plat_base.payload_avg_power_w - total_cons_avg
        power_margin_pct = (
            (power_margin_w / plat_base.payload_avg_power_w) * 100.0
            if plat_base.payload_avg_power_w > 0
            else 0.0
        )

        peak_cons = sum(p.peak_power_w for p in payloads) + sum(
            opt.equipment.peak_power_w for opt in conf_plat.resolved_options
        )

        power_b = PowerBudget(
            platform_avg_power_w=plat_base.orbit_avg_power_w,
            options_avg_power_w=round(opt_power_avg, 1),
            payloads_avg_power_w=round(pl_power_avg, 1),
            total_avg_consumption_w=round(total_cons_avg, 1),
            platform_generation_w=plat_base.payload_avg_power_w,
            power_margin_w=round(power_margin_w, 1),
            power_margin_pct=round(power_margin_pct, 1),
            peak_consumption_w=round(peak_cons, 1),
        )

        if power_margin_w < 0:
            rule_checks.append(
                RuleCheckResult(
                    rule_id="RULE_POWER_AVG_DEFICIT",
                    category="Power",
                    status=CheckStatus.FAIL,
                    message=f"Average consumption ({total_cons_avg:.1f} W) exceeds available platform power ({plat_base.payload_avg_power_w:.1f} W)",
                    current_value=total_cons_avg,
                    target_value=plat_base.payload_avg_power_w,
                    unit="W",
                )
            )
        elif power_margin_pct < 15.0:
            rule_checks.append(
                RuleCheckResult(
                    rule_id="RULE_POWER_MARGIN_LOW",
                    category="Power",
                    status=CheckStatus.WARNING,
                    message=f"Power margin is tight ({power_margin_pct:.1f}% < 15% recommended)",
                    current_value=power_margin_pct,
                    target_value=15.0,
                    unit="%",
                )
            )
        else:
            rule_checks.append(
                RuleCheckResult(
                    rule_id="RULE_POWER_OK",
                    category="Power",
                    status=CheckStatus.PASS,
                    message=f"Power margin healthy ({power_margin_pct:.1f}%)",
                    current_value=power_margin_pct,
                    target_value=15.0,
                    unit="%",
                )
            )

        # 3. Cost & Launcher Budget
        launcher_cost = 0.0
        if config.launcher_id and config.launcher_id in self.catalog.launchers:
            ln = self.catalog.launchers[config.launcher_id]
            launcher_cost = ln.price_base_meur + (
                ln.price_per_kg_meur * launch_mass_with_margin_kg
            )
            ln_cap = launcher_capacity_for_orbit(ln, config.orbit)
            if ln_cap <= 0.0:
                rule_checks.append(
                    RuleCheckResult(
                        rule_id="RULE_LAUNCHER_INCOMPATIBLE_ORBIT",
                        category="Launcher",
                        status=CheckStatus.FAIL,
                        message=f"Launcher '{ln.name}' cannot reach orbit {config.orbit.orbit_type.value.upper()} ({config.orbit.altitude_km:.0f} km)",
                        current_value=0.0,
                        target_value=launch_mass_with_margin_kg,
                        unit="kg",
                    )
                )
            elif launch_mass_with_margin_kg > ln_cap:
                rule_checks.append(
                    RuleCheckResult(
                        rule_id="RULE_LAUNCHER_CAPACITY",
                        category="Launcher",
                        status=CheckStatus.FAIL,
                        message=f"Launch mass with margin ({launch_mass_with_margin_kg:.1f} kg) exceeds '{ln.name}' capacity on this orbit ({ln_cap:.1f} kg)",
                        current_value=launch_mass_with_margin_kg,
                        target_value=ln_cap,
                        unit="kg",
                    )
                )
            else:
                rule_checks.append(
                    RuleCheckResult(
                        rule_id="RULE_LAUNCHER_CAPACITY",
                        category="Launcher",
                        status=CheckStatus.PASS,
                        message=f"Launch mass ({launch_mass_with_margin_kg:.1f} kg) within '{ln.name}' capacity ({ln_cap:.1f} kg)",
                        current_value=launch_mass_with_margin_kg,
                        target_value=ln_cap,
                        unit="kg",
                    )
                )
        elif config.launcher_id:
            rule_checks.append(
                RuleCheckResult(
                    rule_id="RULE_LAUNCHER_MISSING",
                    category="Cost",
                    status=CheckStatus.FAIL,
                    message=f"Selected launcher '{config.launcher_id}' not found in catalog",
                )
            )

        # Calibration cost and facility contracts
        calib_items = []
        for cid in getattr(config, "selected_calibration_ids", []):
            if hasattr(self.catalog, "calibrations") and cid in self.catalog.calibrations:
                calib_items.append(self.catalog.calibrations[cid])

        calib_cost = sum(c.price_meur for c in calib_items)
        plat_cost = plat_base.base_price_meur
        opt_cost = sum(opt.final_price_meur for opt in conf_plat.resolved_options)
        pl_cost = sum(p.price_meur for p in payloads)
        total_cost = plat_cost + opt_cost + pl_cost + launcher_cost + calib_cost
        cost_margin = mission.max_budget_meur - total_cost

        # Geographic return accounting across satellite industrial contracts
        # (Platform base + Options + Payloads + Ground Calibration Test Center)
        sat_cost = plat_cost + opt_cost + pl_cost + calib_cost
        cost_by_country_meur: dict[str, float] = {}

        def _add_country_cost(sup_id: str, amount: float) -> None:
            sup = self.catalog.suppliers.get(sup_id)
            country = sup.country if (sup and sup.country) else "Inconnu"
            cost_by_country_meur[country] = cost_by_country_meur.get(country, 0.0) + amount

        _add_country_cost(plat_base.supplier_id, plat_cost)
        for opt in conf_plat.resolved_options:
            _add_country_cost(opt.equipment.supplier_id, opt.final_price_meur)
        for p in payloads:
            _add_country_cost(p.supplier_id, p.price_meur)
        for c in calib_items:
            _add_country_cost(c.supplier_id, c.price_meur)

        cost_by_country_pct: dict[str, float] = {}
        for c, amt in cost_by_country_meur.items():
            cost_by_country_meur[c] = round(amt, 2)
            cost_by_country_pct[c] = round((amt / sat_cost) * 100.0, 1) if sat_cost > 0 else 0.0

        cost_b = CostBudget(
            platform_base_meur=round(plat_cost, 2),
            options_total_meur=round(opt_cost, 2),
            payloads_total_meur=round(pl_cost, 2),
            launcher_meur=round(launcher_cost, 2),
            space_segment_total_meur=round(total_cost, 2),
            mission_budget_limit_meur=mission.max_budget_meur,
            cost_margin_meur=round(cost_margin, 2),
            satellite_cost_meur=round(sat_cost, 2),
            calibration_total_meur=round(calib_cost, 2),
            cost_by_country_meur=cost_by_country_meur,
            cost_by_country_pct=cost_by_country_pct,
        )

        # Calibration rules
        if calib_items:
            has_tvac = any(c.is_thermal_vacuum for c in calib_items)
            tvac_str = "avec cuve vide thermique (TVAC)" if has_tvac else "en salle blanche ambiante"
            tot_weeks = sum(c.duration_weeks for c in calib_items)
            c_names = ", ".join(f"'{c.name}'" for c in calib_items)
            rule_checks.append(
                RuleCheckResult(
                    rule_id="RULE_CALIB_SELECTED",
                    category="AIT & Calibration Sol",
                    status=CheckStatus.PASS,
                    message=(
                        f"Campagne(s) de calibration sol configurée(s) : {c_names} "
                        f"({tvac_str}, durée cumulée {tot_weeks:.1f} sem., budget AIT +{calib_cost:.2f} M€)."
                    ),
                    current_value=calib_cost,
                    unit="M€",
                )
            )
            if has_tvac:
                rule_checks.append(
                    RuleCheckResult(
                        rule_id="RULE_CALIB_TVAC_QUALIFIED",
                        category="AIT & Calibration Sol",
                        status=CheckStatus.PASS,
                        message=(
                            "Qualification en vide thermique (TVAC) validée : l'instrument est caractérisé "
                            "sous vide poussé et cyclage thermique représentatif du vol spatial (athermalisation et cryogénie qualifiées)."
                        ),
                    )
                )
            else:
                rule_checks.append(
                    RuleCheckResult(
                        rule_id="RULE_CALIB_TVAC_QUALIFIED",
                        category="AIT & Calibration Sol",
                        status=CheckStatus.WARNING,
                        message=(
                            "Essais sol limités aux conditions ambiantes ISO 5. Attention : l'absence d'essais en cuve à vide thermique (TVAC) "
                            "ne permet pas de valider la tenue sous vide spatial ni la stabilité du plan focal lors des cyclages d'orbite."
                        ),
                    )
                )
        else:
            rule_checks.append(
                RuleCheckResult(
                    rule_id="RULE_CALIB_NONE",
                    category="AIT & Calibration Sol",
                    status=CheckStatus.WARNING,
                    message="Aucune campagne d'essais/calibration sol dédiée sélectionnée : risque d'anomalie radiométrique ou de défocalisation thermique en orbite.",
                )
            )

        if total_cost > mission.max_budget_meur:
            compliance_checks.append(
                RuleCheckResult(
                    rule_id="REQ_BUDGET_EXCEEDED",
                    category="Mission Budget",
                    status=CheckStatus.FAIL,
                    message=f"Total cost ({total_cost:.2f} M€) exceeds mission ceiling ({mission.max_budget_meur:.2f} M€)",
                    current_value=total_cost,
                    target_value=mission.max_budget_meur,
                    unit="M€",
                )
            )
        else:
            compliance_checks.append(
                RuleCheckResult(
                    rule_id="REQ_BUDGET_OK",
                    category="Mission Budget",
                    status=CheckStatus.PASS,
                    message=f"Total cost ({total_cost:.2f} M€) within budget ({mission.max_budget_meur:.2f} M€)",
                    current_value=total_cost,
                    target_value=mission.max_budget_meur,
                    unit="M€",
                )
            )

        # 3b. Geographic Return Compliance Checks (ESA juste retour industriel)
        for grc in mission.geo_return_constraints:
            act_pct = cost_by_country_pct.get(grc.country, 0.0)
            act_meur = cost_by_country_meur.get(grc.country, 0.0)
            is_ok = (grc.min_pct <= act_pct <= grc.max_pct)
            status = CheckStatus.PASS if is_ok else CheckStatus.FAIL

            if is_ok:
                msg = (
                    f"Retour géographique {grc.country} : {act_pct:.1f}% ({act_meur:.2f} M€) — "
                    f"Conforme à la souscription ESA [{grc.min_pct:.1f} %, {grc.max_pct:.1f} %]"
                )
            else:
                msg = (
                    f"Retour géographique {grc.country} : {act_pct:.1f}% ({act_meur:.2f} M€) — "
                    f"Hors fourchette ESA [{grc.min_pct:.1f} %, {grc.max_pct:.1f} %]. "
                    f"Ajuster la répartition des fournisseurs (plateforme, options ou charges utiles) pour respecter le juste retour !"
                )

            compliance_checks.append(
                RuleCheckResult(
                    rule_id=f"RULE_GEORETURN_{grc.country.upper()}",
                    category="Retour Géographique ESA",
                    status=status,
                    message=msg,
                    current_value=act_pct,
                    target_value=grc.min_pct,
                    unit="%",
                )
            )

        # 3c. Non-ESA / Third-Country Procurement Ceiling Check (marge COTS / mondial)
        if mission.geo_return_constraints:
            max_non_esa = getattr(mission, "max_non_esa_spend_pct", 15.0)
            non_esa_meur = sum(
                amt for c_name, amt in cost_by_country_meur.items()
                if c_name not in ESA_MEMBER_STATES and c_name != "Inconnu"
            )
            non_esa_pct = round((non_esa_meur / sat_cost) * 100.0, 1) if sat_cost > 0 else 0.0
            is_non_esa_ok = (non_esa_pct <= max_non_esa)
            status_non_esa = CheckStatus.PASS if is_non_esa_ok else CheckStatus.FAIL

            if is_non_esa_ok:
                if non_esa_pct > 0:
                    msg_non_esa = (
                        f"Achats hors États membres ESA (pays tiers / COTS) : {non_esa_pct:.1f}% ({non_esa_meur:.2f} M€) — "
                        f"Conforme au plafond autorisé de {max_non_esa:.1f} %"
                    )
                else:
                    msg_non_esa = (
                        f"Achats hors États membres ESA : 0.0% — Conforme (100% européen, marge autorisée max {max_non_esa:.1f} % pour composants tiers/COTS)"
                    )
            else:
                msg_non_esa = (
                    f"Achats hors États membres ESA : {non_esa_pct:.1f}% ({non_esa_meur:.2f} M€) — "
                    f"Dépasse le plafond autorisé de {max_non_esa:.1f} % pour les pays tiers (COTS mondiaux / hors Europe). "
                    f"Privilégier des fournisseurs européens pour rester sous les {max_non_esa:.1f} % !"
                )

            compliance_checks.append(
                RuleCheckResult(
                    rule_id="RULE_GEORETURN_NON_ESA_CAP",
                    category="Retour Géographique ESA",
                    status=status_non_esa,
                    message=msg_non_esa,
                    current_value=non_esa_pct,
                    target_value=max_non_esa,
                    unit="%",
                )
            )

        # 4. Pointing Compatibility Check
        effective_pointing_accuracy_deg = plat_base.pointing_accuracy_deg
        for opt in conf_plat.resolved_options:
            if opt.equipment.function.value == "adcs":
                adcs_acc = opt.equipment.specs.get("pointing_accuracy_deg")
                if adcs_acc is not None and adcs_acc < effective_pointing_accuracy_deg:
                    effective_pointing_accuracy_deg = adcs_acc

        for req in mission.requirements:
            if req.parameter == "pointing_accuracy_deg":
                thresh = float(req.threshold)
                pass_pt = (
                    effective_pointing_accuracy_deg <= thresh
                    if req.operator == RequirementOperator.LE
                    else False
                )
                compliance_checks.append(
                    RuleCheckResult(
                        rule_id=req.id,
                        category="Mission Requirement",
                        status=CheckStatus.PASS if pass_pt else CheckStatus.FAIL,
                        message=f"{req.title}: platform pointing accuracy = {effective_pointing_accuracy_deg}° (threshold: {thresh}°)",
                        current_value=effective_pointing_accuracy_deg,
                        target_value=thresh,
                        unit="deg",
                    )
                )
            elif req.parameter == "design_lifetime_years":
                thresh = float(req.threshold)
                pass_lt = (
                    plat_base.design_lifetime_years >= thresh
                    if req.operator == RequirementOperator.GE
                    else plat_base.design_lifetime_years <= thresh
                )
                compliance_checks.append(
                    RuleCheckResult(
                        rule_id=req.id,
                        category="Mission Requirement",
                        status=CheckStatus.PASS if pass_lt else CheckStatus.FAIL,
                        message=f"{req.title}: platform design lifetime = {plat_base.design_lifetime_years:.1f} yr (threshold: {thresh:.1f} yr)",
                        current_value=plat_base.design_lifetime_years,
                        target_value=thresh,
                        unit="yr",
                    )
                )

        for pl in payloads:
            if effective_pointing_accuracy_deg > pl.required_pointing_accuracy_deg:
                rule_checks.append(
                    RuleCheckResult(
                        rule_id=f"RULE_POINTING_{pl.id}",
                        category="ADCS Compatibility",
                        status=CheckStatus.FAIL,
                        message=f"Platform pointing accuracy ({effective_pointing_accuracy_deg}°) is worse than required by '{pl.name}' ({pl.required_pointing_accuracy_deg}°)",
                        current_value=effective_pointing_accuracy_deg,
                        target_value=pl.required_pointing_accuracy_deg,
                        unit="deg",
                    )
                )
            else:
                rule_checks.append(
                    RuleCheckResult(
                        rule_id=f"RULE_POINTING_{pl.id}",
                        category="ADCS Compatibility",
                        status=CheckStatus.PASS,
                        message=f"Pointing accuracy ({effective_pointing_accuracy_deg}°) meets requirement for '{pl.name}' ({pl.required_pointing_accuracy_deg}°)",
                        current_value=effective_pointing_accuracy_deg,
                        target_value=pl.required_pointing_accuracy_deg,
                        unit="deg",
                    )
                )

        # 5. Generic Payload Performances & Mission Requirements Verification
        payload_perfs: dict[str, Any] = {}
        for pl in payloads:
            p_dict, p_compliance = evaluate_payload_requirements(
                pl,
                config.orbit,
                mission,
                all_payloads=payloads,
                resolved_options=conf_plat.resolved_options,
            )
            payload_perfs[pl.id] = p_dict
            compliance_checks.extend(p_compliance)

        return SystemBudgets(
            configured_platform=conf_plat,
            mass=mass_b,
            power=power_b,
            cost=cost_b,
            payload_performances=payload_perfs,
            rule_checks=rule_checks,
            compliance_checks=compliance_checks,
        )
