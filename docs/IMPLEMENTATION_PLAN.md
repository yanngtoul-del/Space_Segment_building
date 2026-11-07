# Plan d'implémentation — Space Segment Builder

Référence : [SPECIFICATIONS.md](SPECIFICATIONS.md) (D1–D21).
Durées indicatives pour un développeur (≈ 1 personne + assistance IA) ; à ajuster.

## 1. Principes directeurs

1. **Noyau de calcul sans UI** (`core`, `orbit`, `payload`, `platform`, `system`, `conops`) : testable en ligne de commande, partagé par les applications *Student* et *Teacher*.
2. **Tout est donnée** : catalogues, sujets, règles de slots en JSON validés par schéma ; aucune valeur de produit en dur dans le code.
3. **Calculs transparents et traçables** : chaque résultat porte ses entrées, hypothèses, formule et unité (utile au rapport et à la correction).
4. **Déterminisme** : mêmes entrées ⇒ mêmes sorties (le Teacher rejoue un projet étudiant et retrouve les mêmes chiffres). Version du moteur figée dans le fichier projet.
5. **Vertical slice d'abord** : un scénario de bout en bout (sujet → rapport) dès le jalon 1, puis élargissement.
6. **Portabilité** : aucune dépendance Windows-only ; builds PyInstaller par OS via CI.

## 2. Choix techniques à valider (jalon 0)

| Sujet | Choix proposé | Alternative / risque |
|---|---|---|
| Python | 3.14 si wheels PySide6/numpy/scipy/PyInstaller OK, sinon 3.12/3.13 | **Risque** : compatibilité 3.14 → vérifier en jalon 0, sinon basculer |
| UI | PySide6 (Qt Widgets) ; graphiques `pyqtgraph` (courbes) + `matplotlib` (figures du rapport) | QML : plus joli, plus lourd à maintenir |
| Modèles de données | `pydantic` v2 (validation, JSON schema) | dataclasses + jsonschema |
| Unités | SI en interne, suffixes de noms (`mass_kg`, `power_w`), conversion à l'affichage ; pas de `pint` | `pint` si garde-fous stricts souhaités |
| Orbite | Propagateur maison `numpy`/`scipy` : J2–J4 + traînée (Harris-Priester/exponentiel) + SRP ; Soleil/Lune analytiques (Meeus basse précision) ; pas de gros fichiers d'éphémérides | `sgp4`/`skyfield` (+ DE421 ≈ 17 Mo) si besoin de précision |
| Carte hors-ligne | Traits de côtes Natural Earth simplifiés, embarqués (`.npz`/GeoJSON), dessinés avec pyqtgraph/matplotlib | `cartopy` (GEOS/PROJ lourds → évité) |
| Rapport | `python-docx` + figures matplotlib ; gabarit `.docx` avec styles | `docxtpl` |
| Packaging | PyInstaller (onedir par défaut, onefile optionnel), CI GitHub Actions matrice Windows/macOS/Linux | Nuitka : démarrage plus rapide, build plus long |
| Tests | `pytest`, `hypothesis`, golden files | |
| Qualité | `ruff`, `mypy` (core), pre-commit | |
| Intégrité projet | JSON canonique + SHA-256 + HMAC (clé embarquée) | Signature asymétrique si contrôle fort |

## 3. Architecture cible

```
Space_Segment_building/
  pyproject.toml
  src/ssb/
    core/            # modèles pydantic (Mission, Orbit, Platform, Equipment, Payload, Conops, Project)
                     # versioning de schéma, migration, canonicalisation JSON, hash/HMAC, journal
    catalog/         # chargement, validation croisée (références, slots), index, filtrage
    orbit/           # éléments, repères, propagation, éclipses/β, ground track, accès stations,
                     # couverture/revisite, décroissance orbitale, radiation simplifiée
    payload/         # optique, spectro, sar, comm_optique, qkd, comm_radio
    platform/        # propulsion, ttc, downlink, storage, adcs, eps, obc, thermal
    system/          # assemblage (slots), budgets, compatibilité (règles), coûts, conformité aux exigences
    conops/          # modes, plan d'activités, simulateur temporel
    report/          # génération docx, figures, gabarits
    ui_common/       # widgets partagés (cartes, tableaux, graphiques, thème, i18n)
    student_app/
    teacher_app/
  data/
    catalogs/ (platforms, equipment, payloads, launchers)  missions/  geo/ (côtes, stations)  templates/
  tests/ (unit, integration, golden)   docs/   tools/   build/ (specs PyInstaller, CI)
```

