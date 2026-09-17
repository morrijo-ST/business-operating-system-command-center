import random
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Business OS Command Center",layout="wide")
st.title("Business Operating System Command Center")
st.caption("Synthetic executive view of KPIs, initiatives, risks, decisions, and automated work queues.")
random.seed(77)
functions=["Finance","Sales","Operations","Customer Success","Product"]
kpis=pd.DataFrame([
    ["Revenue Attainment","Finance",.96,1.00],["Gross Margin","Finance",.61,.64],["Pipeline Coverage","Sales",3.2,3.5],["Renewal Rate","Customer Success",.91,.93],["On-Time Delivery","Operations",.88,.95],["Roadmap Delivery","Product",.82,.90]
],columns=["kpi","function","actual","target"])
kpis["attainment"]=kpis.actual/kpis.target
initiatives=[]
for i in range(35):
    initiatives.append({"initiative_id":f"I-{i+1:03}","function":random.choice(functions),"initiative":f"Operating Initiative {i+1}","status":random.choice(["On Track","On Track","At Risk","Blocked"]),"owner":f"Owner {random.randint(1,12)}","progress":random.randint(15,100),"priority":random.choice(["High","Medium","Low"])})
work=pd.DataFrame(initiatives)

c1,c2,c3,c4=st.columns(4)
c1.metric("KPIs On/Above Target",int((kpis.attainment>=1).sum()))
c2.metric("At-Risk / Blocked Initiatives",int(work.status.isin(["At Risk","Blocked"]).sum()))
c3.metric("High-Priority Initiatives",int((work.priority=="High").sum()))
c4.metric("Average Progress",f"{work.progress.mean():.0f}%")

st.subheader("Executive KPI health")
st.plotly_chart(px.bar(kpis,x="kpi",y="attainment",color="function",hover_data=["actual","target"]),use_container_width=True)

left,right=st.columns(2)
with left:
    st.subheader("Initiative status")
    s=work.groupby(["function","status"],as_index=False).size()
    st.plotly_chart(px.bar(s,x="function",y="size",color="status",barmode="stack"),use_container_width=True)
with right:
    st.subheader("Priority workload")
    p=work.groupby("priority",as_index=False).size()
    st.plotly_chart(px.pie(p,names="priority",values="size"),use_container_width=True)

risks=work[work.status.isin(["At Risk","Blocked"])].sort_values(["priority","progress"])
st.subheader("Executive attention queue")
st.dataframe(risks,use_container_width=True,hide_index=True)

under=kpis[kpis.attainment<1].sort_values("attainment")
brief="; ".join([f"{r.kpi} is at {r.attainment:.0%} of target" for _,r in under.iterrows()])
st.subheader("Management briefing")
st.info((brief+". ") if brief else "All KPIs are at or above target. "+f"There are {len(risks)} initiatives requiring executive attention. The operating system keeps KPI health, risks, and delivery work in one governed view.")
