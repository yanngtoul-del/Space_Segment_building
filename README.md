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

### A. Exécutables Autonomes (Windows, macOS, Linux — sans Python)
Des exécutables autonomes sont compilables pour les 4 éditions (`Student`, `Teacher`, `Student-Lite`, `Teacher-Lite`) :
- **Windows (`windows-x86_64`)** : décompresser l'archive `.zip` et lancer `SpaceSegmentBuilder-Student.exe` (ou `Teacher` / `-Lite`).
- **macOS (`macos-arm64` Apple Silicon & `macos-x86_64` Intel)** : décompresser le `.zip` pour obtenir le bundle `.app` (`SpaceSegmentBuilder-Student.app`).
  - *Note Gatekeeper (première ouverture d'une application non notariée)* : faites **clic droit → Ouvrir** sur l'icône `.app`, ou exécutez dans le Terminal :
    ```bash
    xattr -cr SpaceSegmentBuilder-Student.app
    ```
- **Linux (`linux-x86_64`)** : extraire l'archive `.tar.gz` et lancer le binaire :
  ```bash
  tar -xzf SpaceSegmentBuilder-Student-linux-x86_64.tar.gz
  ./SpaceSegmentBuilder-Student/SpaceSegmentBuilder-Student
  ```
  *(Sous Debian/Ubuntu minimal, s'assurer que les bibliothèques Qt6 système sont installées : `libegl1 libgl1 libxkbcommon-x11-0 libxcb-cursor0`.)*

### B. Compilation Multi-OS (Locale & GitHub Actions)
PyInstaller ne permet pas de cross-compiler d'un OS à un autre.
- **Compilation locale** (produit les 4 binaires + tests `--version`/`--test-launch` + archives dans `dist/archives/` pour l'OS courant) :
  ```bash
  python scripts/build_dist.py --archive
  ```
- **Compilation automatique Windows + macOS (arm64 & Intel) + Linux** : le workflow GitHub Actions [`.github/workflows/build.yml`](.github/workflows/build.yml) compile automatiquement les 4 éditions sur les 4 cibles à chaque `push` / `pull_request` (artefacts téléchargeables dans l'onglet *Actions*) et publie une *GitHub Release* complète lors d'un tag `v*` (ex. `git tag v0.1.0 && git push origin v0.1.0`).

### C. Depuis les Sources Python
Nécessite Python 3.12+ (testé et validé sur Python 3.12 et 3.14) :
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
  ├── .github/workflows/  # CI/CD multi-OS (Windows, macOS arm64/x64, Linux)
  ├── build/              # Recettes PyInstaller multi-OS (.spec)
  ├── data/
  │   ├── catalogs/       # Catalogues JSON (platforms, equipment, payloads, launchers)
  │   └── missions/       # Sujets d'examens
  ├── docs/
  │   ├── SPECIFICATIONS.md      # Spécifications détaillées (D1-D21)
  │   └── IMPLEMENTATION_PLAN.md # Plan de développement par tranches
  ├── scripts/
  │   └── build_dist.py   # Script unifié de compilation, test et archivage
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

Pour exécuter la suite de tests complète :
```bash
pytest
```
