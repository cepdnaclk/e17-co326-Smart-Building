import React from "react";
import Icofont from "react-icofont";


const Schedule = ({name, count, floor, index}) => {

    return (
        <div
            data-aos={"fade-up"}
            data-aos-delay={`${index}00`}
            data-aos-duration={700}
            className={
                "col-md-3 pricing-table" +
                // (schedule.featured === "true" ? "=featured" : "") +
                " col-sm-6"
            }
        >
            <div
                className="pricing-box"
                style={
                    count <= 2
                        ? {backgroundColor: "#a3ffac"}
                        : count <= 5 ? {backgroundColor: "#eaf07a"}
                        : count <= 10 ? {backgroundColor: "#ffb46e"}
                        : {backgroundColor: "#a82c2c"}
                }
            >

                <h2>Floor {floor}</h2>

                <h2 style={{fontSize:"30px", color:"#c35ff5"}}>Room {name}</h2>

                {count === 0 && (
                    <Icofont icon="ban"/>

                )}
                {(count >= 1 && count <= 2) && (
                    <Icofont icon="user"/>

                )}

                {(count >= 3 && count <= 5) && (
                    <Icofont icon="users"/>

                )}
                {(count >= 6) && (
                    <Icofont icon="users-social"/>

                )}


                <h4 className="pt-20">
                    <span>{count} People</span>
                </h4>

            </div>
        </div>
    )

};

export default Schedule;
