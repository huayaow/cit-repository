var annualChart = new Chart(document.getElementById("annualChart").getContext("2d"), {
  type: "line",
  data: {
    labels: {{ chart_annual.year }},
    datasets: [
      {
        label: "# Publications",
        backgroundColor: "rgb(23, 125, 255)",
        borderColor: "rgb(23, 125, 255)",
        data: {{ chart_annual.value }}
      },
    ],
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      yAxes: [
        {
          ticks: {
            beginAtZero: true,
          },
        },
      ],
      x: {
        grid: {
          display: false,
        },
      },
    },
    plugins: {
      legend: {
        display: false,
      },
    },
  },
});

Chart.register(ChartjsPluginStacked100.default);
var annualDistChart = new Chart(document.getElementById("annualDistChart").getContext("2d"), {
  type: 'bar',
  data: {
    labels: {{ chart_topic.year }},
    datasets: [
        {
          label: 'Generation',
          data: {{ chart_topic.generation }}
        },
        {
          label: 'Application',
          data: {{ chart_topic.application }}
        },
        {
          label: 'Evaluation',
          data: {{ chart_topic.evaluation }}
        },
        {
          label: 'Optimization',
          data: {{ chart_topic.optimization }}
        },
        {
          label: 'Model',
          data: {{ chart_topic.model }}
        },
        {
          label: 'Diagnosis',
          data: {{ chart_topic.diagnosis }}
        },
    ]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      x: {
        grid: {
          display: false,
        },
      },
      y: {
        ticks: {
          callback: function(value, index, ticks) {
            return value + '%';
          }
        },
      },
    },
    plugins: {
      stacked100: { 
        enable: true, 
        replaceTooltipLabel: false 
      },
      tooltip: {
        callbacks: {
          label: function(tooltipItem) {
            const data = tooltipItem.chart.data;
            const datasetIndex = tooltipItem.datasetIndex;
            const index = tooltipItem.dataIndex;
            const datasetLabel = data.datasets[datasetIndex].label || "";
            // You can use two type values.
            // `data.originalData` is raw values,
            // `data.calculatedData` is percentage values, e.g. 20.5 (The total value is 100.0)
            const originalValue = data.originalData[datasetIndex][index];
            const rateValue = data.calculatedData[datasetIndex][index];
            return `${datasetLabel}: ${rateValue}% (number ${originalValue})`;
          }
        }
      }
    },
  },
});
