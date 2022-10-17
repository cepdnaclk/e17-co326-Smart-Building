import React, {useContext} from "react";
import {
    BrowserRouter as Router,
} from "react-router-dom";

import UserHomePage from "./pages/user_home_page/HomePage";
import ScrollToTop from "./helpers/ScrollToTop";
import {useSelector} from "react-redux";

function App() {
    const isLoggedIn = useSelector((state) => {
        return !!state.auth.token;
    });

    const isAdminLoggedIn = useSelector((state) => {
        return !!state.admin_auth.token;
    });

    const isHomePage = !isLoggedIn && !isAdminLoggedIn;

    return (
        <Router>
            <ScrollToTop>
                <UserHomePage/>

            </ScrollToTop>
        </Router>
    );
}

export default App;
