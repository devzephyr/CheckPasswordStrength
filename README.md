
# CheckPasswordStrength

CheckPasswordStrength is a simple command-line tool to evaluate the strength of passwords. It estimates password entropy, assigns a strength score and tier, and provides actionable tips for improvement.

## Features
- Estimates password entropy in bits
- Assigns a score (0-100) and strength tier (Very weak, Weak, Good, Strong)
- Detects common passwords and obvious patterns
- Provides tips to improve password strength
- No dependencies beyond Python standard library

## Installation
No installation required. Requires Python 3.7 or newer.

Clone the repository or download `password_strength.py`:

```sh
git clone https://github.com/devzephyr/CheckPasswordStrength.git
cd CheckPasswordStrength
```

## Usage

**Warning:** Do NOT use real or sensitive passwords on the command line, as they may be visible in your shell history or process list.

Run the script with your password as an argument:

```sh
python password_strength.py 'Tr33s!Grow!Slowly'
```

### Example Output

```
Password strength: Strong (90/100)
Entropy estimate: 98.5 bits
Tips:
	- (No tips if password is strong)

[Security warning] Do NOT use real or sensitive passwords on the command line!
```

If the password is weak, you will see suggestions for improvement.

## License
MIT License. See [LICENSE](LICENSE) for details.
