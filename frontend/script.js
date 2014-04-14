function onSearch() {
	
	var query = $('#query').val();
	if (query.length == 0) {
		return;
	}

	query.replace(/\s+/g,'+');
	
	$.ajax({
		type: 'GET',
		url: 'http://109.173.222.224:8983/solr/collection1/select?q=text%3A*' + query + '*&wt=json&indent=true',
		dataType: 'json',
		success: function(data) {
			appendResults(data.response.docs)
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

	var total = 'Found ' + docs.length + ' results';
	$('#results').append('<div>' + total + '</div><br/>');
	
	$.each(docs, function(i, item) {
		$('#results').append($('<div>' + item.title + '</div>'));
		$('#results').append($('<div>' + item.text + '</div><br/>'));
	});


}

$(document).ready(onReady);