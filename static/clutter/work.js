$(function(){
    $('#progress').html("<p># actions until next key: " + (25 - (count % 25)) + "</p><p>" + "Previously acquired keys: " + keys + "</p>");
});
