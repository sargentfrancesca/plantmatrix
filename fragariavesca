<html>
<head><title>GeoJSON</title>
<script src='https://api.tiles.mapbox.com/mapbox.js/v2.0.1/mapbox.js'></script>
<link href='https://api.tiles.mapbox.com/mapbox.js/v2.0.1/mapbox.css' rel='stylesheet' />

<style type="text/css">

body {
  font-family: Helvetica, sans-serif;
  -webkit-font-smoothing: antialiased;
}

#map {
	width: 100%;
	height: 100%;

}

.custom-popup .leaflet-popup-content-wrapper {
  background:#2ecc71;
  color:#fff;
  font-size:1em;
  line-height:24px;
  font-weight: normal;
  text-decoration: none;
  font-style: normal;
}

.custom-popup .leaflet-popup-content-wrapper a {
  color:rgba(255,255,255,0.5);
}

.custom-popup .leaflet-popup-tip-container {
  width:30px;
  height:15px;
}

.custom-popup .leaflet-popup-tip {
  border-left:15px solid transparent;
  border-right:15px solid transparent;
  border-top:15px solid #2ecc71;
}

.info {
  position: absolute;
  top: 10%;
  left: 1%;
}

.info div {
  background:#2ecc71;
  padding: 1em;
  border-radius: 1em;
  color: #fff;
  box-shadow: 0.5em 0.5em 0 #95a5a6;
}




</style>
</head>

<body>

<?php

//Connect to MySQL

$connect = mysql_connect("localhost","root","password");

$mapa = "SELECT * FROM plantMatrix.coordsTest WHERE plantMatrix.coordsTest.SpeciesAuthor = 'Fragaria_vesca' && LatitudeDec != 'NA'";

$dbquery = mysql_query($mapa,$connect);

//Creating GeoJSON array, ready to store values in GeoJSON format 
//GeoJSON format reference - http://geojson.org/
$geojson = array( 'type' => 'FeatureCollection', 'features' => array());


  while($row = mysql_fetch_assoc($dbquery)){

    $marker = array(
      'type' => 'Feature',
      'properties' => array(
        'title' => '<em>'.$row['SpeciesAccepted'].'</em><br>'.$row['Population'],
          'database' => array(
          'title' => $row['SpeciesAccepted'],
          'population' => $row['Population'],
          'journal' => $row['Journal'],
          'isbn' => $row['DOIISBN'],
          'growthtype' => $row['GrowthType'],
          'growthform' => $row['GrowthFormRaunkiaer'],
          'numberpopulations' => $row['NumberPopulations'],
          'kingdom' => $row['Kingdom'],
          'phylum' => $row['Phylum'],
          'angiogymno' => $row['AngioGymno'],
          'dicotmonoc' => $row['DicotMonoc'],
          'class' => $row['Class'],
          'order' => $row['_Order'],
          'family' => $row['Family'],
          'genus' => $row['Genus'],
          'studiedsex' => $row['StudiedSex'],
          'matrixcomposite' => $row['MatrixComposite'],
          'matrixtreatment' => $row['MatrixTreatment'],
          'latitudedec' => $row['LatitudeDec'],
          'longitudedec' => $row['LongitudeDec'],
          'altitude' => $row['Altitude'],
          'country' => $row['Country'],
          'continent' => $row['Continent'],
          'matrixsplit' => $row['MatrixSplit'],
          'matrixnumber' => $row['Matrixnumber'],
          'dimension' => $row['Dimension'],
          'planttype' => $row['plantType'],
          'matrix' => $row['matrix'],
          'classnames' => "–Nodes',–Small plants',–Large plants'",
          'statusstudy' => $row['StatusStudy'],
          'statuselsewhere' => $row['StatusElsewhere']
          
        ),
        'marker-color' => '#e74c3c',
        'marker-size' => 'small',
      ),
      'geometry' => array(
        'type' => 'Point',
        'coordinates' => array( 
          $row['LongitudeDec'],
          $row['LatitudeDec']
        )
      )
    );
    array_push($geojson['features'], $marker);
    //echo json_encode($marker);
  }


?>


<div class="custom-popup" id="map"></div>
<div class="info" id="info"></div>


<script>

var 
    click = document.getElementById('click'),
    mousemove = document.getElementById('mousemove');

//Get GeoJSON from PHP, store as js var
var geoJson = <?php echo json_encode($geojson,JSON_NUMERIC_CHECK); ?>;
console.log(geoJson);

L.mapbox.accessToken = 'pk.eyJ1IjoiZnJhbmNlc2Nhc2FyZ2VudCIsImEiOiJvZmFuUzM0In0.-gsScOsPRxKs9E8qNy3qwg';

var map = L.mapbox.map('map', 'examples.map-h67hf2ic')
    .setView([47.49694444, 7.652777778], 12).featureLayer.setGeoJSON(geoJson);


map.eachLayer(function(layer) {
  map.on('mouseover', function(e, layer) {
    e.layer.openPopup();

  });
  map.on('mouseout', function(e, layer) {
    
    e.layer.closePopup();
  });
});

// Listen for individual marker clicks.
map.on('click',function(e) {
    // Force the popup closed.
    e.layer.closePopup();

    var feature = e.layer.feature;
    var ob = feature.properties.database;

    

    //print array in console.log for reference
    for (var key in ob) {
      if (ob.hasOwnProperty(key)) {
        var object = key + " -> " + ob[key].toString();
        console.log(object);
      }
    }

    var content = '<div>' + '<strong>' + 'Species Name: </strong>' + ob.title + '<br>'
                          + '<strong>' + 'Population: </strong>' + ob.population + '<br>'  
                          + '<sub>' + ob.journal + ob.isbn + '</sub><br>'  
                          + '<strong>' + 'Growth Type: </strong>' + ob.growthtype + '<br>' 
                          + '<strong>' + 'Plant Type: </strong>' + ob.planttype + '<br>' 
                          + '<strong>' + 'Continent: </strong>' + ob.continent + '<br>'
                          + '<strong>' + 'Matrix Composite: </strong>' + ob.matrixcomposite + '<br>' 
                          + '<strong>' + 'Continent: </strong>' + ob.continent + '<br>' 


    +'</div>';
    info.innerHTML = content;

});

// Clear the tooltip when map is clicked.
map.on('move', empty);

// Trigger empty contents when the script
// has loaded on the page.
empty();

function empty() {
  info.innerHTML = '';
  }







</script>


</body>
</html>
