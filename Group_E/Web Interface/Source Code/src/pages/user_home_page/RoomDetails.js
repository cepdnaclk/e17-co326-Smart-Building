import React from "react";

import Status from "../../components/Status/Status";
import ActiveSchedules from "../../components/ActiveSchedules/ActiveSchedules";

const RoomDetails = () => {
  return (
    <React.Fragment>
      <Status />
      <ActiveSchedules />
    </React.Fragment>
  );
};

export default RoomDetails;
