$(function () {
    // функция загрузки списока групп
  function getData() {
    $.ajax({
      type: "GET",
      url: "http://localhost:8000/groups/",
      contentType: 'application/json; charset=utf-8',
      dataType: 'json',
    }).success(function(data) {
      // формируем HTML код со списком групп пользователя
      var resultData = "";
      for (var i = 0; i < data.data.length; i++) {
          resultData += "<div class='ui card'>" +
                          "<div class='image'>" +
                            "<img src='" + data.data[i].photo_200 +"' /></div>" +
                          "<div class='content'>" +
                            "<div class='header'>" +
                            data.data[i].name + "</div></div>" +
                          "<div class='ui bottom attached button'>" +
                          "<a href='group/" + data.data[i].id + "'>Go to group</a></div></div>"
      }
      $('#result-container').append(resultData);// setting result table on page
    }).error(function(err) {
      console.log(err);
    })
  }

  getData();

});