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

## Search Modes

| # | Mode | Description |
|---|------|-------------|
| 1-10 | Platform Search | Searches within a specific platform |
| 11 | Custom Domain | Enter any domain manually |
| 12 | Internet Overall | Searches the entire web |
| 13 | Limited Search | Only shows results where the username appears in the URL |
| 14 | Two-Person Association | Searches for two usernames together, only shows URLs containing both |

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
