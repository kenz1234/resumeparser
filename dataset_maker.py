import pandas as pd
import random


NUM_ROWS = 20000
PYTHON_TECHS = ['python', 'pandas', 'numpy', 'flask', 'django']
OTHER_TECHS = ['java', 'spring', 'javascript', 'react', 'node', 'csharp', 'go', 'ruby', 'php', 'html', 'css']


data = []
count_1 = 0
count_0 = 0
i = 1


while len(data) < NUM_ROWS:
    experience = random.randint(0, 20)

    if count_1 < 10000:
        tech = random.choice(PYTHON_TECHS)
        dependent = 1 if experience > 5 else 0
        if dependent == 1:
            data.append([i, f"user{i}@example.com", experience, tech, dependent])
            count_1 += 1
            i += 1
    elif count_0 < 10000:
        tech = random.choice(OTHER_TECHS)
        dependent = 1 if experience > 5 and tech in PYTHON_TECHS else 0
        if dependent == 0:
            data.append([i, f"user{i}@example.com", experience, tech, dependent])
            count_0 += 1
            i += 1


df = pd.DataFrame(data, columns=["no","email","EXPERIENCE","TECH","dependend"])
df.to_csv("python_experience_dataset.csv", index=False)

print("CSV file 'python_5yrs.csv' created successfully!")
