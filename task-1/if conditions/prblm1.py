#asking users input
height=float(input("enter height in meters: "))
weight=float(input("enter weight in kilogram: "))
BMI=weight/(height**2)
#categories
if BMI>=30:
 category ="obesity"
elif 25<= BMI <=29:
 category="overweight"
elif 18.5<= BMI <=25:
 category = "normal"
else:
 category = "underweight"
print(f"bmi: {BMI:.2F}")
print("categories:",category)