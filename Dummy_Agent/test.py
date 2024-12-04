import ast

# The received state as a string array
received_data = ["(807.0192, 2.872828)", "(0, 0)", "(0, 0)", "(0, 0)", "(0, 0)", "(0, 0)", "(0, 0)", "(0, 0)", "(0, 0)", "(0, 0)"]

# Convert the string representations of tuples into actual tuples
parsed_data = [ast.literal_eval(item) for item in received_data]

# Print the parsed data
print(parsed_data)