# Fichier: Dockerfile

# ÉTAPE 1: Partir d'une image Node.js légère (Alpine Linux)
FROM node:18-alpine

# ÉTAPE 2: Définir le dossier de travail à l'intérieur du conteneur
WORKDIR /app

# ÉTAPE 3: Copier les fichiers de définition des dépendances
# On le fait avant le reste pour optimiser le cache Docker
COPY package*.json ./

# ÉTAPE 4: Installer uniquement les dépendances de production
# (On n'a pas besoin de Jest dans l'image finale)
RUN npm install --production

# ÉTAPE 5: Copier tout le code source de l'application
COPY . .

# ÉTAPE 6: Indiquer que l'application écoute sur le port 3000
EXPOSE 3000

# CORRECTIF SÉCURITÉ (Semgrep) : On passe sur l'utilisateur 'node' au lieu de 'root'
USER node

# ÉTAPE 7: La commande de démarrage
CMD ["node", "app.js"]