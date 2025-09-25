
import re
import math
import argparse
from typing import Dict, List, Any

COMMON_PASSWORDS = {"password", "123456", "qwerty", "letmein", "admin", "welcome"}
SYMBOL_SET_SIZE = 33  # Approximate number of printable symbols

def entropy_bits(password: str) -> float:
    """
    Estimate the entropy in bits of a password based on character classes used.
    Args:
        password (str): The password to analyze.
    Returns:
        float: Estimated entropy in bits.
    """
    pool = 0
    if re.search(r"[a-z]", password):
        pool += 26
    if re.search(r"[A-Z]", password):
        pool += 26
    if re.search(r"\d", password):
        pool += 10
    if re.search(r"[^\w\s]", password):
        pool += SYMBOL_SET_SIZE
    pool = max(pool, 1)
    return len(password) * math.log2(pool)

def evaluate(password: str) -> Dict[str, Any]:
    """
    Evaluate the strength of a password and provide feedback.
    Args:
        password (str): The password to evaluate.
    Returns:
        dict: Contains score, tier, entropy_bits, and tips.
    """
    tips: List[str] = []
    score = 0

    if len(password) >= 16:
        score += 30
    elif len(password) >= 12:
        score += 20
    elif len(password) >= 8:
        score += 10
    else:
        tips.append("Use at least 12 to 16 characters")

    classes = sum(bool(re.search(p, password)) for p in [r"[a-z]", r"[A-Z]", r"\d", r"[^\w\s]"])
    score += classes * 10
    if classes < 3:
        tips.append("Mix upper, lower, digits, and symbols")

    lower_pw = password.lower()
    if (
        lower_pw in COMMON_PASSWORDS
        or re.search(r"(.)\1{2,}", password)
        or re.search(r"(123|321|abc|cba)", lower_pw)
    ):
        tips.append("Avoid common words or obvious sequences")
        score -= 15

    ebits = entropy_bits(password)
    score += min(int(ebits // 10) * 5, 25)

    score = max(0, min(100, score))
    tier = (
        "Very weak" if score < 25 else
        "Weak" if score < 50 else
        "Good" if score < 75 else
        "Strong"
    )
    return {"score": score, "tier": tier, "entropy_bits": round(ebits, 1), "tips": tips}

def main() -> None:
    """
    Parse command-line arguments and print password strength evaluation.
    """
    parser = argparse.ArgumentParser(description="Check password strength.")
    parser.add_argument("password", help="Password to evaluate (do NOT use real passwords)")
    args = parser.parse_args()
    result = evaluate(args.password)
    print(f"\nPassword strength: {result['tier']} ({result['score']}/100)")
    print(f"Entropy estimate: {result['entropy_bits']} bits")
    if result['tips']:
        print("Tips:")
        for tip in result['tips']:
            print(f"  - {tip}")

    print("\n[Security warning] Do NOT use real or sensitive passwords on the command line!")

if __name__ == "__main__":
    main()
