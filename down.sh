#!/bin/bash

# আপনার গিটহাব ইউজারনেম এবং রিপোজিটরি নাম
REPO="Kamal9889/tg-downloader"
WORKFLOW="main.yml"

# লিঙ্ক দেওয়া হয়েছে কি না চেক করা
if [ -z "$1" ]; then
    echo "সঠিক ব্যবহার: down [লিঙ্ক]"
    echo "উদাহরণ: down https://unsplash.com/photos/xyz"
    exit 1
fi

echo "গিটহাব অ্যাকশন সচল করা হচ্ছে..."

# গিটহাব ওয়ার্কফ্লো রান করার কমান্ড
gh workflow run $WORKFLOW --repo $REPO -f url="$1"

if [ $? -eq 0 ]; then
    echo "অভিনন্দন! গিটহাব সার্ভারে ডাউনলোড শুরু হয়েছে।"
    echo "আপনার টেলিগ্রাম চ্যাট চেক করুন।"
else
    echo "কিছু একটা সমস্যা হয়েছে! দয়া করে ইন্টারনেট বা গিটহাব লগইন চেক করুন।"
fi

