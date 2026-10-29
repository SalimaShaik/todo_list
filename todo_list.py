
import streamlit as st
import pandas as pd
from datetime import date, timedelta

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="TaskFlow - To-Do List",
    page_icon="✅",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------
st.markdown("""
<style>
/* Main application background */
.stApp {
    background: linear-gradient(
        135deg,
        #f7f8ff,
        #f1f5ff,
        #f8fbff
    );
    color: #1e293b;
}

/* Main content */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #e8edff;
    border-right: 1px solid #dbe4ff;
}

/* Headings */
h1, h2, h3 {
    color: #172554;
}

/* Text inputs */
div[data-testid="stTextInput"] input {
    background-color: #ffffff !important;
    color: #1e293b !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 10px !important;
}

/* Select boxes */
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background-color: #ffffff;
    color: #1e293b;
    border-radius: 10px;
}

/* DATE INPUT BACKGROUND COLOR */
div[data-testid="stDateInput"] input {
    background-color: #E0ECFF !important;
    color: #1E293B !important;
    border: 1px solid #3B82F6 !important;
    border-radius: 10px !important;
    color-scheme: light !important;
}

/* Date input calendar button */
div[data-testid="stDateInput"] button {
    background-color: #E0ECFF !important;
    color: #1E293B !important;
    border-radius: 0 10px 10px 0 !important;
}

/* Date input focus */
div[data-testid="stDateInput"] input:focus {
    border-color: #2563EB !important;
    box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2) !important;
}

/* Buttons */
.stButton > button {
    background-color: #2453e6;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.55rem 1rem;
    font-weight: 600;
    transition: 0.2s ease;
}

.stButton > button:hover {
    background-color: #173fc4;
    color: white;
    border: none;
}

/* Download button */
.stDownloadButton > button {
    background-color: #0f766e;
    color: white;
    border: none;
    border-radius: 10px;
}

/* Metric cards */
div[data-testid="stMetric"] {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    padding: 18px;
    border-radius: 14px;
    box-shadow: 0 3px 10px rgba(30, 64, 175, 0.05);
}

/* Task cards */
.task-card {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-left: 5px solid #3b82f6;
    padding: 16px;
    border-radius: 12px;
    margin-bottom: 12px;
    box-shadow: 0 3px 8px rgba(15, 23, 42, 0.04);
}

/* Completed tasks */
.completed-card {
    border-left-color: #0d9488;
    opacity: 0.85;
}

/* Status labels */
.pending-label {
    color: #2453e6;
    font-weight: bold;
}

.completed-label {
    color: #0f766e;
    font-weight: bold;
}

/* Divider */
hr {
    border-color: #dbe4ff;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "next_task_id" not in st.session_state:
    st.session_state.next_task_id = 1

# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------
def add_task(name, category, priority, due_date):
    task = {
        "ID": st.session_state.next_task_id,
        "Task": name.strip(),
        "Category": category,
        "Priority": priority,
        "Due Date": due_date,
        "Completed": False,
        "Created Date": date.today()
    }

    st.session_state.tasks.append(task)
    st.session_state.next_task_id += 1


def delete_task(task_id):
    st.session_state.tasks = [
        task for task in st.session_state.tasks
        if task["ID"] != task_id
    ]


def toggle_task(task_id, completed):
    for task in st.session_state.tasks:
        if task["ID"] == task_id:
            task["Completed"] = completed
            break


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
with st.sidebar:
    st.title("⚙️ TaskFlow")
    st.caption("Your personal productivity manager")

    st.divider()

    st.header("🔎 Filters")

    search_query = st.text_input(
        "Search by name or ID",
        placeholder="Search tasks..."
    )

    categories = ["All"] + sorted({
        task["Category"] for task in st.session_state.tasks
    })

    selected_category = st.selectbox(
        "Category",
        categories
    )

    selected_status = st.selectbox(
        "Status",
        ["All", "Pending", "Completed"]
    )

    selected_priority = st.selectbox(
        "Priority",
        ["All", "High", "Medium", "Low"]
    )

    st.divider()

    st.markdown("### 📌 Task Status")
    st.markdown(
        '<span class="pending-label">🔵 Pending</span>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<span class="completed-label">🟢 Completed</span>',
        unsafe_allow_html=True
    )

    st.divider()

    if st.button("🗑️ Clear All Tasks", use_container_width=True):
        st.session_state.tasks = []
        st.rerun()


# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.title("✅ TaskFlow")
st.markdown(
    "### Organize your day. Track your goals. Get things done."
)

st.write(
    "Manage your daily activities, prioritize important work, "
    "and track your progress in one place."
)

st.divider()

# --------------------------------------------------
# DASHBOARD METRICS
# --------------------------------------------------
all_tasks = st.session_state.tasks

total_tasks = len(all_tasks)
completed_tasks = sum(
    task["Completed"] for task in all_tasks
)
pending_tasks = total_tasks - completed_tasks

overdue_tasks = sum(
    not task["Completed"] and task["Due Date"] < date.today()
    for task in all_tasks
)

completion_rate = (
    (completed_tasks / total_tasks) * 100
    if total_tasks > 0 else 0
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📋 Total Tasks", total_tasks)

with col2:
    st.metric("⏳ Pending", pending_tasks)

with col3:
    st.metric("✅ Completed", completed_tasks)

with col4:
    st.metric("⚠️ Overdue", overdue_tasks)

st.progress(
    int(completion_rate),
    text=f"Overall completion: {completion_rate:.1f}%"
)

st.divider()

# --------------------------------------------------
# ADD TASK FORM
# --------------------------------------------------
st.subheader("➕ Add a New Task")

with st.form("task_form", clear_on_submit=True):
    task_name = st.text_input(
        "Task name",
        placeholder="e.g. Complete Java practice"
    )

    col1, col2 = st.columns(2)

    with col1:
        category = st.selectbox(
            "Category",
            ["Study", "Work", "Personal", "Health", "Other"]
        )

    with col2:
        priority = st.selectbox(
            "Priority",
            ["High", "Medium", "Low"],
            index=1
        )

    due_date = st.date_input(
        "Due date",
        value=date.today() + timedelta(days=1),
        min_value=date(2000, 1, 1),
        max_value=date(2100, 12, 31),
        format="YYYY/MM/DD"
    )

    submitted = st.form_submit_button(
        "➕ Add Task",
        use_container_width=True
    )

    if submitted:
        if task_name.strip():
            add_task(
                task_name,
                category,
                priority,
                due_date
            )
            st.success("Task added successfully!")
            st.rerun()
        else:
            st.error("Please enter a task name.")

st.divider()

# --------------------------------------------------
# FILTER TASKS
# --------------------------------------------------
filtered_tasks = []

for task in st.session_state.tasks:
    if search_query.strip():
        query = search_query.strip().lower()

        if (
            query not in task["Task"].lower()
            and query not in str(task["ID"])
        ):
            continue

    if (
        selected_category != "All"
        and task["Category"] != selected_category
    ):
        continue

    if (
        selected_status == "Pending"
        and task["Completed"]
    ):
        continue

    if (
        selected_status == "Completed"
        and not task["Completed"]
    ):
        continue

    if (
        selected_priority != "All"
        and task["Priority"] != selected_priority
    ):
        continue

    filtered_tasks.append(task)

# --------------------------------------------------
# TASK LIST
# --------------------------------------------------
st.subheader("📝 Your Tasks")

if not filtered_tasks:
    st.info(
        "No tasks found. Add a new task or change your filters."
    )
else:
    # Pending tasks first, then due date
    filtered_tasks.sort(
        key=lambda task: (
            task["Completed"],
            task["Due Date"]
        )
    )

    for task in filtered_tasks:
        task_id = task["ID"]

        with st.container(border=True):
            left, middle, right = st.columns(
                [0.65, 0.22, 0.13]
            )

            with left:
                checked = st.checkbox(
                    task["Task"],
                    value=task["Completed"],
                    key=f"complete_{task_id}"
                )

                if checked != task["Completed"]:
                    toggle_task(task_id, checked)
                    st.rerun()

                if task["Completed"]:
                    st.markdown(
                        '<span class="completed-label">'
                        '🟢 Completed</span>',
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        '<span class="pending-label">'
                        '🔵 Pending</span>',
                        unsafe_allow_html=True
                    )

                st.caption(
                    f"ID: {task_id}  |  "
                    f"Category: {task['Category']}  |  "
                    f"Priority: {task['Priority']}"
                )

                st.caption(
                    f"📅 Due date: "
                    f"{task['Due Date'].strftime('%d %b %Y')}"
                )

                if (
                    not task["Completed"]
                    and task["Due Date"] < date.today()
                ):
                    st.error("This task is overdue.")
                elif (
                    not task["Completed"]
                    and task["Due Date"] == date.today()
                ):
                    st.warning("This task is due today.")

            with middle:
                if task["Priority"] == "High":
                    st.error("🔴 High")
                elif task["Priority"] == "Medium":
                    st.warning("🟡 Medium")
                else:
                    st.success("🟢 Low")

            with right:
                if st.button(
                    "🗑️ Delete",
                    key=f"delete_{task_id}"
                ):
                    delete_task(task_id)
                    st.rerun()

# --------------------------------------------------
# PROGRESS AND CATEGORY ANALYSIS
# --------------------------------------------------
st.divider()
st.subheader("📊 Progress Dashboard")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown("#### Completion Status")

    if all_tasks:
        status_data = pd.DataFrame({
            "Status": ["Completed", "Pending"],
            "Tasks": [completed_tasks, pending_tasks]
        })

        st.bar_chart(
            status_data.set_index("Status")
        )
    else:
        st.info("Add tasks to view your progress.")

with chart_col2:
    st.markdown("#### Tasks by Category")

    if all_tasks:
        category_counts = {}

        for task in all_tasks:
            cat = task["Category"]
            category_counts[cat] = category_counts.get(cat, 0) + 1

        category_data = pd.DataFrame({
            "Category": list(category_counts.keys()),
            "Tasks": list(category_counts.values())
        })

        st.bar_chart(
            category_data.set_index("Category")
        )
    else:
        st.info("Add tasks to view category statistics.")

# --------------------------------------------------
# EXPORT TASKS TO CSV
# --------------------------------------------------
st.divider()
st.subheader("📥 Export Your Tasks")

if all_tasks:
    export_data = []

    for task in all_tasks:
        export_data.append({
            "ID": task["ID"],
            "Task": task["Task"],
            "Category": task["Category"],
            "Priority": task["Priority"],
            "Due Date": task["Due Date"].isoformat(),
            "Completed": task["Completed"],
            "Created Date": task["Created Date"].isoformat()
        })

    df = pd.DataFrame(export_data)

    st.download_button(
        label="⬇️ Download Tasks as CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="taskflow_tasks.csv",
        mime="text/csv"
    )
else:
    st.info("There are no tasks to export yet.")

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.divider()

st.markdown(
    "<div style='text-align:center; color:#64748b;'>"
    "TaskFlow | Stay organized. Stay productive. 🚀"
    "</div>",
    unsafe_allow_html=True
)
