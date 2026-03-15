# SOSIALREL

A simple command-line OSINT tool that searches for a username across social media platforms and the web using DuckDuckGo.

<img src="https://github.com/rafosw/sosialrel/blob/main/ss/Screenshot%20From%202026-03-15%2019-19-19.png" width="800" height="850" />

---

## Requirements

- Python 3.x
- `duckduckgo_search` or `ddgs`

---

## Usage

### Interactive mode

```
git clone https://github.com/rafosw/sosialrel
cd sosialrel
pip install -r requirements.txt --break-system-packages
python3 sosialrel.py
```

### Command-line mode

```
python sosialrel.py -u <username> -p <platform> -l <limit>
```

---

## Options

| Flag | Description |
|------|-------------|
| `-u` | Username or text to search for |
| `-p` | Platform domain (e.g. `instagram.com`) or `ALL` for the whole web |
| `-l` | Number of results to retrieve (default: 10) |

---
## Hint

1. If you want to perform your search on Instagram, select “Instagram” directly. Don’t ask yourself, “Why shouldn’t I select ‘All Domains’ when Instagram is already included?” Sometimes “All Domains” doesn’t display results from specific domains, so always make sure to narrow down your search.

2. If the username appears in red in the search results, there is a 100% related to that user. If the username you entered doesn’t appear in red on the resulting URL, there are two possibilities: either the description is too long, so that username appears at the very end and isn’t visible on the screen, or that username isn’t present in that URL and it’s being displayed to us as an empty URL. If you don’t want this issue to occur, select the 13th option.

---

## Security

DuckDuckGo is used in the SosialRel tool because of its strong privacy policy and open search access. Unlike traditional search engines such as Google, DuckDuckGo states that it does not log users’ IP addresses or store search queries in a way that creates personal profiles. Many search engines typically collect information such as IP addresses, search queries, browser data, cookies or device fingerprints, and approximate location, which can later be linked to a user profile. In contrast, DuckDuckGo does not create user profiles or associate search queries with specific individuals. This makes it a suitable search engine for SosialRel, since the tool can perform username and footprint searches across the internet while maintaining a higher level of user privacy.

---

## How it works

The tool builds a DuckDuckGo query using `site:` operator for platform-specific searches or plain quoted search for global searches.

If a username appears highlighted in red in the results, it means that username is directly present in that URL or its description. This can indicate the person followed someone, liked a post, left a comment, or has a profile on that platform. If the username doesn't appear in red in the URL description, you can leave the other URLs blank.

---

## Notes

- This tool is for OSINT and research purposes only.
- Results depend on what DuckDuckGo has indexed.
- The number of results returned may be lower than requested depending on availability.

---

## Author

[@rafosw](https://github.com/rafosw)
