(function() {
    
    var global = this;

    var PressureNET = (global.PressureNET || (global.PressureNET = {}));

    var readingsUrl = '';

    var centerLat = 0;
    var centerLon = 0;
    var minVisLat = 38;
    var maxVisLat = 42;
    var minVisLon = -74;
    var maxVisLon = -70;
    var startTime = 0;
    var endTime = 0;
    var zoom = 9;
   
    var dataPoints = [];
    
    var defaultQueryLimit = 2000;
    var defaultQueryIncrement = 5000;
    //var largeQueryIncrement = 10000;
    
    var map;
    
    var currentQueryLimit = defaultQueryLimit;
    
    var events = [{
        eventName: "Sandy",
        eventDates: [new Date(), new Date()],
        eventDescription: "Sandy was a category 2...",
        eventLink: "http://en.wikipedia.org/wiki/Hurricane_Sandy",
        pointsOfInterest: [{
          pointName: "New York", 
          latitude: 40.670345225,
          longitude: -73.9425720,
          startTime: (new  Date(2012, 9, 25)).getTime(),
          endTime: (new  Date(2012, 10, 01)).getTime(),
          zoomLevel: 11
        }, {
          pointName: "New Jersey",
          latitude: 39.9977615,
          longitude: -74.7212280,
          startTime: (new  Date(2012, 9, 29)).getTime(),
          endTime: (new  Date(2012, 10, 01)).getTime(),
          zoomLevel: 9
        }]
    }, { // 29.989573859470866 -91.0675109863281 1346040000000 1346558400000 8
        eventName: "Isaac",
        eventDates: [new Date(), new Date()],
        eventDescription: "Isaac was a ...",
        eventLink: "http://en.wikipedia.org/wiki/Hurricane_Isaac_(2012)",
        pointsOfInterest: [{
          pointName: "Louisiana",
          latitude: 29.989573859470866,
          longitude: -91.0675109863281,
          startTime: 1346040000000,
          endTime: 1346558400000,
          zoomLevel: 8
        }]
    }, { // 39.98355761483058 -74.95125427246091 1352091600000 1352610000000 10
         // boston: 42.326689434570994 -71.50360717773435 1352178000000 1352610000000 9 
        eventName: "Post-Sandy Nor'easter",
        eventDates: [new Date(), new Date()],
        eventDescription: "After Sandy, ...",
        eventLink: "http://en.wikipedia.org/wiki/November_2012_nor'easter",
        pointsOfInterest: [{
          pointName: "Boston",
          latitude: 42.326689434570994,
          longitude: -71.50360717773435,
          startTime: 1352178000000,
          endTime: 1352610000000,
          zoomLevel: 9
        }]
      }];
    

    PressureNET.initialize = function(config) {
        readingsUrl = config.readingsUrl;

        $(function() {
            $("#start_date").datepicker({changeMonth: true,dateFormat: "yy/mm/dd" });
            $("#end_date").datepicker({changeMonth: true,dateFormat: "yy/mm/dd"});
          
            PressureNET.setDates(new Date(2012, 9, 28), new  Date(2012, 10, 01));
            PressureNET.initializeMap();
            PressureNET.loadAndUpdate(0);
        });

    }

    PressureNET.setMapPosition = function(latitude, longitude, zoomLevel, startTime, endTime) {
        PressureNET.setDates(new Date(startTime), new Date(endTime));
        map.setZoom(zoomLevel);
        var latLng = new google.maps.LatLng(latitude, longitude); //Makes a latlng
        map.panTo(latLng);
        PressureNET.updateAllMapParams();
        PressureNET.loadAndUpdate();
    }    

    PressureNET.loadEventInfo = function(eventName) {
      var eventId = 0;
      if(eventName=="sandy") {
        eventId = 0;
      } else if(eventName=="isaac") {
        eventId = 1;
      } else if(eventName=="noreaster") {
        eventId = 2;
      }
      $('#event_title_text').html(events[eventId].eventName);
      $('#event_date_text').html(events[eventId].eventDates[eventId] + ' to ' + events[eventId].eventDates[1]);
      
      var eventDescription = events[eventId].eventDescription;
      
      for(x = 0; x < events[eventId].pointsOfInterest.length; x++) {
          eventDescription += "<br><a style='cursor:pointer' onClick='PressureNET.setMapPosition(" + events[eventId].pointsOfInterest[x].latitude + ", " + events[eventId].pointsOfInterest[x].longitude + ", " + events[eventId].pointsOfInterest[x].zoomLevel + ", " + events[eventId].pointsOfInterest[x].startTime + ", " + events[eventId].pointsOfInterest[x].endTime + ")'>" + events[eventId].pointsOfInterest[x].pointName + "</a>";
      }
      
      $('#event_main_text').html(eventDescription);
    }

    PressureNET.dateRange = function() {
        var start = new Date($('#start_date').val());
        var end = new Date($('#end_date').val());

        // end - start returns difference in milliseconds 
        var diff = end - start;
        
        // get days
        var days = diff/1000/60/60/24;
        return days;
    }
     
    PressureNET.setDates = function(start, end) {
        //var start = new Date(2012, 9, 28);
        
        //var end = new  Date(2012, 10, 01);
        
        $('#start_date').datepicker('setDate',start);
        $('#end_date').datepicker('setDate',end);
        $('#start_date').val($.datepicker.formatDate('yy/mm/dd', start));
        $('#end_date').val($.datepicker.formatDate('yy/mm/dd', end));
    }

    PressureNET.loadAndUpdate = function(increment) {
        if(increment>0) {
            currentQueryLimit += defaultQueryIncrement;
        } else {
            currentQueryLimit = defaultQueryLimit;
        }

        $("#query_results").html("Loading...");
        
        startTime = $('#start_date').datepicker('getDate').getTime();
        endTime = $('#end_date').datepicker('getDate').getTime();
        
        var query_params = {
            format: 'json',
            minVisLat: minVisLat,
            maxVisLat: maxVisLat,
            minVisLon: minVisLon,
            maxVisLon: maxVisLon,
            startTime: startTime,
            endTime: endTime,
            limit: currentQueryLimit
        };

        $.ajax({
            url: readingsUrl,
            cache: false,
            data: query_params,
            dataType: 'json',
            success: function(readings, status) {
                var plot_data = [];
                var readings_sum = 0;
                for(var reading_i in readings) {
                    var reading = readings[reading_i];
                    plot_data.push([reading.daterecorded, reading.reading]);
                    readings_sum += reading.reading;
                }

                // remove outliers; find the mean, 
                // then +- 50 should be fine.
                var mean = readings_sum / readings.length;
                // console.log('mean ' + mean + ' total ' + readings.length);
                var minY = mean - 50;
                var maxY = mean + 50; 
                $.plot($("#placeholder"), [plot_data],{ 
                    lines:{show:false}, 
                    points:{show:true},
                    xaxis:{mode:"time"},
                    yaxis:{min:minY,
                           max:maxY}
                });
                 
                // if the results were likely limited, let the user show more
                var showMore = "";
                if(readings.length%1000 == 0) {
                    var showMore = "<a onClick='PressureNET.loadAndUpdate(1)' style='cursor:pointer'>Show More</a>";
                }
                $("#query_results").html("Showing " + readings.length + " results. " + showMore);
            }
        });
    }
    
    PressureNET.updateChart = function() {
        $('#current_position').html(centerLat + ", " + centerLon + " at zoom " + zoom);
    }
  
    PressureNET.notifyInteresting = function() {
        alert('Show smooth div to verify info and inform of successful submission');
    }
  
    PressureNET.updateAllMapParams = function() {
        centerLat = map.getCenter().lat();
        centerLon = map.getCenter().lng();
        var bounds = map.getBounds();
        var ne = bounds.getNorthEast();
        var sw = bounds.getSouthWest();
        minVisLat = sw.lat();
        maxVisLat = ne.lat();
        minVisLon = sw.lng();
        maxVisLon = ne.lng();
        
        zoom = map.getZoom();
        PressureNET.updateChart();
    },

    PressureNET.alertCumulonimbus = function() {
      startTime = $('#start_date').datepicker('getDate').getTime();
      endTime = $('#end_date').datepicker('getDate').getTime();
      document.location.href = "mailto:software@cumulonimbus.ca?subject=pressureNET%20Interesting%20Data&body=" + centerLat + "%20" + centerLon + "%20" + startTime + "%20" + endTime + "%20" + zoom;
    },
  
    PressureNET.initializeMap = function() {
        var mapOptions = {
          center: new google.maps.LatLng(40.6, -73.9), // start near nyc
          zoom: 10,
          mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        map = new google.maps.Map(document.getElementById("map_canvas"),
            mapOptions);
      
        var aboutToReload;
      
        google.maps.event.addListener(map, 'center_changed', function() {
            window.clearTimeout(aboutToReload);
            PressureNET.updateAllMapParams();
            aboutToReload = setTimeout("PressureNET.loadAndUpdate()", 1000);
        });

        google.maps.event.addListener(map, 'zoom_changed', function() {
            window.clearTimeout(aboutToReload);
            PressureNET.updateAllMapParams();
            aboutToReload = setTimeout("PressureNET.loadAndUpdate()", 1000);
        });
    }

}).call(this);
