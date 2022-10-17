import React, {useCallback, useEffect, useState} from "react";
import ScheduleHistory from "../../components/ScheduleHistory/ScheduleHistory";
import PastChart from "../../components/Chart/PastChart"
import ChartInput from "../../components/Chart/ChartInput";
import {useHistory} from "react-router-dom";
import Loader from "react-loader-spinner";
// import {historyData} from "../../data/HistoryData/history";

const History = () => {

    const history = useHistory();

    const [historyData, setHistoryData] = useState([]);
    const [filteredData, setFilteredData] = useState([]);
    // const [room, setRoom] = useState([]);

    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState();


    const loadPastData = useCallback(() => {
        setError(null);
        setIsLoading(true);

        fetch("http://10.40.18.10:50005/past_data").then((response) => {
            if (!response.ok) {
                throw new Error("Something went wrong!");
            }
            return response.json();
        }).then((data) => {
            // console.log(data);
            setHistoryData((data));
            setIsLoading(false);

        }).catch((error) => {
            setError(error.message)
            console.log(error)
        })
    }, []);

    useEffect(() => {
        loadPastData();
    }, [loadPastData]);


    if (error) {
        history.replace(`${process.env.PUBLIC_URL}/500error`);
        return <React.Fragment/>;
    }


    const filterData = (room, date, number_of_data) => {

        if (!room)
            return
        // console.log(number_of_data)

        let temp_data = []

        let temp = date.split("-")
        let date_threshold = new Date(parseInt(temp[0]), parseInt(temp[1])-1, parseInt(temp[2]));

        let floor_room = room.split(" - ");

        // console.log(room_data);
        // console.log(date_threshold)
        for (let i = historyData.length - 1; i >= 0 && temp_data.length < number_of_data; i--) {

            console.log("inde")
            let date_str = historyData[i].payload.date_time.split(" ")[0].split("/")
            let cur_date = new Date(parseInt(date_str[0]), parseInt(date_str[1])-1, parseInt(date_str[2]));
            console.log(date_threshold, cur_date);
            if (cur_date <= date_threshold) {
                console.log("date")
                historyData[i].payload.details.map((floor_data) => {
                    console.log(floor_data.name, floor_room[0].substring(floor_room[0].indexOf("r") + 1).trim());
                    if (floor_data.name === floor_room[0].trim()) {
                        console.log("floor");
                        floor_data.details.map((room_data) => {
                                if (room_data.name === floor_room[1].trim()) {
                                    console.log("room");

                                    // console.log(cur_date, room_data.name, room_data.count)
                                    temp_data.push({
                                        date_time: date_str,
                                        count: room_data.count,
                                        // floor: floor_data.name

                                    });

                                }
                            }
                        )
                    }

                    // date_times.push(data.date_time)
                    // counts.push(data.details.floor1.room1)
                })
            }
        }

        temp_data = temp_data.reverse()

        setFilteredData(temp_data);
        // console.log(temp_data);


    }

    return (
        <div className="container">

            {isLoading && (
                <div align="center" style={{paddingTop: 150, paddingBottom: 10}}>
                    <Loader type="ThreeDots" color="green" height={100} width={100}/>
                </div>
            )}


            {!isLoading && (
                <section className="pb-2">
                    <div className="section-heading pt-20">
                        <h2
                            className="text-uppercase pb-0 mb-0"
                            data-aos={"fade-up"}
                            data-aos-delay={100}
                            data-aos-duration={700}
                        >
                            Past Data
                        </h2>
                    </div>
                    <div className="pt-20"/>

                    <ChartInput historyData={historyData} filterData={filterData}/>
                    <PastChart filteredData={filteredData}/>
                </section>
            )}
        </div>
    );
};

export default History;