Dépendances : `core` ← `catalog` ← (`orbit`, `payload`, `platform`) ← `system` ← `conops` ← `report` ← apps. Aucun calcul ne dépend de l'UI.

## 4. Jalons

### Jalon 0 — Fondations (≈ 1 semaine)
- Environnement (`pyproject.toml`, venv, `ruff`, `mypy`, `pytest`, pre-commit), arborescence, CI minimale (tests sous 3 OS).
- **Preuve de faisabilité packaging** : mini-app PySide6 + numpy + matplotlib + python-docx packagée par PyInstaller sur Windows/macOS/Linux (taille, temps de démarrage).
- Validation de la version de Python.
- Conventions : unités, repères (ECI J2000/TEME, ECEF, WGS84), dates (UTC, JD).
**Sortie** : squelette qui build et passe les tests ; choix de §2 figés.

### Jalon 1 — Modèle de données & catalogues pilotes (≈ 2 semaines)
- Modèles pydantic : `Mission` (exigences), `Orbit`, `Equipment`, `Platform` (+ `slots`, règles §16), `Payload*`, `Launcher`, `Conops`, `Project`.
- JSON Schema exporté ; validateur de catalogue (références croisées, slots cohérents, plages plausibles).
- **Catalogue pilote** : 2 fournisseurs plateformes (3–4 produits), ~10 équipements (propulsion, TT&C, stockage, ADCS, panneaux), 3 charges utiles, 2 lanceurs.
- Fichier projet : sauvegarde/chargement, version de schéma, canonicalisation + hash/HMAC.
- Moteur de **configuration plateforme** : slots, min/max, `requires`/`exclusive_with`, surcharges locales (D19), remplacement sans crédit (D20), cumuls masse/puissance/volume/prix.
**Tests** : validation de schéma, cas de slots positifs/négatifs, aller-retour de sérialisation.
**Sortie** : on peut décrire et valider un système en JSON, avec budgets masse/puissance/coût.

