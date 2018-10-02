/**
 *  GaragePi
 *
 *  Copyright 2016 pimpybra.com
 *
 */
metadata {
	definition (name: "GaragePi", namespace: "pimpybra", author: "pimpybra.com") {
		capability "Door Control"
		capability "Garage Door Control"
//		capability "Motion Sensor"
		capability "Notification"
		capability "Sensor" 
//		capability "Polling"
	}

	simulator {
		// TODO: define status and reply messages here
	}

	tiles {
        standardTile("button", "device.door", width: 3, height: 2, canChangeIcon: false) {
			// state "unknown", label: 'unknown', icon: "st.doors.garage.garage-open", backgroundColor: "#ffffff" //, action: "close", nextState: "closing"
			state "open", label: 'Open', icon: "st.doors.garage.garage-open", backgroundColor: "#ffffff", action: "close", nextState: "closed"
			state "closed", label: 'Closed', icon: "st.doors.garage.garage-closed", backgroundColor: "#79b821", action: "open", nextState: "open"
			// state "opening", label: 'Opening...', icon: "st.doors.garage.garage-opening", backgroundColor: "#ffffff" //, action: "stoddddpdoor" //, nextState: "open"
			// state "closing", label: 'Closing...', icon: "st.doors.garage.garage-closing", backgroundColor: "#ffffff"//, action: "stopdoor" //, nextState: "closed"
			// state "stopped", label: 'Stopped', icon: "st.doors.garage.garage-closing", backgroundColor: "#ffffff", action: "stopdoor", nextState: "open"
		}
	}
}

// parse events into attributes
def parse(String description) {
	log.debug "Parsing '${description}'"
    
    def paramMap = [:]
    
    def params = description.split(',').each { 
    	def key = it.split(':')[0].trim()
        def val = it.split(':')[1].trim()
 //       log.debug("key: !${key}! val: !${val}!")
    	paramMap[key] = val
    }
//    log.debug "params: ${params}"
   //log.debug "paramMap: ${paramMap}"
   def bodyText = new String(paramMap['body'].decodeBase64())
   //log.debug "body: ${bodyText}"
   
   //sendEvent(name: "door", value: "closing")
	// TODO: handle 'door' attribute
	// TODO: handle 'motion' attribute

}

def lolwat(String derps) {
  log.debug "lolwat ${derps}"
}

def triggerDoor() {
    def result = new physicalgraph.device.HubAction(
        method: "POST",
        path: "/trigger",
        headers: [
            HOST: "192.168.0.120:81"
        ]
    )    
    
    log.debug "trigger result: ${result}"
    return result
}

// handle commands
def open() {
	log.debug "Executing 'open'"
    sendEvent(name: "door", value: "opening")
	
    triggerDoor()
}

def finishOpening() {
    sendEvent(name: "door", value: "open")
    sendEvent(name: "contact", value: "open")
}

def stopdoor() {
	log.debug "STOP DOOR CALLED"
}

def close() {
	log.debug "Executing 'close'"
    
    triggerDoor()
}

def deviceNotification(String msg) {
	log.debug "Executing 'deviceNotification' $msg"
	// TODO: handle 'deviceNotification' command
}

def poll() {
	log.debug "POLLING HERE"
}
