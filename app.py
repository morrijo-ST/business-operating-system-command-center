
import html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

def shell(name, title, subtitle, style):
    global PALETTE, INK, PANEL, BG, ACCENT
    themes = {
      'terminal': ('#091411','#10221d','#e7f5ee','#3fe0a0','#7e9c8d',4),
      'purple': ('#171625','#222137','#f5f1ff','#ba9bff','#9ca1c0',12),
      'indigo': ('#f4f5fb','#ffffff','#242746','#5149b9','#64708b',18),
      'coral': ('#faf7f2','#ffffff','#302a27','#c7543e','#796d65',20),
      'blue': ('#f2f6fa','#ffffff','#183348','#126bb5','#5d7486',8),
      'cyan': ('#07141d','#102330','#def5ff','#53d2ed','#8caab9',4),
      'ops': ('#0b1720','#132733','#e7f5f4','#4edbc4','#99b5bd',10),
      'editorial': ('#f8f7f3','#ffffff','#253b38','#317764','#6b7d77',6),
      'amber': ('#17212c','#223140','#f8f4e9','#efbc67','#a6b2bf',6),
    }
    BG,PANEL,INK,ACCENT,MUTED,RADIUS=themes[style]
    PALETTE=[ACCENT,'#4c9fd6','#d99455','#ae83c6','#6cae8b']
    px.defaults.color_discrete_sequence=PALETTE
    st.markdown(f"""<style>
    .stApp {{background:{BG};color:{INK}}}
    [data-testid="stHeader"] {{background:{BG};}}
    .block-container {{max-width:1480px;padding:2rem 2.5rem 4rem;}}
    [data-testid="stSidebar"] {{background:{PANEL};border-right:1px solid {MUTED}35;}}
    h1,h2,h3,p,label,[data-testid="stMarkdownContainer"], [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {{color:{INK};}}
    h1 {{font-size:2.55rem!important;letter-spacing:-.055em;line-height:1.12!important;font-weight:650!important;}}
    h2,h3 {{letter-spacing:-.025em;}}
    [data-testid="stCaptionContainer"] {{opacity:1!important;}}
    [data-testid="stCaptionContainer"] p {{color:{MUTED}!important;}}
    [data-tag] {{background:{ACCENT}25!important;color:{INK}!important;border:1px solid {ACCENT}50;}}
    [data-tag] span,[data-tag] button {{color:{INK}!important;}}
    [data-testid="stMetric"] {{background:{PANEL};border:1px solid {MUTED}30;border-top:2px solid {ACCENT};border-radius:{RADIUS}px;padding:18px 20px;}}
    [data-testid="stMetricValue"] {{font-variant-numeric:tabular-nums;font-size:1.8rem;}}
    [data-testid="stPlotlyChart"] {{background:{PANEL};border:1px solid {MUTED}30;border-radius:{RADIUS}px;overflow:hidden;}}
    [data-baseweb="select"] > div, [data-baseweb="input"], [data-baseweb="base-input"], textarea {{background:{PANEL}!important;color:{INK}!important;}}
    input,textarea {{color:{INK}!important;-webkit-text-fill-color:{INK}!important;}}
    [data-baseweb="tag"] {{background:{ACCENT}25!important;color:{INK}!important;}}
    [data-baseweb="tag"] span {{color:{INK}!important;}}
    button[kind="secondary"], [data-testid="stDownloadButton"] button {{background:{PANEL};color:{INK};border-color:{MUTED}65;}}
    [data-baseweb="tab"] {{color:{INK}!important;}}
    [data-testid="stAlert"] {{background:{PANEL};color:{INK};}}
    .eyebrow {{font:600 11px ui-monospace,monospace;letter-spacing:.15em;color:{ACCENT};margin-bottom:16px;}}
    .hero {{border-bottom:1px solid {MUTED}40;padding:12px 0 25px;margin-bottom:24px;}}
    .hero p {{max-width:850px;color:{MUTED};font-size:1rem;}}
    .brief {{border-left:3px solid {ACCENT};background:{PANEL};padding:16px 20px;margin:18px 0;color:{INK};}}
    @media(max-width:700px){{.block-container{{padding:1rem;}}h1{{font-size:1.8rem!important;}}}}
    </style>""",unsafe_allow_html=True)
    st.markdown(f'<div class="hero"><div class="eyebrow">MORRIS / {html.escape(name.upper())} · SYNTHETIC DEMO</div><h1>{html.escape(title)}</h1><p>{html.escape(subtitle)}</p></div>',unsafe_allow_html=True)
    st.sidebar.caption('MORRIS · PORTFOLIO LAB')
    st.sidebar.caption('Fictional data. Explore the workflow; no external systems are connected.')

