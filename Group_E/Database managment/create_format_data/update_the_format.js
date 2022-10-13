let details = []
let arr = [{"_id":"63470c6b0502e71145f114f7","floor_number":0,"room_number":1,"count":20,"last_update":"10/13/2022, 1:28:05 PM"},
            {"_id":"6347be0e02f76600070dc7c4","room_number":2,"floor_number":0,"count":1,"last_update":"12/10/2022 12:57 PM"}            
];

// Hnadle uncaught errors
if(arr.length == 0) return msg;

msg = {};
//Create the date and time objects
var targetTime = new Date();
var timeZoneFromDB = 5.45; //time zone value from database
//get the timezone offset from local time in minutes
var tzDifference = timeZoneFromDB * 60 + targetTime.getTimezoneOffset();
//convert the offset to milliseconds, add to targetTime, and make a new Date
var offsetTime = new Date(targetTime.getTime() + tzDifference * 60 * 1000);






for(let floor = 0; floor<4; floor++){
    let floor_data = arr.filter(element => element.floor_number === floor);
    let inner_details = [];

    if(floor_data.length == 0){
        console.log("Error");
    }
    else{
        
        for(let j =0; j < floor_data.length; j++){
            inner_details.push({"name":"room"+ floor_data[j].room_number,"count":floor_data[j].count});
        }
        
    }

    details.push( {"name":"florr"+floor ,"details":inner_details});
   
}

msg.payload = {"date_time":offsetTime.toLocaleString(),"details":details};

console.log(msg.payload);