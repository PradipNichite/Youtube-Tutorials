#aws lambda code for 
#How to Make a Chatbot Using Amazon Lex and AWS Lambda (Python) | Conversational AI Part 2
# https://youtu.be/W6T-RFei6SY
import json
import datetime
import time

def validate(slots):

    valid_cities = ['mumbai','delhi','banglore','hyderabad']
    
    if not slots['Location']:
        print("Inside Empty Location")
        return {
        'isValid': False,
        'violatedSlot': 'Location'
        }        
        
    if slots['Location']['value']['originalValue'].lower() not in  valid_cities:
        
        print("Not Valide location")
        
        return {
        'isValid': False,
        'violatedSlot': 'Location',
        'message': 'We currently  support only {} as a valid destination.?'.format(", ".join(valid_cities))
        }
        
    if not slots['CheckInDate']:
        
        return {
        'isValid': False,
        'violatedSlot': 'CheckInDate',
    }
        
    if not slots['Nights']:
        return {
        'isValid': False,
        'violatedSlot': 'Nights'
    }
        
    if not slots['RoomType']:
        return {
        'isValid': False,
        'violatedSlot': 'RoomType'
    }

    return {'isValid': True}
    
def lambda_handler(event, context):
    
    # print(event)
    slots = event['sessionState']['intent']['slots']
    intent = event['sessionState']['intent']['name']
    print(event['invocationSource'])
    print(slots)
    print(intent)
    validation_result = validate(event['sessionState']['intent']['slots'])
    
    if event['invocationSource'] == 'DialogCodeHook':
        if not validation_result['isValid']:
            
            if 'message' in validation_result:
            
                response = {
                "sessionState": {
                    "dialogAction": {
                        'slotToElicit':validation_result['violatedSlot'],
                        "type": "ElicitSlot"
                    },
                    "intent": {
                        'name':intent,
                        'slots': slots
                        
                        }
                },
                "messages": [
                    {
                        "contentType": "PlainText",
                        "content": validation_result['message']
                    }
                ]
               } 
            else:
                response = {
                "sessionState": {
                    "dialogAction": {
                        'slotToElicit':validation_result['violatedSlot'],
                        "type": "ElicitSlot"
                    },
                    "intent": {
                        'name':intent,
                        'slots': slots
                        
                        }
                }
               } 
    
            return response
           
        else:
            response = {
            "sessionState": {
                "dialogAction": {
                    "type": "Delegate"
                },
                "intent": {
                    'name':intent,
                    'slots': slots
                    
                    }
        
            }
        }
            return response
    
    if event['invocationSource'] == 'FulfillmentCodeHook':
        
        # Add order in Database
        
        response = {
        "sessionState": {
            "dialogAction": {
                "type": "Close"
            },
            "intent": {
                'name':intent,
                'slots': slots,
                'state':'Fulfilled'
                
                }
    
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": "Thanks, I have placed your reservation"
            }
        ]
    }
            
        return response