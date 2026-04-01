import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
from plotly import graph_objs
from typing import Literal


def sub_rate_plot():
    df = pd.read_csv("data/sub_rate.csv")
    freq = df.sort_values("total_minutes_watched").groupby("buckets", as_index=False, sort=False).student_id.count()
    freq["sub_rate"] = df.sort_values("total_minutes_watched").groupby("buckets", sort=False).f2p.sum().values / freq.student_id.values
    
    fig = make_subplots(specs=[[{"secondary_y": True}]], subplot_titles=["Free Plan Students Engagement Groups"])
    fig.add_trace(
        graph_objs.Bar(x=freq.buckets, y=freq.student_id, name="student count"),
        secondary_y=False
    )
    fig.add_trace(
        graph_objs.Scatter(x=freq.buckets, y=freq.sub_rate, name="subscription rate"),
        secondary_y=True
    )
    fig.update_layout(
        hovermode="x unified",
        xaxis=dict(title="minutes watched")
    )

    return fig

def sub_duration_plot():
    df = pd.read_csv("data/sub_duration.csv")
    freq = df.sort_values("total_minutes_watched").groupby("buckets", as_index=False, sort=False).student_id.count()
    df.num_paid_days = df.num_paid_days.str.extract(r"(\d+)").astype(int)
    freq["mean_sub_days"] = np.round(df.sort_values("total_minutes_watched").groupby("buckets", sort=False).num_paid_days.sum().values / freq.student_id.values)

    fig = make_subplots(specs=[[{"secondary_y": True}]], subplot_titles=["Subscribed Students Engagement Groups"])
    fig.add_trace(
        graph_objs.Bar(x=freq.buckets, y=freq.student_id, name="student count"),
        secondary_y=False
    )
    fig.add_trace(
        graph_objs.Scatter(x=freq.buckets, y=freq.mean_sub_days, name="Avg. Subscription Duration (days)"),
        secondary_y=True
    )
    fig.update_layout(
        hovermode="x unified",
        xaxis=dict(title="minutes watched")
    )

    return fig

def consumption_plot(stud_type: Literal["All", "Free", "Paid"]):
    df = pd.read_csv("data/learning.csv")
    df["month"] = pd.to_datetime(df.date_watched).dt.strftime("%Y-%m")
    df_grouped = df.groupby(["month", "paid"], as_index=False).minutes_watched.sum()
    df_grouped["n_students"] = df.groupby(["month", "paid"]).student_id.nunique().values
    if stud_type == "All":
        df_filtered = df_grouped.groupby("month", as_index=False).minutes_watched.sum()
        df_filtered["n_students"] = df_grouped.groupby("month").n_students.sum().values
    else:
        paid = {"Free": 0, "Paid": 1}
        df_filtered = df_grouped[df_grouped.paid == paid[stud_type]]

    fig = make_subplots(specs=[[{"secondary_y": True}]], subplot_titles=[f"Total Consumption; Type: {stud_type}"])
    fig.add_trace(
        graph_objs.Bar(x=df_filtered.month, y=df_filtered.minutes_watched, name="Total (min)"),
        secondary_y=False
    )
    mean_mins_per_student = np.round(df_filtered.minutes_watched.values / df_filtered.n_students.values, 2)
    fig.add_trace(
        graph_objs.Scatter(x=df_filtered.month, y=mean_mins_per_student, name="Average (min)"),
        secondary_y=True
    )
    fig.update_layout(
    hovermode="x unified",
    xaxis=dict(title="Month")
    )
    return fig

def cohort_table(stud_type: Literal["All", "Free", "Paid"]):
    df = pd.read_csv("data/cohorts.csv")
    if stud_type == "All":
        df_grouped = df.groupby(["cohort", "period"], as_index=False).student_id.nunique()
    else:
        paid = {"Free": 0, "Paid": 1}
        df_grouped = df.groupby(["cohort", "period", "paid"], as_index=False).student_id.nunique()
    table = pd.DataFrame(index=np.unique(df_grouped.cohort.values), columns=np.arange(10))
    for idx in table.index:
        for col in table.columns:
            try:
                if stud_type == "All":
                    table.loc[idx, col] = df_grouped[(df_grouped.cohort == idx) & (df_grouped.period == col)].student_id.values[0]
                else:
                    table.loc[idx, col] = df_grouped[(df_grouped.cohort == idx) &
                                                     (df_grouped.period == col) &
                                                     (df_grouped.paid == paid[stud_type])].student_id.values[0]
            except IndexError:
                continue
    
    fig = px.imshow(table, text_auto=True,
                    labels=dict(x="Month", y="Cohort", color="Active Students"),
                    title=f"Retention Cohorts; Type: {stud_type}")
    return fig

