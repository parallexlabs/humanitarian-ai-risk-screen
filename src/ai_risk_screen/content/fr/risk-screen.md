# Écran de risque IA humanitaire

*Traduction de travail — révision bienvenue*

Une liste de contrôle en sept étapes pour décider si et comment utiliser un outil d'IA pour une tâche humanitaire ou d'ONG. Chaque étape désigne un **réviseur responsable** qui approuve avant de continuer.

## Comment utiliser cet écran

1. Compléter les sept étapes avec le réviseur nommé pour chacune.
2. Enregistrer les réponses dans le modèle vierge (`blank-screen.yaml`) ou le formulaire Web.
3. Exécuter `ai-risk-screen evaluate` ou utiliser l'évaluateur du site pour obtenir un résultat **vert**, **ambre** ou **rouge**.
4. Si le résultat est ambre, compléter une [charte pilote](pilot-charter.md) avant un déploiement plus large.
5. Consigner chaque affirmation factuelle dans le [registre de vérification des sources](source-check-ledger.md).

## Résultats

| Résultat | Signification |
|----------|---------------|
| **Vert** | Aide à faible risque approuvée avec vérification obligatoire des sources |
| **Ambre** | Pause pour examen confidentialité, protection ou partenaires ; poursuivre seulement via pilote contrôlé |
| **Rouge** | Ne pas utiliser — entrée prohibée, outil non approuvé, décision à enjeux élevés non vérifiable, ou aucun recours sûr |

---

## Étape 1 — Objectif et alternative sans IA

**Réviseur responsable :** Responsable de programme ou des opérations

| Question | Ce qu'il faut consigner |
|----------|-------------------------|
| Quelle tâche l'IA soutiendra-t-elle ? | Description claire du travail |
| Que feriez-vous sans IA ? | L'alternative sans IA (brouillon manuel, modèle, examen d'expert, réunion communautaire) |
| Qu'est-ce que l'IA ajoute ? | Temps gagné, couverture linguistique, échelle — énoncé honnêtement |
| La voie sans IA est-elle viable ? | Oui/non ; si non, expliquer pourquoi l'IA est proportionnée |

**Arrêt si :** La tâche est mieux servie par l'alternative sans IA et l'IA n'ajoute aucune valeur responsable.

---

## Étape 2 — Personnes et partenaires

**Réviseur responsable :** Point focal protection ou engagement communautaire

| Question | Ce qu'il faut consigner |
|----------|-------------------------|
| Quels intérêts sont touchés ? | Personnes affectées, personnel, bénévoles, communautés d'accueil |
| Quelle sécurité pourrait être compromise par des erreurs ? | Groupes à risque accru si le contenu est erroné ou divulgué |
| Quelles langues et quel contexte local comptent ? | Langues, dialectes, références culturelles, niveaux d'alphabétisation |
| Qui doit être consulté avant utilisation ? | Leaders communautaires, gouvernement, partenaires du cluster, représentants des personnes affectées |

**Signaler pour examen ambre si :** Une consultation de partenaires ou un examen protection est nécessaire.

---

## Étape 3 — Données

**Réviseur responsable :** Point focal protection des données ou gestion de l'information

| Question | Ce qu'il faut consigner |
|----------|-------------------------|
| Quels types de données sont impliqués ? | Personnelles, confidentielles, publiques, non personnelles sensibles (p. ex. lieux de distribution) |
| Quelle est votre autorité juridique ou politique ? | Consentement, contrat, intérêt public, politique organisationnelle |
| Comment minimiserez-vous les données ? | Caviardage, agrégation, exemples synthétiques, flux sans téléversement |
| Combien de temps les données seront-elles conservées ? | Période de conservation et méthode de suppression |

**Arrêt (rouge) si :** Une entrée prohibée est requise (p. ex. listes de bénéficiaires non caviardées dans un outil IA public).

**Signaler pour examen ambre si :** Des données personnelles ou non personnelles sensibles sont impliquées.

---

## Étape 4 — Outil et fournisseur

**Réviseur responsable :** TI, approvisionnement ou approbateur d'outils désigné

| Question | Ce qu'il faut consigner |
|----------|-------------------------|
| Quel outil et quelle version ? | Nom exact du produit |
| Qui est le fournisseur ? | Entité juridique et juridiction |
| Où les données sont-elles traitées ? | Pays/région de traitement et stockage |
| Qui peut accéder aux entrées et sorties ? | Rôles du personnel, personnel du fournisseur, sous-traitants |
| Quelle est la politique d'utilisation ultérieure ? | Entraînement sur vos données, partage avec tiers |
| Quel est le repli si l'outil échoue ? | Processus manuel, outil alternatif, report |

**Arrêt (rouge) si :** L'outil ne figure pas sur la liste approuvée de votre organisation.

---

## Étape 5 — Vérification des sorties

**Réviseur responsable :** Point focal matière ou MEAL

| Question | Ce qu'il faut consigner |
|----------|-------------------------|
| Comment les affirmations seront-elles vérifiées ? | Contre des sources fiables (statistiques officielles, dossiers de programme, textes juridiques) |
| Quelles sources fiables s'appliquent ? | Documents, bases de données ou responsables nommés |
| Comment tester biais et exclusion ? | Révision humaine avec un échantillon incluant les groupes marginalisés |
| Est-ce une décision à enjeux élevés ? | Décisions affectant la sécurité, l'admissibilité ou l'allocation de ressources |

**Arrêt (rouge) si :** Une décision à enjeux élevés ne peut pas être vérifiée par un humain avant action.

---

## Étape 6 — Contrôle humain

**Réviseur responsable :** Supérieur hiérarchique ou autorité déléguée

| Question | Ce qu'il faut consigner |
|----------|-------------------------|
| Qui prend la décision finale d'utiliser la sortie ? | Rôle nommé |
| Qui consigne les raisons ? | Responsable de la piste d'audit |
| Qui peut annuler ou rejeter la sortie IA ? | Autorité nommée |
| Quel recours existe pour les personnes lésées par des erreurs ? | Voie de plainte, processus de correction, indemnisation le cas échéant |

**Arrêt (rouge) si :** Aucune voie de recours sûre n'existe pour les personnes affectées.

---

## Étape 7 — Surveillance et arrêt

**Réviseur responsable :** Responsable du pilote ou des risques

| Question | Ce qu'il faut consigner |
|----------|-------------------------|
| Quelle est la portée du petit test ? | Utilisateurs, géographie ou fenêtre temporelle limités |
| Quel est le seuil d'échec ? | Taux d'erreur, nombre de plaintes ou type d'incident déclenchant l'arrêt |
| Quelle est la voie d'incident ? | Qui notifier et dans quel délai |
| Quand réviserez-vous ? | Date de révision prévue |
| Quelle est la règle de retrait ? | Conditions pour cesser l'IA pour cette tâche |

**Signaler pour examen ambre si :** Un pilote contrôlé est requis avant un déploiement plus large.
