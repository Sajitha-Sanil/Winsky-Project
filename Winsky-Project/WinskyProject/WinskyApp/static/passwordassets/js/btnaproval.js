$('button[name="status"]').on('click', function() {
    var status = $(this).val();
    var form = $(this).closest('form');
    var enquiry_id = form.attr('action').split('/')[3]; 
    if (status == 'approved') {
        $('#approve_btn_' + enquiry_id).html('Approved');
        $('#deny_btn_' + enquiry_id).html('Deny');
        $('#pending_btn_' + enquiry_id).html('Pending');
    } else if (status == 'denied') {
        $('#approve_btn_' + enquiry_id).html('Approve');
        $('#deny_btn_' + enquiry_id).html('Denied');
        $('#pending_btn_' + enquiry_id).html('Pending');
    } else if (status == 'pending') {
        $('#approve_btn_' + enquiry_id).html('Approve');
        $('#deny_btn_' + enquiry_id).html('Deny');
        $('#pending_btn_' + enquiry_id).html('On Pending');
    }
    $(this).html(status.charAt(0).toUpperCase() + status.slice(1));
});