var AWS = require('aws-sdk');
  
exports.handler = (event, context, callback) => {
    
    let cuisines = ['chinese', 'italian', 'japanese','mexican', 'tradamerican'];
    let nextslot = "cuisine";
    
    let response =  {
            "dialogAction": {
                "type": "Delegate",
                "slots": event.currentIntent.slots,
            }
        };
    
    if (event.invocationSource === "DialogCodeHook") {
        
        if (event.currentIntent.slots.location === null || event.currentIntent.slots.cuisine === null) {
            console.log(response);
            callback(null, response);
        }
        
        if (!cuisines.includes(event.currentIntent.slots.cuisine)) {
            callback(null, {
                "dialogAction": {
                    "type": "ElicitSlot",
                    "message": {
                        "contentType": "PlainText",
                        "content": "Please choose between 'chinese', 'italian', 'japanese','mexican', 'tradamerican'"
                    },
                    "intentName": event.currentIntent.name,
                    "slots": event.currentIntent.slots,
                    "slotToElicit" : "cuisine"
                }
            });    
        }
        
        if (event.currentIntent.slots.people === null) {
            callback(null, response);
        }
        
        if (event.currentIntent.slots.people <= 0 || event.currentIntent.slots.people >= 20) {
            callback(null, {
                "dialogAction": {
                    "type": "ElicitSlot",
                    "message": {
                        "contentType": "PlainText",
                        "content": "Please choose between 1 and 20"
                    },
                    "intentName": event.currentIntent.name,
                    "slots": event.currentIntent.slots,
                    "slotToElicit" : "people"
                }
            });  
        }
        
        if (event.currentIntent.slots.time === null) {
            callback(null, response);
        }
        
        if (event.currentIntent.slots.number === null) {
            callback(null, response);
        }
        
        callback(null, response);
    }
    
        
    
    if (event.invocationSource === "FulfillmentCodeHook") {
        
        AWS.config.update({region: 'us-east-1'});

        // Create an SQS service object
        var sqs = new AWS.SQS({apiVersion: '2012-11-05'});

        var params = {
            DelaySeconds: 1,
            MessageBody: JSON.stringify(event.currentIntent.slots),
            QueueUrl: "https://sqs.us-east-1.amazonaws.com/231323952634/custQ"
        };

        
        sqs.sendMessage(params, function(err, data) {
            if (err) {
                console.log("Error", err);
            } else {
                console.log("Success", data.MessageId);
            }
        });
        
        response =  {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "PlainText",
                    "content": "Got it. Watch out for that text message"
                }
            }
        };
        
        //console.log(event.currentIntent.slots);
        callback(null, response);
    }
    
    return response;
};
