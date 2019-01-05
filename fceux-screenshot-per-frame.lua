-- fceux script that collect a screenshot per frame

emu.speedmode("normal") 

outDir = "C:\\mario" -- set this!

function after_frame()
    count = emu.framecount()
    gui.savescreenshotas(string.format("%s\\%d.png", outDir, count))
end

os.execute("mkdir " .. outDir)

emu.registerafter(after_frame)

while true do
    emu.frameadvance()
end 