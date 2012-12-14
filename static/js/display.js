$(document).ready(function() {
    //var sentence = ['by', 'then', 'it', 'was', 'too', 'late'];
    var sentence = ['four', 'score', 'and', 'seven', 'years', 'ago'];

    var fonts = ['Blackout2Am', 'BlackoutSunrise','Raleway', 'Blackout', 'AlteHaasGrotesk', 'Georgia, serif', '"Times New Roman", Times, serif', 'Arial, Helvetica, sans-serif', '"Courier New", Courier, monospace', 'Impact, Charcoal, sans-serif','"Palatino Linotype", "Book Antiqua", Palatino, serif', '"Lucida Console", Monaco, monospace']

    var sizes = ['12', '14', '18', '22', '36', '48', '72', '100'];

    $.each(sentence, function(i, val) {
        // console.log(val)
        var font= fonts[Math.floor(Math.random()*fonts.length)];
        var size= sizes[Math.floor(Math.random()*sizes.length)];
        $('body').append('<div id="' + val + '">' + val + '</div>')
        $('#' + val).css('font-family', font).css('font-size', size + 'px')
            .css('position', 'absolute')
            .css('top', Math.floor(Math.random() * 600) + 'px')
            //TODO don't step on each other, make responsive
            .css('left', (Math.floor(Math.random() * 600) + 300) + 'px')
            .css('-webkit-transform', 'rotate(-' + Math.floor(Math.random() * 180) + 'deg)');
    });
});
