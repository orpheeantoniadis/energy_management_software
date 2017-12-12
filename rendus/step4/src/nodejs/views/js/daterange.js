$(function() {

	$('input[id="daterange"]').daterangepicker({
			timePicker: true,
			timePicker24Hour: true,
			timePickerSeconds: true,
			autoUpdateInput: false,
			locale: {
					cancelLabel: 'Clear'
			}
	});

	$('input[id="daterange"]').on('apply.daterangepicker', function(ev, picker) {
			$(this).val(picker.startDate.format('YYYY-MM-DD hh:mm:ss') + ' - ' + picker.endDate.format('YYYY-MM-DD hh:mm:ss'));
			$('form[id="formDaterange"]').submit();
	});

	$('input[id="daterange"]').on('cancel.daterangepicker', function(ev, picker) {
			$(this).val('');
	});

});