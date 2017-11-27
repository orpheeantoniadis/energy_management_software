var slider = new Slider('#hello', {
	formatter: function(value) {
		return 'Current value: ' + value;
	}
});