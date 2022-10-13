const mqtt = require('mqtt')

var client = mqtt.connect('http://vpn.ce.pdn.ac.lk:8883');

client.on('connect', function() {
    client.subscribe('326/sensor/temp');
    console.log('CLient has subscribed successfully!');
});


const tempControlTopic = '326/control/temp';
const tempCanChange = 2;
const tempThreashold = 32;

client.on('message', function(topic, message) {
    var data = JSON.parse(message);

    // data validation
    dataSize = Object.keys(data).length;
    if (dataSize =! 2 || Object.keys(data)[0] != 'time' || Object.keys(data)[1] != 'temp') {
        return
    }
    else {
        console.log('Do process');

        temperature = data['temp'];
        if (temperature < (tempThreashold - tempCanChange)) {
            client.publish(tempControlTopic, "Provide Hot Air")
            console.log("published 'Provide Hot Air' to topic " + tempControlTopic)
        }
        else if (temperature > (tempThreashold + tempCanChange)) {
            client.publish(tempControlTopic, "Provide Cold Air")
            console.log("published 'Provide Cold Air' to topic " + tempControlTopic)
        }
        else {
            client.publish(tempControlTopic, "Turn OFF")
            console.log("Maintainig current temperature levels")
        }
    }
});





