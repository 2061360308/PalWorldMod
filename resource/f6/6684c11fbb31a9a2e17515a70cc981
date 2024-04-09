-- Author: yakuzadeso

RegisterHook("/Script/Pal.PalBossBattleSequencer:SetBossCharacter", function(Context, BossActor)
	PalStaticCharacterParameterComponents = FindAllOf("PalStaticCharacterParameterComponent")

	for _, PalStaticCharacterParameterComponent in ipairs(PalStaticCharacterParameterComponents) do
		if PalStaticCharacterParameterComponent.IsPal == true and
			PalStaticCharacterParameterComponent.IsBoss_Database == true and
			PalStaticCharacterParameterComponent.IsTowerBoss_Database == true then
			PalStaticCharacterParameterComponent.IsUncapturable = false
		end
	end
end)
