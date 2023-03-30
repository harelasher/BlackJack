def some_function_with_callback(arg1, arg2, callback):
    # Do some work with arg1 and arg2
    result = arg1 + arg2
    # Call the callback function with the result as an argument
    callback(result)


def my_callback(result):
    print("The result is:", result)


some_function_with_callback(3, 5, my_callback)