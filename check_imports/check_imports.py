# python check_imports.py my_imports.txt
import argparse
import sys
import traceback # To get more detailed error info if needed

# --- SECURITY WARNING ---
# This script uses exec() to run import statements from the input file.
# Only use this script with files containing code you trust, as exec()
# can execute arbitrary Python code.
# --- --- --- --- --- ---

def execute_imports_from_file(filepath):
    """
    Reads lines from a file, executes Python import statements,
    prints comments as separators, and reports results.

    Args:
        filepath (str): The path to the file containing import statements
                        and comments (one per line).

    Returns:
        tuple: A tuple containing two lists: (successful_statements, failed_statements)
               failed_statements contains tuples of (statement_string, error_object).
    """
    successful_statements = []
    failed_statements = []
    current_globals = globals() # Use current global scope for exec

    print(f"--- Reading and executing imports from: {filepath} ---")

    try:
        with open(filepath, 'r') as f:
            for line_num, line in enumerate(f, 1):
                statement = line.strip()

                # Skip empty lines
                if not statement:
                    continue

                # If it's a comment line, print it as a separator
                if statement.startswith('#'):
                    # print(f"\n-- Comment -- {statement}\n")
                    print(f"\n{statement}\n")
                    continue

                # print(f"Attempting: {statement}")
                try:
                    # Execute the statement in the current global scope
                    exec(statement, current_globals)
                    successful_statements.append(statement)
                    print(f"   (+) Success: Executed statement correctly - {statement}")

                # Catch specific import errors and general exceptions
                except (ImportError, ModuleNotFoundError, SyntaxError) as e:
                    failed_statements.append((statement, e))
                    print(f" X (-) - - - Failed: Could not execute statement - {statement} - Error: {e}")
                    # Optional: print more detailed traceback
                    # traceback.print_exc(limit=1, file=sys.stdout)
                except Exception as e:
                    # Catch any other unexpected errors during execution
                    failed_statements.append((statement, e))
                    print(f" X (-) Failed: Unexpected error executing statement. Error: {e}")
                    # Optional: print more detailed traceback
                    # traceback.print_exc(limit=1, file=sys.stdout)


    except FileNotFoundError:
        print(f"\nError: The file '{filepath}' was not found.", file=sys.stderr)
        sys.exit(1) # Exit with a non-zero status code indicates an error
    except Exception as e:
        print(f"\nAn unexpected error occurred while reading the file: {e}", file=sys.stderr)
        sys.exit(1)

    return successful_statements, failed_statements

def print_summary(successful, failed):
    """Prints a summary of successful and failed import statements."""
    print("\n--- Execution Summary ---")

    if successful:
        print("\nSuccessfully Executed Statements:")
        for statement in successful:
            print(f"  - {statement}")
    else:
        print("\nNo import statements were executed successfully.")

    if failed:
        print("\nFailed Statements:")
        for statement, error in failed:
            print(f"  - {statement}: {error}")
    else:
        print("\nNo import statements failed.")

    print("\n--- End of Summary ---")

if __name__ == "__main__":
    # Set up argument parser for command-line usage
    parser = argparse.ArgumentParser(
        description="Execute Python import statements from a file and report status. Prints '#' lines as separators.",
        epilog="WARNING: Uses exec(). Only run with trusted input files."
        )
    parser.add_argument("filepath", help="Path to the file containing import statements and comments.")

    # Parse arguments
    args = parser.parse_args()

    # Run the execution check and print the summary
    successful, failed = execute_imports_from_file(args.filepath)
    print_summary(successful, failed)