def retention_curve(stud_type: Literal["All", "Free", "Paid"]):
    df = pd.read_csv("data/cohorts.csv")
    if stud_type == "All":
        df_grouped = df.groupby(["cohort", "period"], as_index=False).student_id.nunique()
    else:
        paid = {"Free": 0, "Paid": 1}
        df_grouped = df.groupby(["cohort", "period", "paid"], as_index=False).student_id.nunique()
        df_grouped = df_grouped[df_grouped.paid == paid[stud_type]]
    df_grouped.loc[df_grouped.period == 0, "total"] = df_grouped.student_id
    df_grouped.total = df_grouped.total.ffill()
    df_grouped["relative"] = np.round(df_grouped.student_id / df_grouped.total * 100, 2)
    
    fig = px.line(df_grouped, x="period", y="relative", color="cohort",
                  labels={"period": "month", "relative": "percent"})
    return fig

def engagement_plot(view: Literal["Daily", "Monthly"],
                    stud_type: Literal["All", "Free", "Paid"],
                    period: tuple[np.datetime64]):
    df = pd.read_csv("data/engagement.csv")
    df.engagement_date = pd.to_datetime(df.engagement_date)
    df["month"] = df.engagement_date.dt.strftime("%Y-%m")
    df = df[(df.engagement_date >= period[0]) & (df.engagement_date <= period[1])]

    if stud_type != "All":
        paid = {"Free": 0, "Paid": 1}
        df = df[df.paid == paid[stud_type]]
    
    if view == "Daily":
        df_grouped = df.groupby("engagement_date", as_index=False).student_id.nunique()
        fig = px.line(x=df_grouped.engagement_date, y=df_grouped.student_id,
                      labels=dict(x="Day", y="Active Students"),
                      title=f"{view} Student Engagement; Type: {stud_type}")
    elif view == "Monthly":
        df_grouped = df.groupby("month", as_index=False).student_id.nunique()
        fig = px.bar(x=df_grouped.month, y=df_grouped.student_id,
                     labels=dict(x="Month", y="Active Students"),
                     title=f"{view} Student Engagement; Type: {stud_type}")
    
    return fig

def onboarding_plot(view: Literal["Daily", "Monthly"],
                    period: tuple[np.datetime64]):
    df = pd.read_csv("data/onboarded.csv")
    df.date_registered = pd.to_datetime(df.date_registered)
    df["month"] = df.date_registered.dt.strftime("%Y-%m")
    df["monthly_onboard_rate"] = df.groupby("month").onboarded.cumsum() / (df.groupby("month").student_id.cumcount() + 1)
    df["overall_onboard_rate"] = df.onboarded.cumsum() / (np.array(df.index) + 1)

    df = df[(df.date_registered >= period[0]) & (df.date_registered <= period[1])]

    if view == "Daily":
        fig = px.line(df, x="date_registered", y="overall_onboard_rate",
                      title="Cumulative Onboard Rate")
        fig.update_layout(yaxis_range=[0.4, 0.7])
    elif view == "Monthly":
        fig = px.line(df, x="date_registered", y="monthly_onboard_rate",
                      title="Cumulative Onboard Rate per Month")
    return fig

def exams_bar_plot(category: Literal["All", "Practice", "Course", "Career Track"]):
    df = pd.read_csv("data/exam_attempts.csv")
    df.date_exam_completed = pd.to_datetime(df.date_exam_completed)
    df["month"] = df.date_exam_completed.dt.strftime("%Y-%m")
    if category != "All":
        cat = {"Practice": 1, "Course": 2, "Career Track": 3}
        df = df[df.exam_category == cat[category]]

    df_fail = df[df.exam_passed == 0].groupby("month", as_index=False).exam_attempt_id.count()
    df_pass = df[df.exam_passed == 1].groupby("month", as_index=False).exam_attempt_id.count()

    fig = graph_objs.Figure(
        data=[
            graph_objs.Bar(name="Exams passed", x=df_pass.month, y=df_pass.exam_attempt_id),
            graph_objs.Bar(name="Exams failed", x=df_fail.month, y=df_fail.exam_attempt_id)
        ]
    )
    fig.update_layout(barmode="stack", title="Exams per Month")
    return fig

