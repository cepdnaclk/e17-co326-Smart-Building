import React, { useState, useContext, useEffect, useCallback } from "react";
import Icofont from "react-icofont";
import CountUp from "react-countup";
import VisibilitySensor from "react-visibility-sensor";
import * as statusActions from "../../store/actions/status";

import Loader from "react-loader-spinner";
import { useDispatch, useSelector } from "react-redux";
import Page500 from "../../pages/error_page/Page500";
import { useHistory } from "react-router-dom";
import { fetchNotification } from "../../store/actions/notifications";

const Status = ({ bg, type }) => {


  const [viewed, setViewed] = useState(true);
  //
  // const status = useSelector((state) => state.status.status);
  // const dispatch = useDispatch();
  const history = useHistory();
  //
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState();

  const initial_status = {
    rooms : 0,
    empty_rooms : 0,
    total_people : 0
  }
  const [status, setStatus] = useState({initial_status});


  const loadStatus = useCallback(() => {
    setError(null);
    setIsLoading(true);

    fetch("http://10.40.18.10:50005/room_details").then((response) => {
      if (!response.ok) {
        throw new Error("Something went wrong!");
      }
      return response.json();
    }).then((data) => {
      console.log(data);
      let temp_status = {
        rooms : data.length,
        empty_rooms : 0,
        total_people : 0
      }


      data.map((room) => {
        temp_status.total_people += room.count;

        if (room.count === 0)
          temp_status.rooms++;

      })
      setStatus(temp_status);


      setIsLoading(false);

    }).catch((error) => {
      setError(error.message)
      console.log(error)
    })
  }, []);

  useEffect(() => {
    loadStatus();
  }, [loadStatus]);

  const viewChangeHandler = (isVisible) => {
    if (isVisible) setViewed(true);
  };

  if (error) {
    history.replace(`${process.env.PUBLIC_URL}/500error`);
    return <React.Fragment />;
  }

  return (
    <section className={"pt-120 pb-80 " + (bg ? bg : "dark-bg")}>
      {isLoading && (
        <div align="center" style={{ paddingTop: 25, paddingBottom: 10 }}>
          <Loader type="ThreeDots" color="green" height={100} width={100} />
        </div>
      )}

      {!isLoading && (
        <div className={"container" + (type === "wide" ? "-fluid" : "")}>
          <div className="row">


            <div
                className="col-md-4 counter text-center col-sm-8 wow fadeTop"
                data-wow-delay="0.1s"
                data-aos-delay="0"
                data-aos={"fade-up"}
                data-aos-easing={"ease-in-sine"}
            >
              <Icofont icon={"home"} className="light-icon font-30px" />

              <h2
                  className={
                    "count font-700 " + (bg === "white-bg" ? "" : "white-color")
                  }
              >
                <VisibilitySensor onChange={viewChangeHandler} delayedCall>
                  <CountUp end={viewed ? status.rooms : 0} />
                </VisibilitySensor>
              </h2>
              <h3 className={bg === "white-bg" ? "dark-color" : ""}>
                Total Rooms
              </h3>
            </div>


            <div
                className="col-md-4 counter text-center col-sm-8 wow fadeTop"
                data-wow-delay="0.1s"
                data-aos-delay="0"
                data-aos={"fade-up"}
                data-aos-easing={"ease-in-sine"}
            >
              <Icofont icon={"ui-home"} className="light-icon font-30px" />

              <h2
                  className={
                    "count font-700 " + (bg === "white-bg" ? "" : "white-color")
                  }
              >
                <VisibilitySensor onChange={viewChangeHandler} delayedCall>
                  <CountUp end={viewed ? status.empty_rooms : 0} />
                </VisibilitySensor>
              </h2>
              <h3 className={bg === "white-bg" ? "dark-color" : ""}>
                Number of Empty Rooms
              </h3>
            </div>

            <div
                className="col-md-4 counter text-center col-sm-8 wow fadeTop"
                data-wow-delay="0.1s"
                data-aos-delay="0"
                data-aos={"fade-up"}
                data-aos-easing={"ease-in-sine"}
            >
              <Icofont icon={"users-social"} className="light-icon font-30px" />

              <h2
                  className={
                    "count font-700 " + (bg === "white-bg" ? "" : "white-color")
                  }
              >
                <VisibilitySensor onChange={viewChangeHandler} delayedCall>
                  <CountUp end={viewed ? status.total_people : 0} />
                </VisibilitySensor>
              </h2>
              <h3 className={bg === "white-bg" ? "dark-color" : ""}>
                Total People
              </h3>
            </div>

            {/*<div*/}
            {/*  className="col-md-3 counter text-center col-sm-6 wow fadeTop"*/}
            {/*  data-wow-delay="0.1s"*/}
            {/*  data-aos-delay="0"*/}
            {/*  data-aos={"fade-up"}*/}
            {/*  data-aos-easing={"ease-in-sine"}*/}
            {/*>*/}
            {/*  <Icofont*/}
            {/*    icon={true === true ? "wifi" : "ban"}*/}
            {/*    className="light-icon font-30px"*/}
            {/*  />*/}

            {/*  <h2*/}
            {/*    className={*/}
            {/*      "count font-700 " + (bg === "white-bg" ? "" : "white-color")*/}
            {/*    }*/}
            {/*  >*/}
            {/*    {true === true ? "ON" : "OFF"}*/}
            {/*  </h2>*/}
            {/*  <h3 className={bg === "white-bg" ? "dark-color" : ""}>Status</h3>*/}
            {/*</div>*/}

            {/*<div*/}
            {/*  className="col-md-3 counter text-center col-sm-6 wow fadeTop"*/}
            {/*  data-wow-delay="0.1s"*/}
            {/*  data-aos-delay="0"*/}
            {/*  data-aos={"fade-up"}*/}
            {/*  data-aos-easing={"ease-in-sine"}*/}
            {/*>*/}
            {/*  <Icofont*/}
            {/*    icon={*/}
            {/*      100 >= 70*/}
            {/*        ? "battery-full"*/}
            {/*        : 100 >= 30*/}
            {/*        ? "battery-half"*/}
            {/*        : "battery-low"*/}
            {/*    }*/}
            {/*    className="light-icon font-30px"*/}
            {/*  />*/}

            {/*  <h2*/}
            {/*    className={*/}
            {/*      "count font-700 " + (bg === "white-bg" ? "" : "white-color")*/}
            {/*    }*/}
            {/*  >*/}
            {/*    <VisibilitySensor onChange={viewChangeHandler} delayedCall>*/}
            {/*      <CountUp end={viewed ? 100 : 0} />*/}
            {/*    </VisibilitySensor>*/}
            {/*    %*/}
            {/*  </h2>*/}
            {/*  <h3 className={bg === "white-bg" ? "dark-color" : ""}>Battery</h3>*/}
            {/*</div>*/}

            {/*<div*/}
            {/*  className="col-md-3 counter text-center col-sm-6 wow fadeTop"*/}
            {/*  data-wow-delay="0.1s"*/}
            {/*  data-aos-delay="0"*/}
            {/*  data-aos={"fade-up"}*/}
            {/*  data-aos-easing={"ease-in-sine"}*/}
            {/*>*/}
            {/*  <Icofont icon={"spinner"} className="light-icon font-30px" />*/}

            {/*  <h2*/}
            {/*    className={*/}
            {/*      "count font-700 " + (bg === "white-bg" ? "" : "white-color")*/}
            {/*    }*/}
            {/*  >*/}
            {/*    <VisibilitySensor onChange={viewChangeHandler} delayedCall>*/}
            {/*      <CountUp end={viewed ? 5 : 0} />*/}
            {/*    </VisibilitySensor>*/}
            {/*  </h2>*/}
            {/*  <h3 className={bg === "white-bg" ? "dark-color" : ""}>*/}
            {/*    Remaining Rounds*/}
            {/*  </h3>*/}
            {/*</div>*/}

            {/*<div*/}
            {/*  className="col-md-3 counter text-center col-sm-6 wow fadeTop"*/}
            {/*  data-wow-delay="0.1s"*/}
            {/*  data-aos-delay="0"*/}
            {/*  data-aos={"fade-up"}*/}
            {/*  data-aos-easing={"ease-in-sine"}*/}
            {/*>*/}
            {/*  <Icofont icon={"clock-time"} className="light-icon font-30px" />*/}

            {/*  <h2*/}
            {/*    className={*/}
            {/*      "count font-700 " + (bg === "white-bg" ? "" : "white-color")*/}
            {/*    }*/}
            {/*  >*/}
            {/*    <VisibilitySensor onChange={viewChangeHandler} delayedCall>*/}
            {/*      <CountUp end={viewed ? 0 : 0} />*/}
            {/*    </VisibilitySensor>*/}
            {/*    {" h"}*/}
            {/*  </h2>*/}
            {/*  <h3 className={bg === "white-bg" ? "dark-color" : ""}>*/}
            {/*    Last Feed Before*/}
            {/*  </h3>*/}
            {/*</div>*/}
          </div>
        </div>
      )}
    </section>
  );
};

export default Status;
