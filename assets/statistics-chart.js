var annualLineChart = document.getElementById("annualLineChart").getContext("2d");

var myBarChart = new Chart(annualLineChart, {
  type: "line",
  data: {
    labels: ["1985", "1987", "1988", "1989", "1992", "1994", "1995", "1996", "1997", "1998", "1999", "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025"],
    datasets: [
      {
        label: "# Publications",
        backgroundColor: "rgb(23, 125, 255)",
        borderColor: "rgb(23, 125, 255)",
        data: [1, 2, 1, 1, 1, 3, 1, 3, 2, 6, 3, 4, 5, 9, 15, 15, 15, 18, 22, 30, 47, 47, 46, 68, 67, 71, 73, 85, 68, 82, 67, 30, 33, 47, 34, 23, 2]
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