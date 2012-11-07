  var service_url = 'https://www.googleapis.com/freebase/v1/mqlread';
  var API_KEY = 'AIzaSyC45Rxmkg12VNKmtxHGB4w63Ve8rjuhJPA';
  var band = 'The Rolling Stones';
  var query = {
    type: '/music/artist',
    name: band,
    album: [{
    name: null,
    release_date: null,
    sort: 'release_date',
    'release_type!=': 'single'
    }]
  };

  var params = {
    'key': API_KEY,
    'query': JSON.stringify(query)
  };

  $.getJSON(service_url + '?callback=?', params, function(response) {
    $.each(response.result.album, function(i, album) {
      console.log(album['name']);
      });
    });
