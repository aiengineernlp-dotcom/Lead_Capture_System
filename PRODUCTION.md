SÉCURITÉ
□ Configurer SPF + DKIM sur tensoratech.com
  (supprimer "via sendgrid.net" dans Gmail)
□ Vérifier que .env n'est jamais commité sur Git
□ Stocker le Recovery Code SendGrid dans
  un gestionnaire de mots de passe sécurisé
□ Remplacer les credentials Docker (admin/secret)
  par des valeurs sécurisées en production

FASTAPI
□ Remplacer @app.on_event("startup/shutdown")
  par lifespan handlers (DeprecationWarning)

BASE DE DONNÉES
□ Configurer les backups automatiques PostgreSQL
□ Utiliser des variables d'environnement pour
  les credentials DB en production

INFRASTRUCTURE
□ Déployer sur un vrai serveur (Railway, Render,
  ou VPS)
□ Configurer un nom de domaine pour l'API
□ Mettre en place HTTPS (SSL certificate)

MONITORING
□ Ajouter des logs structurés en production
□ Configurer des alertes si l'API tombe