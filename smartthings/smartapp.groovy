/**
 *  GaragePi App
 *
 *  Copyright 2018 pimpybra.com
 *
 */
definition(
    name: "GaragePi App",
    namespace: "pimpybra",
    author: "pimpybra.com",
    description: "Allows monitoring of the garage pi device",
    category: "My Apps",
    iconUrl: "https://s3.amazonaws.com/smartapp-icons/Convenience/Cat-Convenience.png",
    iconX2Url: "https://s3.amazonaws.com/smartapp-icons/Convenience/Cat-Convenience@2x.png",
    iconX3Url: "https://s3.amazonaws.com/smartapp-icons/Convenience/Cat-Convenience@2x.png")


preferences {
	section("Title") {
		// TODO: put inputs here
	}
}

def installed() {
	log.debug "Installed with settings: ${settings}"

	initialize()
}

def updated() {
	log.debug "Updated with settings: ${settings}"

	unsubscribe()
	initialize()
}

def initialize() {
	log.debug "Initialized..."
	runEvery5Minutes(pingPi)
}

// parse events into attributes
def parse(String description) {
	log.debug "Parsing '${description}'"
    
    def paramMap = [:]
    
    def params = description.split(',').each { 
        def key = it.split(':')[0].trim()
        def val = it.split(':')[1].trim()
        // log.debug("key: !${key}! val: !${val}!")
        paramMap[key] = val
    }
    // log.debug "params: ${params}"
    // log.debug "paramMap: ${paramMap}"
    def bodyText = new String(paramMap['body'].decodeBase64())

   
    // sendEvent(name: "door", value: "closing")
	// TODO: handle 'door' attribute
	// TODO: handle 'motion' attribute

}


def pingPi() {
    def result = new physicalgraph.device.HubAction(
        method: "GET",
        path: "/ping?test=1",
        headers: [
            HOST: "192.168.0.120:81"
        ]
    )    
    
    sendHubCommand(result)
//    sendPushMessage("TEST PUSH")
    log.debug "ping result: ${result}"
    log.debug "-------"
    log.debug result.toString()
    log.debug "======="
    return result
}

