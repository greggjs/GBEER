function getKeg(element) {
    var selectedValue = $(element).parent().children('.orgCombo').val();
    $.ajax({
        method: 'GET',
        url: '/keg/' + selectedValue
    }).done(function(data) {
        var dataList = data['results'];
        var dataString = "";
        for (var i = 0; i < dataList.length; i++) {
            dataString += "<p>" + dataList[i] + "</p>";
        }
        $('#keg-contents').html(dataString);
    }).error(function() {
        var comboDiv = $('#orgs');
        comboDiv.prepend('<div class="alert alert-danger fade in" role="alert">No Contents for given Keg.</div>');
        window.setTimeout(function() {
            $(".alert").fadeTo(500, 0).slideUp(500, function(){
                $(this).remove();
            });
        }, 3000);
    });
}

function addOperon(element) {
    var selectedValue = $(element).parent().children('.opCombo').val();
    var numSelected = $("#ops").children('.opBlock').length;
    if (selectedValue === "") {
        var comboDiv = $('#ops');
        comboDiv.prepend('<div class="alert alert-danger fade in" role="alert">Please select an Operon before adding it to your query.</div>');
        window.setTimeout(function() {
            $(".alert").fadeTo(500, 0).slideUp(500, function(){
                $(this).remove();
            });
        }, 3000);
    } else if (numSelected >= 3) {
        var comboDiv = $('#ops');
        comboDiv.prepend('<div class="alert alert-info fade in" role="alert">You cannot query more than 3 Operons.</div>');
        window.setTimeout(function() {
            $(".alert").fadeTo(500, 0).slideUp(500, function(){
                $(this).remove();
            });
        }, 3000);
    } else {
        var newComboDiv = $(element).parent().clone();
        var newComboBox = newComboDiv.children('.opCombo');
        var newAddBtn = newComboDiv.children('.btn-success');

        var thisComboBoxIndex = parseInt(newComboDiv.children('.opCombo').attr('data-index'), 10);
        var newComboBoxIndex = thisComboBoxIndex + 1;
        newComboBox.attr('data-index', newComboBoxIndex);
        newComboBox.attr('id', 'opCombo' + newComboBoxIndex);
        newComboBox.attr('form', 'gbeerForm');
        newComboBox.attr('name', 'opList' + newComboBoxIndex);
        newComboBox.addClass('opCombo form-control col-xs-6');
        $('#ops').append(newComboDiv);

        if (!newComboDiv.find('.btn-danger').length != 0) {
            var newRmBtn = newAddBtn.clone().removeClass('btn-success').addClass('btn-danger col-xs-1').text('-');
            newRmBtn.attr("onclick", "removeOperon(this)");
            newComboDiv.append(newRmBtn);
        }
    }
}

function removeOperon(element) {
    var selectedValue = $(element).parent().children('.opCombo').val();
    var rmComboDiv = $(element).parent();
    rmComboDiv.remove();
}
