
function toggleMarkers() {
    if (document.getElementById('show-breweries').checked) {
        showMarkers();
    } else {
        clearMarkers();
    }
}

function toggleLine() {
    if (document.getElementById('show-path').checked) {
        addLine();
    } else {
        removeLine();
    }
}

var flightPath;
var map;
var bounds = new google.maps.LatLngBounds();
var markers = [];

function initMap() {
    var mapOptions = {
        zoom: 4,
        center: new google.maps.LatLng(39, -100),
    };

    map = new google.maps.Map(document.getElementById('map_container'), mapOptions);

    var flightPlanCoordinates = [];
    var len = breweries.length;
    for (var i = 0; i < len; i++) {
        var myLatLng = new google.maps.LatLng(breweries[i][1], breweries[i][2]);
        flightPlanCoordinates.push(myLatLng);
        // Put a different marker for home location.
        if(i == 0 || i == (len - 1)) {
            var marker = new google.maps.Marker({
                position: myLatLng,
                map: map,
                icon: home_icon,
                title: breweries[i][0]
            });
        } else {
            var marker = new google.maps.Marker({
                position: myLatLng,
                map: map,
                icon: beer_icon,
                title: breweries[i][0]
            });
        }

        markers.push(marker);
        bounds.extend(marker.getPosition());
    }
    // connect back to first node
    flightPlanCoordinates.push(new google.maps.LatLng(breweries[0][1], breweries[0][2]));

    flightPath = new google.maps.Polyline({
        path: flightPlanCoordinates,
        strokeColor: '#FF0000',
        strokeOpacity: 1.0,
        strokeWeight: 2
    });

    // addLine();
    // overall display settings
    map.setCenter(bounds.getCenter());
    map.fitBounds(bounds);
}

function addLine() {
    flightPath.setMap(map);
}

function removeLine() {
    flightPath.setMap(null);
}

// Sets the map on all markers in the array.
function setAllMap(map) {
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(map);
    }
}

// Removes the markers from the map, but keeps them in the array.
function clearMarkers() {
    setAllMap(null);
}

// Shows any markers currently in the array.
function showMarkers() {
    setAllMap(map);
}

google.maps.event.addDomListener(window, 'load', initMap);
