-- this will loop and run in the background
-- and ping the server
local modem = perpheral.wrap("top")
local lastString = ""
local url = ""
local waitTime = 60 -- in seconds
os.loadAPI("json")
while true do
    print("Checking for new data....")
    local rawData = http.get(url).readAll()
    if rawData!=lastString then
        print("New data found, enumerating devices....")
        local obj = json.decode(rawData)
        for _, device in pairs(obj) do
            print("Updating device " .. device.name)
            modem.open(device.channel)
            modem.transmit(device.channel, device.channel, json.encode(device.data))
            if device.post then
                print("Getting data off of device...")
                local event, modemSide, senderChannel, replyChannel, rawData, senderDistance = os.pullEvent("modem_message")
                http.post(url, rawData)
                print("Data sent to server.")
            end
            modem.close()
        end
        print("Enumeration complete. Waiting....")
    else
        print("No changes found. Waiting....")
    end
    sleep(waitTime)
end