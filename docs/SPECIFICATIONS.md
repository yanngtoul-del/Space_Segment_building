# Space Segment Builder — Spécifications détaillées (v0.1 — BROUILLON)

> Statut : brouillon de travail co-construit. Les points marqués **[?]** sont des décisions ouvertes.
> Les décisions déjà prises sont marquées **[D]**.

## 1. Objectifs

Logiciel d'examen pour étudiants (master / école d'ingénieur, examen d'une journée ou projet de plusieurs jours) :
à partir d'une **spécification de mission** fournie, l'étudiant construit un **segment spatial cohérent** :
plateforme + une ou plusieurs charges utiles + orbite + CONOPS, en choisissant dans des **catalogues**
multi-fournisseurs avec **prix**. Le logiciel calcule les performances, signale les incohérences
et génère un **rapport .docx** que l'étudiant complète (CONOPS, justifications, comparaison aux specs).

Objectifs pédagogiques : arbitrage charge utile ↔ plateforme ↔ orbite ↔ coût, compréhension des
couplages (masse, puissance, pointage, volume de données, liaison descendante, durée de vie, éclipses…).

## 2. Décisions techniques actées

| # | Décision |
|---|----------|
| D1 | Python 3.14 + interface de bureau **PySide6 (Qt)**, packagé en `.exe` stand-alone (PyInstaller, mode *onedir* ou *onefile*), aucune installation ni compilation côté étudiant |
| D2 | **Un étudiant = un poste, hors-ligne.** Sauvegarde d'un **fichier projet `.json`** (à remettre avec le rapport) |
| D3 | Rapport **Word (.docx)** généré (python-docx), avec sections vides à compléter |
| D4 | Fidélité **simulation avancée** : propagation d'orbite, éclipses, couverture/revisite, visibilité stations sol, budgets |
| D5 | Public : master / ingénieur, durée journée ou multi-jours |

## 3. Utilisateurs et parcours

**Étudiant** : charge sujet → lit la spec mission → choisit orbite → charge utile(s) → plateforme → options
→ définit CONOPS → lance analyses → itère → exporte rapport + fichier projet.

