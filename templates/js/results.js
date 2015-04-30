function downloadOperonZip(requestId, operon) {
    $.fileDownload("/download/" + requestId + "/" + operon).done(function() { alert('success')});
}

function checkQuery(e, imgType, operon, request_id) {
    getStatus = $.Deferred(function(deferred) {
        $.ajax({
            method: 'GET',
            url: '/job/' + request_id
        }).done(function(data, textStatus, jqXHR) {
            $(e).html('<div class="img-container"><img id="' + operon + '-' + imgType + '-png" style="width: 60%; height: 100%;" src="/img/' + request_id + '/'
                + operon + '/' + imgType + '-small.png" data-large-zoom="/img/' + request_id + '/'
                    + operon + '/' + imgType + '-large.png"/><div id="' + operon + '-' + imgType + '-zoombox" class="zoom-container"></div></div>');
            $("#" + operon + '-' + imgType + "-png").elevateZoom({
                zoomWindowPosition: operon + '-' + imgType + '-zoombox',
                cursor: "crosshair",
                zoomWindowHeight: 400,
                zoomWindowWidth: 400,
                scrollZoom: true
            });
            $(".btn-primary").removeAttr("disabled");
            deferred.resolve({ 'check' : true });
        }).fail(function(jqXHR, textStatus, errorThrown) {
            if (jqXHR.status === 500) {
                $(e).html('<div class="waiting center"><p>We\'re sorry, but something went wrong accessing the status of your query. We promise we aren\'t drinking this green beer.<p>'
                            + '<img src="/static/img/green-beer.png"/><p>Are you sure the Organisms you are examining contain the Operon in question?</p><br>'
                            + '<p>If this is an old query, if it\'s been more than a week since its submission, it was removed from the system to make sure '
                            + 'everyone has enough space to make great queries just like yours.</p></div>');
                deferred.resolve({ 'check' : true });
            }
            deferred.resolve({ 'check' : false });
        });
    }).promise();
    return getStatus;
}

$(document).ready(function() {
    var intervals = {};
    $('.tabs .tab-links a').on('click', function(e)  {
        var currentAttrValue = $(this).attr('href');
        // Show/Hide Tabs
        $('.tabs ' + currentAttrValue).show().siblings().hide();
        // Change/remove current tab to active
        $(this).parent('li').addClass('active').siblings().removeClass('active');
        if ($(this).parent().parent().hasClass('inner-tab')) {
            var operon = $(this).parent().parent().parent().attr('id');
            var res = checkQuery(currentAttrValue, $(currentAttrValue).attr('name'), operon, $("#requestId").val());
            $.when(res).done(function(data) {
                if (data.check === true) {
                    var operonKey = currentAttrValue.substring(1)
                    if (operonKey in intervals) {
                        clearInterval(intervals[operonKey]);
                    }
                }
            });

        }
        e.preventDefault();
    });
    $('.inner-tab-content').each(function(index, el) {
        var res = checkQuery(el, $(el).attr('name'), $(el).parent().parent().attr('id'), $("#requestId").val());
        $.when(res).done(function(data) {
            if (data.check === false) {
                intervals[$(el).attr('id')] = setInterval(function() {
                    def = checkQuery(el, $(el).attr('name'), $(el).parent().parent().attr('id'), $("#requestId").val());
                    $.when(def).done(function(data) {
                        if (data.check === true) {
                            var operonKey = $(el).attr('id');
                            if (operonKey in intervals) {
                                clearInterval(intervals[operonKey]);
                            }
                        }
                    });
                }, 3000);
            }
        });

    });
});
