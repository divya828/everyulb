var current_surface_water_chart;
var current_ground_water_chart;

function surface_water_chart(get_data) {
  var ctx = document.getElementById('myChart_surface_water').getContext('2d');
  if (current_surface_water_chart) {
    current_surface_water_chart.destroy();
  }
  current_surface_water_chart = new Chart(ctx, {
      // The type of chart we want to create
      type: 'bar',

      // The data for our dataset
      data: {
          labels: get_data["landfill"],
          datasets: [{
              label: "Surface Water Sample Quality",
              backgroundColor: 'rgb(62, 71, 152)',
              borderColor: 'rgb(62, 71, 152)',
              data: get_data["data"],
          }]
      },

      // Configuration options go here
      options: {
        scales : {
          xAxes : [ {
              gridLines : {
                  display : false
              }
          } ],
          yAxes : [ {
              gridLines : {
                  display : false
              },
              ticks: {
                beginAtZero: true
              }
          } ]
      }
      }
  });
}

function ground_water_chart(get_data) {
  var ctx = document.getElementById('myChart_ground_water').getContext('2d');
  if (current_ground_water_chart) {
    current_ground_water_chart.destroy();
  }
  current_ground_water_chart = new Chart(ctx, {
      // The type of chart we want to create
      type: 'bar',

      // The data for our dataset
      data: {
          labels: get_data["landfill"],
          datasets: [{
              label: "Ground Water Sample Quality",
              backgroundColor: 'rgb(62, 71, 152)',
              borderColor: 'rgb(62, 71, 152)',
              data: get_data["data"],
          }]
      },

      // Configuration options go here
      options: {
        scales : {
          xAxes : [ {
              gridLines : {
                  display : false
              }
          } ],
          yAxes : [ {
              gridLines : {
                  display : false
              },
              ticks: {
                beginAtZero: true
              }
          } ]
      }
      }
  });
}


$(document).ready(function(){

  $.ajax({
      url: '?',
      method: 'POST',
      data: {
          "value": "s0",
          "csrfmiddlewaretoken": csrfmiddlewaretoken,
          "button": "surface_water_get_data"
      },
      success: function (data) {

        surface_water_chart(data);
      }
  });

  $.ajax({
      url: '?',
      method: 'POST',
      data: {
          "value": "s0",
          "csrfmiddlewaretoken": csrfmiddlewaretoken,
          "button": "ground_water_get_data"
      },
      success: function (data) {

        ground_water_chart(data);
      }
  });

  $('#surface_water_get_data').change(function() {
    $.ajax({
        url: '?',
        method: 'POST',
        data: {
            "value": document.getElementById('surface_water_get_data').value.toString(),
            "csrfmiddlewaretoken": csrfmiddlewaretoken,
            "button": "surface_water_get_data"
        },
        success: function (data) {

          surface_water_chart(data);
        }
    });

  });

  $('#ground_water_get_data').change(function() {
    $.ajax({
        url: '?',
        method: 'POST',
        data: {
            "value": document.getElementById('ground_water_get_data').value.toString(),
            "csrfmiddlewaretoken": csrfmiddlewaretoken,
            "button": "ground_water_get_data"
        },
        success: function (data) {

          ground_water_chart(data);
        }
    });

  });
});
