var mysql = require('mysql');
var eol = require('./eolpage');
 
var connection = mysql.createConnection(
    {
      host     : 'localhost',
      user     : 'root',
      password : '',
      database : 'plantMatrix',
    }
);
 
connection.connect();
 
var queryString = 'SELECT * FROM coordsTest WHERE Matrixnumber < 3';



 
connection.query(queryString, function(err, rows, fields) {
    if (err) throw err;
 
    for (var i in rows) {
        var SpeciesString = (rows[i].SpeciesAccepted);
        var Matrixnumber = (rows[i].Matrixnumber);
        console.log("??"+eol.eolScr());
        console.log(Matrixnumber);
        eol.searchTerm(SpeciesString);

    }
});


 
connection.end();
