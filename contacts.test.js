// Fichier: contacts.test.js
const { addContact, getAllContacts, deleteContact, resetContacts } = require('./contacts');

beforeEach(() => {
    resetContacts();
});

test('Doit ajouter un contact valide', () => {
    const contact = addContact('Alice', 'alice@example.com');
    expect(contact.name).toBe('Alice');
    expect(getAllContacts()).toHaveLength(1);
});

test('Doit refuser un contact sans nom', () => {
    expect(() => addContact('', 'test@test.com')).toThrow('Le nom est obligatoire');
});

test('Doit refuser un email invalide (sans @)', () => {
    expect(() => addContact('Bob', 'bob-pas-email')).toThrow('Email invalide');
});

test('Doit supprimer un contact', () => {
    const contact = addContact('Charlie', 'charlie@example.com');
    deleteContact(contact.id);
    expect(getAllContacts()).toHaveLength(0);
});