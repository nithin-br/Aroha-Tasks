emp1_daily_sal = 1000
days = 31
emp1_sal = emp1_daily_sal * days
print('total salary of emp1:', emp1_sal)
emp2_daily_sal = 1
emp2_sal = []
a = emp2_daily_sal
emp2_sal.append(a)
for i in range(days):
    b = a + a
    a = b
    emp2_sal.append(a)
emp2_final_sal = sum(emp2_sal)
print('daily salary of emp2 for 31 days:', emp2_sal)
print('total salary of emp2:', emp2_final_sal)