**Enseignant** (outil / mode séparé, **[?] à confirmer**) :
- éditer les catalogues (fichiers JSON/CSV lisibles, avec schéma validé) ;
- créer/éditer des **sujets de mission** (fichier `.mission.json`) ;
- ouvrir un fichier projet étudiant et **rejouer** les calculs (vérification d'intégrité, grille de contrôle automatique des exigences).

Parcours en onglets/étapes (workflow guidé mais non verrouillé) :
1. **Sujet** (spec mission : exigences, contraintes, budget)
2. **Orbite**
3. **Charge(s) utile(s)**
4. **Plateforme**
5. **Segment sol / liaisons** (stations, terminaux)
6. **CONOPS**
7. **Analyses & budgets** (tableau de bord vert/orange/rouge)
8. **Rapport**

## 4. Spécification de mission (entrée du sujet)

Fichier `.mission.json`, affiché en lecture seule à l'étudiant. Contenu :

- Contexte, intitulé, type de mission (observation optique, hyperspectral, SAR, télécom optique/radio, QKD, mixte…).
- **Exigences quantifiées** (chacune avec ID, valeur, seuil/objectif, méthode de vérification), exemples :
  - GSD ≤ X m, fauchée ≥ Y km, bandes spectrales, résolution spectrale, NESZ SAR, SNR minimal ;
  - revisite ≤ N h sur zone d'intérêt (polygone / liste de lat-lon) ;
  - débit/volume de données utile par jour, latence de livraison ;
  - débit lien optique, disponibilité (météo / nuages), taux de clé QKD ;
  - durée de vie ≥ N ans, fiabilité, désorbitation (règle 25 ans / 5 ans) ;
  - lanceur / masse max / enveloppe (rideshare vs lanceur dédié) ;
  - **budget total max (M€)** et éventuellement calendrier (date de lancement, TRL minimal).
- Contraintes (réglementaires, export, souveraineté : p. ex. n'autoriser que certains fournisseurs, **[?]**).
- Zones d'intérêt, stations sol imposées ou libres.
- Paramètres d'évaluation (pondérations coût / performances / robustesse, **[?]** pour la notation).

## 5. Orbite

Définition par l'étudiant :
- **Types prédéfinis** : LEO quelconque, SSO (heure locale du nœud descendant, altitude → inclinaison auto), LEO équatorial/inclinée,
  MEO, GEO, HEO (Molniya/Tundra), orbite gelée, repeat-ground-track (cycle de N jours / M révolutions, assistant d'altitude).
- **Paramètres libres** : a, e, i, Ω, ω, ν (ou altitude périgée/apogée), date/époque.
- **Constellation** (**[?]** : mono-satellite uniquement, ou N satellites en plans Walker ?).

Propagation :
- J2 (+ éventuellement J3/J4) analytique + traînée atmosphérique (modèle exponentiel ou NRLMSISE-00/Harris-Priester), pression de radiation solaire ;
- éphémérides Soleil/Lune (analytique type Meeus ou `skyfield`/`astropy` embarqué) ;
- pas de temps adaptatif, horizon ≥ durée de vie pour l'analyse de décroissance, ≥ 1 an pour les statistiques.

Sorties : ground track (carte), éclipses (durée, fréquence, β-angle annuel), heure locale, vitesse sol,
altitude/évolution (décroissance, maintien d'orbite), delta-V de maintien et désorbitation, dose de radiation (ceintures, SAA) estimée,
fenêtres de visibilité stations sol (élévation min, masque).

## 6. Catalogues

Principe : catalogues **fictifs mais réalistes**, inspirés des acteurs réels (noms fictifs pour éviter la confusion commerciale — **[?]** ou noms réels ?),
stockés en **JSON/CSV externes** (modifiables par l'enseignant), chacun avec : référence, fournisseur, TRL/héritage de vol, fiche de données,
**prix** (cohérent avec les caractéristiques), délai de livraison, contraintes d'export, notes de compatibilité.

### 6.1 Plateformes (≈ 5 fournisseurs, nombre de produits variable)

| Fournisseur (inspiration) | Gamme | Remarques |
|---|---|---|
| NewSpace modulaire (EnduroSat) | CubeSat 3U–16U, ESPA-class | Bas coût, charge utile limitée, pointage modeste |
| UK small-sat (SSTL) | 50–500 kg | Rapport coût/performance, héritage fort |
| Historique européen A (Airbus D&S) | 500 kg–6 t (type Astrobus/Eurostar) | Haute agilité/pointage, cher, long délai |
| Historique européen B (Thales Alenia Space) | 100 kg–6 t (type Proteus/Spacebus) | Gamme télécom + EO |
| NewSpace US/EU intermédiaire (type Apex/Terran/York) | 100–500 kg | Production série, prix agressif |

Paramètres plateforme (pour chaque produit) :
- masse sèche, **masse charge utile max**, volume/enveloppe, interface mécanique ;
- puissance orbite moyenne/crête **disponible pour la charge utile**, tension de bus, batteries (Wh, DoD, cycles), panneaux (surface, rendement, dégradation, déploiement/orientables) ;
- **pointage** : précision, stabilité, agilité (°/s, slew), capacité de balayage (pour SAR/imageurs push-broom) ;
- propulsion (type, Isp, Δ-V, masse ergols, poussée), interface de **désorbitation** ;
- **TT&C** (bande S/X/Ka/UHF, débit, puissance), stockage embarqué, débit descente charge utile (X/Ka, optique éventuel) ;
- thermique (plage, puissance dissipable), vibration/jitter (micro-vibrations), calculateur, redondance, **fiabilité & durée de vie**, tenue radiation (TID) ;
- orbites compatibles, **lanceurs compatibles** (masse/interface), prix (plateforme + intégration & essais), délai ;
- options (kits : propulsion supplémentaire, panneaux, antenne X, ISL…).

Les caractéristiques de charge utile **éliminent certaines plateformes** (masse, puissance, pointage, jitter, volume, débit, thermique…) via des règles de compatibilité automatiques (§8).

### 6.2 Charges utiles (plusieurs fournisseurs par catégorie)

1. **Imageurs optiques** (télescopes) : diamètres variés (ex. 5 cm → 1,2 m), focale, f/#, pas pixel, nb pixels, bandes (PAN, VNIR, SWIR, MWIR, LWIR/thermique), push-broom vs matriciel, QE, bruit, FTM, niveaux de quantification, masse, puissance, volume, jitter toléré, besoin de pointage, débit de données brut, compression, prix.
2. **Spectromètres** : hyperspectral VNIR/SWIR, thermique, sondeurs atmosphériques (GHG), résolution spectrale, nb de bandes, SNR de référence, fauchée, masse/puissance/prix.
3. **SAR** : bande (P/L/S/C/X/Ku), antenne (plane, réflecteur déployable), modes (stripmap, ScanSAR, spotlight), résolution, NESZ, PRF, puissance crête/moyenne, duty cycle, débit brut, masse, besoin d'agilité/thermique/alimentation.
4. **Télécoms optiques** (têtes optiques LEO↔sol, ISL, GEO relay ; type Mynaric, Tesat, Officina Stellare…) : diamètre d'ouverture, longueur d'onde, puissance émise, débit, sensibilité, divergence, précision de pointage requise, masse/puissance, interopérabilité (SDA, CCSDS…).
5. **Télécoms quantiques (QKD)** : décodeur BB84 / entangled-photons, taux de clé vs perte, nécessité de télescope, pointage ultra-fin, fenêtre nocturne, masse/puissance.
6. **Télécoms radio** : charges utiles (bandes UHF/S/X/Ku/Ka, transpondeurs transparents/régénératifs, antennes réseaux actifs/réflecteurs/cornets), PIRE, G/T, bande passante, empreinte, puissance DC.
7. **Autres** (**[?]** : GNSS-R, ELINT/ AIS, scientifique…).

### 6.3 Autres éléments catalogués (**[?]** à confirmer)

- Segment sol / stations (réseaux commerciaux type KSAT, Leaf, etc. : tarif par passe/par minute ; stations propres) ;
- Lanceurs (rideshare vs dédié : tarif par kg, orbites accessibles) ;
- Options plateforme (propulseur additionnel, stockage, antenne haut débit…) ;
- Assurance, opérations (équipe MOC, coût annuel), éléments de coût récurrents.

## 7. CONOPS (modèle d'opération)

Le logiciel modélise les CONOPS sous forme de **modes d'opération** et d'un **plan d'activités** pour simuler les budgets dans le temps :

- Modes du satellite : LEOP, commissioning, nominal, acquisition, descente, charge batterie/idle, survie, désorbitation.
- Pour chaque mode : consommation par équipement, attitude, pointage, thermique, débit de données.
- **Règles d'activité** : acquisition sur zones d'intérêt (conditions : éclairement, élévation solaire minimale, nuages…), télécharger sur stations lors des passes, durée max d'acquisition par orbite (duty cycle), manœuvres de maintien, calibration.
- Simulation temporelle (typiquement 1 à 30 jours + extrapolation annuelle) → **courbes batterie (SoC), mémoire embarquée, volume descendu, couverture, nombre d'images, revisite effective**.
- L'étudiant **complète textuellement** dans le rapport (LEOP, ops nominales, anomalies, fin de vie) ; le logiciel fournit un **modèle quantitatif minimal** (planning d'acquisition, ratios) et vérifie sa cohérence avec les budgets.

## 8. Moteurs de calcul & règles de cohérence

### 8.1 Calculs par type de charge utile

- **Optique** : GSD, fauchée, SNR (rapport éclairement/albédo, QE, bruit), FTM/NIIRS (approx. GIQE), effets de traînage/jitter, durée de pose, nb de lignes/s, débit brut/compressé, retard ; couverture/revisite sur zones d'intérêt ; dépointage latéral possible via agilité.
- **Spectro** : résolution spectrale, SNR par bande, fauchée, GSD, débit.
- **SAR** : résolution (range/azimut), fauchée, NESZ (équation radar), ambiguïtés, PRF/swath, puissance moyenne, débit, durée d'acquisition max, angle d'incidence vs orbite.
- **Télécom optique** : bilan de liaison (pertes géométriques, pointage, atmosphère, scintillation, nuages), marge, disponibilité (statistiques nuages/météo simplifiées), débit/volume par passe, acquisition/poursuite.
- **QKD** : taux de clé secret (pertes, bruit de fond, fenêtre nocturne), temps de visibilité.
- **Radio** : bilan de liaison montant/descendant (EIRP, G/T, FSPL, pertes, marge), débit/volume par passe, empreinte.

### 8.2 Budgets système

- **Masse** (par équipement, marge par maturité, ex. 5–20 %), vs capacité plateforme & lanceur ;
- **Puissance** (par mode, générée vs consommée sur orbite complète, éclipses, dimensionnement batterie/DoD) ;
- **Données** (génération, stockage, descente, saturation) ;
- **Pointage** (budget d'erreur : plateforme vs exigence charge utile) ;
- **Thermique** simplifié ; **dose de radiation** vs tenue ; **durée de vie** (batteries, panneaux, ergols/Δ-V, traînée) ;
- **Coût** : plateforme + charge(s) utile(s) + intégration/essais + lancement + opérations annuelles + station sol (CAPEX/OPEX), marges.

### 8.3 Règles de compatibilité (élimination)

Tests automatiques `OK / Attention / Bloquant`, avec **explication textuelle** pour l'étudiant (ex. « masse charge utile 78 kg > capacité 50 kg de la plateforme X »).
Exemples : masse, volume, puissance crête/moyenne, pointage/jitter/agilité, débit descendant, stockage, thermique, orbite/lanceur,
durée de vie, TRL, export, budget total.
**[?]** Décider si le logiciel *bloque* l'export du rapport en cas de non-conformité ou s'il l'autorise avec avertissement (recommandé : autoriser + marquer).

## 9. Rapport (.docx)

Généré automatiquement, structure :
1. Page de garde (étudiant, sujet, date, version logicielle, hash du projet) ;
2. Rappel de la spécification mission (exigences) ;
3. Description du système (orbite, plateforme, charge(s) utile(s), options) avec tableaux et schémas (carte ground track, schéma bloc, vue éclatée simplifiée) ;
4. Budgets (masse, puissance, données, coût) + graphiques ;
5. Résultats de performance et **tableau de conformité aux exigences** (valeurs calculées vs spec, statut) ;
6. Analyses orbitales (éclipses, β, revisite, visibilité sol, delta-V, durée de vie) ;
7. **Sections à compléter par l'étudiant** (encadrés balisés) : CONOPS détaillé, justification des choix, analyse des écarts/risques, alternatives étudiées, perspectives ;
8. Annexes : données catalogue utilisées, hypothèses, log des calculs.

## 10. Architecture logicielle (proposition)

```
space_segment_builder/
  app/                # UI PySide6 (vues, widgets, cartes)
  core/               # modèles de données (pydantic), unités (pint), projet
  catalog/            # chargeurs/validateurs JSON, schémas
  orbit/              # propagation, éclipses, couverture, visibilité
  payload/            # modèles par type de charge utile (optique, SAR, links...)
  system/             # budgets, règles de compatibilité, coûts
  conops/             # modes, plan d'activités, simulation temporelle
  report/             # génération .docx, graphiques (matplotlib)
  data/               # catalogues, sujets, stations, lanceurs
  tests/
```

Bibliothèques envisagées : PySide6, numpy/scipy, pydantic, pint, matplotlib (ou pyqtgraph), python-docx, cartographie hors-ligne (cartopy + Natural Earth embarqué, ou carte simple embarquée),
`astropy`/`skyfield`/`sgp4` (selon taille de l'exécutable).

Contraintes : **100 % hors-ligne**, démarrage < 10 s, exécutable < ~500 Mo, Windows (**[?]** macOS/Linux ?).

## 11. Qualité / intégrité

- Tests unitaires des modèles (cas de référence, comparaison à des valeurs de la littérature).
- Fichier projet versionné + horodaté + signature/hash pour éviter la modification triviale (**[?]** niveau de protection).
- Journal des actions (traçabilité de l'examen) : optionnel.

## 12. Plan de développement (proposition)

1. **Jalon 1** : squelette UI + modèle de données + catalogues pilotes (2 fournisseurs plateformes, 3 charges utiles) + orbite SSO + budgets masse/puissance + rapport minimal.
2. **Jalon 2** : propagation complète, éclipses, couverture/revisite, visibilité sol.
3. **Jalon 3** : modèles charges utiles complets (optique, spectro, SAR, comm optique/radio, QKD).
4. **Jalon 4** : CONOPS simulé, règles de compatibilité, coûts.
5. **Jalon 5** : catalogues complets (5 fournisseurs plateformes, ~40–60 charges utiles), sujets de démonstration, rapport complet.
6. **Jalon 6** : packaging `.exe`, tests, documentation étudiants/enseignant.

## 13. Questions ouvertes (à traiter ensemble)

Voir la liste de questions dans la conversation ; les réponses seront reportées ici.

## 14. Décisions complémentaires (session 1)

| # | Décision |
|---|----------|
| D6 | Catalogues : **noms fictifs** inspirés des acteurs réels, ordres de grandeur réalistes |
| D7 | **Mono-satellite uniquement** (pas de constellation ; liens ISL possibles uniquement vers un relais/satellite « externe » supposé) |
| D8 | Éléments catalogués en v1 : plateformes, charges utiles, **lanceurs** (rideshare/dédié, masse/orbite/prix). Segment sol : stations simplement paramétrées par la spec mission (hors catalogue v1) ; options plateforme incluses dans la fiche produit |
| D9 | **Deux applications séparées** : *Student* (construction du système + rapport) et *Teacher* (éditeur de sujets/catalogues, rejeu et contrôle des projets), partageant une bibliothèque `core` commune |
| D10 | **Pas de note automatique** : tableau de conformité + score indicatif (coût, performances, marges) pour aider la correction |
| D11 | Plateformes cibles : **Windows + macOS + Linux** (build PyInstaller par OS ; cartographie et calculs 100 % portables, pas de dépendance Windows-only) |

Conséquences : le §3 (mode enseignant intégré) est remplacé par l'application Teacher séparée ; le §5 « Constellation » est supprimé ;
le §6.3 est réduit aux lanceurs. Prochaine étape : spécifier en détail (1) le schéma des fichiers (mission, catalogues, projet) et
(2) les modèles de calcul par type de charge utile.

## 15. Sous-systèmes plateforme (session 2)

| # | Décision |
|---|----------|
| D12 | Plateforme **configurable** : *base* (structure, énergie de base, calculateur, thermique) + options/sous-systèmes. Les gros fournisseurs historiques offrent peu d'options, les NewSpace beaucoup |
| D13 | **ADCS sélectionnable individuellement** au catalogue (capteurs, actionneurs) avec budget de pointage détaillé |
| D14 | Autres sous-systèmes (propulsion, TT&C, descente charge utile, stockage de masse, énergie) : **modélisés en calcul**, proposés par plateforme sous forme de **variantes/packs d'options** (pas de catalogue individuel en v1) **[?] interprétation à confirmer : l'étudiant ne choisit-il vraiment que l'ADCS à la carte ?** |

### 15.1 Paramètres par sous-système et modèles de calcul

**Propulsion** (variante/pack) : type (gaz froid, électrique, mono/bi-ergol), poussée, Isp, puissance électrique requise, masse sèche, capacité d'ergols (kg, éventuellement extensible), prix.
Calculs : Tsiolkovski avec masse totale réelle ; budget Δv (injection/correction lanceur, LEOP, maintien d'altitude/traînée, évitement, désorbitation) vs capacité ; durée des manœuvres ; énergie requise pour la propulsion électrique ; marge Δv (>= 10 %).

**TT&C** : bande (UHF/S/X), antennes (omni/patch/réseau), puissance émission, débit TM/TC, sensibilité, chiffrement ; compatibilité avec les stations de la spec mission.
Calculs : bilan de liaison montant/descendant, marge, couverture en LEOP/survie (omni), volume TM/TC par jour, durée de passe.

**Descente charge utile** : émetteur X/Ka (ou optique), modulation/codage (CCSDS, DVB-S2X), PIRE, antenne fixe/orientable, puissance DC, masse.
Calculs : bilan de liaison, débit effectif par passe, volume descendu/jour vs volume généré (couplé au CONOPS et aux stations).

**Stockage de masse** : capacité BOL/EOL (dégradation), débit d'écriture/lecture, redondance, chiffrement.
Calculs : remplissage au cours du CONOPS, saturation, volume perdu, priorités.

**Calculateur / traitement** : puissance, capacité de traitement, compression embarquée (CCSDS 122/123), autonomie ; impact sur le débit à stocker/descendre.

**ADCS** (catalogue individuel) : capteurs (viseurs d'étoiles, gyroscopes/IMU, senseurs solaires, magnétomètres, GNSS), actionneurs (roues à réaction/CMG, magnéto-coupleurs, tuyères), masse/puissance/prix/précision.
Calculs : budget de pointage (connaissance, contrôle, stabilité, jitter), agilité (moment cinétique des roues vs inertie), saturation/désaturation des roues, couple de perturbation (gradient de gravité, aérodynamique, solaire, magnétique) ; compatibilité avec le besoin de la charge utile.

**Énergie** : surface et architecture des panneaux (fixes, déployés, orientables), rendement et dégradation, batterie (Wh, DoD, cycles) ; calculs couplés aux éclipses et au β de l'orbite, au bilan par mode.

**Thermique / structure** : bilan simplifié (dissipation charge utile, plage, radiateur) ; marge et vérification d'enveloppe/fréquence propre vs lanceur.

**Transverse** : redondance, FDIR/autonomie, fiabilité et durée de vie, dispositif de désorbitation, tenue radiation (TID).

## 16. Modèle « plateforme à emplacements » (session 3) — remplace D14

| # | Décision |
|---|----------|
| D14 (révisée) | **Tous** les sous-systèmes (propulsion, TT&C, descente charge utile, stockage de masse, ADCS, énergie, calculateur…) sont modélisés avec calcul **et** sélectionnables au catalogue, **dans les limites de ce que chaque plateforme autorise** |
| D15 | Chaque plateforme déclare des **emplacements (slots)** par sous-système : éléments compatibles, **nombre min/max**, éventuellement un élément **de base inclus** (prix inclus dans la plateforme) |
| D16 | Plusieurs équipements d'une même fonction possibles **sur certaines plateformes seulement** (ex. 2 systèmes de propulsion : électrique pour la montée + chimique pour l'évitement ; 2 émetteurs de descente ; 2 mémoires) |
| D17 | Les **options impliquent des surcoûts** : prix de l'option + surcoût d'intégration/qualification propre à la plateforme, délai supplémentaire éventuel |

### 16.1 Structure de données

```
Platform
  base: masse, volume, puissance, ... (prix de base inclus)
  slots: [
    { function: "propulsion",
      allowed: [id_equipement...],      # liste blanche propre à la plateforme
      included: [id...],                # équipement(s) inclus dans le prix de base (optionnel)
      min: 0, max: 2,                   # nb d'équipements simultanés
      exclusive_with: [...],            # exclusions (ex. propulsion électrique XOR bi-ergol)
      requires: [...],                  # dépendances (ex. propulseur électrique => panneaux orientables)
      integration_cost: {fixe, pct},    # surcoût d'intégration par option installée
      lead_time_delta, mass_delta, ... }
  ]
  option_packs: [...]                   # offres groupées (ex. « pack Δv étendu »)
Equipment (catalogue de sous-systèmes, par fonction)
  id, fournisseur, fonction, masse, puissance, volume, performances, prix, TRL, héritage
```

- Le catalogue d'équipements est **partagé** (un équipement peut être « allowed » sur plusieurs plateformes) ; la plateforme porte les règles d'installation.
- Un même équipement peut avoir des **prix/masses d'interface différents selon la plateforme** (surcharge locale) **[?]**.

### 16.2 Règles

- Le nombre d'équipements d'une fonction est borné par `min/max` du slot ; les cumuls masse/puissance/volume sont recalculés et contrôlés (§8.3).
- Les dépendances (`requires`) et exclusions (`exclusive_with`) produisent des messages explicites (« propulseur X nécessite panneaux orientables, non disponibles sur la plateforme Y »).
- **Coût plateforme configurée** = prix de base + Σ prix des équipements ajoutés (hors inclus) + Σ surcoûts d'intégration + éventuelles remises de pack.
- Les équipements **inclus** peuvent être **remplacés** (crédit partiel ou nul **[?]**).
- Les options indisponibles sont **visibles mais grisées avec la raison** (pédagogique) ou **masquées** **[?]**.

### 16.3 Cas d'usage illustratifs

- Petite plateforme NewSpace : 0 ou 1 propulsion (gaz froid ou électrique), 1 TT&C, pas de choix d'ADCS (fixe), stockage extensible.
- Plateforme intermédiaire : 1–2 propulsions, 1–2 émetteurs de descente, choix ADCS, panneaux fixes ou déployés.
- Plateforme historique grand format : peu d'options catalogue (configurations « héritage ») mais options avancées (propulsion bi-ergol + électrique, antennes orientables, redondance) à fort surcoût et délai.

### 16.4 Décisions complémentaires sur les options

| # | Décision |
|---|----------|
| D18 | Options indisponibles **visibles mais grisées avec la raison** |
| D19 | Un même équipement peut avoir **prix, surcoût d'intégration et masse d'interface spécifiques à la plateforme** (surcharge locale dans la définition du slot) |
| D20 | Équipement inclus **remplaçable sans crédit** (le prix de base ne change pas ; l'équipement de remplacement est facturé en plus) |
| D21 | **Pas de packs groupés** : options individuelles uniquement (le champ `option_packs` de §16.1 est retiré) |
