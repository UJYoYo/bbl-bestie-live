import sqlite3

def create_tables():
    conn = sqlite3.connect("service.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS transaction_logs (
            income_id INTEGER PRIMARY KEY,
            transaction_id INTEGER,
            payment_type TEXT,
            amount DECIMAL (10,2),
            source_acc_id INTEGER,
            destination_acc_id INTEGER,
            time_received DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS status_logs (
            status_id INTEGER PRIMARY KEY,
            transaction_id INTEGER,
            employee_id INTEGER,
            payment_type TEXT,
            verify_status TEXT DEFAULT 'pending',
            time_verified DATETIME,
            amount_differences DECIMAL (10,2),
            reconcile_type TEXT,
            FOREIGN KEY (transaction_id) REFERENCES transaction_logs(transaction_id)
        )
        """
    )

    conn.commit()
    conn.close()



