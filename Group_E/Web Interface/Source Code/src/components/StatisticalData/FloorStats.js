import React, {useState, useContext, useEffect, useCallback} from "react";
import Icofont from "react-icofont";
import CountUp from "react-countup";
import VisibilitySensor from "react-visibility-sensor";
import * as statusActions from "../../store/actions/status";

import Loader from "react-loader-spinner";
import {useHistory} from "react-router-dom";

const FloorStats = ({data, bg, type}) => {


    const [viewed, setViewed] = useState(true);

    const history = useHistory();
    //
    const [error, setError] = useState();

    const status = {
        rooms: 0,
        empty_rooms: 0,
        total_people: 0
    }


    const viewChangeHandler = (isVisible) => {
        if (isVisible) setViewed(true);
    };

    if (error) {
        history.replace(`${process.env.PUBLIC_URL}/500error`);
        return <React.Fragment/>;
    }

    return (

        <React.Fragment>

            <section className="pt-100">

                <div className="row">
                    <div className="col-sm-6 section-heading">
                        <h2
                            className="text-uppercase"
                            data-aos={"fade-up"}
                            data-aos-delay={100}
                            data-aos-duration={700}
                        >
                            FLOOR {data.floor} - STATISTICAL DATA
                        </h2>
                    </div>
                </div>
            </section>


            <section className={"pt-80 pb-80 " + (bg ? bg : "dark-bg")}>

                {/*<div className={"container" + (type === "wide" ? "-fluid" : "")}>*/}
                {/*<div className={"container"}>*/}

                    <div className="row">


                        <div
                            className="col-md-3 counter text-center col-sm-6 wow fadeTop"
                            data-wow-delay="0.1s"
                            data-aos-delay="0"
                            data-aos={"fade-up"}
                            data-aos-easing={"ease-in-sine"}
                        >
                            <Icofont icon={"users-social"} className="light-icon font-30px"/>

                            <h2
                                className={
                                    "count font-700 " + (bg === "white-bg" ? "" : "white-color")
                                }
                            >
                                <VisibilitySensor onChange={viewChangeHandler} delayedCall>
                                    <CountUp end={viewed ? data.total : 0}/>
                                </VisibilitySensor>
                            </h2>
                            <h3 className={bg === "white-bg" ? "dark-color" : ""}>
                                Total People
                            </h3>
                        </div>


                        <div
                            className="col-md-3 counter text-center col-sm-6 wow fadeTop"
                            data-wow-delay="0.1s"
                            data-aos-delay="0"
                            data-aos={"fade-up"}
                            data-aos-easing={"ease-in-sine"}
                        >
                            <Icofont icon={"users-alt-2"} className="light-icon font-30px"/>

                            <h2
                                className={
                                    "count font-700 " + (bg === "white-bg" ? "" : "white-color")
                                }
                            >
                                <VisibilitySensor onChange={viewChangeHandler} delayedCall>
                                    <CountUp end={viewed ? data.average : 0}/>
                                </VisibilitySensor>
                            </h2>
                            <h3 className={bg === "white-bg" ? "dark-color" : ""}>
                                Average People Per Room
                            </h3>
                        </div>

                        <div
                            className="col-md-3 counter text-center col-sm-6 wow fadeTop"
                            data-wow-delay="0.1s"
                            data-aos-delay="0"
                            data-aos={"fade-up"}
                            data-aos-easing={"ease-in-sine"}
                        >
                            <Icofont icon={"users-social"} className="light-icon font-30px"/>

                            <h2
                                className={
                                    "count font-700 " + (bg === "white-bg" ? "" : "white-color")
                                }
                            >
                                <VisibilitySensor onChange={viewChangeHandler} delayedCall>
                                    <CountUp end={viewed ? data.maxRoomDetails.count : 0}/>
                                </VisibilitySensor>
                            </h2>
                            <h3 className={bg === "white-bg" ? "dark-color" : ""}>
                                Most People ({data.maxRoomDetails.name})
                            </h3>
                        </div>

                        <div
                            className="col-md-3 counter text-center col-sm-6 wow fadeTop"
                            data-wow-delay="0.1s"
                            data-aos-delay="0"
                            data-aos={"fade-up"}
                            data-aos-easing={"ease-in-sine"}
                        >
                            <Icofont icon={"users-social"} className="light-icon font-30px"/>
                            {/*<h3>Room 3</h3>*/}

                            <h2
                                className={
                                    "count font-700 " + (bg === "white-bg" ? "" : "white-color")
                                }
                            >
                                <VisibilitySensor onChange={viewChangeHandler} delayedCall>
                                    <CountUp end={viewed ? data.minRoomDetails.count : 0}/>
                                </VisibilitySensor>


                            </h2>
                            <h3 className={bg === "white-bg" ? "dark-color" : ""}>
                                Least People ({data.minRoomDetails.name})
                            </h3>
                        </div>
                    </div>
                {/*</div>*/}
            </section>
        </React.Fragment>


    );
};

export default FloorStats;
