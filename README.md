# Website Health Checker

A beginner friendly Python script that runs automated checks against any website and reports the results in a clean, readable format.

Built as part of a weekly SDET challenge series focused on building testing tools from scratch.

---

## What it does

- Checks if the homepage returns a 200 status code
- Measures homepage response time against a configurable threshold
- Discovers all links on the page and checks each one for broken URLs
- Prints a structured summary of passed checks, failed checks, and issues found

---

## Sample output

```
Checking website: https://beinghumantester.github.io/

✓ Check Homepage Status
✓ Check Homepage Speed
✗ Check For Broken Links
  2 broken link(s) found:
  https://beinghumantester.github.io/old-page -> 404
  https://beinghumantester.github.io/missing -> 404

==================================================
Checks Passed: 2
Checks Failed: 1
Total Checks : 3

Issues Found:
- Check For Broken Links
  2 broken link(s) found:
  https://beinghumantester.github.io/old-page -> 404
  https://beinghumantester.github.io/missing -> 404
==================================================
```

---

## Requirements

- Python 3.7 or above
- `requests`
- `beautifulsoup4`

Install dependencies:

```bash
pip install requests beautifulsoup4
```

---

## Usage

Clone the repo and run the script:

```bash
git clone https://github.com/beinghumantester/website-health-checker.git
cd website-health-checker
python link_checker.py
```

To check a different website, update the `BASE_URL` at the top of the file:

```python
BASE_URL = "https://your-website.com/"
```

---

## Configuration

All configurable values are at the top of the script:

| Variable | Default | Description |
|---|---|---|
| `BASE_URL` | `https://beinghumantester.github.io/` | The website to check |
| `TIMEOUT` | `5` | Request timeout in seconds |
| `RESPONSE_TIME_THRESHOLD_MS` | `2000` | Max acceptable response time in milliseconds |

---

## What is skipped

The checker intentionally skips:

- Anchor links starting with `#`
- Email links starting with `mailto:`
- Duplicate URLs are automatically deduplicated

---

## Part of the SDET Challenge Series

This script is the solution to Challenge 1 of a weekly SDET challenge series where instead of just using testing tools, you build them from scratch.

Follow along on Substack for new challenges every week.

---

## Author

**beinghumantester**  
[Substack](https://substack.com/@beinghumantester) · [GitHub](https://github.com/beinghumantester)
