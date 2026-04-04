import webbrowser


COMMON_STARTERS = ["stare", "crate", "slate", "trace", "adieu"]


def run_wordle_task() -> str:
    url = "https://www.nytimes.com/games/wordle/index.html"
    webbrowser.open(url)
    suggestion = ", ".join(COMMON_STARTERS[:3])
    return (
        "Opened Wordle in browser. "
        f"Suggested opening guesses: {suggestion}. "
        "Next step: collect feedback colors and iterate."
    )
