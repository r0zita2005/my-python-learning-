
for i in range(3):
    p = input("password? ")
    if p == "1234":
        print("yes")
        break
    else:
        print("try again")
else:
    print("access denied")