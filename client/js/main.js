$offset = 30;
window.onbeforeunload = function() {
    localStorage.setItem(search_field, $('#search_field').val());
    localStorage.setItem(sort_field, $('#sort_form input[type=radio]:checked').val());
}   
function append(product_fields) {
    var grid = document.querySelector('#columns');
    var item = document.createElement('div');
    var h = '<a href="' + product_fields['url'] + '" target="_blank">';;
    h += '</div>';
    h += '<div class="panel-body">';
    h += '<a href="' + product_fields['url'] + '" target="_blank">';
    h += '<img src="' + product_fields['image_url'] + '"/>';
    h += '<div class="prod_details">'
    h += '<span class="title">' + product_fields['title'] + '</span>';
    h += '<span class="sale_price">&pound;' + product_fields['sale_price'] + '</span>';
    h += '<span class="rrp">&pound;' + product_fields['rrp'] + '</span>';
    h += '</div></a>';
    h += '</div></div>';
    salvattore['append_elements'](grid, [item]);
    $(item).html(h).hide().fadeIn();
}
function getProducts(offset) {
    var sort = $('#sort_form input[type=radio]:checked').val()
    var url = "http://127.0.0.1:5984/salespotlight/_fti/_design/foo/by_title?q=title:" + localStorage.getItem(search_field) +
              "&sort=" + sort +
              "&limit=30&include_docs=true&force_json=true"
    $.ajax({
        type : "GET",
        dataType : "jsonp",
        url : url,
        success: function(data){
            $.each(data.rows, function(key, value) {
                append(value.doc)
            });
        }
    });
}

$(window).load(function() {
    $('#search_field').attr('value', localStorage.getItem(search_field));
    getProducts();
});

$(window).scroll(function() {
    if($(window).scrollTop() >= $(document).height() - $(window).height()) {
        $.ajax({
            type : "GET",
            dataType : "jsonp",
            url : "http://127.0.0.1:5984/salespotlight/_fti/_design/foo/by_title?q=title:" + localStorage.getItem(search_field) + "&skip=" + $offset + "&limit=30&include_docs=true&force_json=true",
            success: function(data){
                $offset += 30;
                $.each(data.rows, function(key, value) {
                    append(value.doc)
                });
            }
        });
    }
});
/* When the user clicks on the button, 
toggle between hiding and showing the dropdown content */
function show_dropdown() {
    document.getElementById("sort_dropdown").classList.toggle("show");
}

// Close the dropdown if the user clicks outside of it
window.onclick = function(event) {
  console.log($('#sort_form input[type=radio]:checked').val())
  if (!event.target.matches('.dropbtn')) {

    var dropdowns = document.getElementsByClassName("dropdown_content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}