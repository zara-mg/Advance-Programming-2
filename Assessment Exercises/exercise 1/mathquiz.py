import random

NUM_QUESTIONS = 10
def displayMenu():
    print("DIFFICULTY LEVEL")
    print(" 1. Easy")
    print(" 2. Moderate")
    print(" 3. Advanced")
    while True:
        choice = input("Choose difficulty (1-3): ").strip()
        if choice in ("1","2","3"):
            return int(choice)
        print("Invalid choice. Enter 1, 2 or 3.")

def randomInt(min_val, max_val):
    return random.randint(min_val, max_val)

def Operation():
    return random.choice(['+','-'])

def answer(user_ans, correct_ans):
    return user_ans == correct_ans

def math_problem(num1, num2, op):
    prompt = f"{num1} {op} {num2} = "
    while True:
        s = input(prompt).strip()
        try:
            return int(s)
        except ValueError:
            print("Please enter an integer answer.")

def displayResults(score):
    print("\nRESULTS")
    print(f"Score: {score} / {NUM_QUESTIONS * 10}")
    total_score = (score / (NUM_QUESTIONS * 10)) * 100
    if total_score > 90:
        grade = "A+"
    elif total_score >= 80:
        grade = "A"
    elif total_score >= 70:
        grade = "B"
    elif total_score >= 60:
        grade = "C"
    else:
        grade = "F"
    print(f"Percent: {total_score:}%  Grade: {grade}\n")

def quiz():
    level = displayMenu()
    if level == 1:
        lo, hi = 0, 9
    elif level == 2:
        lo, hi = 10, 99
    else:
        lo, hi = 1000, 9999

    score = 0
    for q in range(1, NUM_QUESTIONS + 1):
        num1 = randomInt(lo, hi)
        num2 = randomInt(lo, hi)
        op = Operation()
        correct = num1 + num2 if op == '+' else num1 - num2

        print(f"\nQuestion {q}:")
        ans = math_problem(num1, num2, op)
        if answer(ans, correct):
            print("Correct! (+10)")
            score += 10
            continue

        print("Incorrect. Try once more.")
        ans2 = math_problem(num1, num2, op)
        if answer(ans2, correct):
            print("Correct on second attempt. (+5)")
            score += 5
        else:
            print(f"Incorrect. The correct answer was: {correct}")

    displayResults(score)

def main():
    print("Math Quiz")
    while True:
        quiz()
        again = input("Would you like to play again? (yes/no): ").strip()
        if again != 'yes':
            print("Well played. Goodbye.")
            break

if __name__ == "__main__":
    main()