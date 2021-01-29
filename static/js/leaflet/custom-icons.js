L.Icon.Default.prototype.options.iconUrl = 'custom_markers/blue-marker.png';
L.Icon.Default.prototype.options.iconSize = [26, 41];
L.Icon.Default.prototype.options.iconAnchor = [13,41];
L.Icon.Default.prototype.options.popupAnchor = [-13, -30];
L.Icon.Default.prototype.options.shadowUrl = 'custom_markers/marker-shadow.png';

var ObsIcon = L.Icon.extend({
    options: {
    shadowUrl: '/static/leaflet/images/custom_markers/marker-shadow.png',
    iconUrl: '/static/leaflet/images/custom_markers/blue-marker.png',
    iconSize: [26, 41],
    iconAnchor: [13,41],
    popupAnchor:  [0, -25]
    }
});

var ObsIconSquare = L.Icon.extend({
    options: {
    shadowUrl: '/static/leaflet/images/custom_markers/marker-shadow.png',
    iconUrl: '/static/leaflet/images/custom_markers/svg/blue-marker-square.svg',
    shadowSize:   [20, 30],
    shadowAnchor: [5, 42],
    iconSize: [20, 33],
    iconAnchor: [10,33],
    popupAnchor:  [0, -25]
    }
});

var blueIcon = new ObsIcon({iconUrl: '/static/leaflet/images/custom_markers/blue-marker.png'}),
    greenIcon = new ObsIcon({iconUrl: '/static/leaflet/images/custom_markers/green-marker.png'}),
    grayIcon = new ObsIcon({iconUrl: '/static/leaflet/images/custom_markers/gray-marker.png'}),
    blueIconSquare = new ObsIconSquare({iconUrl: '/static/leaflet/images/custom_markers/svg/blue-marker-square.svg'}),
    greenIconSquare = new ObsIconSquare({iconUrl: '/static/leaflet/images/custom_markers/svg/green-marker-square.svg'}),
    grayIconSquare = new ObsIconSquare({iconUrl: '/static/leaflet/images/custom_markers/svg/gray-marker-square.svg'}),
    redIconLocation = new ObsIcon({
        iconUrl: '/static/leaflet/images/custom_markers/svg/red-marker-location-b.svg',
        /*iconSize: [31, 49],
        iconAnchor: [15.5, 49],
        popupAnchor:  [0, -36]*/
    });