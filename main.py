"""Quiz Master - Main game loop and user interface."""

from display import (banner, print_menu, get_input, print_header,
                     print_correct, print_wrong, print_score, _print,
                     CYAN, RESET, BOLD, YELLOW, GREEN)
from questions import (load_questions, get_categories, get_difficulties,
                       filter_questions, pick_questions)
from scoring import ScoreTracker, save_high_score, get_top_scores


def get_choice(prompt: str, max_val: int, default: int | None = None) -> int:
    """Get a validated integer choice from 1 to max_val."""
    raw = get_input(prompt)
    try:
        val = int(raw)
        if 1 <= val <= max_val:
            return val
    except ValueError:
        pass
    if default is not None:
        return default
    return 1


def play_quiz():
    """Run a single quiz session."""
    questions = load_questions()

    # Choose category
    categories = get_categories(questions)
    print_header("Choose Category")
    all_options = ["All Categories"] + categories
    print_menu(all_options)
    cat_idx = get_choice("Category number:", len(all_options), default=1)
    category = None if cat_idx == 1 else categories[cat_idx - 2]

    # Choose difficulty
    difficulties = get_difficulties()
    print_header("Choose Difficulty")
    diff_options = ["All Difficulties"] + [d.capitalize() for d in difficulties]
    print_menu(diff_options)
    diff_idx = get_choice("Difficulty number:", len(diff_options), default=1)
    difficulty = None if diff_idx == 1 else difficulties[diff_idx - 2]

    # Filter and pick questions
    pool = filter_questions(questions, category, difficulty)
    if not pool:
        _print("\n  No questions match your filters. Try again.\n")
        return

    # Ask how many questions
    print_header("How Many Questions?")
    default_count = min(5, len(pool))
    count = get_choice(f"Number (1-{len(pool)}, default {default_count}):",
                       len(pool), default=default_count)

    selected = pick_questions(pool, count)
    tracker = ScoreTracker()

    # Quiz loop
    cat_label = category or "All"
    print_header(f"Quiz: {cat_label} ({difficulty or 'all'} difficulty)")

    for i, q in enumerate(selected, 1):
        _print(f"  {BOLD}Question {i}/{len(selected)}{RESET}")
        _print(f"  {CYAN}{q.text}{RESET}\n")
        print_menu(q.choices)
        choice_idx = get_choice("Your answer (number):", len(q.choices)) - 1
        correct = q.check(choice_idx)

        tracker.record(correct)
        if correct:
            print_correct()
        else:
            print_wrong(q.correct_answer)
        print_score(tracker.correct, tracker.total)

    # Final results
    print_header("Results")
    _print(f"  {BOLD}Final Score: {tracker.correct}/{tracker.total} "
           f"({tracker.percentage:.0f}%){RESET}\n")

    # Save score
    name = get_input("Enter your name for the leaderboard:")
    if name.strip():
        save_high_score(name.strip(), tracker.correct, tracker.total, cat_label)
        _print(f"\n  {GREEN}Score saved!{RESET}\n")


def show_high_scores():
    """Display the leaderboard."""
    scores = get_top_scores(5)
    print_header("Leaderboard - Top 5")
    if not scores:
        _print("  No scores yet. Play a game first!\n")
        return
    _print(f"  {BOLD}{'#':<4}{'Name':<15}{'Score':<10}{'%':<8}{'Date':<16}{'Category'}{RESET}")
    _print(f"  {'-' * 65}")
    for i, s in enumerate(scores, 1):
        _print(f"  {YELLOW}{i:<4}{RESET}{s['name']:<15}"
               f"{s['score']}/{s['total']:<8}"
               f"{s['percentage']:<8}"
               f"{s['date']:<16}"
               f"{s['category']}")
    print()


def main():
    """Main menu loop."""
    banner()
    options = ["Start Quiz", "View High Scores", "Quit"]

    while True:
        print_header("Main Menu")
        print_menu(options)
        choice = get_input("Choose an option:")

        if choice == "1":
            play_quiz()
        elif choice == "2":
            show_high_scores()
        elif choice == "3":
            _print("\n  Thanks for playing! Goodbye.\n")
            break
        else:
            _print("\n  Invalid choice. Try again.\n")


if __name__ == "__main__":
    main()
