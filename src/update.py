import pandas as pd

CURRENT_MPS_SRC = "https://www.theyworkforyou.com/mps/?f=csv"
CURRENT_CONS_SRC = "https://lda.data.parliament.uk/constituencies.csv?exists-endedDate=false&_view=Constituencies&_pageSize=500&_page={}"

mps = pd.read_csv(CURRENT_MPS_SRC)


mps["MP Full Name"] = mps["First name"] + " " + mps["Last name"]
mps = mps.filter(items={"Constituency","MP Full Name","Party"})
mps = mps.replace(to_replace="Weston-Super-Mare",value="Weston-super-Mare")

cons = pd.concat([pd.read_csv(CURRENT_CONS_SRC.format(0)),pd.read_csv(CURRENT_CONS_SRC.format(1))]).filter(items={"gss code", "label"})

cons = cons.rename(columns={"label" : "Constituency","gss code" : "GSS Code"})
cons = cons.filter(items={"GSS Code", "Constituency"})


combined = pd.merge(left=cons,right=mps,on="Constituency",how="outer")
combined = combined[["GSS Code","Constituency","MP Full Name","Party"]]
combined.sort_values(["GSS Code"],inplace=True)
combined.to_csv("data//constituency-info-simple.csv",index=False)
