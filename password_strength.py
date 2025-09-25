import re
import math
import argparse

COMMON = {"password", "123456", "qwerty", "letmein", "admin", "welcome"}

def entropy_bits(pw):
    pool = 0
    if re.search(r"[a-z]", pw): pool += 26
    if re.search(r"[A-Z]", pw): pool += 26
    if re.search(r"\d", pw):    pool += 10
    # rough symbol set
    if re.search(r"[^\w\s]", pw): pool += 33  
    pool = max(pool, 1)
    return len(pw) * math.log2(pool)

def evaluate(pw):
    tips = []
    score = 0

    if len(pw) >= 16: score += 30
    elif len(pw) >= 12: score += 20
    elif len(pw) >= 8: score += 10
    else:
        tips.append("Use at least 12 to 16 characters")
    
    classes = sum(bool(re.search(p, pw)) for p in [r"[a-z]", r"[A-Z]", r"\d", r"[^\w\s]"])
    score += classes * 10
    if classes < 3:
        tips.append("Mix upper, lower, digits, and symbols")
    
    lower_pw = pw.lower()
    if lower_pw in COMMON or re.search(r"(.)\1{2,}", pw) or re.search(r"(123|321|abc|cba)", lower_pw):
        tips.append("Avoid common words or obvious sequences")
        score -= 15

    ebits = entropy_bits(pw)
    score += min(int(ebits // 10) * 5, 25)

    score = max(0, min(100, score))
    tier = ("Very weak" if score < 25 else
            "Weak" if score < 50 else
            "Good" if score < 75 else
            "Strong")
    return {"score": score, "tier": tier, "entropy_bits": round(ebits, 1), "tips": tips}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("password")
    args = ap.parse_args()
    result = evaluate(args.password)
    print(result)

if __name__ == "__main__":
    main()
