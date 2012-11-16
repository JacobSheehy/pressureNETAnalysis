/*
 * pressureNET Analysis Server
 * Jacob Sheehy, Cumulonimbus
 * 
 * Run with node.js: node server.js
 * 
 * This source is released under the MIT license.
*/

var http = require('http');
var pg = require('pg'); 
var sys = require('sys');
var fs = require('fs');
var url = require('url');
var lineReader = require('line-reader');

var connectionString = "postgres://postgres:password@localhost:5432/postgres"; 

var returnPage = "";

http.createServer(function (req, res) {

var minVisLat = 0;
var maxVisLat = 0;
var minVisLon = 0;
var maxVisLon = 0;

 try  {
    minVisLat = url.parse(req.url, true).query.minVisLat;
    maxVisLat = url.parse(req.url, true).query.maxVisLat;
    minVisLon = url.parse(req.url, true).query.minVisLon;
    maxVisLon = url.parse(req.url, true).query.maxVisLon;
    startTime = url.parse(req.url, true).query.startTime;
    endTime   = url.parse(req.url, true).query.endTime;
    
    var after = function(callback) {
      return function(err, queryResult) {
        if(err) {
          return res.end("Error! " + sys.inspect(err))
        }
        callback(queryResult)
      }
    }
  } catch(e) {
    console.log(e);
  }
  
  function assembleJSGraphsFromData(result) {
   var finalJSCode = [];
   for(var i = 0; i < result.rows.length; i++) { 
     finalJSCode.push('[' + [(result.rows[i].daterecorded / 10000) + ',' +  result.rows[i].reading] + ']');
   }
   return '[' + finalJSCode + ']';
  }
  
  pg.connect(connectionString, after(function(client) {
    try{
        var q = "SELECT * FROM archive WHERE latitude > " + minVisLat + " and latitude < " + maxVisLat + " and longitude > " + minVisLon + " and longitude < " + maxVisLon + " and daterecorded > " + startTime + " and daterecorded < " + endTime + " ORDER BY daterecorded ASC limit 10000"; // limit 10000
        console.log(q); 
        client.query(q, after(function(result) {
          //console.log(q);
          var js = assembleJSGraphsFromData(result);
          var text = js;
          res.writeHead(200, {"Content-Type": "text/javascript", "Access-Control-Allow-Origin": "*"});

          res.end(text);
          //console.log(req);
        }))
     } catch(e) {
      console.log(e);      
     }
  }))
}).listen(3142, '127.0.0.1');

console.log('Server running at http://127.0.0.1:3142/');

