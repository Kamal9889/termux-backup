#!/bin/bash

# ২. এলাইয়াস ডেসক্রিপশন
declare -A desc
desc[con]="Audio/Video/Photos Converter"
desc[pdl]="Photos/Video Downloader"
desc[mpvv]="Open URL in Youtube"
desc[aedit]="Configure Bash Settings"
desc[aset]="Apply System Changes"
desc[vpn]="Tor Proxy Toggle"
desc[myip]="Check Local & Tor IP"
desc[td]="Aria2 Torrent High-Speed Download"
desc[file]="Quick File Manager"
desc[yarn]="Grey Yarn Inventory Search"
desc[audio]="Stream YT Music (Audio)"
desc[coin]="Live Crypto Market"
desc[upload]="Sync Scripts to Cloud To Github"
desc[yts]="Youtube Audio Search"
desc[yd]="Search Yarn Dyeing Yarn Stock"
desc[collar]="Collar/Cuff Weight Dashboard"

# ৩. লোকেশন ট্র্যাকিং
ip_info=$(curl -s http://ip-api.com/json/)
local_ip=$(echo "$ip_info" | grep -oP '(?<="query":")[^"]*' || echo "Offline")
city=$(echo "$ip_info" | grep -oP '(?<="city":")[^"]*' || echo "Unknown")
country=$(echo "$ip_info" | grep -oP '(?<="country":")[^"]*' || echo "")
tor_ip=$(torsocks curl -s ifconfig.me 2>/dev/null)

# ৪. ড্যাশবোর্ড হেডার ডিজাইন
echo -e "\e[1;36m┌────────────────────────────────────────────────────────┐\e[0m"
echo -e "\e[1;36m│\e[0m \e[1;32mNet IP:\e[0m $local_ip \e[1;33m($city, $country)\e[0m"
if [ -z "$tor_ip" ]; then
    echo -e "\e[1;36m│\e[0m \e[1;31mTor Status: Disconnected ❌\e[0m                          \e[1;36m│\e[0m"
else
    tor_city=$(torsocks curl -s http://ip-api.com/line/?fields=city 2>/dev/null)
    echo -e "\e[1;36m│\e[0m \e[1;32mTor Status: Active ✅ \e[1;35m(IP: $tor_ip - $tor_city)\e[0m \e[1;36m│\e[0m"
fi
echo -e "\e[1;36m└────────────────────────────────────────────────────────┘\e[0m"

# ৫. মেনু প্রদর্শন
# .bashrc থেকে এলাইয়াসগুলো খুঁজে বের করা
mapfile -t alias_names < <(grep "^alias " ~/.bashrc | cut -d' ' -f2 | cut -d'=' -f1)

for i in "${!alias_names[@]}"; do
    name="${alias_names[$i]}"
    info="${desc[$name]}"
    [ -z "$info" ] && info="No description"
    printf "\e[1;32m %2d)\e[0m \e[1;37m%-8s\e[0m \e[1;34m➜\e[0m \e[1;30m%s\e[0m\n" "$((i+1))" "$name" "$info"
done

echo -e "\n\e[1;31m  q)\e[0m Exit to Terminal"
echo -e "\e[1;36m──────────────────────────────────────────────────────────\e[0m"

read -p " ❯❯❯ Select Number: " choice

if [[ "$choice" == "q" ]]; then
    clear
    exit
elif [[ "$choice" -ge 1 && "$choice" -le "${#alias_names[@]}" ]]; then
    selected_alias="${alias_names[$((choice-1))]}"
    echo -e "\n\e[1;34m[Running]:\e[0m $selected_alias\n"
    
    # ৬. এই লাইনটিই আপনার সমস্যার মেইন সমাধান
    # এটি ইন্টারঅ্যাক্টিভ মোডে কমান্ডটি রান করবে যাতে এলাইয়াসগুলো কাজ করে
    bash -i -c "$selected_alias"
else
    echo -e "\e[1;31mInvalid Selection!\e[0m"; sleep 1; bash "$0"
fi

