<html>
<head><title>Life Cycle</title>
<script src='https://api.tiles.mapbox.com/mapbox.js/v2.0.1/mapbox.js'></script>
 <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
<link href='https://api.tiles.mapbox.com/mapbox.js/v2.0.1/mapbox.css' rel='stylesheet' />
<link href="style.css" rel='stylesheet'/>
<link href="ico.css" rel='stylesheet'/>

</head>

<body>

<?php

//Connect to MySQL
$connect = mysql_connect("localhost","root","your_password");

$mapa = "SELECT * FROM plantMatrix.coordsTest WHERE plantMatrix.coordsTest.LatitudeDec != 'NA' && LongitudeDec !='NA' && SpeciesAccepted !='NA' GROUP BY SpeciesAccepted";

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
          'authors' => $row['Authors'],
          'doiisbn' => $row['DOIISBN'],
          'additionalsource' => $row['AdditionalSource'],
          'yearpublication' => $row['YearPublication'],
          'ecoregion' => $row['Ecoregion'],
          'title' => $row['SpeciesAccepted'],
          'speciesauthor' => $row['SpeciesAuthor'],
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
        'marker-symbol' => 'garden'
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


<div class="custom-popup" id="map">

</div>



<div id="toolbar">
<ul>
  <li><span class="icon-leaf"></span><strong>PlantMatrix</strong></li>
  <li><span class="icon-users"></span><a href="http://144.173.72.162:8080/share">Sign In</li>
</ul>
</div>

<div class="info" id="info"></div>


<script>

//Get GeoJSON from PHP, store as js var
var geoJson = <?php echo json_encode($geojson,JSON_NUMERIC_CHECK); ?>;

var southWest = L.latLng(-84.938342,   -179.473040),
    northEast = L.latLng(84.907230,  179.138422),
    bounds = L.latLngBounds(southWest, northEast),
    access = 'pk.eyJ1IjoiZnJhbmNlc2Nhc2FyZ2VudCIsImEiOiJvZmFuUzM0In0.-gsScOsPRxKs9E8qNy3qwg',
    mapdes = 'francescasargent.ja3p4m1n';



function createMap(access, mapdes, geoJson, bounds, callback) {
  L.mapbox.accessToken = access;
  map = L.mapbox.map('map', mapdes, {
      continuousWorld: false,
      noWrap: true,
      maxBounds: bounds,
      maxZoom: 20,
      minZoom: 4
    
  })
  .setView([42, 7],3);

  if (map.getZoom() <= 3){
    map.fitBounds(bounds);
  }

  callback(geoJson, hoverPopUp);
}

function addFeatureLayer(geoJson, callback) {
  featureLayer = L.mapbox.featureLayer()
  .setGeoJSON(geoJson)
  .addTo(map)

  callback(map, clickEvents) 
}


function hoverPopUp(map, callback) {
  isClicked = $(this).data('clicked');

  featureLayer.on('mouseover', function(e, layer) {
    e.layer.openPopup();
  });

  featureLayer.on('mouseout', function(e, layer) {
    if (!isClicked) {
      return;
    } else {
      e.layer.closePopup();
    }  
  });

  callback(map); 
}

function clickEvents(map) {
  featureLayer.on('click', function(e, layer) {

    feature = e.layer.feature;
    ob = feature.properties.database;
    
    console.log(ob);
    
    e.layer.openPopup();
    contentPopup(feature, ob);
    
    map.panTo(e.layer.getLatLng());

  })
}

function contentPopup(feature, ob) {
  
  for (var key in ob) {
    if (ob.hasOwnProperty(key)) {
      var object = key + " -> " + ob[key].toString();
      console.log(object);
    } else {
      return;
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
    + '<div class="graph"><a href= "graph/'+ ob.matrixnumber +'_' + ob.speciesauthor + '_dot.png" target="_blank"><img src="graph/'+ ob.matrixnumber +'_' + ob.speciesauthor +'_dot.png"></a></div>'                          
    +'</div>';

  info.innerHTML = content;
}

createMap(access, mapdes, geoJson, bounds, addFeatureLayer)


// Clear the tooltip when map is clicked.


// Trigger empty contents when the script
// has loaded on the page.
empty();

function empty() {
  info.innerHTML = '';
}



featureLayer.on('dblclick'), function(e) {
  map.setView(e.latlng, map.getZoom() + 2).panTo(e.latlng);
  map.panTo(e.latlng);
}




</script>


</body>
</html>
