"""Automatic Word (.docx) report generator for student exams."""

from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
import matplotlib.pyplot as plt
import numpy as np

from ssb.core.project import StudentProject
from ssb.system.evaluator import SystemBudgets
from ssb.core.catalog_meta import ESA_MEMBER_STATES
from ssb.core.paths import images_dir


class ReportGenerator:
    """Generates structured .docx report with mission specification sheet, budgets, compliance matrix, and editable student sections."""

    @classmethod
    def generate_ground_track_plot(
        cls, ground_track: list, output_image_path: Path
    ) -> None:
        """Create a clean 2D equirectangular ground track map using matplotlib."""
        fig, ax = plt.subplots(figsize=(8, 4), dpi=150)
        ax.set_facecolor("#0b1426")
        fig.patch.set_facecolor("#ffffff")

        ax.set_xlim(-180, 180)
        ax.set_ylim(-90, 90)
        ax.set_xticks(np.arange(-180, 181, 60))
        ax.set_yticks(np.arange(-90, 91, 30))
        ax.grid(True, color="#2c3e50", linestyle="--", alpha=0.5)
        ax.axhline(0, color="#7f8c8d", linestyle="-", linewidth=0.8, alpha=0.7)

        lons = [p.longitude_deg for p in ground_track]
        lats = [p.latitude_deg for p in ground_track]
        eclipses = [p.in_eclipse for p in ground_track]

        seg_lons: list[float] = []
        seg_lats: list[float] = []
        for i in range(len(lons)):
            seg_lons.append(lons[i])
            seg_lats.append(lats[i])
            if i < len(lons) - 1 and abs(lons[i + 1] - lons[i]) > 180:
                ax.plot(seg_lons, seg_lats, color="#00ffff", linewidth=1.5, alpha=0.85)
                seg_lons = []
                seg_lats = []
        if seg_lons:
            ax.plot(seg_lons, seg_lats, color="#00ffff", linewidth=1.5, alpha=0.85)

        ecl_lons = [lons[i] for i, e in enumerate(eclipses) if e]
        ecl_lats = [lats[i] for i, e in enumerate(eclipses) if e]
        if ecl_lons:
            ax.scatter(ecl_lons, ecl_lats, color="#34495e", s=6, label="Éclipse (ombre)", zorder=3)

        sun_lons = [lons[i] for i, e in enumerate(eclipses) if not e]
        sun_lats = [lats[i] for i, e in enumerate(eclipses) if not e]
        if sun_lons:
            ax.scatter(sun_lons, sun_lats, color="#f1c40f", s=8, label="Ensoleillé", zorder=4)

        if lons:
            ax.scatter([lons[0]], [lats[0]], color="#2ecc71", s=60, marker="o", edgecolors="white", label="Point initial (t0)", zorder=5)

        ax.set_xlabel("Longitude (°)", fontsize=9, color="#1e293b")
        ax.set_ylabel("Latitude (°)", fontsize=9, color="#1e293b")
        ax.set_title("Trace au Sol Orbitale — 24 heures de propagation", fontsize=11, fontweight="bold", color="#0f2744")
        ax.legend(loc="lower right", fontsize=8, facecolor="#ffffff", framealpha=0.9)
        plt.tight_layout()
        fig.savefig(output_image_path, bbox_inches="tight")
        plt.close(fig)

    @classmethod
    def generate(
        cls,
        project: StudentProject,
        budgets: SystemBudgets,
        compliance_matrix: list[dict] | None = None,
        ground_track: list | None = None,
        out_path: Path | None = None,
        output_docx_path: Path | str | None = None,
    ) -> Path:
        resolved_path = Path(out_path or output_docx_path)
        compliance_matrix = compliance_matrix or []

        doc = Document()

        # Styles definition
        primary_color = RGBColor(15, 39, 68)  # Deep Navy #0f2744

        # 1. Page de Garde / En-tête
        title_p = doc.add_paragraph()
        title_run = title_p.add_run("RAPPORT D'AVANT-PROJET SPATIAL — SEGMENT VOL")
        title_run.font.size = Pt(20)
        title_run.font.bold = True
        title_run.font.color.rgb = primary_color
        title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER

        m = project.mission
        sub_p = doc.add_paragraph()
        sub_p.add_run(f"Mission : {m.title} ({m.id})\n").bold = True
        if m.domain_label:
            sub_p.add_run(f"Domaine : {m.domain_label} | Commanditaire : {m.client_agency}\n")
        sub_p.add_run(f"Étudiant : {project.student_name} (ID: {project.student_id})\n")
        sub_p.add_run(f"Empreinte numérique d'intégrité (SHA-256) : {project.compute_hash()[:16]}...")
        sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_paragraph()

        # 2. Fiche de Spécification Mission & Exigences
        h2 = doc.add_heading("1. Fiche de Spécification de la Mission et Exigences", level=1)
        h2.paragraph_format.space_before = Pt(12)

        # Mission illustration
        if m.image:
            img_path = images_dir() / m.image
            if img_path.exists():
                p_img = doc.add_paragraph()
                p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_img_run = p_img.add_run()
                p_img_run.add_picture(str(img_path), width=Inches(4.8))
                cap = doc.add_paragraph()
                cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
                cap_run = cap.add_run(f"Figure 1 : Vue d'artiste / concept opérationnel — {m.title}")
                cap_run.font.size = Pt(9)
                cap_run.font.italic = True

        p_bud = doc.add_paragraph()
        p_bud.add_run(
            f"Budget total plafond alloué : {m.max_budget_meur:.2f} M€ TTC (plateforme + options + charge utile + essais sol + lancement) "
            f"| Durée de vie cible : {m.target_lifetime_years} ans | TRL minimal : {m.min_trl}"
        ).bold = True
        doc.add_paragraph(f"Contexte opérationnel : {m.context}")
        if m.primary_objective:
            doc.add_paragraph(f"Objectif principal décrit : {m.primary_objective}")
        if m.scientific_or_operational_need:
            doc.add_paragraph(f"Besoin scientifique / opérationnel : {m.scientific_or_operational_need}")
        if m.orbit_constraints_description:
            doc.add_paragraph(f"Contraintes orbitales : {m.orbit_constraints_description}")
        if m.conops_guidance:
            doc.add_paragraph(f"Orientation CONOPS : {m.conops_guidance}")

        t_req = doc.add_table(rows=1, cols=4)
        t_req.alignment = WD_TABLE_ALIGNMENT.CENTER
        hdr_cells = t_req.rows[0].cells
        hdr_cells[0].text = "ID"
        hdr_cells[1].text = "Intitulé"
        hdr_cells[2].text = "Seuil"
        hdr_cells[3].text = "Unité"
        for c in hdr_cells:
            c.paragraphs[0].runs[0].font.bold = True

        for req in m.requirements:
            row_cells = t_req.add_row().cells
            row_cells[0].text = req.id
            row_cells[1].text = req.title
            row_cells[2].text = f"{req.operator.value} {req.threshold}"
            row_cells[3].text = req.unit

        # 3. Architecture Retenue
        doc.add_heading("2. Architecture du Segment Spatial", level=1)
        plat = budgets.configured_platform.base
        p_arch = doc.add_paragraph()
        p_arch.add_run("• Plateforme sélectionnée : ").bold = True
        p_arch.add_run(f"{plat.name} ({plat.supplier_name}) — Catégorie {plat.category}\n")
        p_arch.add_run("• Orbite : ").bold = True
        p_arch.add_run(
            f"{project.configuration.orbit.orbit_type.value.upper()} @ {project.configuration.orbit.altitude_km} km "
            f"(i = {project.configuration.orbit.inclination_deg}°)\n"
        )
        p_arch.add_run("• Options & Sous-systèmes configurés :\n").bold = True
        for opt in budgets.configured_platform.resolved_options:
            inc_tag = " (Inclus)" if opt.is_included else f" (+{opt.final_price_meur:.2f} M€)"
            p_arch.add_run(f"   - [{opt.equipment.function.value.upper()}] {opt.equipment.name}{inc_tag}\n")

        if ground_track:
            plot_path = resolved_path.parent / f"ground_track_{project.project_id}.png"
            cls.generate_ground_track_plot(ground_track, plot_path)
            doc.add_picture(str(plot_path), width=Inches(6.0))

        # 4. Budgets Système
        doc.add_heading("3. Budgets Système (Masse, Puissance, Coût)", level=1)
        t_bud = doc.add_table(rows=1, cols=4)
        t_bud.alignment = WD_TABLE_ALIGNMENT.CENTER
        h_bud = t_bud.rows[0].cells
        h_bud[0].text = "Budget"
        h_bud[1].text = "Valeur Calculée"
        h_bud[2].text = "Capacité / Plafond"
        h_bud[3].text = "Marge"
        for c in h_bud:
            c.paragraphs[0].runs[0].font.bold = True

        r_mass = t_bud.add_row().cells
        r_mass[0].text = "Masse au Lancement (avec 20% marge)"
        r_mass[1].text = f"{budgets.mass.launch_mass_with_margin_kg:.1f} kg"
        r_mass[2].text = f"{plat.max_launch_mass_kg:.1f} kg (plateforme)"
        r_mass[3].text = f"+{budgets.mass.margin_pct:.0f} %"

        r_pow = t_bud.add_row().cells
        r_pow[0].text = "Consommation Moyenne Orbite"
        r_pow[1].text = f"{budgets.power.total_avg_consumption_w:.1f} W"
        r_pow[2].text = f"{budgets.power.platform_generation_w:.1f} W"
        r_pow[3].text = f"{budgets.power.power_margin_pct:+.1f} %"

        r_cost = t_bud.add_row().cells
        r_cost[0].text = "Coût Total Consolidé (Sat + Essais Sol + Lanceur)"
        r_cost[1].text = f"{budgets.cost.space_segment_total_meur:.2f} M€"
        r_cost[2].text = f"{budgets.cost.mission_budget_limit_meur:.2f} M€"
        r_cost[3].text = f"{budgets.cost.cost_margin_meur:+.2f} M€"

        # 5. Répartition Géographique (Juste Retour Industriel ESA)
        doc.add_heading("4. Analyse du Retour Géographique Industriel", level=1)
        p_geo = doc.add_paragraph()
        p_geo.add_run(
            "Dans le cadre des règles d'approvisionnement inspirées des programmes ESA, les achats industriels "
            "(plateforme, options, charges utiles, campagnes d'essais/calibration sol) sont ventilés selon le pays d'origine du fournisseur. "
            "Les achats hors Europe (COTS mondiaux) sont plafonnés à 15 % du total.\n"
        )
        t_geo = doc.add_table(rows=1, cols=3)
        t_geo.alignment = WD_TABLE_ALIGNMENT.CENTER
        h_geo = t_geo.rows[0].cells
        h_geo[0].text = "Pays / Région Fournisseur"
        h_geo[1].text = "Montant Dépensé (M€)"
        h_geo[2].text = "Part Industrielle (%)"
        for c in h_geo:
            c.paragraphs[0].runs[0].font.bold = True

        tot_spend = sum(budgets.cost.cost_by_country_meur.values()) or 1.0
        for country, amount in sorted(budgets.cost.cost_by_country_meur.items(), key=lambda x: -x[1]):
            pct = budgets.cost.cost_by_country_pct.get(country, (amount / tot_spend) * 100.0)
            r_g = t_geo.add_row().cells
            flag = "🇪🇺 " if country in ESA_MEMBER_STATES else "🌐 "
            r_g[0].text = f"{flag}{country}"
            r_g[1].text = f"{amount:.2f} M€"
            r_g[2].text = f"{pct:.1f} %"

        # 6. Matrice de Conformité
        doc.add_heading("5. Matrice de Conformité aux Exigences", level=1)
        t_mat = doc.add_table(rows=1, cols=4)
        t_mat.alignment = WD_TABLE_ALIGNMENT.CENTER
        h_mat = t_mat.rows[0].cells
        h_mat[0].text = "Exigence"
        h_mat[1].text = "Spécifié"
        h_mat[2].text = "Obtenu"
        h_mat[3].text = "Statut"
        for c in h_mat:
            c.paragraphs[0].runs[0].font.bold = True

        for item in compliance_matrix:
            row = t_mat.add_row().cells
            row[0].text = item.get("id", "")
            row[1].text = item.get("required", "")
            row[2].text = item.get("actual", "")
            status = item.get("status", "")
            row[3].text = status
            if status == "COMPLIANT":
                row[3].paragraphs[0].runs[0].font.color.rgb = RGBColor(46, 204, 113)
            elif status == "NON_COMPLIANT":
                row[3].paragraphs[0].runs[0].font.color.rgb = RGBColor(231, 76, 60)
            elif status == "WARNING":
                row[3].paragraphs[0].runs[0].font.color.rgb = RGBColor(241, 196, 15)

        # 7. Cadres Rédactionnels Étudiants
        doc.add_heading("6. Justifications Techniques, Arbitrages & Demandes de Dérogation (Waivers)", level=1)

        doc.add_heading("6.1. Concept d'Opérations (CONOPS) et Segment Sol", level=2)
        conops_val = project.conops_text.strip() if project.conops_text else (
            "[CADRE ÉTUDIANT - DÉCRIVEZ LES MODES OPÉRATIONNELS (LEOP, COMMISSIONING, NOMINAL, VISIBILITÉ STATIONS, GESTION DES ÉCLIPSES)]"
        )
        p_ed1 = doc.add_paragraph(conops_val)
        if not project.conops_text.strip():
            p_ed1.runs[0].font.italic = True
            p_ed1.runs[0].font.color.rgb = RGBColor(127, 140, 141)

        doc.add_heading("6.2. Justification des choix d'architecture, arbitrages d'altitude et retour géographique ESA", level=2)
        justif_val = project.justification_text.strip() if project.justification_text else (
            "[CADRE ÉTUDIANT - EXPLIQUEZ LES COMPROMIS ENTRE L'ALTITUDE, LA CHARGE UTILE, LA PLATEFORME, LA CALIBRATION TVAC ET LE RETOUR GÉOGRAPHIQUE ESA]"
        )
        p_ed2 = doc.add_paragraph(justif_val)
        if not project.justification_text.strip():
            p_ed2.runs[0].font.italic = True
            p_ed2.runs[0].font.color.rgb = RGBColor(127, 140, 141)

        doc.add_heading("6.3. Justification des Non-Conformités (Demandes de Dérogation / Waivers), Risques et Marges", level=2)
        risks_val = project.risk_analysis_text.strip() if project.risk_analysis_text else (
            "[CADRE ÉTUDIANT - JUSTIFIEZ ICI TOUTE NON-CONFORMITÉ ASSUMÉE (EXIGENCE PHYSIQUEMENT OU BUDGÉTAIREMENT ANTAGONISTE, DEMANDE DE DÉROGATION / WAIVER) AINSI QUE L'ANALYSE DES RISQUES ET MARGES SYSTÈME]"
        )
        p_ed3 = doc.add_paragraph(risks_val)
        if not project.risk_analysis_text.strip():
            p_ed3.runs[0].font.italic = True
            p_ed3.runs[0].font.color.rgb = RGBColor(127, 140, 141)

        doc.save(resolved_path)
        return resolved_path
