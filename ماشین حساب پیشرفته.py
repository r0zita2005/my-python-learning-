import math
num1=float(input("عدد مورد نظر را انتخاب کنید"))
op=input("عملگر مورد نظر راانتخاب نمایید (+ - * / ^ sqrt)")
if op != "sqrt":
    num2=float(input("عدد دوم را انتخاب کنید "))

if op == "+":
    result = num1 + num2
elif op == "-":
    result = num1 - num2
elif op == "*":
    result = num1 * num2
elif op == "/":
    if num2 == 0:
        result = "تقسیم بر صفر ممکن نیست!"
    else:
        result = num1 / num2
elif op == "^":
    result = num1 ** num2
elif op == "sqrt":
    import math
    result = math.sqrt(num1)
else:
    result = "عملیات نامعتبر است"
print("نتیجه : ", result)