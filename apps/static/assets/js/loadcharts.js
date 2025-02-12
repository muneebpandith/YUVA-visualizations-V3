
function generatePieChart(canvas, chart) {
    Highcharts.chart(canvas, {
        chart: { type: chart.type },
        title: { text: chart.chart_title },
        subtitle: { text: chart.chart_subtitle },
        tooltip: { 
            pointFormat: '{point.name}: <b>{point.percentage:.1f}%</b>' // Fix for correct tooltip
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    format: '<b>{point.name}</b>: {point.percentage:.1f}%', // Fix for correct data display
                    style: {
                        fontSize: '14px',
                        fontWeight: 'bold',
                        color: '#333'
                    }
                },
                showInLegend: true
            }
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            itemStyle: {
                fontSize: '16px',
                fontWeight: 'bold',
                color: '#444'
            },
            itemHoverStyle: { color: '#000' }
        },
        series: [{
            name: chart.series[0].name,
            data: chart.series[0].data.map(item => ({
                name: item.name,
                y: item.data // Removed * 100, assuming data is already in correct format
            }))
        }]
    });
}


xx = [];
function generateColumnChart(canvas, chart) {
    // Ensure chart.series[0].data is an array
    if (!Array.isArray(chart.series[0].data)) {
        console.error("chart.series[0].data is not an array:", chart.series[0].data);
        return;
    }

    // Log the data for debugging
    //console.log("Data:", chart.series[0].data);
    // Calculate the total sum of all data points
    const total = chart.series[0].data.reduce((sum, point) => {
        if (Array.isArray(point) && point.length === 2 && typeof point[1] === 'number') {
            return sum + point[1]; // Use the numeric value from each array
        } else {
            console.error("Invalid data point:", point);
            return sum;
        }
    }, 0);

    


    //console.log("Total:", total); // Debugging: Log the total

    Highcharts.chart(canvas, {
        chart: { type: chart.type, height: 600 },
        title: { text: chart.chart_title },
        subtitle: { text: chart.chart_subtitle },
        tooltip: {
            pointFormat: '{point.name}: <b>{point.y:.1f}%</b>' // Show as percentage
        },
        plotOptions: {
            column: {
                dataLabels: {
                    enabled: true,
                    verticalAlign: 'bottom',  // Position the label at the top of the column
                    style: {
                        fontSize: '12px',
                        fontWeight: 'bold',
                        color: '#333'
                    },
                    formatter: function () {
                        // Ensure this.y is a valid number
                        if (typeof this.y !== 'number' || isNaN(this.y)) {
                            console.error("Invalid value in dataLabels formatter:", this.y);
                            return 'N/A';
                        }

                        // Calculate percentage
                        const percentage = ((this.y / total) * 100).toFixed(0);
                        // Format value in 'k' and add percentage
                        return `${formatValue(this.y)}(${percentage}%)`;
                    },
                }
            }
        },
        xAxis: {
            type: chart.x_axis.type,
            title: {
                text: chart.x_axis.title,
                style: {
                    fontSize: '16px',
                    fontWeight: 'bold',
                    color: '#000'
                }
            },
            labels: {
                autoRotation: [-45, -90],
                style: {
                    fontSize: '13px',
                    fontFamily: 'Verdana, sans-serif'
                }
            }
        },
        yAxis: {
            min: 0,
            title: {
                text: chart.y_axis.title,
                style: {
                    fontSize: '16px',
                    fontWeight: 'bold',
                    color: '#333'
                }
            }
        },
        legend: {
            enabled: false
        },
        tooltip: {
            pointFormat: '<b>Value: {point.y:.1f}</b>'
        },
        showInLegend: true,
        series: [{
            name: chart.series[0].name,
            colorByPoint: true,
            groupPadding: 0,
            data: chart.series[0].data
        }]
    });
}

