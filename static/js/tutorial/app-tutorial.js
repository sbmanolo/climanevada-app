function startTutorial() {
    introJs().setOptions({
        tooltipClass: 'intro-js-obsnev',
        keyboardNavigation:true,
        showProgress:true,
        steps: [{
            intro: "<h4>Welcome to Climanevada.</h4><br>" +
                    "<p>Follow this short tutorial to learn how to use the application.</p> <p>You can skip it by clicking outside this box.</p>"
        }, {
            element: document.querySelector('#div_id_variables'),
            intro: "Select one or more variables. If you have previously selected one or more stations, only the variables measured at those stations will be displayed."
        }, {
            element: document.querySelector('#div_id_variable_type'),
            intro: "You can filter the displayed variables using the <i>Variable type</i> field."
        }, {
            element: document.querySelector('#div_id_station_name'),
            intro: "Select one or more stations. If you have previously selected one or more variables, only the stations where these variables are measured will be displayed."
        }, {
            element: document.querySelector('#id_location-map'),
            intro: "You can also select stations by clicking on them on the map."
        }, {
            element: document.querySelector('#div_id_altitude'),
            intro: "You can filter the stations by altitude range using this slider..."
        }, {
            element: document.querySelector('#toggle-group'),
            intro: "...and by the type of station (Station or Sensor)."
        }, {
            element: document.querySelector('#div_id_date_range'),
            intro: "Finally, select the date range for which you want to download data."
        }, {
            element: document.querySelector('#submit-id-download'),
            intro: "<p>Once you have selected at least one variable, one station and a valid date range, click here to start the download.</p>" +
                    "<p>Note that the more variables and stations you have selected and the wider the date range, the longer the download will take.</p>"
        }, {
            intro: "<h4>Tutorial completed.</h4><br>" +
            "<p>You can continue to use the application freely by clicking on <i>Done</i></p>"
        }]

    }).start();
};