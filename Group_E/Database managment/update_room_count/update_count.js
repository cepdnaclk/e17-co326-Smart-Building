let arr = msg.payload;
let sensor_data = global.get("01_us_data");


//Create the date and time objects
var targetTime = new Date();
var timeZoneFromDB = 5.45; //time zone value from database
//get the timezone offset from local time in minutes
var tzDifference = timeZoneFromDB * 60 + targetTime.getTimezoneOffset();
//convert the offset to milliseconds, add to targetTime, and make a new Date
var offsetTime = new Date(targetTime.getTime() + tzDifference * 60 * 1000);


let count ;

if (arr.length == 0){
    count = 1;
}
else{
    count = arr[0].count + sensor_data; 
}

msg.payload = {"$set":{"room_number":1, "floor_number":0,"count":count,"last_update":offsetTime.toLocaleString()} }

msg.query = {"room_number":1,"floor_number":0};
msg.topic = "db query";
return msg;