function onSearch() {
	
	var query = encodeURIComponent($('#query').val()),
		location = encodeURIComponent($('#location').val()),
		minArea = $('#area').val(),
		maxPrice = $('#price').val(),
		roomsNo = $('#rooms').val(),
		mode = '&mode=native';
		end = '&wt=json&indent=true'
		url = 'http://94.72.127.27:8983/solr/collection1/select?q=';
		url2 = 'http://94.72.127.27/index.php?url=';
	
	if (roomsNo === 'dowolna') {
		roomsNo = '';
	}	

	query.replace(/\s+/g,'+');
	
	if (query.length > 0) {
		url += 'text%3A*' + query + '*';
	}

	if (location.length > 0) {
		if (query.length > 0) { 
			url += '+AND+'; 
		}		
		url += 'address%3A*' + location + '*%0A';
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
	
	var temp = '&full_headers=1&full_status=1';
	url += '&wt=json&indent=true' + mode;	

	//url = encodeURI(url);
	url = encodeURIComponent(url);
	url = url2 + url;

	$.ajax({
		type: 'GET',
		url: url,
		dataType: 'json',
		success: function(data) {
			console.log(data);
			appendResults(data.contents.response.docs)
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

function appendResults(docs) {
	
	console.log(docs);
	$('#results').empty();
	var total = docs.length;

	$.each(docs, function(i, item) {
		
				
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
	
	$('#results').prepend('<p id="resultInfo">Liczba znalezionych ofert: ' + total + '</p><br/>');
}

$(document).ready(onReady);