
answer = "  Based on the given SQL query and response, the total contract value in year 2024 is $1500."

prefix = "  Based on the given SQL query and response,"

if prefix in answer:
    result = answer[len(prefix)+ 1: len(answer)]
    print(result)