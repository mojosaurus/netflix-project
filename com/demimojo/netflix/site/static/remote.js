var bestPictures = new Bloodhound({
  datumTokenizer: Bloodhound.tokenizers.obj.whitespace('value'),
  queryTokenizer: Bloodhound.tokenizers.whitespace,
  remote: {
    url: "/locations/search.json?q=%QUERY",
    ajax: {
      beforeSend: function(xhr, settings) {
        alert('hello');
      },
      complete: function(xhr, status) {
      }
    }
  }
});

bestPictures.initialize();

$(.typeahead').typeahead(null, {
  name: 'best-pictures',
  displayKey: 'value',
  source: bestPictures.ttAdapter()
});