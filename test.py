import pandas as pd




data = {
    'id' : [1,2,3,4],
    'value' : [True, '2', '3', '4']
}

df = pd.DataFrame(data)
print(df.id.values.tolist())


df = df[
    (df.id == 2) & (df.value == 3) 
]
print(df.id.values.tolist())