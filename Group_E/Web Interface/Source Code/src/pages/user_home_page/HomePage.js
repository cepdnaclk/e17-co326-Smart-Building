import React, {useEffect} from "react";

import Header from "../../components/Header/Header";
import Loader from "../../components/Loader/Loader";
import FooterCopyright from "../../components/Footer/FooterCopyright";
import AOS from "aos";

import {Redirect, Route, Switch} from "react-router-dom";
import RoomDetails from "./RoomDetails";
import History from "./History";
import Page500 from "../error_page/Page500";
import StatisticalData from "./StatisticalData";


const homePage = () => {
    useEffect(() => {
        AOS.init();
        AOS.refresh();
    }, []);
    return (
        <Loader>
            <div className="flex-wrapper">
                <div className="content">
                    <Header type={"white"} dropdown={false}/>

                    <Switch>
                        <Route
                            exact
                            path={`${process.env.PUBLIC_URL}/home`}
                            component={RoomDetails}
                        />

                        <Route
                            exact
                            path={`${process.env.PUBLIC_URL}/history`}
                            component={History}
                        />

                        <Route
                            exact
                            path={`${process.env.PUBLIC_URL}/statistical_data`}
                            component={StatisticalData}
                        />

                        <Route
                            path={`${process.env.PUBLIC_URL}/500error`}
                            component={Page500}
                        />

                        <Route path="*">
                            <Redirect to={`${process.env.PUBLIC_URL}/home`}/>
                        </Route>
                    </Switch>
                </div>

                <FooterCopyright classname="userpage_footer"/>
            </div>
        </Loader>
    );
};

export default homePage;
