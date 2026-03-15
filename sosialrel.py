import sys
import webbrowser
import os
import time
import argparse

RED = '\033[91m'
RESET = '\033[0m'

try:
    from duckduckgo_search import DDGS
except ImportError:
    try:
        from ddgs import DDGS
    except ImportError:
        print("[!] Neither 'duckduckgo_search' nor 'ddgs' module found.", file=sys.stderr)
        print("[!] Please install the requirements: pip install -r requirements.txt", file=sys.stderr)
        sys.exit(1)

import subprocess

def print_banner():
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    
    banner = f"""{GREEN}
    ███████╗ ██████╗ ███████╗██╗ █████╗ ██╗     ██████╗ ███████╗██╗     
    ██╔════╝██╔═══██╗██╔════╝██║██╔══██╗██║     ██╔══██╗██╔════╝██║     
    ███████╗██║   ██║███████╗██║███████║██║     ██████╔╝█████╗  ██║     
    ╚════██║██║   ██║╚════██║██║██╔══██║██║     ██╔══██╗██╔══╝  ██║     
    ███████║╚██████╔╝███████║██║██║  ██║███████╗██║  ██║███████╗███████╗ 
    ╚══════╝ ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝ v1.0
{CYAN}                 Social Relations Footprint Scanner                     
                           by @rafosw                                             
{RESET}"""
    print(banner)

