
local reactor = peripheral.wrap("back")
local modem = peripheral.wrap("top")
os.loadAPI("json")
local channel = 6942
modem.open(channel)
while true do
    local event, modemSide, senderChannel, replyChannel, rawData, senderDistance = os.pullEvent("modem_message")
    print("Received data on channel: "..senderChannel)
    local data = json.decode(rawData)

    if data.reactor_state == true then
        print("Setting reactor state to on.")
        reactor.setActive(true)
    else
        print("Setting reactor state to off.")
        reactor.setActive(false)
    end
    print("Getting reactor data...")
    local waste = reactor.getWasteAmount()
    local output = reactor.getEnergyProducedLastTick()
    local fuel = reactor.getFuelAmount()
    local fuel_temp = reactor.getFuelTemperature()
    local casing_temp = reactor.getCasingTemperature()
    local react = reactor.getFuelReactivity()
    local on = reactor.getActive()
    local energy = reactor.getEnergyStored()
    
    local sendTable = {
        name="reactor",
        channel=channel,
        reactor_state=on,
        waste=waste,
        output=output,
        fuel=fuel,
        fuel_temp=fuel_temp,
        casing_temp=casing_temp,
        reactivity=react,
        energy=energy
    }
    local sendString = json.encode(sendTable)
    print("Sending reactor data...")
    modem.transmit(channel, channel, sendString)
    print("Waiting for transmission data....")
end