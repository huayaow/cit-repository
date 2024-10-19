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
        data: [26, 30, 39, 50, 62, 76, 91, 113, 140, 181, 224, 268, 331, 394, 456, 522, 597, 659, 716, 765, 786, 803, 836, 839, 853]
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
    },
  },
});

var myPieChart = new Chart(pieChart, {
  type: "pie",
  data: {
    datasets: [
      {
        data: [350, 260, 74, 59, 48, 39, 23],
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
    tooltips: true    
  },
});