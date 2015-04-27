$(function() {
    $('body').on('change', '.orgCombo', function() {
        var selectedValue = $(this).val();
        if (selectedValue !== '') {
            var newComboBox = $(this).clone();
            var thisComboBoxIndex = parseInt($(this).attr('data-index'), 10);
            var newComboBoxIndex = thisComboBoxIndex + 1;

            // $('.parentCombo' + thisComboBoxIndex).remove();

            if (selectedValue !== '') {
                newComboBox.attr('data-index', newComboBoxIndex);
                newComboBox.attr('id', 'orgCombo' + newComboBoxIndex);
                newComboBox.attr('form', 'gbeerForm');
                newComboBox.attr('name', 'orgList' + newComboBoxIndex);
                // newComboBox.addClass('parentCombo' + thisComboBoxIndex);
                // newComboBox.find('option[val="' + selectedValue + '"]').remove();
                $('#orgs').append(newComboBox);
                $('#orgs').append('<br/>')
            }
        } else {
            $(this).remove();
        }
    });

    $('body').on('change', '.opCombo', function() {
        var selectedValue = $(this).val();
        if (selectedValue !== '') {
            var newComboBox = $(this).clone();
            var thisComboBoxIndex = parseInt($(this).attr('data-index'), 10);
            var newComboBoxIndex = thisComboBoxIndex + 1;

            // $('.parentCombo' + thisComboBoxIndex).remove();

            if (selectedValue !== '') {
                newComboBox.attr('data-index', newComboBoxIndex);
                newComboBox.attr('id', 'opCombo' + newComboBoxIndex);
                newComboBox.attr('form', 'gbeerForm');
                newComboBox.attr('name', 'opList' + newComboBoxIndex);
                // newComboBox.addClass('parentCombo' + thisComboBoxIndex);
                // newComboBox.find('option[val="' + selectedValue + '"]').remove();
                $('#ops').append(newComboBox);
                $('#ops').append('<br/>')
            }
        } else {
            $(this).remove();
        }
    });
});

function addOperon(element) {
    var selectedValue = $(element).val();
    var newComboBox = $(element).clone();
    var thisComboBoxIndex = parseInt($(this).attr('data-index'), 10);
    var newComboBoxIndex = thisComboBoxIndex + 1;
    newComboBox.attr('data-index', newComboBoxIndex);
    newComboBox.attr('id', 'orgCombo' + newComboBoxIndex);
    newComboBox.attr('form', 'gbeerForm');
    newComboBox.attr('name', 'orgList' + newComboBoxIndex);
    // newComboBox.addClass('parentCombo' + thisComboBoxIndex);
    // newComboBox.find('option[val="' + selectedValue + '"]').remove();
    $('#orgs').append(newComboBox);
    $('#orgs').append('<br/>')
}