def open_url(url):
    try:
        if sys.platform == 'win32':
            os.startfile(url)
        elif sys.platform == 'darwin':
            subprocess.Popen(['open', url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            subprocess.Popen(['xdg-open', url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"[!] Could not open browser: {e}")

def display_results(results_info, username, username2=None):
    if not results_info:
        print("\n[-] Unfortunately, no results were found for this search.")
        return False

    print("\n" + "="*80)
    print("                 SEARCH RESULTS                 ".center(80))
    print("="*80)
    
    for i, info in enumerate(results_info, 1):
        url = info['url'].replace(username, f"{RED}{username}{RESET}")
        title = info['title'].replace(username, f"{RED}{username}{RESET}")
        desc = info['desc'].replace(username, f"{RED}{username}{RESET}")
        if username2:
            url = url.replace(username2, f"{RED}{username2}{RESET}")
            title = title.replace(username2, f"{RED}{username2}{RESET}")
            desc = desc.replace(username2, f"{RED}{username2}{RESET}")
        
        print(f"\n[{i}] URL: {url}")
        print(f"    Title: {title}")
        print(f"    Caption: {desc}")
        print("-" * 40)
        
    print("\n" + "="*80)
    
    while True:
        try:
            print("\nEnter the number of the URL to open, 'r' to run a new scan, or 'q' to quit:")
            choice = input("\033[92m./f>\033[0m ").strip()
            
            if choice.lower() == 'q':
                print("[*] Exiting interactive mode.")
                return False
            
            if choice.lower() == 'r':
                print("[*] Restarting scan...")
                return True
                
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(results_info):
                print(f"[*] Opening: {results_info[choice_idx]['url']}")
                open_url(results_info[choice_idx]['url'])
            else:
                print("[!] Invalid number. Please select a number from the list.")
                
        except ValueError:
            print("[!] Please enter a valid number, 'r' to restart, or 'q' to quit.")
        except KeyboardInterrupt:
            print("\n[!] Exiting interactive mode.")
            return False
    return False


def duckduckgo_search(query, num_results, username, limited=False, username2=None, dual=False):
    print(f"[*] Expected number of results: {num_results}")
    if limited:
        print("[*] Limited Search mode enabled — filtering URLs that contain your text...")
    if dual and username2:
        print("[*] Two-Person Association mode — only showing URLs containing BOTH usernames...")
    print("[*] Searching... Please wait.\n")
    
    results_info = []
    try:
        results = DDGS().text(query, max_results=num_results)
        
        if not results:
            print("[-] No results found.")
            return False
            
        for count, result in enumerate(results):
            url = result.get('href', '')
            title = result.get('title', 'No Title')
            desc = result.get('body', 'No Description (Caption)')
            
            if url:
                if limited and username.lower() not in url.lower():
                    continue
                if dual and username2:
                    if username.lower() not in url.lower() or username2.lower() not in url.lower():
                        continue
                results_info.append({
                    'url': url,
                    'title': title,
                    'desc': desc
                })

        if limited:
            print(f"[*] {len(results_info)} result(s) passed the URL filter.")
        if dual:
            print(f"[*] {len(results_info)} result(s) passed the dual-username URL filter.")
                    
        return display_results(results_info, username, username2)
        
    except Exception as e:
        print(f"[!] An error occurred during the search: {e}")
        return False

def get_platform_domain():
    print("""
    [1]  Instagram
    [2]  TikTok
    [3]  X (Twitter)
    [4]  GitHub
    [5]  Facebook
    [6]  LinkedIn
    [7]  YouTube
    [8]  Reddit
    [9]  Pinterest
    [10] Snapchat
    [11] Custom Domain
    [12] Internet Overall (All domains)
    [13] Limited Search (only shows results where username is in the URL)
    [14] Two-Person Association (are both usernames in the same URL?)
    """)
    choice = input("\033[92m./f>\033[0m ").strip()
    
    platforms = {
        '1': 'instagram.com',
        '2': 'tiktok.com',
        '3': 'x.com',
        '4': 'github.com',
        '5': 'facebook.com',
        '6': 'linkedin.com',
        '7': 'youtube.com',
        '8': 'reddit.com',
        '9': 'pinterest.com',
        '10': 'snapchat.com'
    }
    
    if choice in platforms:
        return platforms[choice], False, False
    elif choice == '11':
        custom = input(f"\n[-] Enter a domain (e.g. example.com):\n\033[92m./f>\033[0m ").strip()
        if custom:
            return custom, False, False
        else:
            print("[-] Aborted! Custom domain cannot be empty.\n")
            time.sleep(1)
            os.system('cls' if os.name == 'nt' else 'clear')
            return None, False, False
    elif choice == '12':
        return 'ALL', False, False
    elif choice == '13':
        print("""
    Which platform for Limited Search?
    [1] Instagram  [2] TikTok   [3] X (Twitter)  [4] GitHub
    [5] Facebook   [6] LinkedIn [7] YouTube       [8] Reddit
    [9] Pinterest  [10] Snapchat [11] Custom Domain [12] All Internet
    """)
        sub = input("\033[92m./f>\033[0m ").strip()
        if sub in platforms:
            return platforms[sub], True, False
        elif sub == '11':
            custom = input(f"\n[-] Enter a domain (e.g. example.com):\n\033[92m./f>\033[0m ").strip()
            if custom:
                return custom, True, False
            else:
                print("[-] Aborted! Custom domain cannot be empty.\n")
                time.sleep(1)
                os.system('cls' if os.name == 'nt' else 'clear')
                return None, False, False
        elif sub == '12':
            return 'ALL', True, False
        else:
            print("[-] Invalid choice.\n")
            time.sleep(1)
            os.system('cls' if os.name == 'nt' else 'clear')
            return None, False, False
    elif choice == '14':
        print("""
    Select platform:
    [1] Instagram  [2] TikTok   [3] X (Twitter)  [4] GitHub
    [5] Facebook   [6] LinkedIn [7] YouTube       [8] Reddit
    [9] Pinterest  [10] Snapchat [11] Custom Domain [12] All Internet
    """)
        sub = input("\033[92m./f>\033[0m ").strip()
        if sub in platforms:
            return platforms[sub], False, True
        elif sub == '11':
            custom = input(f"\n[-] Enter a domain (e.g. example.com):\n\033[92m./f>\033[0m ").strip()
            if custom:
                return custom, False, True
            else:
                print("[-] Aborted! Custom domain cannot be empty.\n")
                time.sleep(1)
                os.system('cls' if os.name == 'nt' else 'clear')
                return None, False, False
        elif sub == '12':
            return 'ALL', False, True
        else:
            print("[-] Invalid choice.\n")
            time.sleep(1)
            os.system('cls' if os.name == 'nt' else 'clear')
            return None, False, False
    else:
        print("[-] Aborted! Invalid choice. Please try again...\n")
        time.sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')
        return None, False, False

def main():
    parser = argparse.ArgumentParser(
        description="""This tool primarily searches for the username across all webpages indexed by Google.
It is a very functional, simple tool designed for OSINT purposes.""",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('-u', '--username', help='Username or text to search for')
    parser.add_argument('-p', '--platform', help='Platform domain to search (e.g. instagram.com, tiktok.com, or ALL for internet overall)')
    parser.add_argument('-l', '--limit', type=int, default=10, help='Number of results to retrieve (default: 10)')
    
    args = parser.parse_args()

    if args.username and args.platform:
        print_banner()
        if args.platform.upper() == 'ALL':
            search_query = f'"{args.username}"'
        else:
            search_query = f'site:{args.platform} "{args.username}"'
            
        print("\n" + "-"*60)
        duckduckgo_search(search_query, num_results=args.limit, username=args.username)
        return

    while True:
        print_banner()
        
        try:
            result = get_platform_domain()
            domain, limited, dual = result
            
            if not domain:
                continue
                
            if domain == 'ALL':
                platform_name = "Global Internet"
            else:
                platform_name = domain.split('.')[0].capitalize()

            username2 = None

            if dual:
                print(f"\n[-] [{platform_name}] Two-Person Association — enter 1st username:")
                username = input("\033[92m./f>\033[0m ").strip()
                if not username:
                    print("[-] Empty input. Exiting.")
                    sys.exit(0)
                print(f"\n[-] Enter 2nd username:")
                username2 = input("\033[92m./f>\033[0m ").strip()
                if not username2:
                    print("[-] Empty input. Exiting.")
                    sys.exit(0)
                if domain == 'ALL':
                    search_query = f'"{username}" "{username2}"'
                else:
                    search_query = f'site:{domain} "{username}" "{username2}"'
            else:
                mode_label = " [LIMITED]" if limited else ""
                print(f"\n[-] Enter the {platform_name}{mode_label} username (or text) you want to search for:")
                username = input("\033[92m./f>\033[0m ").strip()
                if not username:
                    print("[-] You entered empty data. Exiting.")
                    sys.exit(0)
                if domain == 'ALL':
                    search_query = f'"{username}"'
                else:
                    search_query = f'site:{domain} "{username}"'
            
            print("\n[-] How many results do you want to see? (Default: 10):")
            limit_input = input("\033[92m./f>\033[0m ").strip()
            limit = int(limit_input) if limit_input.isdigit() else 10
            
            print("\n" + "-"*60)

            if dual:
                restart = duckduckgo_search(search_query, num_results=limit, username=username, dual=True, username2=username2)
            else:
                restart = duckduckgo_search(search_query, num_results=limit, username=username, limited=limited, username2=username2)

            if not restart:
                break
            else:
                os.system('cls' if os.name == 'nt' else 'clear')
                continue
            
        except KeyboardInterrupt:
            print("\n\n[!] Program terminated by the user.")
            sys.exit(0)

if __name__ == "__main__":
    main()
