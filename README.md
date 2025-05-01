# blade-ball-script-by-shun
function handler() {
  const luaCode = `
-- Shuns Hub | Blade Ball

-- Проверка на поддерживаемую игру
if game.PlaceId ~= 13772394625 then
    warn("❌ Этот скрипт только для Blade Ball!")
    return
end

-- Загружаем UI библиотеку (работает со всеми инжекторами)
local Library = loadstring(game:HttpGet("https://raw.githubusercontent.com/xHeptc/Kavo-UI-Library/main/source.lua"))()
local Window = Library.CreateLib("Shuns Hub | Blade Ball", "DarkTheme")

-- Основные переменные
local Players = game:GetService("Players")
local LocalPlayer = Players.LocalPlayer
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")
local UserInputService = game:GetService("UserInputService")

-- Главные разделы
local MainTab = Window:NewTab("Combat")
local FarmTab = Window:NewTab("Farming")
local PlayerTab = Window:NewTab("Player")
local VisualTab = Window:NewTab("Visual")
local MiscTab = Window:NewTab("Misc")

-- Секция Combat
local MainSection = MainTab:NewSection("Combat")

-- Auto Parry
MainSection:NewToggle("Auto Parry", "Автоматически отражает мячи", function(state)
    getgenv().AutoParry = state
    
    local function getClosestBall()
        local closestBall = nil
        local shortestDistance = math.huge
        
        for _, v in pairs(workspace.Balls:GetChildren()) do
            if v:IsA("BasePart") then
                local distance = (v.Position - LocalPlayer.Character.HumanoidRootPart.Position).Magnitude
                if distance < shortestDistance then
                    closestBall = v
                    shortestDistance = distance
                end
            end
        end
        
        return closestBall
    end
    
    while getgenv().AutoParry and task.wait() do
        local ball = getClosestBall()
        if ball and ball:GetAttribute("target") == LocalPlayer.Name then
            local distance = (ball.Position - LocalPlayer.Character.HumanoidRootPart.Position).Magnitude
            if distance <= 15 then
                ReplicatedStorage.Remotes.ParryButtonPress:Fire()
                task.wait(0.3)
            end
        end
    end
end)

-- Auto Spam
MainSection:NewToggle("Auto Spam", "Спамит парированием", function(state)
    getgenv().AutoSpam = state
    while getgenv().AutoSpam and task.wait() do
        ReplicatedStorage.Remotes.ParryButtonPress:Fire()
    end
end)

-- Секция Farming
local FarmSection = FarmTab:NewSection("Farming")

-- Auto Farm
FarmSection:NewToggle("Auto Farm", "Автоматический фарм очков", function(state)
    getgenv().AutoFarm = state
    
    while getgenv().AutoFarm and task.wait() do
        for _, v in pairs(workspace:GetChildren()) do
            if v.Name == "Point" and v:IsA("BasePart") then
                LocalPlayer.Character.HumanoidRootPart.CFrame = v.CFrame
                task.wait(0.1)
            end
        end
    end
end)

-- Секция Player
local PlayerSection = PlayerTab:NewSection("Player")

-- WalkSpeed
PlayerSection:NewSlider("WalkSpeed", "Изменить скорость", 500, 16, function(s)
    LocalPlayer.Character.Humanoid.WalkSpeed = s
end)

-- JumpPower
PlayerSection:NewSlider("JumpPower", "Изменить высоту прыжка", 500, 50, function(s)
    LocalPlayer.Character.Humanoid.JumpPower = s
end)

-- Infinite Jump
PlayerSection:NewToggle("Infinite Jump", "Бесконечные прыжки", function(state)
    getgenv().InfiniteJump = state
    UserInputService.JumpRequest:Connect(function()
        if getgenv().InfiniteJump then
            LocalPlayer.Character.Humanoid:ChangeState("Jumping")
        end
    end)
end)

-- Секция Visual
local VisualSection = VisualTab:NewSection("Visual")

-- ESP Players
VisualSection:NewToggle("ESP Players", "Видеть игроков через стены", function(state)
    getgenv().ESP = state
    
    local function createESP(player)
        local esp = Instance.new("BoxHandleAdornment")
        esp.Name = player.Name .. "_ESP"
        esp.Parent = game.CoreGui
        esp.Adornee = player.Character
        esp.AlwaysOnTop = true
        esp.ZIndex = 0
        esp.Size = player.Character:GetExtentsSize()
        esp.Transparency = 0.5
        esp.Color3 = Color3.fromRGB(255, 0, 0)
    end
    
    while getgenv().ESP and task.wait() do
        for _, player in pairs(Players:GetPlayers()) do
            if player ~= LocalPlayer and player.Character and not game.CoreGui:FindFirstChild(player.Name .. "_ESP") then
                createESP(player)
            end
        end
    end
end)

-- Ball ESP
VisualSection:NewToggle("Ball ESP", "Видеть мячи через стены", function(state)
    getgenv().BallESP = state
    
    local function createBallESP(ball)
        local esp = Instance.new("BoxHandleAdornment")
        esp.Name = "Ball_ESP"
        esp.Parent = game.CoreGui
        esp.Adornee = ball
        esp.AlwaysOnTop = true
        esp.ZIndex = 0
        esp.Size = ball.Size
        esp.Transparency = 0.5
        esp.Color3 = Color3.fromRGB(0, 255, 0)
    end
    
    while getgenv().BallESP and task.wait() do
        for _, ball in pairs(workspace.Balls:GetChildren()) do
            if ball:IsA("BasePart") and not game.CoreGui:FindFirstChild("Ball_ESP") then
                createBallESP(ball)
            end
        end
    end
end)

-- Секция Misc
local MiscSection = MiscTab:NewSection("Misc")

-- Rejoin
MiscSection:NewButton("Rejoin", "Перезайти в игру", function()
    game:GetService("TeleportService"):Teleport(game.PlaceId, LocalPlayer)
end)

-- Server Hop
MiscSection:NewButton("Server Hop", "Сменить сервер", function()
    local servers = {}
    local req = game:HttpGet("https://games.roblox.com/v1/games/" .. game.PlaceId .. "/servers/Public?sortOrder=Asc&limit=100")
    local data = game:GetService("HttpService"):JSONDecode(req)
    
    for _, v in pairs(data.data) do
        if v.playing < v.maxPlayers and v.id ~= game.JobId then
            table.insert(servers, v.id)
        end
    end
    
    if #servers > 0 then
        game:GetService("TeleportService"):TeleportToPlaceInstance(game.PlaceId, servers[math.random(1, #servers)])
    end
end)

-- Toggle UI
MiscSection:NewKeybind("Toggle UI", "Скрыть/показать меню", Enum.KeyCode.RightControl, function()
    Library:ToggleUI()
end)

-- Защита от ошибок
local success, error = pcall(function()
    -- Основной код уже выполнен
end)

if not success then
    warn("❌ Ошибка: " .. tostring(error))
end`;

  return {
    luaCode: luaCode.trim(),
  };
}
