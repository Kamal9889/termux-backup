#!/bin/bash
clear
echo "------------------------------------------------"
echo "    Master Converter: Video, Audio & Image      "
echo "------------------------------------------------"

read -p "Enter File Name (e.g., file.mp4 or photo.jpg): " input

if [ ! -f "$input" ]; then
    echo "Error: '$input' file not found!"
    exit 1
fi

# Get video dimensions for scaling
width=$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of default=nw=1:nk=1 "$input" 2>/dev/null)
height=$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of default=nw=1:nk=1 "$input" 2>/dev/null)

if [ "$width" -lt "$height" ] 2>/dev/null; then
    is_vertical=true
else
    is_vertical=false
fi

echo -e "\n========= VIDEO RESOLUTIONS ========="
echo "1.  8K Ultra HD    (Best for large screens)"
echo "2.  4K Ultra HD    (Crisp High Quality)"
echo "3.  2K Quad HD     (Cinematic High Res)"
echo "4.  1080p Full HD  (Standard High Quality)"
echo "5.  720p HD        (Good Quality, Small Size)"
echo "6.  480p SD        (Standard for Mobile)"
echo "7.  360p Medium    (Save Data, Fair Quality)"
echo "8.  240p Small     (Low Quality, Very Small)"
echo "9.  144p Very Low  (Minimum Quality)"
echo "10. 96p Ultra Low  (Smallest - Very Blurry)"
echo "11. HEVC (H.265)   (720p - Half File Size)"

echo -e "\n========= AUDIO FORMATS ========="
echo "12. 320k MP3       (Best Music Quality)"
echo "13. 192k MP3       (High Quality Audio)"
echo "14. 128k MP3       (Standard Quality)"
echo "15. 64k  MP3       (Good for Voice/Lecture)"
echo "16. 32k  MP3       (Small File Size)"
echo "17. 24k  MP3       (Very Small - Low Quality)"
echo "18. 16k  MP3       (Call Recorder Quality)"
echo "19. 8k   MP3       (Smallest - Voice Only)"
echo "20. OPUS 16k       (Best Smallest - Clear Voice)"
echo "21. AAC (M4A)      (High Quality for Mobile)"
echo "22. WAV Lossless   (Original Quality - Large)"

echo -e "\n========= IMAGE OPTIONS ========="
echo "23. WebP High Q    (Modern Tech, Best Size)"
echo "24. WebP Low Q     (Smallest Photo Size)"
echo "25. JPG Medium Q   (Standard Compression)"
echo "26. Resize 50%     (Half Dimensions)"
echo "27. Resize 25%     (Quarter Dimensions)"

echo "------------------------------------------------"
read -p "Select an option (1-27): " choice

case $choice in
    1) p="4320"; label="8K"; ext="mp4"; codec="libx264" ;;
    2) p="2160"; label="4K"; ext="mp4"; codec="libx264" ;;
    3) p="1440"; label="2K"; ext="mp4"; codec="libx264" ;;
    4) p="1080"; label="1080p"; ext="mp4"; codec="libx264" ;;
    5) p="720"; label="720p"; ext="mp4"; codec="libx264" ;;
    6) p="480"; label="480p"; ext="mp4"; codec="libx264" ;;
    7) p="360"; label="360p"; ext="mp4"; codec="libx264" ;;
    8) p="240"; label="240p"; ext="mp4"; codec="libx264" ;;
    9) p="144"; label="144p"; ext="mp4"; codec="libx264" ;;
    10) p="96"; label="96p_UltraLow"; ext="mp4"; codec="libx264" ;;
    11) p="720"; label="HEVC_720p"; ext="mkv"; codec="libx265" ;;
    12) br="320k"; label="320kbps"; ext="mp3" ;;
    13) br="192k"; label="192kbps"; ext="mp3" ;;
    14) br="128k"; label="128kbps"; ext="mp3" ;;
    15) br="64k"; label="64kbps"; ext="mp3" ;;
    16) br="32k"; label="32kbps"; ext="mp3" ;;
    17) br="24k"; label="24kbps"; ext="mp3" ;;
    18) br="16k"; label="16kbps"; ext="mp3" ;;
    19) br="8k"; label="8kbps"; ext="mp3" ;;
    20) br="16k"; label="Opus_Ultra"; ext="opus" ;;
    21) br="256k"; label="AAC_HQ"; ext="m4a" ;;
    22) label="Lossless"; ext="wav" ;;
    23) q="75"; label="High_WebP"; ext="webp" ;;
    24) q="30"; label="Small_WebP"; ext="webp" ;;
    25) q="50"; label="Med_JPG"; ext="jpg" ;;
    26) r="50%"; label="Resize_50"; ext="${input##*.}" ;;
    27) r="25%"; label="Resize_25"; ext="${input##*.}" ;;
    *) echo "Invalid Selection!"; exit 1 ;;
esac

output="${input%.*}_${label}.${ext}"

echo -e "\nProcessing... Please wait.\n"

if [ $choice -le 11 ]; then
    # Video Conversion Logic
    if [ "$is_vertical" = true ]; then
        scale_filter="scale='trunc(oh*a/2)*2:$p'"
    else
        scale_filter="scale='$p:trunc(ow/a/2)*2'"
    fi
    ffmpeg -i "$input" -vf "$scale_filter" -c:v $codec -crf 25 -preset faster -c:a aac -b:a 64k "$output"
elif [ $choice -ge 12 ] && [ $choice -le 22 ]; then
    # Audio Conversion Logic
    if [ $choice -eq 20 ]; then
        ffmpeg -i "$input" -vn -c:a libopus -b:a 16k -ac 1 "$output"
    elif [ $choice -eq 22 ]; then
        ffmpeg -i "$input" -vn "$output"
    else
        ffmpeg -i "$input" -vn -ab "$br" -ac 1 "$output"
    fi
elif [ $choice -le 25 ]; then
    # Image Compression (Quality)
    magick "$input" -quality $q "$output"
else
    # Image Resize (Dimensions)
    magick "$input" -resize $r "$output"
fi

if [ $? -eq 0 ]; then
    echo -e "\n------------------------------------------------"
    echo "Success! Saved as: $output"
    echo "------------------------------------------------"
else
    echo -e "\nSorry! Processing Failed."
fi
