import React, {useState, useCallback, useEffect, useContext} from "react";
import Schedule from "./Schedule";

import ScheduleForm from "../ScheduleForm/ScheduleForm";
import ConfirmationBox from "../ConfirmationBox/ConfirmationBox";
import Loader from "react-loader-spinner";
import {useDispatch, useSelector} from "react-redux";
import * as schedulesActions from "../../store/actions/schedules";
import Page500 from "../../pages/error_page/Page500";
import {useHistory} from "react-router-dom";
import Button from "@material-ui/core/Button";
import {makeStyles} from "@material-ui/core/styles";
import {Tooltip} from "@material-ui/core";
import {forEach} from "react-bootstrap/ElementChildren";
import * as ScheduleActions from "../../store/actions/schedules";
import FeedNowConfirmation from "../ConfirmationBox/FeedNowConfirmation";


const useStyles = makeStyles((theme) => ({

    button: {
        backgroundColor: "#1d9a6c",
        fontSize: 14,
        fontFamily: "Jost",
        borderRadius: 3,
        border: 0,
        color: "white",
        height: 48,
        padding: "0 30px",
        boxShadow: "0 3px 5px 2px rgba(255, 105, 135, .3)",
        // width:"300px",
        // $disabled is a reference to the local disabled
        // rule within the same style sheet.
        // By using &, we increase the specificity.
        "&:hover": {
            backgroundColor: "#1d9a6c",
        },
        "&$disabled": {
            background: "rgba(0, 0, 0, 0.12)",
            color: "white",
            boxShadow: "none",
        },
    },
    disabled: {},
}));

const ActiveSchedules = (props) => {

    const [room_details, setRoomDetails] = useState([]);

    const classes = useStyles();
    // const schedules = useSelector((state) => state.schedules.schedules);
    // const remainingRounds = useSelector((state) => state.status.status.remainingRounds);
    // const dispatch = useDispatch();
    const history = useHistory();

    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState();


    const loadRoomData = useCallback(() => {
        setError(null);
        setIsLoading(true);

        fetch("http://10.40.18.10:50005/room_details").then((response) => {
            if (!response.ok) {
                throw new Error("Something went wrong!");
            }
            return response.json();
        }).then((data) => {
            let temp_arr = [];

            data.map((room) => {
                    let temp = {
                        name: room.room_number,
                        count: room.count,
                        floor: room.floor_number

                    }
                    temp_arr.push(temp);
                }
            )

            setRoomDetails(temp_arr);
            console.log(temp_arr);
            setIsLoading(false);

        }).catch((error) => {
            setError(error.message)
            console.log(error)
        })
    }, []);

    useEffect(() => {
        loadRoomData();
    }, [loadRoomData]);


    if (error) {
        history.replace(`${process.env.PUBLIC_URL}/500error`);
        return <React.Fragment/>;
    }


    return (
        <React.Fragment>

            <section className="">
                <div className="container">
                    <div className="row">
                        <div className="col-sm-8 section-heading">
                            <h2
                                className="text-uppercase"
                                data-aos={"fade-up"}
                                data-aos-delay={100}
                                data-aos-duration={700}
                            >
                                OCCUPANCY DETAILS
                            </h2>
                        </div>
                    </div>
                    {isLoading && (
                        <div align="center">
                            <Loader type="ThreeDots" color="green" height={100} width={100}/>
                        </div>
                    )}
                    {!isLoading && (

                        <React.Fragment>

                            <div className="row mt-30">
                                {room_details.map((room, i) => (
                                    <Schedule
                                        name={room.name}
                                        count={room.count}
                                        floor={room.floor}
                                        index={i}
                                        key={i}
                                    />
                                ))}
                            </div>
                        </React.Fragment>

                    )}
                </div>
            </section>
        </React.Fragment>
    );
};

export default ActiveSchedules;