### Jalon 2 — Moteur orbital (≈ 3 semaines)
- Éléments ↔ vecteur d'état ; repères ; temps.
- Propagateur : J2–J4, traînée, SRP ; pas adaptatif (scipy DOP853) ; mode « moyenné » rapide pour études annuelles.
- Assistants : SSO (i en fonction de a, e), repeat-ground-track (solveur d'altitude), orbite gelée, Molniya/Tundra, GEO.
- Soleil/Lune analytiques ; **éclipses** (ombre/pénombre), **β**, heure locale du nœud.
- Ground track, vitesse sol, empreinte instantanée.
- **Accès stations** (élévation min, masque), durées de passe.
- **Couverture/revisite** sur zones d'intérêt avec contraintes d'éclairement et dépointage ; statistiques (moyenne, max, percentiles).
- Décroissance orbitale, durée de vie, Δv de maintien/désorbitation ; dose de radiation simplifiée (tabulée).
**Tests** : valeurs de référence (périodes, précession SSO ≈ 0,9856 °/jour, durées d'éclipse, ground track connu), invariants énergétiques, tests de propriété.
**Sortie** : bibliothèque orbitale validée, CLI de démonstration.

### Jalon 3 — Modèles charge utile (≈ 4 semaines, parallélisable par type)
Pour chaque type : équations documentées, entrées/sorties typées, cas de test de référence, fiche dans `docs/models/`.
1. **Optique** : GSD, fauchée, SNR (radiance TOA, QE, bruits), FTM, NIIRS (GIQE), jitter/traînage, débit brut/compressé.
2. **Spectromètre** : résolution spectrale, SNR par bande, fauchée, débit.
3. **SAR** : résolutions, NESZ, ambiguïtés, PRF/fauchée, puissance moyenne, débit, géométrie d'incidence.
4. **Comm optique** : bilan de liaison (géométrie, pointage, atmosphère, scintillation, nuages), marge, volume par passe, disponibilité.
5. **QKD** : taux de clé secret (pertes, bruit, fenêtre nocturne), temps de visibilité.
6. **Comm radio** : EIRP, G/T, FSPL, marges, débit/volume, empreinte.
**Sortie** : chaque charge utile retourne ses performances en fonction de l'orbite et du pointage plateforme.

### Jalon 4 — Sous-systèmes plateforme & compatibilité (≈ 3 semaines)
- **Propulsion** : Tsiolkovski couplé à la masse totale, budget Δv (LEOP, maintien, évitement, désorbitation), durée de manœuvre, puissance requise, marges.
- **TT&C** : bilan UL/DL, couverture LEOP/survie, volume TM/TC.
- **Descente charge utile** : bilan, débit effectif par passe, volume/jour.
- **Stockage de masse** : capacité BOL/EOL, débit, remplissage.
- **ADCS** : budget de pointage, agilité, couples de perturbation, saturation de roues.
- **EPS** : puissance générée/consommée par orbite, éclipses, batterie (DoD, cycles), dégradation.
- **Thermique/structure** simplifiés ; fiabilité/durée de vie ; radiation (TID).
- **Moteur de règles de compatibilité** : règles déclaratives (`OK/Attention/Bloquant`, message pédagogique, référence d'exigence) ; grisage des plateformes et options avec la raison (D18).
- **Coûts** : plateforme + options + intégration + charge utile + lanceur + opérations annuelles ; marges.
**Sortie** : tableau de conformité complet sur un système de test.

### Jalon 5 — CONOPS & simulation temporelle (≈ 3 semaines)
- Modes (LEOP, commissioning, nominal, acquisition, descente, survie, désorbitation) avec consommation/attitude/débit.
- Règles d'activité : acquisitions sur zones d'intérêt (éclairement, élévation solaire, nuages), passes stations, duty cycle, manœuvres.
- Simulateur temporel (1–30 jours + extrapolation annuelle) : SoC batterie, mémoire, volume descendu, images/surface, revisite effective, roues, ergols.
- Détection de violations horodatées (batterie < seuil, mémoire saturée, pointage impossible…).
**Sortie** : CONOPS quantifié branché sur les budgets et les exigences.

### Jalon 6 — Application Student (≈ 4 semaines, démarrable dès jalon 1)
- Navigation par étapes (Sujet, Orbite, Charges utiles, Plateforme, Liaisons, CONOPS, Analyses, Rapport).
- Vues : spec mission (lecture seule), éditeur d'orbite (types prédéfinis + libre, aperçu ground track), sélecteur catalogue (filtres, comparaison, prix), configurateur plateforme (slots, options grisées avec raison), éditeur CONOPS, tableau de bord vert/orange/rouge, courbes temporelles.
- Calculs lourds en thread/process séparé, annulation, progression ; cache.
- Sauvegarde automatique, annuler/rétablir, export `.json`.
- Aide intégrée et infobulles pédagogiques.
**Sortie** : parcours complet possible.

### Jalon 7 — Rapport .docx (≈ 2 semaines, démarrable dès jalon 1)
- Gabarit Word (styles, en-têtes/pieds, page de garde avec hash du projet) ; chapitres de la §9 des spécifications.
- Tableaux (exigences, conformité, budgets, nomenclature et coûts), figures (ground track, schéma bloc, courbes CONOPS, éclipses).
- **Encadrés balisés** à compléter ; contrôle de présence côté Teacher.
- Annexes : hypothèses, données catalogue, journal de calcul.
**Tests** : génération sur projets de référence, ouverture Word/LibreOffice.

### Jalon 8 — Application Teacher (≈ 3 semaines)
- Éditeur de **sujets de mission** (exigences, zones, stations, contraintes, budget, fournisseurs autorisés, TRL).
- Éditeur/validateur de **catalogues** (tableaux, import/export CSV/JSON, contrôles de plausibilité).
- **Ouverture de projets étudiants** : intégrité (hash/HMAC), rejeu des calculs, comparaison aux valeurs enregistrées, tableau de conformité, score indicatif (D10), synthèse de lot (CSV/Excel).
- Variantes de sujets (paramètres aléatoires encadrés) **[optionnel]**.

### Jalon 9 — Catalogues complets (≈ 4 semaines, en parallèle dès jalon 3)
- 5 fournisseurs plateformes fictifs × 3–8 produits ; règles de slots par plateforme.
- ~40–60 charges utiles (imageurs 5 cm → 1,2 m, spectromètres VNIR/SWIR/TIR, SAR X/C/L/P, têtes optiques, QKD, radio).
- ~40–60 équipements (propulsion, TT&C, descente, stockage, ADCS, EPS, calculateur) ; lanceurs rideshare/dédiés.
- Prix cohérents : lois d'échelle (masse, ouverture, puissance) + héritage/TRL + prime fournisseur, script de contrôle, revue d'expert.
- ≥ 3 **sujets de démonstration** (EO haute résolution, SAR/revisite, relais optique ou QKD) avec corrigé Teacher.

### Jalon 10 — Intégration, qualité, packaging (≈ 3 semaines)
- Tests de bout en bout et golden sur les sujets de démonstration.
- Performances : ouverture < 10 s, recalcul interactif < 2 s, simulation CONOPS 30 j < 30 s.
- Builds PyInstaller 3 OS (CI), signature/notarisation macOS **[?]**, tests sur machines propres, taille < ~500 Mo.
- Documentation : guide étudiant, guide enseignant, notes de modèles.
- Recette avec 2–3 étudiants/enseignants pilotes.

## 5. Planning global

| Phase | Jalons | Durée |
|---|---|---|
| Fondations | 0–1 | ~3 sem. |
| Cœur de calcul | 2–5 | ~13 sem. |
| Applications & rapport | 6–8 (chevauchement) | ~+4 sem. |
| Données & finition | 9–10 | ~+4 sem. |
| **Total** | | **≈ 5–6 mois à 1 personne ; ≈ 3–4 mois à 2–3 personnes** |

Chemin critique : 0 → 1 → 2 → 3/4 → 5 → 10. Les jalons 6, 7, 8, 9 démarrent dès que le modèle de données du jalon 1 est stable.

## 6. Tests et validation

- **Unitaires** par équation, cas de référence issus de la littérature (SMAD, Wertz, Larson, Kidder, Hemmati…).
- **Propriétés** (`hypothesis`) : monotonies, conservation, bornes.
- **Golden files** : sortie complète d'un projet de référence figée ; changements de moteur intentionnels et versionnés.
- **Validation croisée** des modèles orbitaux (GMAT/poliastro/skyfield) hors production.
- **Revue pédagogique** : plausibilité des résultats, messages guidant sans donner la solution.
- **UI** : `pytest-qt` sur parcours clés ; test fumée de l'exécutable construit.

## 7. Risques et mitigations

| Risque | Impact | Mitigation |
|---|---|---|
| Python 3.14 / dépendances | Blocage packaging | Preuve de faisabilité jalon 0, repli 3.12/3.13 |
| Taille / démarrage de l'exécutable | Gêne en examen | Éviter `cartopy`/`astropy`, onedir, exclusions, mesures CI |
| Complexité de la simulation | Retards | Mode moyenné rapide + mode détaillé ; CONOPS minimal puis enrichi |
| Plausibilité catalogues/prix | Crédibilité | Lois d'échelle + script de contrôle + revue d'expert |
| Modèles trop simplistes/complexes | Pédagogie | Niveaux de fidélité documentés ; pilotes tôt |
| Triche (partage/modif de fichiers) | Équité | HMAC, journal, variantes de sujet, rejeu Teacher |
| Dérive de périmètre | Délais | Livraison par type de charge utile (slices §8) |
| Divergence entre OS | Bugs | CI 3 OS dès jalon 0, `pathlib`, thème Qt maîtrisé |

## 8. Ordre de livraison par vertical slices

1. **Slice A** — EO optique panchromatique + plateforme petite/moyenne + SSO + budgets + rapport (première version utilisable vers le jalon 6).
2. **Slice B** — SAR + revisite/accès stations + CONOPS simple.
3. **Slice C** — Spectromètres.
4. **Slice D** — Télécoms optiques et radio.
5. **Slice E** — QKD, HEO/GEO, cas avancés.
Chaque slice ajoute modèles + catalogue + sujet de démonstration + tests.

## 9. Prochaines actions

1. Valider les choix techniques du §2 (Python 3.14, carte hors-ligne, pas de `pint`).
2. Lancer le **jalon 0** : environnement, squelette, CI, preuve de packaging.
3. En parallèle, rédiger les **modèles de calcul** (`docs/models/*.md`) et le **schéma des fichiers** (jalon 1).
