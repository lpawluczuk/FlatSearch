function onSearch() {
	
	var query = $('#query').val(),
		location = $('#query').val(),
		minArea = $('#area').val(),
		maxPrice = $('#price').val(),
		roomsNo = $('#rooms').val()
		url = 'http://94.72.127.27:8983/solr/collection1/select?q=text%3A*';
	
	query.replace(/\s+/g,'+');
	
	if (query.length > 0) {
		url += query + '*';
	}

	if (location.length > 0) {
		url += '%0Aaddress%3A*' + location + '*%0A';
	}	
	
	url += '&wt=json&indent=true';

	$.ajax({
		type: 'GET',
		url: url,
		dataType: 'json',
		success: function(data) {
			appendResults(data.response.docs, minArea, maxPrice, roomsNo)
		},
		error: function(XMLHttpRequest, textStatus, errorThrown) {
			alert("error: " + textStatus);    
		}
	})
	
}

function onReady() {
	$('#search').click(onSearch);
	/* Hook enter to search */
	$('body').keypress(function(e) {
		if (e.keyCode == '13') {
			onSearch();
		}
	});
}

function appendResults(docs, minArea, maxPrice, roomsNo) {
	
	console.log(docs);
	$('#results').empty();
	var total = docs.length;

	$.each(docs, function(i, item) {
		
		maxPrice = parseInt(maxPrice, 10);
		if (maxPrice !== '' && parseInt(item.price, 10) > maxPrice) {
			total--;
			return;
		}
	
		minArea = parseInt(minArea, 10);
		if (minArea !== '' && parseInt(item.area, 10) < minArea) {
			total--;
			return;
		}
				
		if (roomsNo !== 'dowolna') {
			if (roomsNo !== item.rooms) {
				total--;
				return;
			}
		}
				
		$('#results').append($(
		'<div class="result"><p class="resultTitle">' 
		+ item.title + '</p><p class="resultTitle">' 
		+ item.area + ' m | ' 
		+ item.price + ' zł | ' 
		+ item.rooms + ' pokoje | <a href="' + item.url +' " class="resultLink">link</a></p>'
		+ ' <p class="resultText">' 
		+ item.text + '</p></div>'));

	});
	
	$('#results').prepend('<p id="resultInfo">Found ' + total + ' results</p><br/>');
}

$(document).ready(onReady);