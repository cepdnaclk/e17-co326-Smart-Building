const totalArray = [];
const averageArray = [];
const maxRoomArray = [];
const minRoomArray = [];

let floor;
let rooms;
let room;
let totalCountOnFloor;
let maxIndex = 0;
let minIndex = 0;

let lastObj = msg.payload.details;

//calculate the average count of each room
for(let i=0;i<lastObj.length;i++){
    
    floor = lastObj[i].details;

    totalCountOnFloor = 0;
    maxIndex = 0;
    minIndex = 0;
    for(let j=0;j<floor.length;j++){

        room = floor[j];
        totalCountOnFloor += room.count;
        if(room.count>floor[maxIndex].count){
            maxIndex = j;
        }
        if (room.count < floor[minIndex].count) {
            minIndex = j;
        }

    }

    totalArray.push(totalCountOnFloor);
    averageArray.push(totalCountOnFloor/floor.length);
    maxRoomArray.push(floor[maxIndex]);
    minRoomArray.push(floor[minIndex]);

}

msg.payload = {
    "totalArray":totalArray,
    "averageArray" : averageArray,
    "maxRoomArray" : maxRoomArray,
    "minRoomArray" : minRoomArray
    }

return msg;