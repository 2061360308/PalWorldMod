local vuxConfig = require "config"
NotifyOnNewObject("/Script/Pal.PalGameSetting", function(vuxPalGameSetting)
	vuxPalGameSetting.PalBoxReviveTime = vuxConfig.vuxReviveTimer
	print("Pal revive timer set to " .. vuxConfig.vuxReviveTimer)
end)


RegisterHook("/Script/Engine.PlayerController:ServerAcknowledgePossession", function()
	if vuxConfig.vuxCheckAcknowledge ~= 1 then
		local items = FindAllOf("PalGameSetting")
	    if items then
	        for _, item in ipairs(items) do
	            item.PalBoxReviveTime = vuxConfig.vuxReviveTimer
	        end
	    end
	    print("Pal revive timer set to " .. vuxConfig.vuxReviveTimer)
	end
	vuxConfig.vuxCheckAcknowledge = 1
end)

RegisterHook("/Script/Engine.PlayerController:ClientRestart", function()
	if vuxConfig.vuxCheckRestart ~= 1 then
		local items = FindAllOf("PalGameSetting")
	    if items then
	        for _, item in ipairs(items) do
	            item.PalBoxReviveTime = vuxConfig.vuxReviveTimer
	        end
	    end
    	print("Pal revive timer mod version " .. vuxConfig.vuxModVersion .. " loaded for game version " .. vuxConfig.vuxGameVersion)
    end
	vuxConfig.vuxCheckRestart = 1
end)