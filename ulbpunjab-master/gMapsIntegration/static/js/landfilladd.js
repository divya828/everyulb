var markers = [];
var map;
var area;
var overlay_polygon;

function initialize() {
  var uluru = {lat:  26.168301, lng: 91.695671};
  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 10,
    center: uluru,
    mapTypeId: 'hybrid'
  });

  var drawingManager = new google.maps.drawing.DrawingManager({
          drawingMode: google.maps.drawing.OverlayType.POLYGON,
          drawingControl: true,
          drawingControlOptions: {
            position: google.maps.ControlPosition.TOP_CENTER,
            drawingModes: ['polygon']
          }
        });
    drawingManager.setMap(map);
    google.maps.event.addListener(drawingManager, 'overlaycomplete', function(event) {
      if (event.type == 'polygon') {
        overlay_polygon = event.overlay;
        var path = event.overlay.getPath();
        area = google.maps.geometry.spherical.computeArea(path);
        var min_lat;
        var max_lat;
        var min_lng;
        var max_lng;

        for (var i =0; i < path.getLength(); i++) {
          var xy = path.getAt(i);
          if (i == 0) {
            min_lat = xy.lat();
            max_lat = xy.lat();
            min_lng = xy.lng();
            max_lng = xy.lng();
          }
          else {
            if (min_lat > xy.lat()) {
              min_lat = xy.lat();
            }
            if (max_lat < xy.lat()) {
              max_lat = xy.lat();
            }
            if (min_lng > xy.lng()) {
              min_lng = xy.lng();
            }
            if (max_lng < xy.lng()) {
              max_lng = xy.lng();
            }

          }
        }

        lat_cent = (min_lat + max_lat)/2;
        lng_cent = (min_lng + max_lng)/2;



        cent = {lat: lat_cent, lng: lng_cent};

        contentString = 'Area: ' + area.toString() + ' m^2';
        var infoWindow = new google.maps.InfoWindow;

        var latlng = lat_cent.toString() + "," + lng_cent.toString();
        document.getElementById('latlng').value = latlng;
        document.getElementById('area').value = area;

        markers.push(addMarker(cent, map));
        infoWindow.setContent(contentString);
        infoWindow.open(map, markers[0]);

        $.ajax({
            url: '?',
            method: 'POST',
            data: {
                "latlng": document.getElementById('latlng').value.toString(),
                "area": document.getElementById('area').value.toString(),
                "name": document.getElementById('title').value,
                "csrfmiddlewaretoken": csrfmiddlewaretoken,
                "button": "ajax_request"
            },
            success: function (data) {
                if (parseFloat(data["area"]) > 8903092) {
                    alert("Please Select a reasonable area! The largest Dumpsite in the world is 2200acres, i.e. 8903092 sq. meters. Select a smaller dumpsite");
                }
                changeData(data);
            }
        });

      }
    });

}

function removePolygon() {
  if (overlay_polygon) {
    overlay_polygon.setMap(null);
  }

  if(markers.length != 0) {
      markers[0].setMap(null);
      document.getElementById('latlng').value = "";
      document.getElementById('area').value = "";
      markers = [];
    }
}

// Adds a marker to the map.
function addMarker(location, map) {
  // Add the marker at the clicked location, and add the next-available label
  // from the array of alphabetical characters.
  var marker = new google.maps.Marker({
    position: location,
    map: map
  });

  return marker;
}

function changeData(data) {
  document.getElementById('cards_data').innerHTML = '<ul class="list-group list-group-flush">' +
  '<li class="list-group-item"><strong>Coordinates(Lat, Lng) : ' + data["latitude"] + ',' + data["longitude"] + '</strong></li>' +
  '<li class="list-group-item"><strong>State : ' + data["state"] + '</strong></li>' +
  '<li class="list-group-item"><strong>District : ' + data["district"] + '</strong></li>' +
  '<li class="list-group-item"><strong>The nearest Airport is : ' + data["airport_name"] + '</strong></li>' +
  '<li class="list-group-item"><strong>The distance from the Airport is : ' + data["distance_airport"] + 'meters</strong></li>' +
  '<li class="list-group-item"><strong>The nearest Road is : ' + data["road_name"] + '</strong></li>' +
  '<li class="list-group-item"><strong>The distance from Road is : ' + data["distance_road"] + 'meters</strong></li>' +
  '<li class="list-group-item"><strong>The distance from nearest WaterBody(Lakes, Ponds) is : ' + data["distance_water"] + 'meters</strong></li>' +
  '<li class="list-group-item"><strong>The distance from nearest Well is : ' + data["distance_well"] + 'meters</strong></li>' +
  '<li class="list-group-item"><strong>The nearest River is : ' + data["river_name"] + '</strong></li>' +
  '<li class="list-group-item"><strong>The distance from River is : ' + data["distance_river"] + 'meters</strong></li>' +
  '</ul>' ;
}

google.maps.event.addDomListener(window, 'load', initialize);
var me;

$('#landfill').click(function(event) {
  me = $(this);
  event.preventDefault();

  if ( me.data('requestRunning') ) {
      return;
  }

  me.data('requestRunning', true);

  $.ajax({
      url: '?',
      method: 'POST',
      data: {
          "latlng": document.getElementById('latlng').value.toString(),
          "area": document.getElementById('area').value.toString(),
          "name": document.getElementById('title').value,
          "csrfmiddlewaretoken": csrfmiddlewaretoken,
          "button": "landfill"
      },
      success: function (data) {
          alert("success");
          // removePolygon();
      },
      complete: function() {
          me.data('requestRunning', false);
      }
  });
});
