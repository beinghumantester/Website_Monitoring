from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
import time

BASE_URL = "https://beinghumantester.github.io/"
TIMEOUT = 5
RESPONSE_TIME_THRESHOLD_MS = 2000

summary = {
    "passed": 0,
    "failed": 0,
    "issues": []
}


def get_page(url):
    start_time = time.time()

    response = requests.get(
        url,
        timeout=TIMEOUT
    )

    response_time_ms = round(
        (time.time() - start_time) * 1000,
        2
    )

    return response, response_time_ms


def get_links(html):
    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    links = set()

    for tag in soup.find_all("a"):
        href = tag.get("href")

        if not href:
            continue

        if href.startswith("#"):
            continue

        if href.startswith("mailto:"):
            continue

        links.add(
            urljoin(BASE_URL, href)
        )

    return links


def run_check(check):
    name = check.__name__.replace("_", " ").title()

    try:
        check()

        print(f"- {name}")
        summary["passed"] += 1

    except Exception as error:

        print(f"✗ {name}")
        print(f"  {error}")

        summary["failed"] += 1

        summary["issues"].append((name, str(error)))


def check_homepage_status():

    response, _ = get_page(BASE_URL)

    if response.status_code != 200:
        raise Exception(
            f"Expected status code 200 but got {response.status_code}"
        )


def check_homepage_speed():

    _, response_time_ms = get_page(BASE_URL)

    if response_time_ms >= RESPONSE_TIME_THRESHOLD_MS:
        raise Exception(
            f"Homepage took {response_time_ms}ms. "
            f"Expected less than {RESPONSE_TIME_THRESHOLD_MS}ms"
        )


def check_for_broken_links():

    response, _ = get_page(BASE_URL)

    links = get_links(response.text)

    if not links:
        print("No links found on the page")
        return

    broken_links = []

    for link in links:

        try:
            link_response = requests.get(
                link,
                timeout=TIMEOUT
            )

            if link_response.status_code >= 400:
                broken_links.append(
                    (
                        link,
                        link_response.status_code
                    )
                )

        except requests.exceptions.Timeout:

            broken_links.append(
                (
                    link,
                    "Timeout"
                )
            )

        except requests.exceptions.ConnectionError:

            broken_links.append(
                (
                    link,
                    "Connection Error"
                )
            )

    if broken_links:

        issue_list = "\n".join(
            [
                f"  {url} -> {status}"
                for url, status in broken_links
            ]
        )

        raise Exception(f"{len(broken_links)} broken link(s) found:\n{issue_list}")


def print_summary():

    total_checks = (
        summary["passed"] +
        summary["failed"]
    )

    print("\n" + "=" * 50)

    print(f"Checks Passed: {summary['passed']}")
    print(f"Checks Failed: {summary['failed']}")
    print(f"Total Checks : {total_checks}")

    if summary["issues"]:
        print("\nIssues Found:")

        for check_name, issue in summary["issues"]:
            print(f"- {check_name}")

            print(f"  {issue}")

    print("=" * 50)


if __name__ == "__main__":

    checks = [
        check_homepage_status,
        check_homepage_speed,
        check_for_broken_links
    ]

    print(f"\nChecking website: {BASE_URL}\n")

    for check in checks:
        run_check(check)

    print_summary()