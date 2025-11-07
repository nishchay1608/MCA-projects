// charts.js - All chart functionality for the business analytics dashboard

// Initialize all charts when the page loads
document.addEventListener('DOMContentLoaded', function() {
    initializeCharts();
});

function initializeCharts() {
    // Check if chart data is available
    if (typeof chartData === 'undefined') {
        console.error('Chart data not found');
        return;
    }

    // Initialize Sales Trend Chart
    initializeSalesTrendChart();
    
    // Initialize Customer Segmentation Chart
    initializeCustomerSegmentationChart();
}

function initializeSalesTrendChart() {
    const ctx = document.getElementById('salesTrendChart');
    if (!ctx) {
        console.error('Sales trend chart canvas not found');
        return;
    }

    // Check if we have data
    if (!chartData.salesTrend || chartData.salesTrend.data.length === 0) {
        console.warn('No sales trend data available');
        displayNoDataMessage(ctx, 'Sales Trend');
        return;
    }

    try {
        const salesTrendChart = new Chart(ctx.getContext('2d'), {
            type: 'line',
            data: {
                labels: chartData.salesTrend.labels,
                datasets: [{
                    label: 'Revenue ($)',
                    data: chartData.salesTrend.data,
                    borderColor: 'rgb(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.1)',
                    borderWidth: 2,
                    tension: 0.1,
                    fill: true,
                    pointBackgroundColor: 'rgb(75, 192, 192)',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 4,
                    pointHoverRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Monthly Revenue Trend',
                        font: {
                            size: 16,
                            weight: 'bold'
                        }
                    },
                    legend: {
                        display: true,
                        position: 'top'
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                        callbacks: {
                            label: function(context) {
                                return `Revenue: $${context.parsed.y.toFixed(2)}`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Revenue ($)',
                            font: {
                                weight: 'bold'
                            }
                        },
                        ticks: {
                            callback: function(value) {
                                return '$' + value.toLocaleString();
                            }
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Month',
                            font: {
                                weight: 'bold'
                            }
                        }
                    }
                },
                interaction: {
                    intersect: false,
                    mode: 'nearest'
                }
            }
        });
        
        console.log('Sales trend chart initialized successfully');
        return salesTrendChart;
    } catch (error) {
        console.error('Error initializing sales trend chart:', error);
        displayErrorMessage(ctx, 'Error loading sales trend chart');
    }
}

function initializeCustomerSegmentationChart() {
    const ctx = document.getElementById('customerSegmentationChart');
    if (!ctx) {
        console.error('Customer segmentation chart canvas not found');
        return;
    }

    // Check if we have data
    if (!chartData.customerSegmentation || chartData.customerSegmentation.data.length === 0) {
        console.warn('No customer segmentation data available');
        displayNoDataMessage(ctx, 'Customer Segmentation');
        return;
    }

    try {
        const customerSegChart = new Chart(ctx.getContext('2d'), {
            type: 'doughnut',
            data: {
                labels: chartData.customerSegmentation.labels,
                datasets: [{
                    data: chartData.customerSegmentation.data,
                    backgroundColor: [
                        'rgb(255, 99, 132)',
                        'rgb(54, 162, 235)',
                        'rgb(255, 205, 86)',
                        'rgb(75, 192, 192)',
                        'rgb(153, 102, 255)',
                        'rgb(255, 159, 64)',
                        'rgb(201, 203, 207)',
                        'rgb(102, 204, 153)'
                    ],
                    borderColor: 'white',
                    borderWidth: 2,
                    hoverOffset: 15,
                    hoverBorderWidth: 3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Revenue by Customer Type',
                        font: {
                            size: 16,
                            weight: 'bold'
                        }
                    },
                    legend: {
                        display: true,
                        position: 'bottom',
                        labels: {
                            padding: 20,
                            usePointStyle: true,
                            pointStyle: 'circle'
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.parsed;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = Math.round((value / total) * 100);
                                return `${label}: $${value.toLocaleString()} (${percentage}%)`;
                            }
                        }
                    }
                },
                cutout: '50%',
                animation: {
                    animateScale: true,
                    animateRotate: true
                }
            }
        });
        
        console.log('Customer segmentation chart initialized successfully');
        return customerSegChart;
    } catch (error) {
        console.error('Error initializing customer segmentation chart:', error);
        displayErrorMessage(ctx, 'Error loading customer segmentation chart');
    }
}

// Utility function to display no data message
function displayNoDataMessage(canvasElement, chartName) {
    const ctx = canvasElement.getContext('2d');
    ctx.font = '16px Arial';
    ctx.fillStyle = '#6c757d';
    ctx.textAlign = 'center';
    ctx.fillText(`No data available for ${chartName}`, canvasElement.width / 2, canvasElement.height / 2);
}

// Utility function to display error message
function displayErrorMessage(canvasElement, message) {
    const ctx = canvasElement.getContext('2d');
    ctx.font = '14px Arial';
    ctx.fillStyle = '#dc3545';
    ctx.textAlign = 'center';
    ctx.fillText(message, canvasElement.width / 2, canvasElement.height / 2);
}

// Function to update chart data dynamically
function updateChartData(chartInstance, newData, newLabels = null) {
    if (chartInstance && chartInstance.data) {
        chartInstance.data.datasets[0].data = newData;
        if (newLabels) {
            chartInstance.data.labels = newLabels;
        }
        chartInstance.update();
        return true;
    }
    return false;
}

// Function to create a bar chart (for future use)
function createBarChart(canvasId, data, labels, title, color = 'rgb(54, 162, 235)') {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;

    return new Chart(ctx.getContext('2d'), {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: title,
                data: data,
                backgroundColor: color.replace('rgb', 'rgba').replace(')', ', 0.7)'),
                borderColor: color,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: title
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Function to create a pie chart (for future use)
function createPieChart(canvasId, data, labels, title) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;

    return new Chart(ctx.getContext('2d'), {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: [
                    'rgb(255, 99, 132)',
                    'rgb(54, 162, 235)',
                    'rgb(255, 205, 86)',
                    'rgb(75, 192, 192)',
                    'rgb(153, 102, 255)',
                    'rgb(255, 159, 64)'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: title
                }
            }
        }
    });
}

// Export functions for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initializeCharts,
        initializeSalesTrendChart,
        initializeCustomerSegmentationChart,
        updateChartData,
        createBarChart,
        createPieChart
    };
}