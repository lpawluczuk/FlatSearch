var page = 0,
    url = '';

function onSearch() {
  
  composeURL();
  page = 0;

	$.ajax({
		type: 'GET',
		url: url,
		dataType: 'json',
		success: function(data) {
			appendResults(data.contents.response, true)
		},
		error: function(XMLHttpRequest, textStatus, errorThrown) {
			alert("error: " + textStatus);    
		}
	})
  
  $('body').scrollTop(0);
  
}

function composeURL() {

	var query = encodeURIComponent($('#query').val()),
      location = encodeURIComponent($('#location').val()),
      minArea = $('#area').val(),
      maxPrice = $('#price').val(),
      roomsNo = $('#rooms').val(),
      mode = '&mode=native',
      end = '&wt=json&indent=true',
      proxy = 'http://94.72.127.27/index.php?url=';
      
  url = 'http://94.72.127.27:8983/solr/collection1/select?q=';
  
  if (roomsNo === 'dowolna') {
		roomsNo = '';
	}	

	query.replace(/\s+/g,'+');
	location.replace(/\s+/g,'+');

	if (query.length > 0) {
		url += 'text%3A*' + query + '*';
	}

	if (location.length > 0) {
		if (query.length > 0) { 
			url += '+AND+'; 
		}		
		url += 'city%3A*' + location + '*%0A';
	}

	if (minArea.length > 0) {
		if (query.length > 0 || location.length > 0) { 
			url += '+AND+'; 
		}			
		url += 'area%3A%5B' + minArea + '+TO+*%5D%0A';
	}

	if (maxPrice.length > 0) {
		if (query.length > 0 || location.length > 0 || minArea.length > 0) { 
			url += '+AND+'; 
		}	
		url += 'price%3A%5B*+TO+' + maxPrice + '%5D%0A';
	}

	if (roomsNo.length > 0) {
		if (query.length > 0 || location.length > 0 || minArea.length > 0 || maxPrice > 0) { 
			url += '+AND+'; 
		}	
		url += 'rooms%3A' + roomsNo + '%0A%0A';
	}

	url = proxy + encodeURIComponent(url + '&rows=10&start=' + (page * 10) + '&wt=json&indent=true' + mode);
}

function onReady() {
	$('#search').click(onSearch);
  
  $('div').delegate('#more', 'click', function() {
    
    page++;
    composeURL();
    
    $.ajax({
      type: 'GET',
      url: url,
      dataType: 'json',
      success: function(data) {
        appendResults(data.contents.response, false)
      },
      error: function(XMLHttpRequest, textStatus, errorThrown) {
        alert("error: " + textStatus);    
      }
    })    
  });
  
	$('body').keypress(function(e) {
		if (e.keyCode == '13') {
			onSearch();
		}
	});
}

function appendResults(docs, erase) {
	
  var total = docs.numFound;
  
  if (erase) {
    $('#results').empty();
    $('#results').prepend('<p id="resultInfo">Liczba znalezionych ofert: ' + total + '</p><br/>');
  } else {
    $('#results').children().last().remove();
  }
  
	$.each(docs.docs, function(i, item) {		
		$('#results').append($(
		'<div class="result"><p class="resultTitle">' 
		+ item.title + '</p><p class="resultTitle">' 
		+ item.area + ' m | ' 
		+ item.price + ' zł | ' 
		+ item.rooms + ' pokoje | <a href="' + item.url +' " class="resultLink">link</a></p>'
		+ ' <p class="resultAddress">' 
		+ item.address + '</p>'
		+ ' <p class="resultText">' 
		+ item.text + '</p></div>'));

	});
  	  
  if (total - (page * 10) > 10) {
    $('#results').append('<div id="moreButtonContainer"><button id="more">Więcej</button></div>');
  }
}

$(document).ready(onReady);