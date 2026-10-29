import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, timedelta

st.set_page_config(page_title="TaskFlow To-Do", page_icon="✅", layout="wide")

# High-contrast, readable light theme
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f3f6fb, #eef3ff, #f8fafc);
    color: #172033;
}
.block-container {
    max-width: 1400px;
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}
.stApp h1, .stApp h2, .stApp h3, .stApp h4,
.stApp p, .stApp label, .stApp span,
.stApp .stMarkdown, [data-testid="stCaptionContainer"] {
    color: #172033;
}
.hero {
    padding: 1.7rem;
    border-radius: 22px;
    color: #ffffff !important;
    background: linear-gradient(115deg, #172554, #0f766e, #2563eb);
    margin-bottom: 1.2rem;
    box-shadow: 0 8px 22px rgba(30, 64, 175, .15);
}
.hero h1 {
    color: #ffffff !important;
    margin: 0;
}
.hero p {
    color: #eaf2ff !important;
    margin: .3rem 0 0;
}
.kpi {
    background: #ffffff;
    border: 1px solid #d8e0ed;
    border-radius: 16px;
    padding: 1rem;
    min-height: 100px;
    box-shadow: 0 3px 12px rgba(15, 23, 42, .05);
}
.klabel {
    color: #475569 !important;
    font-size: .85rem;
}
.kvalue {
    font-size: 1.7rem;
    font-weight: 750;
    color: #12316b !important;
}
/* Sidebar */
[data-testid="stSidebar"] {
    background: #eaf0fa;
    border-right: 1px solid #d8e0ed;
}
[data-testid="stSidebar"] * {
    color: #172033 !important;
}
/* Inputs and dropdowns */
.stApp input, .stApp textarea,
.stApp [data-baseweb="select"] > div,
.stApp [data-baseweb="input"] > div {
    background-color: #ffffff !important;
    color: #172033 !important;
    border-color: #b8c5d8 !important;
}
.stApp input::placeholder, .stApp textarea::placeholder {
    color: #64748b !important;
    opacity: 1;
}
.stApp [data-baseweb="select"] *,
.stApp [data-baseweb="popover"] * {
    color: #172033 !important;
}
.stApp [data-testid="stWidgetLabel"] label {
    color: #172033 !important;
    font-weight: 600;
}
/* Buttons */
.stApp button[kind="primary"],
.stApp [data-testid="stFormSubmitButton"] button,
.stApp [data-testid="stDownloadButton"] button {
    background: #1d4ed8 !important;
    color: #ffffff !important;
    border: 1px solid #1d4ed8 !important;
}
.stApp button[kind="primary"] *,
.stApp [data-testid="stFormSubmitButton"] button *,
.stApp [data-testid="stDownloadButton"] button * {
    color: #ffffff !important;
}
.stApp button[kind="secondary"] {
    background: #ffffff !important;
    color: #1d4ed8 !important;
    border: 1px solid #9bb6e8 !important;
}
.stApp button[kind="secondary"] * {
    color: #1d4ed8 !important;
}
/* Progress bar */
.stProgress > div > div > div {
    background-color: #2563eb !important;
}
/* Captions and helper text */
[data-testid="stCaptionContainer"] {
    color: #64748b !important;
}
/* Checkboxes */
.stApp [data-testid="stCheckbox"] label,
.stApp [data-testid="stCheckbox"] label p {
    color: #172033 !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="hero"><h1>✅ TaskFlow</h1>'
    '<p>Your productivity workspace • Prioritize wisely • Finish strong</p></div>',
    unsafe_allow_html=True
)

today = date.today()
sample = [
    {"Task": "Revise Python functions", "Category": "Study", "Priority": "High",
     "Due date": today + timedelta(days=1), "Done": False},
    {"Task": "Practice SQL joins", "Category": "Study", "Priority": "Medium",
     "Due date": today + timedelta(days=2), "Done": False},
    {"Task": "Prepare project report outline", "Category": "Project", "Priority": "High",
     "Due date": today + timedelta(days=3), "Done": False},
    {"Task": "Organize internship certificates", "Category": "Personal",
     "Priority": "Low", "Due date": today - timedelta(days=1), "Done": True}
]

if "tasks" not in st.session_state:
    st.session_state.tasks = pd.DataFrame(sample)

with st.sidebar:
    st.header("🧭 Task filters")
    sf = st.selectbox("Status", ["All", "Pending", "Completed", "Overdue"])
    cats = ["All"] + sorted(st.session_state.tasks["Category"].unique().tolist())
    cf = st.selectbox("Category", cats)
    pf = st.selectbox("Priority", ["All", "High", "Medium", "Low"])
    if st.button("Reset demo tasks", use_container_width=True):
        st.session_state.tasks = pd.DataFrame(sample)
        st.rerun()

tasks = st.session_state.tasks.copy()
tasks["Overdue"] = (
    tasks.apply(lambda r: not r["Done"] and r["Due date"] < today, axis=1)
    if len(tasks) else False
)
total = len(tasks)
done = int(tasks["Done"].sum()) if total else 0
pending = total - done
overdue = int(tasks["Overdue"].sum()) if total else 0
progress = round(done / total * 100) if total else 0

cols = st.columns(4)
for c, label, val, sub in zip(
    cols,
    ["Total tasks", "Completed", "Pending", "Overdue"],
    [total, done, pending, overdue],
    ["Tasks in workspace", "Nice work!", "Still on your list", "Past due and unfinished"]
):
    c.markdown(
        f'<div class="kpi"><div class="klabel">{label}</div>'
        f'<div class="kvalue">{val}</div><div class="klabel">{sub}</div></div>',
        unsafe_allow_html=True
    )

st.write("")
a, b = st.columns([1, 1.6])

with a:
    st.subheader("Your progress")
    st.progress(progress / 100)
    st.markdown(f"### {progress}% completed")
    if total:
        chart = px.pie(
            pd.DataFrame({"Status": ["Completed", "Pending"], "Tasks": [done, pending]}),
            names="Status",
            values="Tasks",
            hole=.65,
            color="Status",
            color_discrete_map={"Completed": "#0f766e", "Pending": "#647fea"}
        )
        chart.update_traces(
            textfont=dict(color="#ffffff", size=13),
            marker=dict(line=dict(color="#ffffff", width=2)),
            hoverlabel=dict(bgcolor="#ffffff", font=dict(color="#172033"))
        )
        chart.update_layout(
            height=280,
            margin=dict(l=0, r=0, t=5, b=0),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#172033", family="Arial", size=13),
            legend=dict(font=dict(color="#172033", size=12))
        )
        st.plotly_chart(chart, use_container_width=True)

with b:
    st.subheader("＋ Create a task")
    with st.form("new_task", clear_on_submit=True):
        title = st.text_input("Task name", placeholder="e.g. Complete Java practice")
        c1, c2 = st.columns(2)
        category = c1.selectbox(
            "Category", ["Study", "Project", "Work", "Personal", "Health", "Other"]
        )
        priority = c2.selectbox("Priority", ["High", "Medium", "Low"], index=1)
        due = st.date_input("Due date", value=today + timedelta(days=1))
        add = st.form_submit_button("Add task", use_container_width=True)
        if add:
            if not title.strip():
                st.error("Please enter a task name.")
            else:
                st.session_state.tasks = pd.concat(
                    [
                        st.session_state.tasks,
                        pd.DataFrame([{
                            "Task": title.strip(),
                            "Category": category,
                            "Priority": priority,
                            "Due date": due,
                            "Done": False
                        }])
                    ],
                    ignore_index=True
                )
                st.success("Task added.")
                st.rerun()

st.subheader("Your task board")
view = st.session_state.tasks.copy()
if len(view):
    view["Overdue"] = view.apply(
        lambda r: not r["Done"] and r["Due date"] < today, axis=1
    )

if sf == "Pending":
    view = view[~view["Done"]]
elif sf == "Completed":
    view = view[view["Done"]]
elif sf == "Overdue":
    view = view[view["Overdue"]]

if cf != "All":
    view = view[view["Category"] == cf]
if pf != "All":
    view = view[view["Priority"] == pf]

if view.empty:
    st.info("No tasks match these filters. Add a task or change the filters.")
else:
    for idx, row in view.iterrows():
        c1, c2, c3, c4, c5 = st.columns([.45, 4.2, 1.15, 1.3, 1])
        checked = c1.checkbox(
            "Done", value=bool(row["Done"]), key=f"done_{idx}",
            label_visibility="collapsed"
        )
        if checked != bool(row["Done"]):
            st.session_state.tasks.at[idx, "Done"] = checked
            st.rerun()

        task_text = str(row["Task"])
        if row["Done"]:
            c2.markdown(f"~~{task_text}~~")
        else:
            c2.markdown(f"**{task_text}**")
        c2.caption(f'{row["Category"]} · Due {row["Due date"].strftime("%d %b %Y")}')
        c3.markdown({"High": "🔴 High", "Medium": "🟠 Medium", "Low": "🟢 Low"}[row["Priority"]])
        c4.markdown(
            "⚠️ Overdue" if row["Overdue"]
            else "✅ Complete" if row["Done"]
            else "🕒 Pending"
        )
        if c5.button("Delete", key=f"del_{idx}"):
            st.session_state.tasks = (
                st.session_state.tasks.drop(index=idx).reset_index(drop=True)
            )
            st.rerun()

st.download_button(
    "⬇️ Export tasks as CSV",
    st.session_state.tasks.to_csv(index=False).encode("utf-8"),
    "todo_tasks.csv",
    "text/csv"
)
st.caption(
    "Demo tasks are examples. Tasks are stored in session state "
    "and may reset when the session restarts."
)
