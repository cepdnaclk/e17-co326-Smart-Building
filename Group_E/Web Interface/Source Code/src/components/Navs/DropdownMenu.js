import React, {useContext} from "react";
import {Link} from "react-scroll";
import {Link as DomLink, useHistory} from "react-router-dom";
import BarChart from "@material-ui/icons/BarChart";
import History from "@material-ui/icons/History";
import InfoIcon from "@material-ui/icons/Info";
import VideoIcon from "@material-ui/icons/OndemandVideo";
import NotificationsIcon from "@material-ui/icons/Notifications";
import NotificationAddIcon from "@material-ui/icons/AddAlert";
import MessageIcon from "@material-ui/icons/Email";
import FeedbackIcon from "@material-ui/icons/ClearAll";
import LogoutIcon from "@material-ui/icons/ExitToApp";
import GroupIcon from "@material-ui/icons/Group";
import TelegramIcon from "@material-ui/icons/Telegram";

import useWindowResizeListener from "../../helpers/useWindowResizeListener";
import {useDispatch, useSelector} from "react-redux";

import * as authActions from "../../store/actions/auth";
import * as adminAuthActions from "../../store/actions/admin_auth";

const DropdownMenu = (props) => {


    useWindowResizeListener();


    const history = useHistory();

    return (
        <div className="collapse navbar-collapse" id="navbar-menu">
            <ul className="nav navbar-nav" data-in="fadeIn" data-out="fadeOut">
                {props.data &&
                props.data.map((dropdown, i) => (
                    <Link
                        className={
                            props.fixed || props.type === "white" ? "white_bg" : "black_bg"
                        }
                        activeclassname={"active"}
                        to={dropdown.to}
                        spy={true}
                        duration={200}
                        delay={0}
                        key={i}
                        smooth={"easeInOutQuart"}
                    >
                        {dropdown.title}
                    </Link>
                ))}
            </ul>

            <ul className="nav navbar-nav" data-in="fadeIn" data-out="fadeOut">


                <DomLink
                    to={"/Status"}
                    className={
                        props.fixed || props.type === "white" ? "white_bg" : "black_bg"
                    }
                    onClick={(e) => {
                        e.preventDefault();

                        history.push(`${process.env.PUBLIC_URL}/homw`);
                    }}
                >
                    Room Details
                    <InfoIcon className="pb-1"/>
                </DomLink>

                <DomLink
                    to={"/History"}
                    className={
                        props.fixed || props.type === "white" ? "white_bg" : "black_bg"
                    }
                    onClick={(e) => {
                        e.preventDefault();
                        history.push(`${process.env.PUBLIC_URL}/history`);
                    }}
                >
                    History
                    <History className="pb-1"/>
                </DomLink>

                <DomLink
                    to={"/StatisticalData"}
                    className={
                        props.fixed || props.type === "white" ? "white_bg" : "black_bg"
                    }
                    onClick={(e) => {
                        e.preventDefault();
                        history.push(`${process.env.PUBLIC_URL}/statistical_data`);
                    }}
                >
                    Statistical Data
                    <BarChart className="pb-1"/>
                </DomLink>

            </ul>
        </div>
    );
};

export default DropdownMenu;
