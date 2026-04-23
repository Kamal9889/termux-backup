import os
import subprocess
import sys

def get_yt_results(query, start_index, count=10):
    # নির্দিষ্ট রেঞ্জ অনুযায়ী (যেমন ১-১০, তারপর ১১-২০) সার্চ করা
    search_range = f"ytsearch{start_index + count - 1}:{query}"
    cmd = ['yt-dlp', search_range, '--get-id', '--get-title', '--flat-playlist', 
           '--playlist-start', str(start_index), '--playlist-end', str(start_index + count - 1)]
    
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, _ = process.communicate()
    lines = stdout.strip().split('\n')
    
    results = []
    for i in range(0, len(lines), 2):
        if i+1 < len(lines):
            results.append({'title': lines[i], 'id': lines[i+1]})
    return results

def main():
    try:
        os.system('clear')
        print("\033[1;32m=== Fast YouTube Search (10 results per load) ===\033[0m")
        query = input("Search for: ")
        if not query: return

        current_playlist = []
        start_from = 1
        page_size = 10

        while True:
            print(f"\033[1;33mLoading results {start_from} to {start_from + page_size - 1}...\033[0m")
            new_results = get_yt_results(query, start_from, page_size)
            
            if not new_results:
                print("No more results found.")
                break
            
            current_playlist.extend(new_results)
            
            # fzf এর জন্য শুধু বর্তমান পেজের রেজাল্ট সাজানো
            fzf_input = ""
            current_page_items = current_playlist[start_from-1:]
            for i, res in enumerate(current_page_items):
                fzf_input += f"{str(start_from + i).zfill(2)}. {res['title']}\n"
            
            fzf_input += ">> NEXT PAGE (আরো ১০টি লোড করুন)\n"

            fzf_proc = subprocess.Popen(['fzf', '--reverse', '--header', f'Select Song (Total Loaded: {len(current_playlist)}):', '--height', '50%', '--border'], 
                                       stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
            selection, _ = fzf_proc.communicate(input=fzf_input)

            if not selection: break
            selection = selection.strip()

            if "NEXT PAGE" in selection:
                start_from += page_size
                continue
            else:
                # কত নম্বর গান সিলেক্ট হয়েছে তা বের করা
                total_idx = int(selection.split('.')[0]) - 1
                
                print(f"\033[1;34mPlaying: {current_playlist[total_idx]['title']}\033[0m")
                
                # সিলেক্ট করা গান থেকে বর্তমান লিস্টের শেষ পর্যন্ত প্লেলিস্ট করা
                video_urls = []
                for r in current_playlist[total_idx:]:
                    video_urls.append(f"https://www.youtube.com/watch?v={r['id']}")
                
                cmd = ['mpv', '--no-video', '--ytdl-format=bestaudio'] + video_urls
                subprocess.run(cmd)
                break

    except KeyboardInterrupt:
        print("\nExit.")
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    main()

