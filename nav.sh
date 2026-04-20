#!/bin/bash
shopt -s expand_aliases
source ~/.bashrc

# Global Clipboard file path
CLIP_FILE="/data/data/com.termux/files/usr/tmp/.clip_path"
MODE_FILE="/data/data/com.termux/files/usr/tmp/.clip_mode"

navigate() {
    while true; do
        clear
        # স্টোরেজ ডাটা (Full Info with 3 Decimals)
        total_kb=$(df . | awk 'NR==2 {print $2}')
        used_kb=$(df . | awk 'NR==2 {print $3}')
        free_kb=$(df . | awk 'NR==2 {print $4}')
        
        total_gb=$(echo "scale=3; $total_kb/1048576" | bc)
        used_gb=$(echo "scale=3; $used_kb/1048576" | bc)
        free_gb=$(echo "scale=3; $free_kb/1048576" | bc)
        perc=$(df . | awk 'NR==2 {print $5}' | sed 's/%//')

        # প্রগ্রেস বার লজিক
        bar_size=20
        filled=$(( perc * bar_size / 100 ))
        empty=$(( bar_size - filled ))
        bar=$(printf "%${filled}s" | tr ' ' '█')
        spacer=$(printf "%${empty}s" | tr ' ' '░')

        echo -e "\e[1;36mPath:\e[0m $(pwd)"
        echo -e "\e[1;33mStorage: $total_gb GB Total | $used_gb GB Used | $free_gb GB Free\e[0m"
        echo -e "\e[1;32mUsage: [\e[1;31m$bar\e[1;37m$spacer\e[1;32m] $perc%\e[0m"
        echo "--------------------------------------------------------"
        echo -e "\e[1;32mn)NEW\e[0m \e[1;33mr)REN\e[0m \e[1;31md)DEL\e[0m \e[1;35me)EDIT\e[0m \e[1;36mc)COPY\e[0m \e[1;34mx)CUT\e[0m \e[1;32mp)PASTE\e[0m"
        echo -e "\e[1;31m0)BACK\e[0m  \e[1;33mm)MENU\e[0m  \e[1;31mq)EXIT\e[0m"
        
        if [ -f "$CLIP_FILE" ]; then
            C_FILE=$(cat "$CLIP_FILE")
            C_MODE=$(cat "$MODE_FILE")
            echo -e "\e[1;43;30m Clipboard: $(basename "$C_FILE") ($C_MODE) \e[0m"
        fi
        echo "--------------------------------------------------------"

        shopt -s dotglob
        items=( * )
        i=1
        for item in "${items[@]}"; do
            if [ -d "$item" ]; then
                count=$(ls -1A "$item" 2>/dev/null | wc -l)
                echo -e "$i) \e[1;34m[DIR]\e[0m  $item \e[0;37m($count)\e[0m"
            elif [ -f "$item" ]; then
                size=$(du -h "$item" 2>/dev/null | cut -f1)
                echo -e "$i) \e[1;32m[FILE]\e[0m $item \e[1;33m($size)\e[0m"
            fi
            ((i++))
        done

        echo "--------------------------------------------------------"
        read -p "Select: " input

        case $input in
            q) exit ;;
            m) break ;;
            0) cd .. ;;
            n) read -p "Name: " f; mkdir -p "$f" ;;
            r) read -p "Num: " n; read -p "New Name: " nn; mv "${items[$((n-1))]}" "$nn" ;;
            d) read -p "Num: " n; rm -rf "${items[$((n-1))]}" ;;
            e) read -p "Num: " n; nano "${items[$((n-1))]}" ;;
            c) read -p "Copy Num: " n; echo "$(pwd)/${items[$((n-1))]}" > "$CLIP_FILE"; echo "COPY" > "$MODE_FILE"; echo "Copied."; sleep 1 ;;
            x) read -p "Cut Num: " n; echo "$(pwd)/${items[$((n-1))]}" > "$CLIP_FILE"; echo "MOVE" > "$MODE_FILE"; echo "Cut."; sleep 1 ;;
            p) 
                if [ ! -f "$CLIP_FILE" ]; then echo "Empty!"; sleep 1;
                else
                    SRC=$(cat "$CLIP_FILE"); M=$(cat "$MODE_FILE")
                    if [ "$M" == "COPY" ]; then
                        echo "Copying with progress..."
                        rsync -ah --progress "$SRC" .
                    else
                        echo "Moving..."
                        mv "$SRC" .
                        rm "$CLIP_FILE"
                    fi
                    echo "Done. Press Enter..."; read
                fi ;;
            [0-9]*)
                selected="${items[$((input-1))]}"
                if [ -d "$selected" ]; then cd "$selected"
                else
                    ext="${selected##*.}"
                    ext=$(echo "$ext" | tr '[:upper:]' '[:lower:]')
                    if [[ "$ext" == "mp4" || "$ext" == "mkv" || "$ext" == "webm" ]]; then termux-open "$selected"
                    elif [[ "$ext" == "mp3" || "$ext" == "m4a" ]]; then mpv "$selected"; echo "Press Enter..."; read
                    else termux-open "$selected"; fi
                fi ;;
            *) eval "$input"; echo "Done."; read ;;
        esac
    done
}

# প্রয়োজনীয় টুলস চেক
if ! command -v rsync &> /dev/null; then pkg install rsync -y; fi
if ! command -v bc &> /dev/null; then pkg install bc -y; fi

while true; do
    clear
    echo -e "\e[1;33mSelect Storage:\e[0m"
    echo "1) Internal (/sdcard)"
    echo "2) SD Card (5499-8E58)"
    echo "q) Exit"
    read -p ">> " choice
    if [[ "$choice" == "1" ]]; then cd /sdcard && navigate
    elif [[ "$choice" == "2" ]]; then cd /storage/5499-8E58 && navigate
    elif [[ "$choice" == "q" ]]; then exit
    fi
done
