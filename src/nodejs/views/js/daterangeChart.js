function display_chart(date, temperature, humidity, luminance, battery) {
	new Chart(document.getElementById("line-chart"), {
		type: 'line',
		data: {
			labels: date,
			datasets: [{ 
					data: temperature,
					label: "Temperature",
					borderColor: "#3e95cd",
					fill: false
				}, { 
					data: humidity,
					label: "Humidity",
					borderColor: "#8e5ea2",
					fill: false
				}, { 
					data: luminance,
					label: "Luminance",
					borderColor: "#3cba9f",
					fill: false
				}, { 
					data: battery,
					label: "Battery",
					borderColor: "#e8c3b9",
					fill: false
				}
			]
		},
		options: {
			title: {
				display: true,
				text: 'Sensor measures in function of time'
			}
		}
	});
}