-- Pastebin w5Dve5Rz
-- Really helps with setup
print("Enter url to download from:")
local url = read()
print("Enter filename to save to:")
local name = read()
print("Downloading...")
local request, err = http.get(url)
local contents = request.readAll()
request.close()
print("Saving to file...")
local file = fs.open(name, "w")
file.write(contents)
file.close()
print("Done.")