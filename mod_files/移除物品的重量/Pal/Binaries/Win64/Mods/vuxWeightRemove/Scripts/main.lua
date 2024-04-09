-- Tested on version 0.1.3.0
local vuxGameVersion = "0.1.3.0"
local vuxModVersion = "Weight Remove"
local vuxWeightMulti = 0
local vuxWeightBase = 0
local vuxCheckRestart = 0
local vuxCheckAcknowledge = 0

NotifyOnNewObject("/Script/Pal.PalStaticItemDataBase", function(vuxItem)
	if vuxItem.Weight then
		if vuxWeightMulti == 0 then
			vuxItem.Weight = 0
		elseif vuxWeightMulti > 0 then
			vuxItem.Weight = vuxItem.Weight / vuxWeightMulti
		end
	end
end)

RegisterHook("/Script/Engine.PlayerController:ServerAcknowledgePossession", function()
	if vuxCheckAcknowledge ~= 1 then
		local items = FindAllOf("PalStaticItemDataBase")
		if items then
			for _, item in ipairs(items) do
				if item.Weight then
					if vuxWeightMulti == 0 then
						item.Weight = 0
						vuxWeightBase = item.Weight
					elseif vuxWeightMulti > 0 then
						vuxWeightBase = item.Weight
						item.Weight = item.Weight / vuxWeightMulti
					end
				end
			end
		end
	end
	vuxCheckAcknowledge = 1
end)

RegisterHook("/Script/Engine.PlayerController:ClientRestart", function()
	if vuxCheckRestart ~= 1 then
		local items = FindAllOf("PalStaticItemDataBase")
		if items then
			for _, item in ipairs(items) do
				if item.Weight then
					if vuxWeightBase == item.Weight then
						if vuxWeightMulti == 0 then
							item.Weight = 0
						elseif vuxWeightMulti > 0 then
							item.Weight = item.Weight / vuxWeightMulti
						end
					end
				end
			end
		end
		print("Weight reduction mod version " .. vuxModVersion .. " loaded for game version " .. vuxGameVersion)
	end
	vuxCheckRestart = 1
end)