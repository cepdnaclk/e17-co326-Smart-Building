import React, {useState, useEffect} from "react";
import "./ChartInput.css"
import 'react-dropdown/style.css';
import Dropdown from 'react-dropdown';


export default function ChartInput(props) {

    const [rooms, setRooms] = useState([]);

    useEffect(() => {
        let temp_rooms = []
        if (props.historyData.length !== 0) {
            props.historyData[0].payload.details.map((floor_data) => {
                floor_data.details.map((room_data) => {
                    temp_rooms.push(floor_data.name + " - " + room_data.name)
                })
            })
        }

        setRooms(temp_rooms);
        setRoom(temp_rooms[0]);
    }, [props.historyData]);

    // console.log(rooms)

    let date_now = new Date();
    let date_now_str = date_now.getUTCFullYear() + "-" + (date_now.getUTCMonth() + 1) + "-" + date_now.getUTCDate();

    const [room, setRoom] = useState();
    // console.log("room" + room);
    const [endDate, setEndDate] = useState(date_now_str);
    const [num_of_data, setNumberOfData] = useState(20);

    props.historyData.map((data) => {
        let date_time = data.date_time;
        data.payload.details.map((floor_data) => {
            floor_data.details.map((room_data) => {
                let room_name = room_data.name;
                let count = room_data.count;
                // console.log(date_time, room_name, count)
            })
        })
    })

    useEffect(() => {
        props.filterData(room, endDate, num_of_data);
    }, [room, endDate, num_of_data]);

    const onChangeRoom = (event) => {
        setRoom(event.value)
    }

    const onChangeDate = (event) => {
        setEndDate(event.target.value)
    }

    const onChangeNumOfRooms = (event) => {
        setNumberOfData(event.target.value)
    }


    // console.log(room, endDate, num_of_data)
    return (
        <form className="justify-content-center">
            <div className='new-expense__controls'>

                <div className='new-expense__control room__ ' style={{width: '300px'}}>
                    <label>Select Room</label>
                    {/*<input type='text' />*/}
                    <Dropdown options={rooms} value={room} placeholder="Select a room" onChange={onChangeRoom}/>;

                </div>

                <div className='new-expense__control room__'>
                    <label>Enter End Date</label>
                    <input type='date' min='2019-01-01' max='2022-12-31' value={endDate} onChange={onChangeDate}/>
                </div>

                <div className='new-expense__control room__'>
                    <label>Select Number Of Data</label>
                    <input type='number' min={10} max={50} value={num_of_data}
                           onChange={onChangeNumOfRooms}/>
                </div>
            </div>
        </form>
    );
}