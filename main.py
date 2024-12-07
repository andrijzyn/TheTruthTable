import re
import unicodedata
from itertools import product
from tabulate import tabulate


def parse_input(input_text):
    """Parses the given text and returns a list of functions."""
    functions = []
    lines = input_text.strip().split("\n")
    for line in lines:
        if "=" in line:
            name, expression = line.split("=", 1)
            functions.append((name.strip(), expression.strip()))
    return functions


def preprocess_expression(expression):
    """Preprocesses the expression to replace logical operators with Python equivalents."""
    # Normalize and replace logical operators
    expression = unicodedata.normalize('NFC', expression)
    expression = expression.replace("∧", " and ").replace("∨", " or ").replace("¬", " not ")

    # Handle overlined variables (e.g., x̅ -> not x)
    expression = re.sub(r'([a-zA-Z])̅', r'not \1', expression)

    # Handle negation of entire brackets (e.g., \overline{(x ∧ y)} -> not (x and y))
    expression = re.sub(r'̅\((.+?)\)', r'not (\1)', expression)

    return expression


def replace_variables(expression, variables):
    """Replaces variables in the expression with their values."""
    for var, value in variables.items():
        # Replace overlined variables (e.g., x̅ -> not value)
        expression = re.sub(fr"{var}̅", f"not {value}", expression)
        # Replace normal variables (e.g., x -> value)
        expression = re.sub(fr"\b{var}\b", str(value), expression)
    return expression


def evaluate_expression(expression, variables):
    """Evaluates the logical expression and records the computation steps."""
    steps = []

    # Replace variables with their values
    replaced_expression = replace_variables(expression, variables)
    steps.append(f"Replaced variables: {replaced_expression}")

    # Preprocess logical operators
    processed_expression = preprocess_expression(replaced_expression)
    steps.append(f"Preprocessed expression: {processed_expression}")

    try:
        result = int(eval(processed_expression))  # Evaluate the expression
    except Exception as e:
        result = None
        steps.append(f"Error during evaluation: {e}")

    steps.append(f"Final result: {result}")
    return result, "\n".join(steps)


def generate_truth_table(functions, variables):
    """Generates a truth table with detailed steps."""
    variable_names = sorted(variables)
    combinations = list(product([0, 1], repeat=len(variable_names)))

    truth_table = []

    for combination in combinations:
        current_vars = dict(zip(variable_names, combination))
        row = list(combination)

        for name, expression in functions:
            result, steps = evaluate_expression(expression, current_vars)
            row.append(result)
            row.append(steps)  # Append steps for each function

        truth_table.append(row)

    return variable_names, truth_table


def display_truth_table(variable_names, truth_table, functions):
    """Displays the truth table including steps."""
    headers = variable_names + [name for name, _ in functions] + ["Steps"]
    table = []

    for row in truth_table:
        # Separate results and steps
        steps = row[len(variable_names) + len(functions):]
        table.append(row[:len(variable_names) + len(functions)] + ["; ".join(steps)])

    print(tabulate(table, headers=headers, tablefmt="grid"))


if __name__ == "__main__":
    print("Enter logical functions (one per line).")
    print("Example: g1(x, y) = (x ∨ y̅) ∧ (x ∨ y)")
    print("Press Enter on an empty line to finish input.\n")

    input_lines = []
    while True:
        line = input()
        if not line:
            break
        input_lines.append(line)

    input_text = "\n".join(input_lines)
    functions = parse_input(input_text)

    if not functions:
        print("No valid functions entered.")
    else:
        # Determine all unique variables
        all_variables = set()
        for _, expression in functions:
            all_variables.update(re.findall(r'\b[a-zA-Z]\b', expression))

        variables = {var: 0 for var in all_variables}
        variable_names, truth_table = generate_truth_table(functions, variables)

        display_truth_table(variable_names, truth_table, functions)
