
function generatePieChart(canvas, chart) {
    Highcharts.chart(canvas, {
        chart: { type: chart.type},
        title: { text: chart.chart_title},
        subtitle: { text: chart.chart_subtitle },
        tooltip: { 
            pointFormat: '{point.name}: <b>{point.y:.1f}</b>' // Show as percentage
        },
        dataLabels: {
            enabled: true,
            format: '<b>{point.name}</b>: {point.y:.1f}%',
            style: {
                fontSize: '14px',
                fontWeight: 'bold',
                color: '#333'
            }
        },
        plotOptions: {
            series: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: [{
                    enabled: true,
                    distance: 20,
                    style: {
                        fontSize: '18px',
                        textOutline: 'none',
                        opacity: 0.7
                    },
                    //format: '{point.name}: {point.y:.1f}%', // Comment to show labels inside slices
                }, {
                    enabled: true,
                    distance: -40,
                    format: '{point.percentage:.1f}%',
                    style: {
                        fontSize: '16px',
                        textOutline: 'none',
                        opacity: 0.7
                    },
                    
                    // filter: {
                    //     operator: '>',
                    //     property: 'percentage',
                    //     value: 10
                    // }  //uncomment to apply to show labels only greater than 10 percent for example
                }],
                showInLegend: true, // Enable legend
                /*borderWidth: 5,
                borderColor: '#000',
                shadow: {
                    color: 'rgba(0, 0, 0, 0.2)',
                    offsetX: 2,
                    offsetY: 2,
                    opacity: 0.5,
                    width: 5
                } Uncomment to apply border effects*/ 
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
            data: chart.series[0].data.map(item => ({ name: item.name, y: item.data * 100 })) // Convert to percentage
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
                        return `${formatValue(this.y)}, ${percentage}%`;
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