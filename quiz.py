import pandas as pd 
import numpy as np
import os

wkdir =os.path.dirname(os.path.abspath(__file__))
file = os.path.join(wkdir,"quiz.csv")

def UI(file):
    # Import csv file
    df = pd.read_csv(file, header=0)
    # Calculate weighting
    prop = Weighting(df)   

    cont = ""
    while cont != "F":
        # Update df after each quiz
        df = quiz(df, prop)
        cont = input("Continue? (F for quit)")
    
    # Saving
    save = input("Save? (T/F)")
    while save not in ["T", "F"]:
        save = input("Save? (T/F)")
    if save == "T":
        df.to_csv(file, index=False)

        
def Weighting(df):
    total_times = df["Tested times"].sum()
    dic_importance = {"A": 1.5, "B": 1, "C":0.5}
    
    # adjust by +1 to avoid 0 being denominator
    importance = np.array([*map(lambda x: dic_importance[x], df["Importance"])])
    tested_freq = (df["Tested times"]+1) / total_times
    average_score = (df["Average score"]+1) 
    
    weight = importance * (1/tested_freq) * (1/average_score)
    prop = weight / weight.sum()

    return prop

def quiz(df, prop):
    wdf = df.copy()
    
    # Capturing qustion and answers
    entry = wdf.sample(weights=prop).T.dropna()
    q = entry.loc["Question"].reset_index(drop=True)[0]
    a = entry.iloc[4:].reset_index(drop=True)
    a
    # Creating a mask for updating parameters
    mask = wdf["Question"] == q
    
    # Asking questions
    print("\n", q,"\n")
    
    # Showing hint
    show_hint = input("Show hint? (T for showing hint)")   
    if show_hint == "T":
        l = f"{len(a)} entries" if len(a)>1 else "1 entry"
        print("\n",l,"in the answer")
        
    # Showing answer
    input("Showing answer... (Press any key)\n") 
    show = list(a.iloc[:,0])
    for ans in show:
        print(ans)

    # Asking for feedback for updating parameters
    score = input("You score? (from 0 to 10)")
    while score not in [*map(str,[*range(11)])]:
        score = input("You score? (from 0 to 10)")
    score = int(score)
    
    # Updates Tested Times
    wdf.loc[mask,"Tested times"] += 1
    # Updates score
    old_total_score = int(entry.loc["Average score"] * entry.loc["Tested times"])
    new_score = (old_total_score + score) / wdf.loc[mask,"Tested times"]
    wdf.loc[mask,"Average score"] = new_score
    
    return wdf
        
UI(file)