def career_track_funnel(track: Literal["Data Scientist", "Data Analyst", "Business Analyst"]):
    df = pd.read_csv("data/career_track_stats.csv")
    track_id = {"Data Scientist": 1, "Data Analyst": 2, "Business Analyst": 3}
    df = df[df.track_id == track_id[track]]
    fig = px.funnel(df, x="n_students", y="action", title=f"{track} Career Track Funnel")
    return fig

def certs_bar_plot(category: Literal["All", "Course", "Career Track"]):
    df = pd.read_csv("data/certs.csv")
    df.date_issued = pd.to_datetime(df.date_issued)
    df["month"] = df.date_issued.dt.strftime("%Y-%m")
    if category != "All":
        cat = {"Course": 1, "Career Track": 2}
        df = df[df.cert_type == cat[category]]

    df_free = df[df.paid == 0].groupby("month", as_index=False).cert_id.count()
    df_paid = df[df.paid == 1].groupby("month", as_index=False).cert_id.count()

    fig = graph_objs.Figure(
        data=[
            graph_objs.Bar(name="Free Plan", x=df_free.month, y=df_free.cert_id),
            graph_objs.Bar(name="Paid Plan", x=df_paid.month, y=df_paid.cert_id)
        ]
    )
    fig.update_layout(barmode="stack", title=f"{category} Certificates Issued")
    return fig

def ratings_plot():
    df = pd.read_csv("data/ratings.csv")
    freq = pd.DataFrame(data=[], columns=["rating", "rating_count"])
    freq.rating_count = df.value_counts().values
    freq.rating = [f"{i[0]} Star" for i in df.value_counts().index]

    fig = px.pie(freq, values="rating_count", names="rating", hole=0.6,
                 title="Course Ratings")
    fig.add_annotation(text=f"Average<br>Rating:<br>{df.course_rating.mean():.2f}",
                       showarrow=False)

    return fig

def courses_plot(metric: Literal["Total", "Per Student", "Completion Rate"],
                 limit: int):
    metrics = {"Total": "total_mins_watched",
               "Per Student": "mean_mins_per_student",
               "Completion Rate": "mean_completion_rate"}
    df = pd.read_csv("data/course_stats.csv").sort_values(metrics[metric])[-limit:]
    unit = " (min)" if metric != "Completion Rate" else ""

    fig = px.bar(df, y="title", x=metrics[metric], orientation="h",
                 title=f"Most Consumed Courses ({metric})")
    fig.update_layout(xaxis=dict(title=metric + unit))

    return fig

def engagement_kpi(period: tuple[np.datetime64],
                   stud_type: Literal["All", "Free", "Paid"]):
    df = pd.read_csv("data/engagement.csv")
    df.engagement_date = pd.to_datetime(df.engagement_date)
    df = df[(df.engagement_date >= period[0]) & (df.engagement_date <= period[1])]
    if stud_type != "All":
        paid = {"Free": 0, "Paid": 1}
        df = df[df.paid == paid[stud_type]]
    n = df.student_id.nunique()

    fig = graph_objs.Figure(
        data=graph_objs.Indicator(
            mode="number",
            value=n,
            title=dict(text="Engaged Students")
        )
    )
    
    return fig

def time_watched_kpi(period: tuple[np.datetime64],
                     stud_type: Literal["All", "Free", "Paid"]):
    df = pd.read_csv("data/learning.csv")
    df.date_watched = pd.to_datetime(df.date_watched)
    df = df[(df.date_watched >= period[0]) & (df.date_watched <= period[1])]
    if stud_type != "All":
        paid = {"Free": 0, "Paid": 1}
        df = df[df.paid == paid[stud_type]]
    n = df.minutes_watched.sum() / df.student_id.nunique()

    fig = graph_objs.Figure(
        data=graph_objs.Indicator(
            mode="number",
            value=n,
            title=dict(text="Mean Minutes Watched per Student")
        )
    )
    
    return fig

def certs_kpi(period: tuple[np.datetime64],
              stud_type: Literal["All", "Free", "Paid"]):
    df = pd.read_csv("data/certs.csv")
    df.date_issued = pd.to_datetime(df.date_issued)
    df = df[(df.date_issued >= period[0]) & (df.date_issued <= period[1])]
    if stud_type != "All":
        paid = {"Free": 0, "Paid": 1}
        df = df[df.paid == paid[stud_type]]
    n = df.cert_id.count()

    fig = graph_objs.Figure(
        data=graph_objs.Indicator(
            mode="number",
            value=n,
            title=dict(text="Certificates Issued"),
            number=dict(valueformat="f")
        )
    )
    
    return fig

