"""Dedicated Mission Specification Sheet (Fiche de Spécification Mission) viewer widget."""

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor
from PySide6.QtWidgets import (
    QScrollArea,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)
from ssb.core.mission import MissionSpecification


MISSION_TYPE_BADGES_FR = {
    "optical_eo": "Observation de la Terre — Optique",
    "sar_eo": "Observation de la Terre — Radar SAR",
    "atmosphere": "Connaissance de l'Atmosphère Terrestre",
    "cosmology": "Cosmologie & Astrophysique Spatiale",
    "telecom_opt": "Télécommunications — Liaison Optique Haut Débit",
    "telecom_radio": "Télécommunications & Collecte RF",
    "qkd": "Cryptographie Quantique Spatiale (QKD)",
    "science": "Mission Scientifique",
}


class MissionSheetView(QScrollArea):
    """Renders a complete, structured 'Fiche de Spécification Mission' for the student."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.Shape.NoFrame)

        self._container = QWidget()
        self._layout = QVBoxLayout(self._container)
        self._layout.setContentsMargins(6, 6, 6, 6)
        self._layout.setSpacing(10)
        self.setWidget(self._container)

        # 1. Top dark-blue banner: Title, ID, Client, Domain, Total Budget, Lifetime, Min TRL
        banner = QFrame()
        banner.setStyleSheet(
            "QFrame { background: #0f2744; border: 1px solid #1e4976; border-radius: 6px; padding: 8px; }"
            "QLabel { color: #f8fafc; }"
        )
        bl = QHBoxLayout(banner)

        left_col = QVBoxLayout()
        self.lbl_title = QLabel()
        self.lbl_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffffff;")
        self.lbl_subtitle = QLabel()
        self.lbl_subtitle.setStyleSheet("font-size: 12px; color: #93c5fd;")
        left_col.addWidget(self.lbl_title)
        left_col.addWidget(self.lbl_subtitle)
        bl.addLayout(left_col, stretch=1)

        right_col = QHBoxLayout()
        self.lbl_budget_box = QLabel()
        self.lbl_budget_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_budget_box.setStyleSheet(
            "background: #1e3a5f; border: 1px solid #fbbf24; border-radius: 5px; padding: 6px 12px; "
            "color: #fbbf24; font-weight: bold; font-size: 13px;"
        )
        self.lbl_life_box = QLabel()
        self.lbl_life_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_life_box.setStyleSheet(
            "background: #1e3a5f; border: 1px solid #38bdf8; border-radius: 5px; padding: 6px 12px; "
            "color: #e0f2fe; font-weight: bold; font-size: 12px;"
        )
        right_col.addWidget(self.lbl_budget_box)
        right_col.addWidget(self.lbl_life_box)
        bl.addLayout(right_col)
        self._layout.addWidget(banner)

        # 2. Narrative card: Context, Primary Objective, Secondary Objectives, Need, Orbit & CONOPS guidance
        card = QFrame()
        card.setStyleSheet(
            "QFrame { background: #f8fafc; color: #0f172a; border: 1px solid #cbd5e1; border-radius: 6px; padding: 8px; }"
            "QLabel { color: #0f172a; }"
        )
        cl = QVBoxLayout(card)
        self.lbl_narrative = QLabel()
        self.lbl_narrative.setWordWrap(True)
        self.lbl_narrative.setTextFormat(Qt.TextFormat.RichText)
        self.lbl_narrative.setStyleSheet("font-size: 12px; color: #0f172a;")
        cl.addWidget(self.lbl_narrative)
        self._layout.addWidget(card)

        # 3. Quantified requirements table
        lbl_req = QLabel("Exigences Techniques & Budgétaires Quantifiées (vérifiées par le simulateur)")
        lbl_req.setStyleSheet("font-weight: bold; font-size: 13px; color: #0f2744;")
        self._layout.addWidget(lbl_req)

        tbl_style = """
            QTableWidget {
                background-color: #ffffff;
                color: #0f172a;
                gridline-color: #cbd5e1;
                font-size: 12px;
                alternate-background-color: #f8fafc;
                selection-background-color: #2563eb;
                selection-color: #ffffff;
            }
            QHeaderView::section {
                background-color: #0f2744;
                color: #ffffff;
                font-weight: bold;
                padding: 5px;
                border: 1px solid #1e3a5f;
            }
            QTableWidget::item {
                color: #0f172a;
            }
        """
        self.t_reqs = QTableWidget(0, 6)
        self.t_reqs.setStyleSheet(tbl_style)
        self.t_reqs.setHorizontalHeaderLabels(
            ["Code", "Intitulé de l'exigence", "Paramètre système", "Seuil obligatoire", "Objectif (Goal)", "Description"]
        )
        self.t_reqs.verticalHeader().setVisible(False)
        self.t_reqs.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.t_reqs.setAlternatingRowColors(True)
        self.t_reqs.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.t_reqs.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.t_reqs.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.t_reqs.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.t_reqs.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.t_reqs.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)
        self._layout.addWidget(self.t_reqs)

        # 3b. Geographic Return Constraints table (ESA-style juste retour)
        self.lbl_geo = QLabel("Contraintes de Retour Géographique (Principe du Juste Retour Industriel ESA)")
        self.lbl_geo.setStyleSheet("font-weight: bold; font-size: 13px; color: #0f2744;")
        self._layout.addWidget(self.lbl_geo)

        self.t_georeturn = QTableWidget(0, 4)
        self.t_georeturn.setStyleSheet(tbl_style)
        self.t_georeturn.setHorizontalHeaderLabels(
            ["État Membre (Pays)", "Fourchette requise (%)", "Fourchette estimée (M€)", "Rôle industriel & Justification souscription"]
        )
        self.t_georeturn.verticalHeader().setVisible(False)
        self.t_georeturn.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.t_georeturn.setAlternatingRowColors(True)
        self.t_georeturn.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.t_georeturn.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.t_georeturn.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.t_georeturn.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self._layout.addWidget(self.t_georeturn)

        # 4. Ground stations & Target zones table
        lbl_gs = QLabel("Segment Sol Imposé / Disponible & Zones d'Intérêt")
        lbl_gs.setStyleSheet("font-weight: bold; font-size: 13px; color: #0f2744;")
        self._layout.addWidget(lbl_gs)

        self.t_stations = QTableWidget(0, 5)
        self.t_stations.setStyleSheet(tbl_style)
        self.t_stations.setHorizontalHeaderLabels(
            ["Station Sol / Zone", "Coordonnées (Lat, Lon)", "Altitude / Élévation min.", "Bandes supportées", "Coût / passage"]
        )
        self.t_stations.verticalHeader().setVisible(False)
        self.t_stations.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.t_stations.setAlternatingRowColors(True)
        self.t_stations.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self._layout.addWidget(self.t_stations)

        self._layout.addStretch(1)

    def set_mission(self, m: MissionSpecification) -> None:
        domain = m.domain_label or MISSION_TYPE_BADGES_FR.get(m.mission_type, m.mission_type)
        self.lbl_title.setText(f"FICHE DE SPÉCIFICATION MISSION — {m.title}   [{m.id}]")
        self.lbl_subtitle.setText(f"Domaine : {domain}   •   Commanditaire : {m.client_agency}")

        self.lbl_budget_box.setText(f"BUDGET TOTAL PLAFOND\n{m.max_budget_meur:.2f} M€ TTC\n(Segment spatial + Lanceur)")
        self.lbl_life_box.setText(f"DURÉE DE VIE CIBLE : {m.target_lifetime_years:.1f} ans\nTRL minimal exigé : TRL {m.min_trl}")

        primary_obj = m.primary_objective or m.context
        html_parts = [
            f"<p style='margin-bottom:6px;'><b style='color:#1e3a8a;'>1. Contexte général :</b> {m.context}</p>",
            f"<p style='margin-bottom:6px;'><b style='color:#1e3a8a;'>2. Objectif principal de la mission :</b> {primary_obj}</p>",
        ]
        if m.secondary_objectives:
            sec_li = "".join(f"<li>{s}</li>" for s in m.secondary_objectives)
            html_parts.append(
                f"<b style='color:#1e3a8a;'>3. Objectifs secondaires :</b>"
                f"<ul style='margin-top:2px;margin-bottom:6px;'>{sec_li}</ul>"
            )
        if m.scientific_or_operational_need:
            html_parts.append(
                f"<p style='margin-bottom:6px;'><b style='color:#1e3a8a;'>4. Besoin scientifique / opérationnel & utilisateurs :</b> "
                f"{m.scientific_or_operational_need}</p>"
            )
        if m.orbit_constraints_description:
            html_parts.append(
                f"<p style='margin-bottom:6px;'><b style='color:#1e3a8a;'>5. Contraintes & orientations orbitales :</b> "
                f"{m.orbit_constraints_description}</p>"
            )
        if m.conops_guidance:
            html_parts.append(
                f"<p style='margin-bottom:6px;'><b style='color:#1e3a8a;'>6. Concept d'opérations attendu (CONOPS) :</b> "
                f"{m.conops_guidance}</p>"
            )
        if m.deliverables_expected:
            del_li = "".join(f"<li>{d}</li>" for d in m.deliverables_expected)
            html_parts.append(
                f"<b style='color:#1e3a8a;'>7. Points à justifier par l'étudiant dans le rapport :</b>"
                f"<ul style='margin-top:2px;margin-bottom:2px;'>{del_li}</ul>"
            )
        self.lbl_narrative.setText("".join(html_parts))

        # Populate requirements table (+ row 0 = total budget requirement so it is always explicit)
        total_rows = len(m.requirements) + 1
        self.t_reqs.setRowCount(total_rows)

        b_font = QFont()
        b_font.setBold(True)
        budget_cells = [
            "REQ-BUDGET",
            "Plafond budgétaire total mission",
            "space_segment_total_meur",
            f"<= {m.max_budget_meur:.2f} M€",
            f"<= {m.max_budget_meur * 0.90:.2f} M€",
            "Coût complet : plateforme de base + options & intégration + charge(s) utile(s) + lancement.",
        ]
        for c_idx, val in enumerate(budget_cells):
            it = QTableWidgetItem(val)
            it.setForeground(QColor("#0f172a"))
            if c_idx in (0, 3):
                it.setFont(b_font)
            self.t_reqs.setItem(0, c_idx, it)
        self.t_reqs.setRowHeight(0, 26)

        for r, req in enumerate(m.requirements, start=1):
            goal_str = f"{req.operator.value} {req.goal} {req.unit}".strip() if req.goal is not None else "—"
            vals = [
                req.id,
                req.title,
                req.parameter,
                f"{req.operator.value} {req.threshold} {req.unit}".strip(),
                goal_str,
                req.description,
            ]
            for c_idx, val in enumerate(vals):
                it = QTableWidgetItem(val)
                it.setForeground(QColor("#0f172a"))
                if c_idx in (0, 3):
                    it.setFont(b_font)
                self.t_reqs.setItem(r, c_idx, it)
            self.t_reqs.setRowHeight(r, 26)
        self.t_reqs.setFixedHeight(min(260, 32 + 26 * total_rows))

        # Populate geographic return constraints (ESA juste retour)
        flag_map = {
            "France": "🇫🇷 France",
            "Allemagne": "🇩🇪 Allemagne",
            "Italie": "🇮🇹 Italie",
            "Espagne": "🇪🇸 Espagne",
            "Royaume-Uni": "🇬🇧 Royaume-Uni",
            "Suisse": "🇨🇭 Suisse",
            "Belgique": "🇧🇪 Belgique",
            "Pays-Bas": "🇳🇱 Pays-Bas",
            "Suède": "🇸🇪 Suède",
            "Finlande": "🇫🇮 Finlande",
        }
        if m.geo_return_constraints:
            self.lbl_geo.setVisible(True)
            self.t_georeturn.setVisible(True)
            self.t_georeturn.setRowCount(len(m.geo_return_constraints))
            for r_idx, grc in enumerate(m.geo_return_constraints):
                country_label = flag_map.get(grc.country, grc.country)
                min_m = m.max_budget_meur * (grc.min_pct / 100.0)
                max_m = m.max_budget_meur * (grc.max_pct / 100.0)

                it_c = QTableWidgetItem(country_label)
                it_c.setForeground(QColor("#0f172a"))
                it_c.setFont(b_font)
                it_range = QTableWidgetItem(f"[{grc.min_pct:.1f} %, {grc.max_pct:.1f} %]")
                it_range.setForeground(QColor("#0f172a"))
                it_range.setFont(b_font)
                it_meur = QTableWidgetItem(f"~{min_m:.2f} à {max_m:.2f} M€")
                it_meur.setForeground(QColor("#0f172a"))
                it_rat = QTableWidgetItem(grc.rationale or "Souscription industrielle obligatoire au programme")
                it_rat.setForeground(QColor("#0f172a"))

                self.t_georeturn.setItem(r_idx, 0, it_c)
                self.t_georeturn.setItem(r_idx, 1, it_range)
                self.t_georeturn.setItem(r_idx, 2, it_meur)
                self.t_georeturn.setItem(r_idx, 3, it_rat)
                self.t_georeturn.setRowHeight(r_idx, 26)
            self.t_georeturn.setFixedHeight(min(180, 32 + 26 * len(m.geo_return_constraints)))
        else:
            self.lbl_geo.setVisible(False)
            self.t_georeturn.setVisible(False)

        # Populate ground stations + target zones
        gs_rows = len(m.ground_stations) + len(m.target_zones)
        self.t_stations.setRowCount(gs_rows)
        row_i = 0
        for gs in m.ground_stations:
            self.t_stations.setItem(row_i, 0, QTableWidgetItem(f"Station : {gs.name} [{gs.id}]"))
            self.t_stations.setItem(row_i, 1, QTableWidgetItem(f"{gs.latitude_deg:.2f}°, {gs.longitude_deg:.2f}°"))
            self.t_stations.setItem(row_i, 2, QTableWidgetItem(f"Alt. {gs.altitude_m:.0f} m | Élév. ≥ {gs.min_elevation_deg:.0f}°"))
            self.t_stations.setItem(row_i, 3, QTableWidgetItem(", ".join(gs.bands_supported)))
            self.t_stations.setItem(row_i, 4, QTableWidgetItem(f"{gs.cost_per_pass_eur:.0f} € / passage"))
            self.t_stations.setRowHeight(row_i, 24)
            row_i += 1
        for tz in m.target_zones:
            pts = " ; ".join(f"({lat:.1f}°, {lon:.1f}°)" for lat, lon in tz.points_lat_lon[:4])
            self.t_stations.setItem(row_i, 0, QTableWidgetItem(f"Zone cible : {tz.name}"))
            self.t_stations.setItem(row_i, 1, QTableWidgetItem(pts))
            self.t_stations.setItem(row_i, 2, QTableWidgetItem(f"Priorité {tz.priority}"))
            self.t_stations.setItem(row_i, 3, QTableWidgetItem("—"))
            self.t_stations.setItem(row_i, 4, QTableWidgetItem("—"))
            self.t_stations.setRowHeight(row_i, 24)
            row_i += 1
        self.t_stations.setFixedHeight(min(180, max(65, 30 + 24 * max(1, gs_rows))))
