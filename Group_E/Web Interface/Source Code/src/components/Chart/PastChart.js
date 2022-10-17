import ReactApexChart from 'react-apexcharts'
import Chart from 'react-apexcharts'
import React from "react";
// import { useWindowSize } from 'usehooks-ts'

export default function pastChart(props) {
    // const { width, height } = useWindowSize()


    // const series = [{
    //     name: "Desktops",
    //     data: [10, 41, 35, 51, 49, 62, 69, 91, 148]
    // }];
    // const options = {
    //     pastChart: {
    //         height: 350,
    //         type: 'line',
    //         zoom: {
    //             enabled: false
    //         }
    //     },
    //     dataLabels: {
    //         enabled: false
    //     },
    //     stroke: {
    //         curve: 'straight'
    //     },
    //     title: {
    //         text: 'Product Trends by Month',
    //         align: 'left'
    //     },
    //     grid: {
    //         row: {
    //             colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
    //             opacity: 0.5
    //         },
    //     },
    //     xaxis: {
    //         categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep'],
    //     }
    // };
    //
    // return (
    //     <div id="pastChart">
    //         <ReactApexChart options={options} series={series} type="line" height={350}/>
    //     </div>
    // );

    console.log(props.filteredData)

    let date_times = [];
    let counts = []
    props.filteredData.map((data) => {
        date_times.push(data.date_time)
        counts.push(data.count)
    })


    const options = {
        chart: {
            id: 'past-data-chart'
        },
        xaxis: {
            categories: date_times

        }
    };
    const series = [{
        name: 'Number of people',
        data: counts
    }]


    return (
        <div>


            <Chart options={options} series={series} type="bar" width={1300} height={500}/>
        </div>
    )


}
