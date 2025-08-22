# - verify
# - too much => by how much + type of payment
# - too little => by how much + type of payment
# - listen out for next transfer, if match the number. have a button for verifying and add to the previous one
# - cash
# - verify cash slip
# - summary by cash types
# - summary report for owner
import sqlite3

def employee_verify(transaction_id, employee_id, payment_type, verify_status, time_verified, amount_differences=None, reconcile_type=None):

    #regardless of what happens = store/update database?
    conn = sqlite3.connect("service.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO status_logs (transaction_id, employee_id, payment_type, verify_status, time_verified, amount_differences, reconcile_type) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            transaction_id, employee_id, payment_type, verify_status, time_verified, amount_differences, reconcile_type
        )
    )

    conn.commit()
    conn.close()


def get_too_little_transactions():
    conn = sqlite3.connect("service.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT transaction_id, amount_differences 
        FROM status_logs 
        WHERE payment_type = ? AND verify_status = ? AND reconcile_type = ?
        ORDER BY time_verified DESC
        """, ('transfer', 'too little', 'transfer')
    )

    too_little_transactions = cursor.fetchall()
    conn.commit()
    conn.close()
    return too_little_transactions