def chart(fig, height=340):
    for axis in [fig.layout.xaxis,fig.layout.yaxis]:
        if axis.title.text:axis.title.text=axis.title.text.replace('_',' ').title()
    for trace in fig.data:
        if trace.name:trace.name=trace.name.replace('_',' ').title()
    fig.update_layout(template='plotly_white',paper_bgcolor=PANEL,plot_bgcolor=PANEL,font=dict(color=INK,size=12),colorway=PALETTE,height=height,margin=dict(l=55,r=25,t=55,b=55),legend=dict(orientation='h',y=-.24,x=0),hoverlabel=dict(bgcolor=PANEL,font_color=INK))
    fig.update_xaxes(automargin=True,gridcolor='rgba(128,145,155,.14)',zerolinecolor='rgba(128,145,155,.3)')
    fig.update_yaxes(automargin=True,gridcolor='rgba(128,145,155,.14)',zerolinecolor='rgba(128,145,155,.3)')
    st.plotly_chart(fig,use_container_width=True,theme=None)

def brief(text):
    st.markdown('<div class="brief">'+html.escape(text)+'</div>',unsafe_allow_html=True)

def money(value):
    sign='−' if value<0 else ''
    return f'{sign}${abs(value)/1e6:,.2f}M' if abs(value)>=1e6 else f'{sign}${abs(value):,.0f}'

def metrics(items):
    for col,(label,value) in zip(st.columns(len(items)),items):col.metric(label,value)

def table(df, name='detail', height=360):
    config={}
    for col in df.columns:
        label=str(col).replace('_',' ').title()
        if pd.api.types.is_numeric_dtype(df[col]) and not pd.api.types.is_bool_dtype(df[col]):
            if any(x in str(col) for x in ['pct','margin','confidence','attainment','probability','achievement']):
                config[col]=st.column_config.NumberColumn(label,format='%.3f')
            elif any(x in str(col) for x in ['amount','revenue','arr','acv','cost','expense','cash','earned','capitalized','amortization','balance','asset','budget','forecast','variance','value','backlog','receipts','payroll','subcontractor','materials','labor']):
                config[col]=st.column_config.NumberColumn(label,format='$%.2f')
            else:config[col]=st.column_config.NumberColumn(label)
        else:config[col]=st.column_config.Column(label)
    st.dataframe(df,use_container_width=True,hide_index=True,height=height,column_config=config)
    st.download_button('Download '+name.replace('_',' ')+' CSV',df.to_csv(index=False),name+'.csv','text/csv',key='export_'+name)

def nonempty(df):
    if df.empty:
        st.info('No records in this selection. Choose at least one filter value to continue.')
        st.stop()

import random
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Business OS Command Center",layout="wide")
shell('OPERATING REVIEW','Focus the leadership conversation.','Connect target gaps with accountable initiatives, blocked work, and the next management decision.','ops')
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


function=st.sidebar.selectbox('Function',['All functions']+functions)
if function!='All functions':
    kpis=kpis[kpis.function==function]
    work=work[work.function==function]
risks=work[work.status.isin(['At Risk','Blocked'])].copy()
risks['priority_order']=risks.priority.map({'High':0,'Medium':1,'Low':2})
risks=risks.sort_values(['priority_order','progress']).drop(columns='priority_order')
metrics([('KPIs at target',f'{int((kpis.attainment>=1).sum())} / {len(kpis)}'),('Blocked initiatives',str(int(work.status.eq('Blocked').sum()))),('At-risk initiatives',str(int(work.status.eq('At Risk').sum()))),('Average progress',f'{work.progress.mean():.0f}%')])
under=kpis[kpis.attainment<1].sort_values('attainment')
brief(('; '.join(f'{r.kpi}: {r.attainment:.0%} of target' for _,r in under.iterrows())+'. ' if len(under) else 'All selected KPIs meet target. ')+f'{len(risks)} initiatives need management attention.')
a,b=st.columns([1,1.8])
with a:
    st.subheader('Target gaps')
    for _,r in kpis.iterrows():
        st.write(f'**{r.kpi}**')
        st.progress(min(float(r.attainment),1),text=f'{r.attainment:.0%} of target')
        st.caption(f'Actual {r.actual:.2f}× / target {r.target:.2f}×' if r.kpi=='Pipeline Coverage' else f'Actual {r.actual:.0%} / target {r.target:.0%}')
with b:
    st.subheader('Leadership attention queue')
    table(risks,'executive_attention',420)
    if len(risks):
        selected=st.selectbox('Initiative briefing',risks.initiative_id.tolist())
        r=risks[risks.initiative_id==selected].iloc[0]
        st.info(f'{r.initiative} · {r.owner} · {r.status}. Next review: confirm the blocker, assign a concrete next step, and agree a due date.')
with st.expander('All initiatives'):table(work,'initiatives')
st.caption('KPIs and initiatives are fictional fixtures. This screen demonstrates a management review workflow; no autonomous agents are connected.')
