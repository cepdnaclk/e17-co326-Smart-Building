import React, {useState, useContext, useEffect, useCallback} from "react";
import Loader from "react-loader-spinner";
import {useHistory} from "react-router-dom";
import FloorStats from "../../components/StatisticalData/FloorStats";

const StatisticalData = ({bg, type}) => {


    const [stats, setStats] = useState([]);

    // useEffect(() => {
    //     let temp_data = []
    //
    //     for (let i = 0; i < initial_stats.totalArray.length; i++) {
    //         let total = initial_stats.totalArray[i];
    //         let average = initial_stats.averageArray[i];
    //         let max_room_details = initial_stats.maxRoomArray[i];
    //         let min_room_details = initial_stats.minRoomArray[i];
    //
    //         temp_data.push({
    //             "floor": i,
    //             "total": total,
    //             "average": average,
    //             "maxRoomDetails": max_room_details,
    //             "minRoomDetails": min_room_details
    //         })
    //
    //         setStats(temp_data);
    //     }
    // }, []);

    const [viewed, setViewed] = useState(true);

    const history = useHistory();
    //
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState();


    const loadStatisticalData = useCallback(() => {
        setError(null);
        setIsLoading(true);

        fetch("http://10.40.18.10:50005/statistical_data").then((response) => {
            if (!response.ok) {
                throw new Error("Something went wrong!");
            }
            return response.json();
        }).then((data) => {

            let temp_data = []

            for (let i = 0; i < data.payload.totalArray.length; i++) {
                let total = data.payload.totalArray[i];
                let average = data.payload.averageArray[i];
                let max_room_details = data.payload.maxRoomArray[i];
                let min_room_details = data.payload.minRoomArray[i];

                temp_data.push({
                    "floor": i,
                    "total": total,
                    "average": average,
                    "maxRoomDetails": max_room_details,
                    "minRoomDetails": min_room_details
                })

            }
            setStats(temp_data);
            setIsLoading(false);

        }).catch((error) => {
            setError(error.message)
            console.log(error)
        })
    }, []);

    useEffect(() => {
        loadStatisticalData();
    }, [loadStatisticalData]);

    const viewChangeHandler = (isVisible) => {
        if (isVisible) setViewed(true);
    };

    if (error) {
        history.replace(`${process.env.PUBLIC_URL}/500error`);
        return <React.Fragment/>;
    }

    return (
        <div className="pb-100 pl-40 pr-40">

            {isLoading && (
                <div align="center" style={{paddingTop: 150, paddingBottom: 10}}>
                    <Loader type="ThreeDots" color="green" height={100} width={100}/>
                </div>
            )}

            {!isLoading && (

                <div>
                    {stats.map((stat_data, i) => (
                        <FloorStats
                            data={stat_data}
                            key={i}
                        />
                    ))}

                </div>

            )}
        </div>
    );
};

export default StatisticalData;
