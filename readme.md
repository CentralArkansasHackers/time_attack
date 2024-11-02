# Timing Attack Password Cracker

This project contains a Python script that performs a timing attack to brute-force the correct password for a target executable (`vault.o`). The executable verifies a password character by character, allowing the script to exploit time differences in verification to determine the correct password.

## Requirements

- Python 3.7 or higher
- PyCharm (recommended for development)
- A Linux environment (or a compatible terminal) to run the target executable

## Installation and Setup

1. Clone the repository:
   ```
   git clone <repo_url>
   ```

2. Navigate to the project directory:
   ```
   cd <project_directory>
   ```

3. Ensure the `vault.o` file has execute permissions:
   ```
   chmod +x vault.o
   ```


## How to Run

Run the Python script to start the timing attack:
```
python3 crack.py
```

The script will output the current password guess as it attempts to find the correct password. Once it successfully finds the password, it will print `Password found` along with the correct password.

## How It Works

1. The script uses a timing side-channel attack by measuring the time it takes for the target executable to verify each character.
2. It builds the password one character at a time by appending characters that show the longest execution time.
3. The median time for each character is used to reduce the influence of outliers and improve the accuracy of guesses.
4. Each guessed character is further confirmed by consistency checks.

## Notes

- **Timing Variations**: The timing measurements are sensitive to environmental noise (e.g., CPU load), which may cause some divergence in guesses. It is recommended to run the script in a low-noise environment.
- **Performance**: The script measures each character 200 times and verifies the best guess with 50 additional checks. This provides a good balance between accuracy and speed but may be adjusted based on your requirements.

## Remarks

- Make sure that you test the code thoroughly before submitting or using it.
- The code should be run in an environment that allows for accurate time measurement (minimal background processes).

## Example Output

```
Current password guess: c
Vault output: Wrong password
Current password guess: cn
Vault output: Wrong password
...
Current password guess: cnqkoieqmhc
Vault output: SUCCESS!
Password found: cnqkoieqmhc
```

