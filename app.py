"""
CyberKit - Beginner Cybersecurity Toolkit
Tools: Password Strength Analyzer | Hash Generator | Caesar Cipher
Author: Hamid Shafiq | University of Haripur
"""

import hashlib
import string
import sys
import os

COMMON_PASSWORDS = [
    "password", "123456", "password123", "admin", "letmein",
    "qwerty", "abc123", "iloveyou", "111111", "123123",
    "1234567890", "password1", "12345678", "superman", "batman"
]

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    print("""
╔══════════════════════════════════════════════╗
║       CyberKit v1.0 - By Hamid Shafiq        ║
║       Beginner Cybersecurity Toolkit         ║
╠══════════════════════════════════════════════╣
║  [1] Password Strength Analyzer              ║
║  [2] Hash Generator (MD5 / SHA256)           ║
║  [3] Caesar Cipher (Encrypt / Decrypt)       ║
║  [0] Exit                                    ║
╚══════════════════════════════════════════════╝
""")

# ─── TOOL 1: Password Strength Analyzer ───────────────────────────────────────

def analyze_password(password: str) -> dict:
    score = 0
    feedback = []

    checks = {
        "length_8":    len(password) >= 8,
        "length_12":   len(password) >= 12,
        "uppercase":   any(c.isupper() for c in password),
        "lowercase":   any(c.islower() for c in password),
        "digits":      any(c.isdigit() for c in password),
        "symbols":     any(c in string.punctuation for c in password),
        "not_common":  password.lower() not in COMMON_PASSWORDS,
    }

    weights = {
        "length_8": 1, "length_12": 2, "uppercase": 1,
        "lowercase": 1, "digits": 1, "symbols": 2, "not_common": 2
    }

    for key, passed in checks.items():
        if passed:
            score += weights[key]
        else:
            tips = {
                "length_8":   "Use at least 8 characters.",
                "length_12":  "12+ characters is much stronger.",
                "uppercase":  "Add uppercase letters (A-Z).",
                "lowercase":  "Add lowercase letters (a-z).",
                "digits":     "Include numbers (0-9).",
                "symbols":    "Add symbols (!@#$%^&*).",
                "not_common": "This is a commonly known password. Change it.",
            }
            feedback.append(tips[key])

    max_score = sum(weights.values())
    percentage = int((score / max_score) * 100)

    if percentage < 40:
        strength = "WEAK"
    elif percentage < 65:
        strength = "MODERATE"
    elif percentage < 85:
        strength = "STRONG"
    else:
        strength = "VERY STRONG"

    return {
        "score": score,
        "max": max_score,
        "percentage": percentage,
        "strength": strength,
        "checks": checks,
        "feedback": feedback
    }

def tool_password():
    print("\n[ PASSWORD STRENGTH ANALYZER ]\n")
    password = input("Enter password to analyze: ")

    if not password:
        print("No password entered.")
        return

    result = analyze_password(password)

    bar_filled = int(result["percentage"] / 5)
    bar = "█" * bar_filled + "░" * (20 - bar_filled)

    print(f"\n  Strength  : {result['strength']}")
    print(f"  Score     : {result['score']}/{result['max']}")
    print(f"  Progress  : [{bar}] {result['percentage']}%")

    print("\n  Checks:")
    labels = {
        "length_8": "Min 8 chars", "length_12": "Min 12 chars",
        "uppercase": "Uppercase", "lowercase": "Lowercase",
        "digits": "Digits", "symbols": "Symbols", "not_common": "Not common"
    }
    for key, passed in result["checks"].items():
        mark = "✓" if passed else "✗"
        print(f"    [{mark}] {labels[key]}")

    if result["feedback"]:
        print("\n  Suggestions:")
        for tip in result["feedback"]:
            print(f"    → {tip}")

# ─── TOOL 2: Hash Generator ───────────────────────────────────────────────────

def hash_text(text: str) -> dict:
    encoded = text.encode("utf-8")
    return {
        "MD5":    hashlib.md5(encoded).hexdigest(),
        "SHA1":   hashlib.sha1(encoded).hexdigest(),
        "SHA256": hashlib.sha256(encoded).hexdigest(),
        "SHA512": hashlib.sha512(encoded).hexdigest(),
    }

def tool_hash():
    print("\n[ HASH GENERATOR ]\n")
    text = input("Enter text to hash: ")

    if not text:
        print("No text entered.")
        return

    hashes = hash_text(text)
    print()
    for algo, digest in hashes.items():
        print(f"  {algo:<8}: {digest}")
    print()
    print("  Note: Hashes are one-way. Same input always gives same output.")

# ─── TOOL 3: Caesar Cipher ────────────────────────────────────────────────────

def caesar_cipher(text: str, shift: int, mode: str = "encrypt") -> str:
    if mode == "decrypt":
        shift = -shift

    result = []
    for char in text:
        if char.isupper():
            result.append(chr((ord(char) - ord("A") + shift) % 26 + ord("A")))
        elif char.islower():
            result.append(chr((ord(char) - ord("a") + shift) % 26 + ord("a")))
        else:
            result.append(char)
    return "".join(result)

def tool_caesar():
    print("\n[ CAESAR CIPHER ]\n")
    print("  [1] Encrypt")
    print("  [2] Decrypt")
    print("  [3] Brute Force (try all 25 shifts)\n")

    choice = input("  Choose: ").strip()

    if choice not in ("1", "2", "3"):
        print("Invalid choice.")
        return

    text = input("  Enter text: ")

    if not text:
        print("No text entered.")
        return

    if choice in ("1", "2"):
        try:
            shift = int(input("  Enter shift (1-25): "))
            if not 1 <= shift <= 25:
                raise ValueError
        except ValueError:
            print("Invalid shift. Must be 1-25.")
            return

        mode = "encrypt" if choice == "1" else "decrypt"
        output = caesar_cipher(text, shift, mode)
        label = "Encrypted" if choice == "1" else "Decrypted"
        print(f"\n  {label}: {output}")

    elif choice == "3":
        print("\n  Brute Force Results:\n")
        for s in range(1, 26):
            result = caesar_cipher(text, s, "decrypt")
            print(f"  Shift {s:>2}: {result}")

# ─── MAIN LOOP ────────────────────────────────────────────────────────────────

def main():
    tools = {"1": tool_password, "2": tool_hash, "3": tool_caesar}

    while True:
        clear()
        banner()
        choice = input("  Select tool: ").strip()

        if choice == "0":
            print("\n  Exiting CyberKit. Stay secure.\n")
            sys.exit(0)
        elif choice in tools:
            tools[choice]()
        else:
            print("  Invalid option.")

        input("\n  Press Enter to return to menu...")

if __name__ == "__main__":
    main()
