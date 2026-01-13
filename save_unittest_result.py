import unittest
import os
import unit_tests


def save_failures_to_file(filename="raport_bledow.txt"):
    suite = unittest.defaultTestLoader.loadTestsFromModule(unit_tests)
    runner = unittest.TextTestRunner(verbosity=0)
    result = runner.run(suite)
    all_problems = result.errors + result.failures

    with open(filename, "w", encoding="utf-8") as f:
        if not all_problems:
            f.write("Gratulacje! Wszystkie testy przeszły pomyślnie.\n")
            print("Wszystko zielone! Brak błędów do zapisania.")
            return

        counter = 1
        for test_case, traceback_text in all_problems:
            lines = traceback_text.strip().split('\n')
            last_line = lines[-1]
            if ':' in last_line:
                parts = last_line.split(':', 1)
                error_type = parts[0].strip()
                error_message = parts[1].strip()
            else:
                error_type = "Inny Błąd"
                error_message = last_line

            test_name = str(test_case).split(' ')[0]

            f.write(f"{counter}.\n")
            f.write(f"nieudany test: {test_name}\n")
            f.write(f"*typ błędu: {error_type}\n")
            f.write(f"*informacja/komunikat błędu: {error_message}\n")
            f.write("\n" + "-" * 40 + "\n\n")

            counter += 1

    print(f"Znaleziono {len(all_problems)} błędów.")
    print(f"Raport zapisano w pliku: {filename}")


if __name__ == "__main__":
    save_failures_to_file()