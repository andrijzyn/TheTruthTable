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
    expression = expression.replace("∧", "and").replace("∨", "or").replace("¬", "not ")
    expression = expression.replace("̅", "")  # Removes overline and prepares for proper NOT handling.

    # Convert `y̅` to `not y`
    result = ""
    skip_next = False
    for i, char in enumerate(expression):
        if skip_next:
            skip_next = False
            continue

        if i < len(expression) - 1 and expression[i + 1] == "̅":  # Check if char is followed by `̅`.
            result += f"not {char}"
            skip_next = True
        else:
            result += char

    return result


def evaluate_expression(expression, variables):
    """Computes the value of a logical expression for the current set of variables."""
    steps = []

    # Replace variables with their values
    for var, value in variables.items():
        expression = expression.replace(var, str(value))
        steps.append(f"Replace {var} with {value}: {expression}")

    # Preprocess logical operators
    expression = preprocess_expression(expression)
    steps.append(f"Preprocessed expression: {expression}")

    # Evaluate the expression
    result = int(eval(expression))
    steps.append(f"Final result: {result}")
    return result, " -> ".join(steps)


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
            row.append(steps)

        truth_table.append(row)

    return variable_names, truth_table


def display_truth_table(variable_names, truth_table, functions):
    """Displays truth table using tabulate with detailed steps."""
    # Create headers for the table
    headers = variable_names + [name for name, _ in functions] + [
        f"Steps for {name}" for name, _ in functions
    ]
    print("\nTruth Table with Detailed Steps:")
    print(tabulate(truth_table, headers=headers, tablefmt="grid"))


if __name__ == "__main__":
    while True:
        print("\nEnter logical functions (one per line). Enter an empty line to finish:")
        print("Example format: g1(x,y) = (x ∨ y̅) ∧ (x ∨ y)")

        input_lines = []
        while True:
            line = input()
            if not line:
                break
            input_lines.append(line)

        if not input_lines:
            print("No functions entered. Exiting...")
            break

        input_text = "\n".join(input_lines)
        functions = parse_input(input_text)

        if not functions:
            print("No valid functions found. Please check your input format.")
            continue

        # Calculate unique variables
        all_variables = set()
        for _, expression in functions:
            all_variables.update(var for var in expression if var.isalpha())

        variables = {var: 0 for var in all_variables}
        variable_names, truth_table = generate_truth_table(functions, variables)

        # Display results
        display_truth_table(variable_names, truth_table, functions)

        # Ask if user wants to continue
        cont = input("\nDo you want to enter more functions? (y/n): ")
        if cont.lower() != 'y':
            break