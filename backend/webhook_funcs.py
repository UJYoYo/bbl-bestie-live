import sqlite3

def store_transaction_db(payload_verified):
    conn = sqlite3.connect("service.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO transaction_logs (transaction_id, payment_type, amount, source_acc_id, destination_acc_id)
        VALUES (?, ?, ?, ?, ?)
        """, (
        payload_verified['transaction_id'],
        'transfer',
        payload_verified['amount'],
        payload_verified['source'],
        payload_verified['destination']
    ))

    conn.commit()
    conn.close()