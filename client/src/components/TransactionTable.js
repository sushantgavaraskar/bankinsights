import React from "react";
import { Table } from "react-bootstrap";

export default function TransactionTable({ transactions }) {
  return (
    <Table striped bordered hover responsive className="shadow-sm">
      <thead className="table-dark">
        <tr>
          <th>Date</th>
          <th>Description</th>
          <th>Amount</th>
          <th>Category</th>
          <th>Type</th>
        </tr>
      </thead>
      <tbody>
        {transactions.map((txn) => (
          <tr key={txn.id}>
            <td>{txn.date}</td>
            <td>{txn.description}</td>
            <td className={txn.is_credit ? "text-success" : "text-danger"}>₹ {txn.amount}</td>
            <td>{txn.category}</td>
            <td>{txn.is_credit ? "Credit" : "Debit"}</td>
          </tr>
        ))}
      </tbody>
    </Table>
  );
}
