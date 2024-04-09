local palConfig = require "config"

print(palConfig.palRedColorWrapperFront .. palConfig.palModName .. "Mod Version " .. palConfig.palModVersion .. " - Working as of game version " .. palConfig.palGameVersion .. palConfig.palRedColorWrapperBack)

NotifyOnNewObject("/Script/Pal.PalWeaponBase", function(PalWeaponBase)
    PalWeaponBase.CoolDownTime = palConfig.CoolDownTime
end)

-- Made by pleby
-- FYI I got no fucking clue what im doing, but aye it works.