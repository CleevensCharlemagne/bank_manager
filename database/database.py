import sqlite3

def create_database():
    conn = sqlite3.connect("banque.db")
    cursor = conn.cursor()

    # Table clients
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            client_id TEXT PRIMARY KEY,
            last_name TEXT NOT NULL,
            first_name TEXT NOT NULL,
            tax_id TEXT UNIQUE NOT NULL,
            address TEXT,
            birth_date DATE,
            email TEXT,
            phone TEXT,
            status TEXT CHECK(status IN ('0', '1')),
            registration_date DATE
        );
    ''')

    # Table accounts
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            account_num TEXT PRIMARY KEY,
            account_name TEXT NOT NULL,
            balance REAL NOT NULL,
            owner_id TEXT NOT NULL,
            status TEXT CHECK(status IN ('0', '1')),
            creation_date DATE,
            close_date DATE,
            account_type TEXT CHECK(account_type IN ('courant', 'epargne')),
            FOREIGN KEY (owner_id) REFERENCES clients(client_id)
        );
    ''')

    # Table courant_details
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courant_details (
            account_num TEXT PRIMARY KEY,
            overdraft_percentage REAL,
            interest_rate REAL,
            overdraft_used REAL,
            debt REAL,
            FOREIGN KEY (account_num) REFERENCES accounts(account_num)
        );
    ''')

    conn.commit()
    conn.close()
    print("Base de données créée avec succès.")

