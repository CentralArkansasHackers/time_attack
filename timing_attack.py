import string
import subprocess
import time
import statistics

def measure_time(password_attempt):
    """
    Measures the time taken for the vault program to run with a given password attempt.
    Args:
        password_attempt (str): The password attempt to try.
    Returns:
        float: The time taken for the vault program to execute with the given password attempt.
    """
    start_time = time.time()
    try:
        subprocess.run(["./vault.o", password_attempt], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        # Ignore errors as we are only interested in measuring time
        pass
    end_time = time.time()
    return end_time - start_time

def brute_force_password():
    """
    Performs a brute-force timing attack to guess the correct password for the vault program.
    The attack measures the time taken to verify each character and uses timing information to determine the correct password.
    """
    password = ""  # Start with an empty password
    possible_characters = string.ascii_lowercase  # The password consists of lowercase letters
    
    while True:
        time_durations = {char: [] for char in possible_characters}
        
        # Measure each character multiple times (200 times) to gather timing data
        for _ in range(200):
            for char in possible_characters:
                attempt = password + char
                duration = measure_time(attempt)
                time_durations[char].append(duration)
        
        # Calculate the median duration for each character
        median_durations = [(char, statistics.median(durations)) for char, durations in time_durations.items()]
        
        # Sort by median duration, descending
        median_durations.sort(key=lambda x: x[1], reverse=True)
        
        # Assume the character with the longest median duration is the correct next character
        best_guess = median_durations[0][0]
        
        # Consistency verification: Re-measure the best guess to confirm
        confirmation_durations = []
        for _ in range(50):
            attempt = password + best_guess
            confirmation_durations.append(measure_time(attempt))
        
        # If the median of the confirmation measurements is still the highest, accept the character
        if statistics.median(confirmation_durations) > statistics.median([dur for _, dur in median_durations[1:]]):
            password += best_guess  # Add the correct character to the password
        else:
            # If not, re-evaluate by increasing the number of measurements
            continue
        
        print(f"Current password guess: {password}")
        
        # Check if the vault returns "Success"
        result = subprocess.run(["./vault.o", password], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Vault output: {result.stdout.decode().strip()}")
        if b"SUCCESS" in result.stdout.upper():
            print(f"Password found: {password}")
            break

if __name__ == "__main__":
    brute_force_password()
