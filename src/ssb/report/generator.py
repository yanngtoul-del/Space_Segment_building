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
            if i > 0 and abs(lons[i] - lons[i - 1]) > 180:
                ax.plot(seg_lons, seg_lats, color="#00d2d3", linewidth=1.5, alpha=0.85)
                seg_lons = [lons[i]]
                seg_lats = [lats[i]]
            else:
                seg_lons.append(lons[i])
                seg_lats.append(lats[i])
        if seg_lons:
            ax.plot(seg_lons, seg_lats, color="#00d2d3", linewidth=1.5, label="Satellite Track")

        eclipse_lons = [lons[i] for i in range(len(lons)) if eclipses[i]]
        eclipse_lats = [lats[i] for i in range(len(lats)) if eclipses[i]]
        if eclipse_lons:
            ax.scatter(eclipse_lons, eclipse_lats, color="#ff6b6b", s=8, alpha=0.7, label="Eclipse")

        ax.set_title("Satellite Ground Track & Eclipse Passes", color="#1e272e", fontsize=11, fontweight="bold")
        ax.set_xlabel("Longitude (°)", fontsize=9)
        ax.set_ylabel("Latitude (°)", fontsize=9)
        ax.legend(loc="lower right", facecolor="#ffffff", edgecolor="#bdc3c7", fontsize=8)

        plt.tight_layout()
        plt.savefig(output_image_path, format="png")
        plt.close(fig)

    @classmethod
    def generate(
        cls,
        project: StudentProject,
        budgets: SystemBudgets,
        output_docx_path: Path | str,
        ground_track: list | None = None,
    ) -> Path:
        out_path = Path(output_docx_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        doc = Document()
        primary_color = RGBColor(26, 82, 118)

        # 1. Document Title
        title_p = doc.add_paragraph()
        title_run = title_p.add_run("RAPPORT DE CONCEPTION SYSTÈME SPATIAL")
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
        p_bud = doc.add_paragraph()
        p_bud.add_run(
            f"Budget total plafond alloué : {m.max_budget_meur:.2f} M€ TTC (plateforme + options + charge utile + lancement) "
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
            plot_path = out_path.parent / f"ground_track_{project.project_id}.png"
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
        r_pow[3].text = f"{budgets.power.power_margin_pct:.1f} %"

        r_cost = t_bud.add_row().cells
        r_cost[0].text = "Coût Total Segment Spatial"
        r_cost[1].text = f"{budgets.cost.space_segment_total_meur:.2f} M€"
        r_cost[2].text = f"{budgets.cost.mission_budget_limit_meur:.2f} M€"
        r_cost[3].text = f"{budgets.cost.cost_margin_meur:+.2f} M€"

        # 5. Matrice de Conformité aux Exigences
        doc.add_heading("4. Matrice de Conformité aux Exigences & Règles", level=1)
        t_comp = doc.add_table(rows=1, cols=4)
        t_comp.alignment = WD_TABLE_ALIGNMENT.CENTER
        h_comp = t_comp.rows[0].cells
        h_comp[0].text = "Exigence / Règle"
        h_comp[1].text = "Statut"
        h_comp[2].text = "Valeur"
        h_comp[3].text = "Commentaire"
        for c in h_comp:
            c.paragraphs[0].runs[0].font.bold = True

        for chk in (budgets.compliance_checks + budgets.rule_checks):
            r = t_comp.add_row().cells
            r[0].text = chk.rule_id
            r[1].text = chk.status.value.upper()
            val_txt = f"{chk.current_value} {chk.unit}" if chk.current_value is not None else "-"
            r[2].text = val_txt
            r[3].text = chk.message

        # 6. Sections à compléter par l'étudiant
        doc.add_page_break()
        doc.add_heading("5. Concept d'Opérations (CONOPS) — À Rédiger par l'Étudiant", level=1)
        p_conops_intro = doc.add_paragraph()
        p_conops_intro.add_run(
            "[CADRE ÉTUDIANT - DÉCRIVEZ LES MODES OPÉRATIONNELS (LEOP, COMMISSIONING, NOMINAL, VISIBILITÉ STATIONS, GESTION DES ANOMALIES)]\n"
        ).italic = True
        conops_box = doc.add_paragraph(project.conops_text if project.conops_text else "\n\n\n\n\n")
        conops_box.paragraph_format.left_indent = Inches(0.5)

        doc.add_heading("6. Justification des Choix Techniques & Arbitrages", level=1)
        p_just_intro = doc.add_paragraph()
        p_just_intro.add_run(
            "[CADRE ÉTUDIANT - JUSTIFIEZ LE COMPROMIS ENTRE L'OUVERTURE DE L'INSTRUMENT, L'ALTITUDE D'ORBITE, LE CHOIX DE LA PLATEFORME ET LE COÛT]\n"
        ).italic = True
        just_box = doc.add_paragraph(project.justification_text if project.justification_text else "\n\n\n\n\n")
        just_box.paragraph_format.left_indent = Inches(0.5)

        doc.add_heading("7. Analyse des Risques et Perspectives", level=1)
        p_risk_intro = doc.add_paragraph()
        p_risk_intro.add_run(
            "[CADRE ÉTUDIANT - ANALYSE DE LA DURÉE DE VIE, MARGES DE DÉPENSES ÉNERGÉTIQUES, DÉGRADATION DES PERFORMANCES EN FIN DE VIE]\n"
        ).italic = True
        risk_box = doc.add_paragraph(project.risk_analysis_text if project.risk_analysis_text else "\n\n\n\n\n")
        risk_box.paragraph_format.left_indent = Inches(0.5)

        doc.save(str(out_path))
        return out_path
