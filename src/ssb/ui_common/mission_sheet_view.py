"""Dedicated Mission Specification Sheet (Fiche de Spécification Mission) viewer widget."""

import html
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor, QPixmap
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
    QSizePolicy,
)
from ssb.core.mission import MissionSpecification
from ssb.core.paths import images_dir


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

        # 1. Top dark-blue banner: Illustration, Title, ID, Client, Domain, Total Budget, Lifetime, Min TRL
        banner = QFrame()
        banner.setStyleSheet(
            "QFrame { background: #0f2744; border: 1px solid #1e4976; border-radius: 6px; padding: 8px; }"
            "QLabel { color: #f8fafc; }"
        )
        bl = QHBoxLayout(banner)
        bl.setSpacing(12)

        self.lbl_image = QLabel()
        self.lbl_image.setFixedSize(160, 90)
        self.lbl_image.setStyleSheet(
            "background: #0b192c; border: 1px solid #38bdf8; border-radius: 5px;"
        )
        self.lbl_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_image.setScaledContents(True)
        bl.addWidget(self.lbl_image)

        left_col = QVBoxLayout()
        self.lbl_title = QLabel()
        self.lbl_title.setStyleSheet("font-size: 15px; font-weight: bold; color: #ffffff;")
        self.lbl_title.setWordWrap(True)
        self.lbl_title.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.lbl_title.setMinimumWidth(100)
        self.lbl_subtitle = QLabel()
        self.lbl_subtitle.setStyleSheet("font-size: 11px; color: #93c5fd;")
        self.lbl_subtitle.setWordWrap(True)
        self.lbl_subtitle.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.lbl_subtitle.setMinimumWidth(100)
        left_col.addWidget(self.lbl_title)
        left_col.addWidget(self.lbl_subtitle)
        bl.addLayout(left_col, stretch=1)

        right_col = QHBoxLayout()
        self.lbl_budget_box = QLabel()
        self.lbl_budget_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_budget_box.setStyleSheet(
            "background: #1e3a5f; border: 1px solid #fbbf24; border-radius: 5px; padding: 6px 12px; "
            "color: #fbbf24; font-weight: bold; font-size: 12px;"
        )
        self.lbl_life_box = QLabel()
        self.lbl_life_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_life_box.setStyleSheet(
            "background: #1e3a5f; border: 1px solid #38bdf8; border-radius: 5px; padding: 6px 12px; "
            "color: #e0f2fe; font-weight: bold; font-size: 11px;"
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

        self.lbl_tradeoff_hint = QLabel(
            "⚖️ <b>Arbitrages d'Architecture & Gestion des Non-Conformités (Demandes de Dérogation / Waivers) :</b> "
            "Les cahiers des charges spatiaux comportent des antagonismes physiques et budgétaires délibérés entre les <b>Seuils obligatoires</b>, "
            "les <b>Objectifs étendus (Goals)</b>, la qualification <b>TVAC au sol</b>, le <b>plafond financier</b> et le <b>retour géographique ESA</b>. "
            "Il appartient à l'architecte système de choisir le meilleur compromis global et, si certaines exigences ou objectifs s'avèrent mutuellement "
            "incompatibles, d'argumenter rigoureusement ses <b>Demandes de Dérogation (Requests for Deviation / Waiver)</b> à l'Onglet 9."
        )
        self.lbl_tradeoff_hint.setStyleSheet(
            "background-color: #fffbeb; color: #78350f; border-left: 4px solid #f59e0b; padding: 6px 10px; border-radius: 4px; font-size: 11px;"
        )
        self.lbl_tradeoff_hint.setWordWrap(True)
        self._layout.addWidget(self.lbl_tradeoff_hint)

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

        self.lbl_geo_hint = QLabel(
            "ℹ️ <b>Règle du retour géographique ESA :</b> Les souscriptions nationales fixent les quotes-parts budgétaires par État membre "
            "sans imposer de type d'équipement particulier (choix libre plateforme / charges utiles / équipements / centre d'essais TVAC). "
            "Une enveloppe jusqu'à <b>15 %</b> est autorisée pour des composants hors Europe (COTS mondiaux : USA, Canada, Japon...)."
        )
        self.lbl_geo_hint.setStyleSheet(
            "background-color: #f1f5f9; color: #0f172a; border-left: 4px solid #2563eb; padding: 6px 10px; border-radius: 4px; font-size: 11px;"
        )
        self.lbl_geo_hint.setWordWrap(True)
        self._layout.addWidget(self.lbl_geo_hint)

        self.t_georeturn = QTableWidget(0, 4)
        self.t_georeturn.setStyleSheet(tbl_style)
        self.t_georeturn.setHorizontalHeaderLabels(
            ["État Membre / Origine", "Fourchette requise (%)", "Fourchette estimée (M€)", "Justification souscription ESA & Clé de répartition"]
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

        # Mission illustration
        if m.image:
            img_path = images_dir() / m.image
            if img_path.exists():
                pix = QPixmap(str(img_path))
                self.lbl_image.setPixmap(
                    pix.scaled(
                        self.lbl_image.size(),
                        Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                        Qt.TransformationMode.SmoothTransformation,
                    )
                )
                self.lbl_image.setToolTip(f"Illustration conceptuelle : {m.title}")
                self.lbl_image.setVisible(True)
            else:
                self.lbl_image.clear()
                self.lbl_image.setVisible(False)
        else:
            self.lbl_image.clear()
            self.lbl_image.setVisible(False)

        self.lbl_budget_box.setText(f"BUDGET TOTAL PLAFOND\n{m.max_budget_meur:.2f} M€ TTC\n(Segment spatial + Lanceur)")
        self.lbl_life_box.setText(f"DURÉE DE VIE CIBLE : {m.target_lifetime_years:.1f} ans\nTRL minimal exigé : TRL {m.min_trl}")

        primary_obj = m.primary_objective or m.context
        html_parts = [
            f"<p style='margin-bottom:6px;'><b style='color:#1e3a8a;'>1. Contexte général :</b> {html.escape(m.context)}</p>",
            f"<p style='margin-bottom:6px;'><b style='color:#1e3a8a;'>2. Objectif principal de la mission :</b> {html.escape(primary_obj)}</p>",
        ]
        if m.secondary_objectives:
            sec_li = "".join(f"<li>{html.escape(s)}</li>" for s in m.secondary_objectives)
            html_parts.append(
                f"<b style='color:#1e3a8a;'>3. Objectifs secondaires :</b>"
                f"<ul style='margin-top:2px;margin-bottom:6px;'>{sec_li}</ul>"
            )
        if m.scientific_or_operational_need:
            html_parts.append(
                f"<p style='margin-bottom:6px;'><b style='color:#1e3a8a;'>4. Besoin scientifique / opérationnel & utilisateurs :</b> "
                f"{html.escape(m.scientific_or_operational_need)}</p>"
            )
        if m.orbit_constraints_description:
            html_parts.append(
                f"<p style='margin-bottom:6px;'><b style='color:#1e3a8a;'>5. Contraintes & orientations orbitales :</b> "
                f"{html.escape(m.orbit_constraints_description)}</p>"
            )
        if m.conops_guidance:
            html_parts.append(
                f"<p style='margin-bottom:6px;'><b style='color:#1e3a8a;'>6. Concept d'opérations attendu (CONOPS) :</b> "
                f"{html.escape(m.conops_guidance)}</p>"
            )
        if m.deliverables_expected:
            del_li = "".join(f"<li>{html.escape(d)}</li>" for d in m.deliverables_expected)
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
            "Plafond Budgétaire Global",
            "total_cost_meur",
            f"≤ {m.max_budget_meur:.2f} M€",
            f"≤ {m.max_budget_meur * 0.90:.2f} M€",
            "Le coût consolidé (plateforme, options, charges utiles, calibration sol, lancement) ne doit pas dépasser le plafond.",
        ]
        for col_idx, val in enumerate(budget_cells):
            item = QTableWidgetItem(val)
            item.setFont(b_font)
            item.setBackground(QColor("#fef3c7"))
            item.setForeground(QColor("#78350f"))
            self.t_reqs.setItem(0, col_idx, item)

        op_display = {"<=": "≤", ">=": "≥", "<": "<", ">": ">", "==": "="}
        for row_idx, r in enumerate(m.requirements, start=1):
            op_sym = op_display.get(r.operator.value, r.operator.value)
            goal_str = f"{op_sym} {r.goal} {r.unit}".strip() if r.goal is not None else "—"
            thresh_str = f"{op_sym} {r.threshold} {r.unit}".strip()
            row_vals = [
                r.id,
                r.title,
                r.parameter,
                thresh_str,
                goal_str,
                r.description,
            ]
            for col_idx, val in enumerate(row_vals):
                item = QTableWidgetItem(str(val))
                self.t_reqs.setItem(row_idx, col_idx, item)

        # Populate Geographic Return Constraints table (ESA-style)
        self.t_georeturn.setRowCount(len(m.geo_return_constraints))
        for row_idx, geo in enumerate(m.geo_return_constraints):
            min_meur = (geo.min_pct / 100.0) * m.max_budget_meur
            max_meur = (geo.max_pct / 100.0) * m.max_budget_meur
            pct_str = f"[{geo.min_pct:.1f} %  –  {geo.max_pct:.1f} %]"
            meur_str = f"[{min_meur:.2f} M€  –  {max_meur:.2f} M€]"
            country_label = f"🇪🇺 {geo.country}" if geo.country in [
                "France", "Allemagne", "Italie", "Espagne", "Royaume-Uni", "Belgique", "Suisse", "Pays-Bas", "Suède", "Autriche", "Finlande", "Norvège"
            ] else geo.country

            c_item = QTableWidgetItem(country_label)
            c_item.setFont(b_font)
            p_item = QTableWidgetItem(pct_str)
            p_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            m_item = QTableWidgetItem(meur_str)
            m_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            r_item = QTableWidgetItem(geo.rationale or "Souscription au programme ESA")

            self.t_georeturn.setItem(row_idx, 0, c_item)
            self.t_georeturn.setItem(row_idx, 1, p_item)
            self.t_georeturn.setItem(row_idx, 2, m_item)
            self.t_georeturn.setItem(row_idx, 3, r_item)

        # Populate ground stations & target zones
        total_gs_rows = len(m.ground_stations) + len(m.target_zones)
        self.t_stations.setRowCount(total_gs_rows)
        row_i = 0
        for gs in m.ground_stations:
            coords = f"{gs.latitude_deg:.2f}°, {gs.longitude_deg:.2f}°"
            alt = f"{gs.altitude_m:.0f} m / elev. min {gs.min_elevation_deg:.1f}°"
            bands = ", ".join(gs.bands_supported)
            cost = f"{gs.cost_per_pass_eur:.0f} €" if gs.cost_per_pass_eur > 0 else "Inclus / sans frais"
            for col_idx, val in enumerate([f"Station Sol — {gs.name} [{gs.id}]", coords, alt, bands, cost]):
                self.t_stations.setItem(row_i, col_idx, QTableWidgetItem(val))
            row_i += 1

        for tz in m.target_zones:
            pts = ", ".join(f"({lat:.1f}, {lon:.1f})" for lat, lon in tz.points_lat_lon[:3])
            if len(tz.points_lat_lon) > 3:
                pts += " ..."
            for col_idx, val in enumerate([f"Zone d'intérêt — {tz.name}", pts or "Nadir global", f"Priorité {tz.priority}", "Capteurs bord", "—"]):
                self.t_stations.setItem(row_i, col_idx, QTableWidgetItem(val))
            row_i += 1