function generateGroupedBarChart(canvas, chart) {
    const totalValues = chart.series.flatMap(series => series.data);
    const total = totalValues.reduce((sum, value) => sum + value, 0);
    Highcharts.chart(canvas, {
        chart: { type: 'column' },  // Change to 'column' for vertical bars
        title: { text: chart.chart_title },
        subtitle: { text: chart.chart_subtitle },
        xAxis: {
            categories: chart.x_axis.categories,
            crosshair: true,
            accessibility: {
                description: 'Countries'
            }
        },
        yAxis: {
            min: 0,
            title: { text: chart.y_axis.title }
        },
        tooltip: { shared: true },
        plotOptions: {
            column: {
                dataLabels: {
                    enabled: true,
                    verticalAlign: 'bottom',  // Position the label at the top of the column
                    style: {
                        fontSize: '12px',
                        fontWeight: 'bold',
                        color: '#333'
                    },
                    formatter: function () {
                        if (typeof this.y !== 'number' || isNaN(this.y)) {
                            console.error("Invalid value in dataLabels formatter:", this.y);
                            return 'N/A';
                        }

                        // Compute total sum for this category
                        const categoryIndex = this.point.index;
                        const categoryTotal = chart.series.reduce((sum, series) => sum + series.data[categoryIndex], 0);

                        // Calculate percentage relative to category total
                        const percentage = ((this.y / categoryTotal) * 100).toFixed(1);
                        return `${formatValue(this.y)} (${percentage}%)`;
                    },
                },
                pointPadding: 0.2,
                borderWidth: 0
        }
        },
       series: chart.series  // Ensure Python is sending valid JSON data
    });
}

function formatValue(value) {
    if (value >= 1000) {
        return (value / 1000).toFixed(2) + 'k'; // Convert to 'k' if greater than or equal to 1000
    }
    return value; // Return the original value if less than 1000
}
/*function generateColumnChart(canvas, chart) {
    //xx= chart;
    // Calculate the total sum of all data points for percentage calculation
    const total = chart.series[0].data.reduce((sum, point) => sum + point.y, 0);
    Highcharts.chart(canvas, {
        chart: { type: chart.type, height:600},
        title: { text: chart.chart_title},
        subtitle: { text: chart.chart_subtitle },
        tooltip: { 
            pointFormat: '{point.name}: <b>{point.y:.1f}%</b>' // Show as percentage
        },
        plotOptions: {
            column: {
                dataLabels: {
                    enabled: true,
                    verticalAlign: 'bottom',  // Position the label at the top of the column
                    style: {
                        fontSize: '12px',
                        fontWeight: 'bold',
                        color: '#333'
                    },
                    formatter: function() {
                        // Calculate percentage
                        const percentage = ((this.y / total) * 100).toFixed(0);
                        // Format value in 'k' and add percentage
                        return `${formatValue(this.y)}, ${percentage}%`;
                    },
                }
            }
        },
        xAxis: {
            type: chart.x_axis.type,
            title: {text:chart.x_axis.title,
                style: {
                    fontSize: '16px',
                    fontWeight: 'bold',
                    color: '#000'
                }

            },
            
            labels: {
                autoRotation: [-45, -90],
                style: {
                    fontSize: '13px',
                    fontFamily: 'Verdana, sans-serif'
                }
            }
        },
        yAxis: {
            min: 0,
            title: {
                text: chart.y_axis.title,
                style: {
                    fontSize: '16px',
                    fontWeight: 'bold',
                    color: '#333'
                }
            }
        },
        legend: {
            enabled: false
        },
        tooltip: {
            pointFormat: '<b>Value: {point.y:.1f}</b>'
        },
        showInLegend: true,
        
        series: [{  
            name: chart.series[0].name,
            // colors: [
            //     '#9b20d9', '#9215ac', '#861ec9', '#7a17e6', '#7010f9', '#691af3',
            //     '#6225ed', '#5b30e7', '#533be1', '#4c46db', '#4551d5', '#3e5ccf',
            //     '#3667c9', '#2f72c3', '#277dbd', '#1f88b7', '#1693b1', '#0a9eaa',
            //     '#03c69b',  '#00f194'
            // ],
            colorByPoint: true,
            groupPadding: 0,
            data: chart.series[0].data
            // dataLabels: {
            //     enabled: true,
            //     rotation: -90,
            //     color: '#FFFFFF',
            //     inside: false,
            //     verticalAlign: 'top',
            //     format: '{point.y:.1f}', // one decimal
            //     y: 10, // 10 pixels down from the top
            //     style: {
            //         fontSize: '10px',
            //         fontFamily: 'Verdana, sans-serif'
            //     }
            // }
        }]
    });
}
		

function formatValue(value) {
    if (value >= 1000) {
        return (value / 1000).toFixed(2) + 'k'; // Convert to 'K' if greater than 999
    }
    return value;
}*/