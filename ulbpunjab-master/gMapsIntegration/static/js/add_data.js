var markers = [];

function initialize() {
  var uluru = {lat:  26.168301, lng: 91.695671};
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 10,
    center: uluru,
    mapTypeId: 'hybrid'
  });

  // addMarker(uluru, map);

  google.maps.event.addListener(map, 'click', function(event) {
    var latlng = event.latLng.lat().toString() + "," + event.latLng.lng().toString();
    if(markers.length == 0) {
        markers.push(addMarker(event.latLng, map));
        document.getElementById('latlng').value = latlng;
    }
    else {
      markers[0].setMap(null);
      markers[0] = addMarker(event.latLng, map);
      document.getElementById('latlng').value = latlng;
    }
    map.panTo(markers[0].getPosition());
  });

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

google.maps.event.addDomListener(window, 'load', initialize);

$('#water').click(function(event) {
  event.preventDefault();
  $.ajax({
      url: '?',
      method: 'POST',
      data: {
          "latlng": document.getElementById('latlng').value.toString(),
          "area": document.getElementById('area').value.toString(),
          "csrfmiddlewaretoken": csrfmiddlewaretoken,
          "button": "water"
      },
      success: function (data) {
          alert("Successfully added water data");
      }
  });
});
$('#well').click(function(event) {
  event.preventDefault();
  $.ajax({
      url: '?',
      method: 'POST',
      data: {
          "latlng": document.getElementById('latlng').value.toString(),
          "area": document.getElementById('area').value.toString(),
          "csrfmiddlewaretoken": csrfmiddlewaretoken,
          "button": "well"
      },
      success: function (data) {
          alert("Successfully added Well data");
      }
  });
});
$('#airport').click(function(event) {
  event.preventDefault();
  $.ajax({
      url: '?',
      method: 'POST',
      data: {
          "latlng": document.getElementById('latlng').value.toString(),
          "area": document.getElementById('area').value.toString(),
          "name": document.getElementById('title').value,
          "csrfmiddlewaretoken": csrfmiddlewaretoken,
          "button": "airport"
      },
      success: function (data) {
          alert("Successfully added Airport Data");
      }
  });
});
$('#highway').click(function(event) {
  event.preventDefault();
  $.ajax({
      url: '?',
      method: 'POST',
      data: {
          "latlng": document.getElementById('latlng').value.toString(),
          "area": document.getElementById('area').value.toString(),
          "name": document.getElementById('title').value,
          "csrfmiddlewaretoken": csrfmiddlewaretoken,
          "button": "highway"
      },
      success: function (data) {
          alert("Successfully added Highway Data");
      }
  });
});
$('#river').click(function(event) {
  event.preventDefault();
  $.ajax({
      url: '?',
      method: 'POST',
      data: {
          "latlng": document.getElementById('latlng').value.toString(),
          "area": document.getElementById('area').value.toString(),
          "name": document.getElementById('title').value,
          "csrfmiddlewaretoken": csrfmiddlewaretoken,
          "button": "river"
      },
      success: function (data) {
          alert("Successfully added River Data");
      }
  });
});
