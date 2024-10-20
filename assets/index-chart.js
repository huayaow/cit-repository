var barChart = document.getElementById("barChart").getContext("2d");
var pieChart = document.getElementById("pieChart").getContext("2d");

var myBarChart = new Chart(barChart, {
  type: "bar",
  data: {
    labels: ["2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024"],
    datasets: [
      {
        label: "# Publications",
        backgroundColor: "rgb(23, 125, 255)",
        borderColor: "rgb(23, 125, 255)",
        data: [26, 30, 39, 50, 62, 76, 91, 113, 140, 181, 224, 268, 331, 394, 456, 522, 597, 659, 721, 778, 804, 831, 870, 895, 910]
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
        }
      },
    },
    plugins: {
      legend: {
        display: false,
      },
    },
  },
});

var myPieChart = new Chart(pieChart, {
  type: "pie",
  data: {
    datasets: [
      {
        data: [354, 299, 80, 60, 48, 44, 25],
        borderWidth: 0,
      },
    ],
    labels: ["Generation", "Application", "Evaluation", "Optimization", "Model", "Diagnosis", "Other"]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    pieceLabel: {
      render: "percentage",
      fontColor: "white",
      fontSize: 14,
    },
    tooltips: true,
    plugins: {
      legend: {
        position: 'bottom',
      },
    },
  },
});