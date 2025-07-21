# TODO Architecture Technique & Déploiement

## Objectif
Définir et mettre en œuvre une architecture scalable, sécurisée et maintenable.

### Étapes
1. **✅ Initialisation de l'infrastructure Docker** ([Issue #26](https://github.com/MrRaph/Bloomzy/issues/26)) - **TERMINÉ**
   - ✅ Branche `infra/docker-init` créée et développée.
   - ✅ Docker Compose amélioré (dev, prod, full, monitoring).
   - ✅ Health checks et dépendances conditionnelles.
   - ✅ Stack de monitoring (Prometheus, Grafana, exporters).
   - ✅ CI/CD pipeline avec GitHub Actions.
   - ✅ Scripts de backup/recovery automatisés.
   - ✅ Makefile enrichi avec nouvelles commandes.
   - ✅ Tests et validation complète.
   - **Commit** : c7e107b - Infrastructure complète et opérationnelle

2. **⏸️ Déploiement des microservices** ([Issue #27](https://github.com/MrRaph/Bloomzy/issues/27)) - **DÉPRIORISÉ - À TRAITER EN DERNIER**
   - ⚠️ **DÉCISION ARCHITECTURALE** : Les microservices sont mis de côté pour se concentrer sur les fonctionnalités
   - API Gateway, Auth, Indoor, Garden, Notifications, AI, File, Weather.
   - Objectif : Orchestration, scaling, monitoring.
   - Validation : Tests d'intégration, monitoring Prometheus/Grafana.
   - **Prérequis** : ✅ Infrastructure Docker terminée
   - **Note** : À implémenter APRÈS tous les autres modules (Garden, AI, Community)

3. **⏸️ Sécurité et conformité** ([Issue #28](https://github.com/MrRaph/Bloomzy/issues/28)) - **DÉPRIORISÉ**
   - ⚠️ **DÉPENDANT** : Attend le déploiement microservices
   - Chiffrement, RBAC, MFA, audit, RGPD.
   - Objectif : Implémentation, documentation, tests de sécurité.
   - Validation : Audit automatisé, tests de conformité.
   - **Prérequis** : Microservices déployés

4. **⏸️ Monitoring, backup et recovery** ([Issue #29](https://github.com/MrRaph/Bloomzy/issues/29)) - **DÉPRIORISÉ**
   - ⚠️ **DÉPENDANT** : Attend le déploiement microservices
   - Logs, alertes, backup, disaster recovery.
   - Objectif : Implémentation, documentation, tests unitaires.
   - Validation : Scénarios de recovery testés, monitoring opérationnel.
   - **Prérequis** : Microservices déployés

### Critères de validation
- Fonctionnalités testées (TDD)
- Documentation technique
- PRs avec revue et merge

### Statut global
**Module Architecture** : ⏸️ **DÉPRIORISÉ** (1/4 terminé - 3/4 reporté)
- ✅ Issue #26 : Infrastructure Docker terminée
- ⏸️ **NOUVELLE PRIORITÉ** : Se concentrer sur API Consistency puis Garden/AI/Community
- ⏸️ Issues #27, #28, #29 reportées en fin de roadmap
- **Note** : Infrastructure Docker robuste disponible pour tous les autres modules

### Nouveau planning architectural
1. **Phase actuelle** : Consolidation API Consistency (priorité #1)
2. **Phase suivante** : Modules fonctionnels (Garden → AI → Community)  
3. **Phase finale** : Architecture microservices (Issues #27, #28, #29)
