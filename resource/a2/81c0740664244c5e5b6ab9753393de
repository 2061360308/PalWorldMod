local vuxConfig = require "config"

NotifyOnNewObject("/Script/Pal.PalGameSetting", function(vuxPalGameSetting)
	vuxPalGameSetting.DefaultMaxInventoryWeight = vuxConfig.vuxMaxWeight
	vuxPalGameSetting.AddMaxInventoryWeightPerStatusPoint = vuxConfig.vuxWeightPerSP
	print("Default max weight set to " .. vuxConfig.vuxMaxWeight)
	print("Weight per SP set to " .. vuxConfig.vuxWeightPerSP)
end)

RegisterHook("/Script/Engine.PlayerController:ServerAcknowledgePossession", function()
	if vuxConfig.vuxCheckAcknowledge ~= 1 then
		local items = FindAllOf("PalGameSetting")
	    if items then
	        for _, item in ipairs(items) do
	            item.DefaultMaxInventoryWeight = vuxConfig.vuxMaxWeight
	            item.AddMaxInventoryWeightPerStatusPoint = vuxConfig.vuxWeightPerSP
	        end
	    end
        print("Default max weight set to " .. vuxConfig.vuxMaxWeight)
        print("Weight per SP set to " .. vuxConfig.vuxWeightPerSP)
	end
	vuxConfig.vuxCheckAcknowledge = 1
end)

RegisterHook("/Script/Engine.PlayerController:ClientRestart", function()
	if vuxConfig.vuxCheckRestart ~= 1 then
		local items = FindAllOf("PalGameSetting")
	    if items then
	        for _, item in ipairs(items) do
	            item.DefaultMaxInventoryWeight = vuxConfig.vuxMaxWeight
	            item.AddMaxInventoryWeightPerStatusPoint = vuxConfig.vuxWeightPerSP
	        end
		print("Default max weight set to " .. vuxConfig.vuxMaxWeight)
		print("Weight per SP set to " .. vuxConfig.vuxWeightPerSP)
	    end
    	print("Weight capacity mod version " .. vuxConfig.vuxModVersion .. " loaded for game version " .. vuxConfig.vuxGameVersion)
    end
	vuxConfig.vuxCheckRestart = 1
end)