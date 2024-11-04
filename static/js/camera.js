// const get_robot_position = (msg) => {
//     const json = JSON.parse(msg);
//     console.log(json);
// }

// const onMessageArrived = (message) => {
//     let topic = message.destinationName;
//     let msg = message.payloadString;

//     switch (topic) {
//         case "ros_thermocam":
//             get_robot_position(msg);
//             break;
//         default:
//             break;
//     }
// }

// const publish = (topic, message) => {
//     let msg = new Paho.Message(message);
//     msg.destinationName = topic;
//     client.send(msg);
// }

// const onConnectionLost = (responseObject) => {
//     if (responseObject.errorCode !== 0) {
//         alert(responseObject.errorMessage);
//     }
// }

// const onConnect = () => {
//     client.subscribe("ros_thermocam");
//     console.log("연결성공")
   
// }

// const connect = () => {

    
//     const clientnum = Math.floor(Math.random() * 101);

//     client = new Paho.Client('1.220.178.46', 11883, "Medical" + String(clientnum));

//     client.onConnectionLost = onConnectionLost;
//     client.onMessageArrived = onMessageArrived;

//     client.connect({
//         onSuccess: onConnect
//     });

// }

// window.onload = () => {
//     connect();
// }


