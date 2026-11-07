"""Platform slot assembly and configuration resolution engine."""

from dataclasses import dataclass, field
from ssb.core.platform import PlatformBase, Equipment, SubsystemFunction
from ssb.core.project import SelectedOption
from ssb.catalog.database import CatalogDatabase


@dataclass
class ResolvedEquipment:
    equipment: Equipment
    is_included: bool
    override_price_meur: float | None = None
    override_mass_kg: float | None = None
    integration_cost_meur: float = 0.0

    @property
    def final_price_meur(self) -> float:
        if self.is_included:
            # Included equipment adds 0 to extra price, only replacement would cost
            return 0.0
        base = self.override_price_meur if self.override_price_meur is not None else self.equipment.price_meur
        return base + self.integration_cost_meur

    @property
    def final_mass_kg(self) -> float:
        if self.override_mass_kg is not None:
            return self.override_mass_kg
        return self.equipment.mass_kg


@dataclass
class ConfiguredPlatform:
    """Platform with all options resolved and applied."""

    base: PlatformBase
    resolved_options: list[ResolvedEquipment] = field(default_factory=list)
    validation_errors: list[str] = field(default_factory=list)
    validation_warnings: list[str] = field(default_factory=list)

    @property
    def total_platform_cost_meur(self) -> float:
        extra = sum(opt.final_price_meur for opt in self.resolved_options)
        return self.base.base_price_meur + extra

    @property
    def total_platform_dry_mass_kg(self) -> float:
        options_mass = sum(opt.final_mass_kg for opt in self.resolved_options)
        return self.base.dry_mass_kg + options_mass

    @property
    def total_power_consumption_options_w(self) -> float:
        return sum(opt.equipment.power_w for opt in self.resolved_options)


class PlatformConfigurator:
    """Applies student selections onto a platform according to slot rules (D15-D21)."""

    def __init__(self, catalog: CatalogDatabase) -> None:
        self.catalog = catalog

    def configure(
        self, platform_id: str, selections: list[SelectedOption]
    ) -> ConfiguredPlatform:
        if platform_id not in self.catalog.platforms:
            res = ConfiguredPlatform(base=None)  # type: ignore
            res.validation_errors.append(f"Platform '{platform_id}' not found in catalog")
            return res

        platform = self.catalog.platforms[platform_id]
        configured = ConfiguredPlatform(base=platform)

        # Map selections by slot function
        selections_by_func: dict[str, list[SelectedOption]] = {}
        for sel in selections:
            selections_by_func.setdefault(sel.slot_function, []).append(sel)

        for slot in platform.slots:
            func_key = slot.function.value if hasattr(slot.function, "value") else str(slot.function)
            slot_sels = selections_by_func.get(func_key, [])

            # If nothing selected for this slot, automatically retain the default included equipments
            if not slot_sels and slot.included_equipment_ids:
                for inc_id in slot.included_equipment_ids:
                    if inc_id in self.catalog.equipments:
                        eq = self.catalog.equipments[inc_id]
                        configured.resolved_options.append(
                            ResolvedEquipment(equipment=eq, is_included=True)
                        )
                # Included items satisfy the min_qty requirement
                continue

            # Count total quantity explicitly selected for this slot
            total_qty = sum(s.quantity for s in slot_sels)

            # Check min/max quantities
            if total_qty < slot.min_qty:
                configured.validation_errors.append(
                    f"Slot '{func_key}' requires at least {slot.min_qty} equipment(s) (selected: {total_qty})"
                )
            if total_qty > slot.max_qty:
                configured.validation_errors.append(
                    f"Slot '{func_key}' allows at most {slot.max_qty} equipment(s) (selected: {total_qty})"
                )

            # Process explicit student selections
            for sel in slot_sels:
                eq_id = sel.equipment_id
                if eq_id not in slot.allowed_equipment_ids:
                    configured.validation_errors.append(
                        f"Equipment '{eq_id}' is not allowed in slot '{func_key}' on platform '{platform.name}'"
                    )
                    continue

                if eq_id not in self.catalog.equipments:
                    configured.validation_errors.append(
                        f"Equipment '{eq_id}' not found in catalog"
                    )
                    continue

                eq = self.catalog.equipments[eq_id]
                is_inc = eq_id in slot.included_equipment_ids

                # Local overrides (D19)
                overrides = slot.equipment_overrides.get(eq_id, {})
                price_override = overrides.get("price_meur")
                mass_override = overrides.get("mass_kg")

                # Integration cost
                effective_price = price_override if price_override is not None else eq.price_meur
                integ_cost = slot.integration_cost_fixed_meur + (
                    slot.integration_cost_pct / 100.0 * effective_price
                )

                for _ in range(sel.quantity):
                    configured.resolved_options.append(
                        ResolvedEquipment(
                            equipment=eq,
                            is_included=is_inc,
                            override_price_meur=price_override,
                            override_mass_kg=mass_override,
                            integration_cost_meur=integ_cost if not is_inc else 0.0,
                        )
                    )

        return configured
