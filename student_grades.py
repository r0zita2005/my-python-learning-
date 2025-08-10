grades=[]
cont=int(input("How many scores do you want to enter?"))
for i in range(cont):
    grade=float(input(f"Enter the score of person {i+1}."))
    grades.append(grade)
print("average: ", sum(grades)/len(grades))
print("max: ", max(grades))
print("min: ",min(grades))