# TODO Architecture Technique & Déploiement

## Objectif
Définir et mettre en œuvre une architecture scalable, sécurisée et maintenable.

### Étapes
1. **Initialisation de l’infrastructure Docker**
   - Créer la branche `infra/docker-init`.
   - Objectif : Docker Compose, base images, CI/CD.
   - Validation : Build et tests automatisés.

2. **Déploiement des microservices**
   - API Gateway, Auth, Indoor, Garden, Notifications, AI, File, Weather.
   - Objectif : Orchestration, scaling, monitoring.
   - Validation : Tests d’intégration, monitoring Prometheus/Grafana.

3. **Sécurité et conformité**
   - Chiffrement, RBAC, MFA, audit, RGPD.
   - Objectif : Implémentation, documentation, tests de sécurité.
   - Validation : Audit automatisé, tests de conformité.

4. **Monitoring, backup et recovery**
   - Logs, alertes, backup, disaster recovery.
   - Objectif : Implémentation, documentation, tests unitaires.
   - Validation : Scénarios de recovery testés, monitoring opérationnel.

### Critères de validation
- Fonctionnalités testées (TDD)
- Documentation technique
- PRs avec revue et merge
