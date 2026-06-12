
// ===== FORCE ELMS SANS EVERYWHERE =====
Chart.defaults.font.family = "'Elms Sans', sans-serif";

Chart.defaults.plugins.legend.labels.font = {
    family: "'Elms Sans', sans-serif",
    size: 12
};

Chart.defaults.plugins.tooltip.titleFont = {
    family: "'Elms Sans', sans-serif"
};

Chart.defaults.plugins.tooltip.bodyFont = {
    family: "'Elms Sans', sans-serif"
};
// ======================================


// ===== Force Elms Sans for Charts =====
Chart.defaults.font.family = "'Elms Sans', sans-serif";
Chart.defaults.font.size = 18;
Chart.defaults.color = "#6B7280";


// ===== iPon Chart Typography =====
Chart.defaults.font.family = "'Elms Sans', sans-serif";
Chart.defaults.font.size = 18;
Chart.defaults.color = "#6B7280";

if (Chart.defaults.plugins?.legend?.labels) {
    Chart.defaults.plugins.legend.labels.usePointStyle = true;
}


document.addEventListener(
'DOMContentLoaded',
() => {

    const data =
        window.analyticsData;

    const textColor =
        '#6B7280';

    const gridColor =
        '#E5E7EB';

    // CATEGORY

    new Chart(
        document.getElementById(
            'categoryChart'
        ),
        {
            type:'doughnut',

            data:{
                labels:
                    data.category.labels,

                datasets:[
                    {
                        data:
                            data.category.data,

                        backgroundColor:[
                            '#00C26F',
                            '#34D399',
                            '#6EE7B7',
                            '#A7F3D0',
                            '#D1FAE5',
                            '#10B981',
                            '#059669',
                            '#047857'
                        ]
                    }
                ]
            },

            options:{
                plugins:{
                    legend:{
                        labels:{
                            color:textColor,
                            font:{
                                family:"'Elms Sans', sans-serif",
                                size:12
                            }
                        }
                    }
                }
            }
        }
    );

    // INCOME VS EXPENSE

    new Chart(
        document.getElementById(
            'incomeExpenseChart'
        ),
        {
            type:'bar',

            data:{
                labels:
                    data.incomeExpense.labels,

                datasets:[
                    {
                        label:'Amount',

                        data:
                            data.incomeExpense.data,

                        backgroundColor:[
                            '#00C26F',
                            '#EF4444'
                        ]
                    }
                ]
            },

            options:{
                plugins:{
                    legend:{
                        labels:{
                            color:textColor,
                            font:{
                                family:"'Elms Sans', sans-serif",
                                size:12
                            }
                        }
                    }
                },

                scales:{
                    x:{
                        ticks:{
                            color:textColor,
                            font:{
                                family:"'Elms Sans', sans-serif",
                                size:12
                            }
                        },
                        grid:{
                            color:gridColor
                        }
                    },
                    y:{
                        ticks:{
                            color:textColor,
                            font:{
                                family:"'Elms Sans', sans-serif",
                                size:12
                            }
                        },
                        grid:{
                            color:gridColor
                        }
                    }
                }
            }
        }
    );

    // MONTHLY

    new Chart(
        document.getElementById(
            'monthlyChart'
        ),
        {
            type:'line',

            data:{
                labels:
                    data.monthly.labels,

                datasets:[
                    {
                        label:'Income',

                        data:
                            data.monthly.income,

                        borderColor:'#00C26F',

                        backgroundColor:
                            'rgba(0,194,111,.15)',

                        fill:true,

                        tension:.35
                    },

                    {
                        label:'Expense',

                        data:
                            data.monthly.expense,

                        borderColor:'#EF4444',

                        backgroundColor:
                            'rgba(239,68,68,.15)',

                        fill:true,

                        tension:.35
                    }
                ]
            },

            options:{
                plugins:{
                    legend:{
                        labels:{
                            color:textColor,
                            font:{
                                family:"'Elms Sans', sans-serif",
                                size:12
                            }
                        }
                    }
                },

                scales:{
                    x:{
                        ticks:{
                            color:textColor,
                            font:{
                                family:"'Elms Sans', sans-serif",
                                size:12
                            }
                        },
                        grid:{
                            color:gridColor
                        }
                    },
                    y:{
                        ticks:{
                            color:textColor,
                            font:{
                                family:"'Elms Sans', sans-serif",
                                size:12
                            }
                        },
                        grid:{
                            color:gridColor
                        }
                    }
                }
            }
        }
    );

});