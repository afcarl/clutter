$(function(){
    $('.cloud').each(function(index){
        (function(node){
            $.ajax({
                url: "cloud/" + $(node).attr("cloud-id") + ".json"
            }).done(function(data){

                padding = 20;
                var area = ($(node).width()-padding)*($(node).height()-padding);
                var length = data.length;

                new_node = $('<div/>');
                new_node.addClass('overflow');
                span = $('<span/>');
                span.addClass('clear');
                $(node).append(new_node);
                $(node).append(span);
                node = new_node;

                data.sort(function(a,b){return b['frequency'] - a['frequency'];});
                if (!data[0]['word']){
                    $.each(data, function(index, image_object){
                        var img = $('<img src="' + image_object + '" />');
                        $(new_node).prepend(img);
                        img.load(function(){
                            if (img.width() > img.height()){
                                $(img).css('width', (170 / data.length) + 'px');
                            }
                            else{
                                $(img).css('height', (170 / data.length) + 'px');
                            }
                        });
                    });
                }
                else{
                    $.each(data, function(index ,word_object){
                        word = word_object['word'];
                        frequency = word_object['frequency'];
                        var div = $('<div/>');
                        div.addClass('word');
                        div.append(word);
                        $(node).append(div);
                        div.css({'font-size': 
                            (frequency * 
                             parseFloat(div.css('font-size'))) +
                                "px"});
                        if (index == length-1){
                            var word_area = 0;
                            words = $(node).find('.word');
                            var largest_width = 0.0;
                            for (w = 0; w < words.length; w++){
                                word_area += $(words[w]).width() * $(words[w]).height();
                                if ($(words[w]).width() > largest_width){
                                    largest_width = $(words[w]).width();
                                }
                            }

                            multiplier = Math.sqrt(area / word_area);
                            if (largest_width * multiplier > ($(node).width()-padding)){
                                multiplier = ($(node).width()-padding) / largest_width;
                            }

                            words.each(function(idx, word){
                                $(word).css({'font-size':
                                    (multiplier * 
                                     parseFloat($(word).css('font-size'))) + 
                                        "px"});
                                if (idx == words.length - 1){
                                    if ($(node).height() > ($(node).parent().height()-padding)){
                                        multiplier2 = ($(node).parent().height()-padding) / $(node).height();
                                        words.each(function(idx, word){
                                            $(word).css({'font-size':
                                                (multiplier2 * 
                                                 parseFloat($(word).css('font-size'))) + 
                                                    "px"});
                                        });
                                    }
                                }
                            });
                        }
                    });
                }
            });
        })(this);
    });
});
