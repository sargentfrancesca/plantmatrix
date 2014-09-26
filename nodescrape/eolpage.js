var http = require("http");
var cheerio = require("cheerio");
var fs = require('fs'),
    request = require('request');
    path = require('path');

function download(tehurl, callback) {
  http.get(tehurl, function(res) {
    //console.log(tehurl);
 
var data = "";
    res.on('data', function (chunk) {
      //console.log("chunky");
      data += chunk;
    });
    res.on("end", function() {
      //console.log("endy");
      callback(data);
    });
  }).on("error", function() {
    //console.log("errorey");
    callback(null);
  });
}

//var SpeciesString = 'Calochortus macrocarpus';

eolScrape = '';

function linkify(string) {
	noNum = string.replace(/[0-9]/g, '');
	underscoreSpecies = string.replace(/\W/g, "+");
	searchTerm = 'http://eol.org/search?q=' + underscoreSpecies + '&show_all=true';
	console.log("Search URL: " + searchTerm)
	return searchTerm;
}

//var followLink = linkify(SpeciesString);

function searchTerm(string) {
	console.log('----------------------------')
	console.log("Search Term: " + string);
	followLink = linkify(string);
	searchLink(followLink, string);
}


function searchLink(url,string) {
	download(url, function(data) {
		if (data) {
			
			console.log('Data Exists, Loading Data...');

			$ = cheerio.load(data);
			topResult = $('#main > div > ul > li:nth-child(1) > h4 > a').text();
			secondResult = $('#main > div > ul > li:nth-child(2) > h4 > a').text();

				if ($('#main > div > div.header > h3:contains("No results")').length > 0) {
					console.log('No Results');
					return
				} else {
					console.log("Search Page Exists, Comparing Top Result...")
					console.log("Top Result: "+ topResult + ", Search Term: "+string);
						
						if (topResult == string) {
							console.log('Top Result matches Species Name');
							createFollow('1');
						} else {
							
							console.log('Second Result: '+secondResult);
							console.log('Checking second link...');
							
							if (secondResult == string) {
								createFollow('2');
							} else {

							console.log('Top Result '+ topResult + ' Species Name: ' + string + ' mismatch. Checking for any word match...');
							searchString = string.split(/[ \s]+/);
							resultString = topResult.split(/[ \s]+/);
							
							searchString.forEach(function(entry, string) {
								console.log('Checking: '+entry+'...');
								if (entry == resultString[0]) {
									stringMatch = true;

									createFollow('1');
									console.log('Match here: ' + followUrl);
									

								} else {
									stringMatch = true;
									return;
								}
							});
							console.log(searchString);

						}
					}
				}
			}
		});
}

function createFollow(i) {
	followUrlHref = $('#main > div > ul > li:nth-child('+i+') > h4 > a').attr('href');
	followUrl = 'http://eol.org' + followUrlHref;
	getData(followUrl);
}


function getData(url) {
	console.log("Get Data Initiated...");
	download(url, function(data) {
		if (data) {
			console.log("Data Available")
			$ = cheerio.load(data);
			var sciName = $('#page_heading > div > div.hgroup > h1 > i').text();
			var commonName = $(".hgroup h2").clone().children().remove().end().text();
			var commonName = commonName.replace(/(\r\n|\n|\r|)/gm,"");
			var commonName = commonName.replace(/\\/g, '');
			var imageUrl = $(".image img").attr("src");


			downloadImage(imageUrl, sciName);


			expObj(sciName, commonName, imageUrl);

		} else {
			console.log("No Data Available")
			return;
		}
	});
}

function downloadImage(url, name) {
    request.head(url, function (err, res, body) {
        name = name.replace(/(\s)/gm, '_'); 
        request(url).pipe(fs.createWriteStream('images/'+name+'.jpg'));
        console.log('Image was saved as: images/'+name+'.jpg')
    });
};

function expObj(sciName, commonName, imageUrl){
	eolScrape = {
				sciName : sciName,
				commonName : commonName,
				imageUrl : imageUrl
			}

			//console.log(eolScrape);
			return eolScrape;
			
}

function saveFile(category, country) {
    exportJSON = JSON.stringify(thisBlog);
    var filename = country + "-" + category;
    fs.writeFile(filename+".json", exportJSON, function (err) {
        if (err) {
            console.log(err);
        } else {
            console.log("The File " + filename + ".json was saved")
        }

    });
}


//searchTerm('Calochortus macrocarpus');


exports.eolScr = function(){ return eolScrape };
exports.searchLink = searchLink;
exports.download = download;
exports.searchTerm = searchTerm;
exports.linkify = linkify;
exports.getData = getData;
exports.downloadImage = downloadImage;
exports.saveFile = saveFile;
exports.createFollow = createFollow;
exports.eolScrape = eolScrape;

