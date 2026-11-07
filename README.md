# Space Segment Builder (SSB)

Logiciel pédagogique autonome d'évaluation et de conception de systèmes spatiaux pour étudiants de niveau Master / École d'Ingénieur.

---

## 1. Vue d'ensemble

À partir d'un sujet de mission fourni (`.mission.json`), l'étudiant dimensionne un segment spatial complet et cohérent :
- **Orbite** (LEO, SSO avec calcul d'inclinaison $J_2$, circularité, repeat ground track, GEO).
- **Plateforme** choisie parmi plusieurs constructeurs réalistes (NewSpace, SmallSat, Historique européen).
- **Sous-systèmes configurables à emplacements (slots)** : propulsion (gaz froid, électrique Hall, monergol hydrazine, bi-ergol), TT&C bande S, liaison descendante haut débit X/Ka, mémoire de masse, suites ADCS haute précision ou forte agilité (CMG).
- **Charges utiles** : télescopes optiques sub-métriques à grand diamètre, radar SAR bande X, spectromètres imageurs VNIR, terminaux laser optiques 10 Gbps, terminaux quantiques QKD (BB84).
- **Lanceurs** : rideshare vs vols dédiés légers, moyens ou lourds.
- **CONOPS & Budgets** : bilan de masse (avec marge 20%), bilan de puissance (modes et duty cycles), bilan de coût, budget de pointage et simulation de décharge batterie / remplissage mémoire sur orbite.
- **Rapport d'examen Word (.docx)** généré automatiquement, prêt à être complété (justifications, CONOPS détaillé, analyse de risques) et accompagné du fichier projet `.json` signé cryptographiquement (SHA-256).

---

## 2. Démarrage Rapide

### A. Exécutables Autonomes (Stand-Alone, sans Python)
Les exécutables portables compilés sont disponibles dans le dossier `dist/` :
- **Application Étudiant :** `dist/SpaceSegmentBuilder-Student/SpaceSegmentBuilder-Student.exe`
- **Application Enseignant :** `dist/SpaceSegmentBuilder-Teacher/SpaceSegmentBuilder-Teacher.exe`

### B. Depuis les Sources Python
Nécessite Python 3.12+ (testé et validé sur Python 3.14) :
```bash
# Lancer l'application Étudiant
python main.py

# Lancer l'application Enseignant
python main.py teacher
```

---

## 3. Architecture du Logiciel

```
Space_Segment_building/
  ├── build/              # Recettes PyInstaller (.spec)
  ├── data/
  │   ├── catalogs/       # Catalogues JSON (platforms, equipment, payloads, launchers)
  │   └── missions/       # Sujets d'examens
  ├── docs/
  │   ├── SPECIFICATIONS.md      # Spécifications détaillées (D1-D21)
  │   └── IMPLEMENTATION_PLAN.md # Plan de développement par tranches
  ├── src/ssb/
  │   ├── catalog/        # Chargement et validation croisée des catalogues
  │   ├── conops/         # Simulation dynamique des opérations
  │   ├── core/           # Modèles Pydantic (Mission, Orbit, Platform, Project...)
  │   ├── orbit/          # Propagateur J2, éclipses, accès stations sol
  │   ├── payload/        # Modèles analytiques (optique, SAR, spectro, comms, QKD)
  │   ├── report/         # Générateur de rapport Word (.docx) avec graphiques
  │   ├── student_app/    # Interface graphique PySide6 Étudiant
  │   ├── teacher_app/    # Interface graphique PySide6 Enseignant
  │   └── system/         # Configurator (slots) & Evaluator (budgets & conformité)
  └── tests/unit/         # Suite de tests unitaires automatisés
```

---

## 4. Tests et Validation

Pour exécuter la suite de tests complète (12 tests unitaires couvrant l'ensemble des modèles de calcul et d'intégrité) :
```bash
pytest
```
