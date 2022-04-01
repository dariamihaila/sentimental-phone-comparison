function phone_selected() {
    let first_phone = $('#first_phone_select')[0].value;
    let second_phone = $('#second_phone_select')[0].value;

    if (first_phone != 'no_phone' && second_phone != 'no_phone') {
        $('#form')[0].submit();
    }
}

$('#first_phone_select').on('change', phone_selected);
$('#second_phone_select').on('change', phone_selected);
