"""Shared helpers for the catalog source files (development tool, not shipped)."""

SUPPLIER_NAMES = {
    # platforms
    "newspace_micro": "AeroMicro Dynamics",
    "sstl_inspired": "Albion Satellite Technologies",
    "heritage_aero": "Astra Space Systems",
    "apex_inspired": "Apex Orbital Manufacturing",
    "heritage_prime": "AeroPrime Defense & Space",
    # equipment
    "orbital_prop": "PlasmaTech Propulsion",
    "comms_euro": "EuroSpace Link",
    "space_avionics": "Starlight Avionics",
    "gyro_dyn": "Gyrodyne Attitude Systems",
    # payloads
    "optics_lab": "AeroOptics Instruments",
    "heritage_optics": "Helios Space Instruments",
    "stellare_ottica": "Stellara Ottica",
    "cirrus_ir": "Cirrus Infrared Systems",
    "spectra_tech": "SpectraSpace Instruments",
    "radar_tech": "NovaRadar Systems",
    "boreal_sar": "Boreal Radar Technologies",
    "laser_space": "PhotonCom Optics",
    "tesa_link": "TeraLink Photonics",
    "quanta_space": "QuantaSpace Technologies",
    "rf_payload": "Meridian RF Payloads",
    # launchers
    "launch_global": "Aether Launch Services",
    "heritage_launch": "EuroSpace Launch Consortium",
    "polar_launch": "Borealis Launch Systems",
}


def base(item_id: str, supplier_id: str, **kw) -> dict:
    d = {"id": item_id, "supplier_id": supplier_id, "supplier_name": SUPPLIER_NAMES[supplier_id]}
    d.update(kw)
    return d
