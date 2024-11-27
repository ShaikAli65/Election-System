// VotesBarChart.js
import React from "react";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

// Register necessary components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const VotesBarChart = () => {
  // Sample data for candidates and their vote counts
  const data = {
    labels: ["Alice", "Bob", "Charlie", "Diana"],
    datasets: [
      {
        label: "Votes",
        data: [120, 150, 80, 200], // Sample vote counts
        backgroundColor: ["#4CAF50", "#FF6384", "#36A2EB", "#FFCE56"],
      },
    ],
  };

  const options = {
    animation: {
      duration: 2000, // Duration in milliseconds
      easing: "easeOutCirc", // Easing effect
    },
    scales: {
      x: {
        title: {
          display: true,
          text: "Candidates",
        },
      },
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: "Vote Count",
        },
      },
    },
  };

  return (
    <div className="h-3/5 w-3/6">
      <h2>Election Results</h2>
      <Bar data={data} options={options} />
    </div>
  );
};

export default VotesBarChart;
