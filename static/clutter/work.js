$(function(){
    $('#progress').html("<p># actions until next key: " + (10 - (count % 10)) + "</p><p>" + "Previously acquired keys: " + keys + "</p>");
});
