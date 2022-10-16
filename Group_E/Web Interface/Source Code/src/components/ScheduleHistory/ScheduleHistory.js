import React, {useCallback, useEffect, useState} from "react";
import ScheduleBar from "./ScheduleBar";
import {useDispatch, useSelector} from "react-redux";
import {fetchHistory} from "../../store/actions/history";
import Loader from "react-loader-spinner";
import {useHistory} from "react-router-dom";
import {dateCompare} from "../../helpers/functions";
import Chart from "../Chart/PastChart"

export default function ScheduleHistory() {
    const historyData = [
        {
            date_time: "2022/10/22 22:10:15",
            details: {
                floor1: {
                    room1: 0,
                    room2: 2
                },
                floor2: {
                    room3: 6,
                    room4: 9,
                    room5: 0
                }
            }
        },
        {
            date_time: "2022/10/22 22:10:32",
            details: {
                floor1: {
                    room1: 3,
                    room2: 2
                },
                floor2: {
                    room3: 7,
                    room4: 1,
                    room5: 2
                }
            }
        },

        {
            date_time: "2022/10/23 22:10:32",
            details: {
                floor1: {
                    room1: 3,
                    room2: 4
                },
                floor2: {
                    room3: 2,
                    room4: 3,
                    room5: 4
                }
            }
        },

    ]
    const history = useHistory();
    // const historyData = useSelector((state) => state.history.history).sort(
    //   (date1, date2) => dateCompare(date1, date2)
    // );

    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState();
    const [isChecked, setChecked] = useState(false);
    // const dispatch = useDispatch();

    const handleChange = () => {
        setChecked((prevState) => !prevState);
    };
    // const loadHistory = useCallback(() => {
    //   setError(null);
    //   setIsLoading(true);
    //
    //   return dispatch(fetchHistory())
    //     .then((response) => {
    //       setIsLoading(false);
    //     })
    //     .catch((err) => {
    //       setError(err.message);
    //     });
    // }, [dispatch, setIsLoading, setError]);

    // useEffect(() => {
    //   loadHistory();
    // }, [dispatch, loadHistory]);

    if (error) {
        history.replace(`${process.env.PUBLIC_URL}/500error`);
        return <React.Fragment/>;
    }

    if (isLoading) {
        return (
            <div align="center">
                <Loader type="ThreeDots" color="green" height={100} width={100}/>
            </div>
        );
    }

    return (
        <div className="container">
            <Chart/>
            {/*<div className="form-group">*/}
            {/*  <div className="">*/}
            {/*    <h4 className="">Show Latest</h4>*/}
            {/*  </div>*/}
            {/*  <div className="">*/}
            {/*    <Switch onChange={handleChange} checked={isChecked} height={25} />*/}
            {/*  </div>*/}
            {/*</div>*/}

            {/*{historyData.map((data) => (*/}
            {/*    <ScheduleBar*/}
            {/*        title={data.title}*/}
            {/*        date_time={data.date_time}*/}
            {/*        status={data.status}*/}
            {/*        key={data._id}*/}
            {/*    />*/}
            {/*))}*/}
        </div>
    );
}
