import React from "react";
import { Card } from "react-bootstrap";
import { FaMoneyBillWave, FaWallet, FaPiggyBank, FaLightbulb } from "react-icons/fa";

const ICONS = [
  <FaMoneyBillWave size={24} color="#008080" />,
  <FaWallet size={24} color="#008080" />,
  <FaPiggyBank size={24} color="#008080" />,
  <FaLightbulb size={24} color="#008080" />,
];

export default function InsightCards({ insights }) {
  const { savings_summary } = insights;

  const cardData = [
    { title: "Total Income", value: savings_summary.total_income },
    { title: "Total Expenses", value: savings_summary.total_expenses },
    { title: "Estimated Savings", value: savings_summary.estimated_savings },
    { title: "Advice", value: savings_summary.suggestion },
  ];

  return (
    <div className="row">
      {cardData.map((card, idx) => (
        <div key={idx} className="col-md-3 mb-3">
          <Card className="h-100">
            <Card.Body>
              <div className="d-flex align-items-center mb-2">
                {ICONS[idx]}
                <Card.Title className="ms-2 mb-0">{card.title}</Card.Title>
              </div>
              <Card.Text className="text-muted">{card.value}</Card.Text>
            </Card.Body>
          </Card>
        </div>
      ))}
    </div>
  );
}
