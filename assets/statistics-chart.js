var annualChart = new Chart(document.getElementById("annualChart").getContext("2d"), {
  type: "line",
  data: {
    labels: ["1985", "1987", "1988", "1989", "1992", "1994", "1995", "1996", "1997", "1998", "1999", "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025"],
    datasets: [
      {
        label: "# Publications",
        backgroundColor: "rgb(23, 125, 255)",
        borderColor: "rgb(23, 125, 255)",
        data: [1, 2, 1, 1, 1, 3, 1, 3, 2, 6, 3, 4, 5, 9, 15, 15, 15, 18, 22, 30, 47, 47, 46, 68, 67, 71, 73, 85, 68, 82, 68, 33, 40, 53, 40, 32, 5]
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
    labels: ["1985", "1987", "1988", "1989", "1992", "1994", "1995", "1996", "1997", "1998", "1999", "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025"],
    datasets: [
        {
          label: 'Generation',
          data: [0, 0, 0, 0, 0, 2, 1, 3, 1, 2, 1, 3, 2, 7, 9, 9, 8, 10, 11, 20, 25, 30, 21, 34, 20, 22, 34, 29, 24, 37, 24, 11, 14, 23, 13, 10, 3]
        },
        {
          label: 'Application',
          data: [1, 2, 1, 1, 1, 1, 0, 0, 1, 3, 2, 1, 1, 0, 4, 1, 3, 4, 7, 4, 12, 10, 13, 17, 20, 25, 13, 26, 24, 25, 33, 6, 15, 23, 22, 15, 2]
        },
        {
          label: 'Evaluation',
          data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 2, 1, 0, 5, 0, 3, 1, 2, 2, 3, 3, 5, 6, 4, 7, 14, 7, 4, 3, 3, 2, 2, 3, 4, 0]
        },
        {
          label: 'Optimization',
          data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 3, 5, 2, 5, 4, 7, 9, 5, 5, 4, 5, 2, 4, 3, 2, 0, 1, 0]
        },
        {
          label: 'Model',
          data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1, 0, 1, 0, 1, 0, 0, 2, 8, 5, 8, 6, 6, 3, 3, 3, 1, 0, 0, 0, 0]
        },
        {
          label: 'Diagnosis',
          data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 2, 4, 4, 2, 1, 2, 2, 8, 2, 6, 2, 2, 2, 2, 0]
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
