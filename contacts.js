// Fichier: contacts.js
let contacts = [];

// Récupérer tous les contacts
function getAllContacts() {
    return contacts;
}

// Ajouter un contact
function addContact(name, email) {
    // Validation simple : nom requis
    if (!name || name.trim() === '') {
        throw new Error('Le nom est obligatoire');
    }
    
    // Validation simple : format email
    if (!email || !email.includes('@')) {
        throw new Error('Email invalide');
    }

    const newContact = {
        id: Date.now(),
        name: name.trim(),
        email: email.trim(),
        createdAt: new Date()
    };

    contacts.push(newContact);
    return newContact;
}

// Supprimer un contact
function deleteContact(id) {
    const index = contacts.findIndex(c => c.id === parseInt(id));
    if (index === -1) throw new Error('Contact non trouvé');
    contacts.splice(index, 1);
    return true;
}

// Réinitialiser (pour les tests)
function resetContacts() {
    contacts = [];
}

module.exports = { getAllContacts, addContact, deleteContact, resetContacts };