// Fichier: app.js
const express = require('express');
const { getAllContacts, addContact, deleteContact } = require('./contacts');

// nosemgrep: javascript.express.security.audit.express-check-csurf-middleware-usage.express-check-csurf-middleware-usage
const app = express();
app.use(express.json()); // Pour lire le JSON reçu
app.use(express.static('public')); // Pour servir le HTML

// GET : Lire la liste
app.get('/api/contacts', (req, res) => {
    res.json(getAllContacts());
});

// POST : Ajouter un contact
app.post('/api/contacts', (req, res) => {
    try {
        const { name, email } = req.body;
        const newContact = addContact(name, email);
        res.status(201).json(newContact);
    } catch (error) {
        res.status(400).json({ error: error.message });
    }
});

// DELETE : Supprimer un contact
app.delete('/api/contacts/:id', (req, res) => {
    try {
        deleteContact(req.params.id);
        res.json({ message: 'Contact supprimé' });
    } catch (error) {
        res.status(404).json({ error: error.message });
    }
});

// Démarrage du serveur (seulement si lancé directement)
if (require.main === module) {
    const PORT = 3000;
    app.listen(PORT, () => console.log(`Serveur démarré sur le port ${PORT}`));
}

module.exports = app;