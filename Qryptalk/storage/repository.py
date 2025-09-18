class Repository:
    """
    Provides higher-level data access combining database and key store.
    """
    def __init__(self, database, key_store):
        self.database = database
        self.key_store = key_store

    def add_contact(self, contact_id, public_key):
        # Add contact to database and store public key
        pass

    def get_contact(self, contact_id):
        # Retrieve contact info and public key
        pass

    def save_message(self, contact_id, message):
        # Save message to database
        pass

    def get_messages(self, contact_id):
        # Retrieve messages for contact
        pass
