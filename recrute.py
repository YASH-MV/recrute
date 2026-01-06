"""
RecruitIQ — Intelligent HR Analytics & Interview Evaluation Platform

Main entry point for the RecruitIQ application.
Run with: streamlit run recrute.py
"""

import streamlit as st
from datetime import datetime
import pandas as pd
from pathlib import Path

# Import our modules
from src import data
from src import tab_interview
from src import plots


def main():
    st.set_page_config(
        page_title="RecruitIQ",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize database
    data.init_db()
    
    # Custom CSS for better styling
    st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: 700;
            color: #1f77b4;
            margin-bottom: 0.5rem;
        }
        .sub-header {
            color: #666;
            font-size: 1.1rem;
            margin-bottom: 2rem;
        }
        .metric-card {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #1f77b4;
        }
        .stButton>button {
            width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Main Header
    st.markdown('<h1 class="main-header">🎯 RecruitIQ</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Intelligent HR Analytics & Interview Evaluation Platform</p>', unsafe_allow_html=True)
    
    # Sidebar Navigation
    st.sidebar.title("📊 Navigation")
    page = st.sidebar.radio(
        "Select Module",
        ["🏢 Interview Evaluation", "📈 Analytics Dashboard", "🔍 Candidate Ranking", "📊 Visualizations", "⚙️ Data Management"]
    )
    
    # Page Routing
    if page == "🏢 Interview Evaluation":
        tab_interview.show_interview()
    elif page == "📈 Analytics Dashboard":
        show_analytics_dashboard()
    elif page == "🔍 Candidate Ranking":
        show_ranking_module()
    elif page == "📊 Visualizations":
        show_visualizations()
    elif page == "⚙️ Data Management":
        show_data_management()


def show_analytics_dashboard():
    """Main analytics dashboard with key metrics"""
    st.header("📈 Analytics Dashboard")
    
    sessions = data.list_sessions()
    if not sessions:
        st.info("No sessions available. Create an interview session first.")
        return
    
    # Session selector
    session_options = {f"{s['name']} ({s.get('date', 'N/A')})": s['id'] for s in sessions}
    selected_session = st.selectbox("Select Session", list(session_options.keys()))
    session_id = session_options[selected_session]
    
    # Get aggregated data
    candidates = data.list_candidates(session_id)
    
    if not candidates:
        st.info("No candidates in this session yet.")
        return
    
    # Calculate metrics
    total_candidates = len(candidates)
    
    # Get all scores
    all_scores = []
    for cand in candidates:
        scores = data.get_scores_for_candidate(cand['id'])
        if scores:
            score_dict = {s['metric']: s['value'] for s in scores}
            score_dict['candidate_name'] = cand['name']
            all_scores.append(score_dict)
    
    if not all_scores:
        st.info("No scores recorded yet. Start evaluating candidates.")
        return
    
    df_scores = pd.DataFrame(all_scores)
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Candidates", total_candidates)
    
    with col2:
        avg_total = df_scores.drop('candidate_name', axis=1).mean().mean() if len(df_scores) > 0 else 0
        st.metric("Average Score", f"{avg_total:.2f}")
    
    with col3:
        completed = len([c for c in candidates if data.get_scores_for_candidate(c['id'])])
        st.metric("Evaluated", f"{completed}/{total_candidates}")
    
    with col4:
        top_score = df_scores.drop('candidate_name', axis=1).max().max() if len(df_scores) > 0 else 0
        st.metric("Highest Score", f"{top_score:.2f}")
    
    st.divider()
    
    # Score distribution
    st.subheader("Score Distribution by Metric")
    metrics = [col for col in df_scores.columns if col != 'candidate_name']
    
    if metrics:
        fig_dist = plots.plot_score_distribution(df_scores, metrics)
        st.plotly_chart(fig_dist, use_container_width=True)
    
    # Performance by candidate
    st.subheader("Performance Overview")
    fig_overview = plots.plot_multi_metric_comparison(df_scores)
    st.plotly_chart(fig_overview, use_container_width=True)


def show_ranking_module():
    """Advanced candidate ranking and comparison"""
    st.header("🔍 Candidate Ranking Engine")
    
    sessions = data.list_sessions()
    if not sessions:
        st.info("No sessions available.")
        return
    
    session_options = {f"{s['name']} ({s.get('date', 'N/A')})": s['id'] for s in sessions}
    selected_session = st.selectbox("Select Session", list(session_options.keys()))
    session_id = session_options[selected_session]
    
    candidates = data.list_candidates(session_id)
    if not candidates:
        st.info("No candidates in this session.")
        return
    
    # Get all candidate data with scores
    candidate_data = []
    for cand in candidates:
        scores = data.get_scores_for_candidate(cand['id'])
        if scores:
            data_dict = {
                'id': cand['id'],
                'name': cand['name'],
                'position': cand.get('position', 'N/A'),
                'experience': cand.get('experience_years', 0)
            }
            for score in scores:
                data_dict[score['metric']] = score['value']
            candidate_data.append(data_dict)
    
    if not candidate_data:
        st.info("No scores recorded. Score candidates first.")
        return
    
    df = pd.DataFrame(candidate_data)
    metrics = [col for col in df.columns if col not in ['id', 'name', 'position', 'experience']]
    
    if not metrics:
        st.info("No metrics available.")
        return
    
    # Ranking options
    st.subheader("Ranking Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        ranking_metric = st.selectbox("Rank by Metric", metrics)
        top_n = st.number_input("Show Top N", min_value=1, max_value=len(df), value=min(10, len(df)))
        normalize = st.checkbox("Normalize Scores", value=False)
    
    with col2:
        weight_method = st.radio(
            "Ranking Method",
            ["Single Metric", "Weighted Average", "Composite Score"]
        )
        
        if weight_method == "Weighted Average":
            st.write("Set weights for each metric:")
            weights = {}
            for metric in metrics:
                weights[metric] = st.slider(f"{metric}", 0.0, 1.0, 1.0, 0.1, key=f"weight_{metric}")
    
    # Calculate rankings
    if weight_method == "Single Metric":
        df_ranked = df.sort_values(by=ranking_metric, ascending=False).head(top_n)
        df_ranked['rank'] = range(1, len(df_ranked) + 1)
        df_ranked = df_ranked[['rank', 'name', ranking_metric]]
    
    elif weight_method == "Weighted Average":
        df['weighted_score'] = sum(df[metric] * weights.get(metric, 1.0) for metric in metrics)
        df_ranked = df.sort_values(by='weighted_score', ascending=False).head(top_n)
        df_ranked['rank'] = range(1, len(df_ranked) + 1)
        df_ranked = df_ranked[['rank', 'name', 'weighted_score'] + metrics]
    
    else:  # Composite Score
        if normalize:
            for metric in metrics:
                df[metric + '_norm'] = (df[metric] - df[metric].min()) / (df[metric].max() - df[metric].min())
            composite_cols = [m + '_norm' for m in metrics]
        else:
            composite_cols = metrics
        
        df['composite_score'] = df[composite_cols].mean(axis=1)
        df_ranked = df.sort_values(by='composite_score', ascending=False).head(top_n)
        df_ranked['rank'] = range(1, len(df_ranked) + 1)
        df_ranked = df_ranked[['rank', 'name', 'composite_score'] + metrics]
    
    # Display rankings
    st.subheader(f"🏆 Top {top_n} Candidates")
    st.dataframe(df_ranked, use_container_width=True, hide_index=True)
    
    # Visualization
    st.subheader("Ranking Visualization")
    
    if weight_method == "Single Metric":
        fig = plots.plot_single_metric_ranking(df_ranked, ranking_metric)
    else:
        score_col = 'weighted_score' if weight_method == "Weighted Average" else 'composite_score'
        fig = plots.plot_multi_metric_ranking(df_ranked, metrics, score_col)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Radar chart for top candidates
    if st.checkbox("Show Detailed Radar Chart"):
        selected_candidate = st.selectbox("Select Candidate", df_ranked['name'].tolist())
        candidate_row = df[df['name'] == selected_candidate].iloc[0]
        
        fig_radar = plots.plot_radar_chart(candidate_row, metrics)
        st.plotly_chart(fig_radar, use_container_width=True)


def show_visualizations():
    """Advanced visualizations module"""
    st.header("📊 Visual Intelligence")
    
    sessions = data.list_sessions()
    if not sessions:
        st.info("No sessions available.")
        return
    
    session_options = {f"{s['name']} ({s.get('date', 'N/A')})": s['id'] for s in sessions}
    selected_session = st.selectbox("Select Session", list(session_options.keys()))
    session_id = session_options[selected_session]
    
    candidates = data.list_candidates(session_id)
    if not candidates:
        st.info("No candidates in this session.")
        return
    
    # Get all scores
    all_scores = []
    for cand in candidates:
        scores = data.get_scores_for_candidate(cand['id'])
        if scores:
            score_dict = {s['metric']: s['value'] for s in scores}
            score_dict['candidate_name'] = cand['name']
            all_scores.append(score_dict)
    
    if not all_scores:
        st.info("No scores available.")
        return
    
    df = pd.DataFrame(all_scores)
    metrics = [col for col in df.columns if col != 'candidate_name']
    
    # Visualization options
    viz_type = st.selectbox(
        "Select Visualization Type",
        ["Multi-Metric Comparison", "Score Distribution", "Candidate Radar", "Performance Heatmap"]
    )
    
    if viz_type == "Multi-Metric Comparison":
        st.subheader("Multi-Metric Comparison")
        fig = plots.plot_multi_metric_comparison(df)
        st.plotly_chart(fig, use_container_width=True)
    
    elif viz_type == "Score Distribution":
        st.subheader("Score Distribution by Metric")
        selected_metric = st.selectbox("Select Metric", metrics)
        fig = plots.plot_metric_distribution(df, selected_metric)
        st.plotly_chart(fig, use_container_width=True)
    
    elif viz_type == "Candidate Radar":
        st.subheader("Candidate Skill Radar")
        selected_candidate = st.selectbox("Select Candidate", df['candidate_name'].tolist())
        candidate_row = df[df['candidate_name'] == selected_candidate].iloc[0]
        fig = plots.plot_radar_chart(candidate_row, metrics, name_col='candidate_name')
        st.plotly_chart(fig, use_container_width=True)
    
    elif viz_type == "Performance Heatmap":
        st.subheader("Performance Heatmap")
        fig = plots.plot_performance_heatmap(df, metrics)
        st.plotly_chart(fig, use_container_width=True)


def show_data_management():
    """Data management and export"""
    st.header("⚙️ Data Management")
    
    sessions = data.list_sessions()
    
    if not sessions:
        st.info("No sessions available.")
        return
    
    # Session management
    st.subheader("Sessions")
    session_df = pd.DataFrame(sessions)
    st.dataframe(session_df[['name', 'interviewer', 'date']], use_container_width=True, hide_index=True)
    
    # Export data
    st.subheader("Export Data")
    
    session_options = {f"{s['name']} ({s.get('date', 'N/A')})": s['id'] for s in sessions}
    selected_session = st.selectbox("Select Session to Export", list(session_options.keys()))
    session_id = session_options[selected_session]
    
    # Prepare export data
    candidates = data.list_candidates(session_id)
    export_data = []
    
    for cand in candidates:
        scores = data.get_scores_for_candidate(cand['id'])
        row = {
            'Candidate Name': cand['name'],
            'Email': cand.get('email', ''),
            'Position': cand.get('position', ''),
            'Experience (Years)': cand.get('experience_years', 0)
        }
        
        if scores:
            for score in scores:
                row[score['metric']] = score['value']
        else:
            for metric in tab_interview.METRICS:
                row[metric] = None
        
        export_data.append(row)
    
    export_df = pd.DataFrame(export_data)
    
    st.dataframe(export_df, use_container_width=True)
    
    # Download button
    csv = export_df.to_csv(index=False)
    st.download_button(
        label="📥 Download as CSV",
        data=csv,
        file_name=f"recruitiq_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )
    
    # Statistics
    st.subheader("Database Statistics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Sessions", len(sessions))
    
    with col2:
        total_candidates = sum(len(data.list_candidates(s['id'])) for s in sessions)
        st.metric("Total Candidates", total_candidates)
    
    with col3:
        conn = data.get_conn()
        cur = conn.execute("SELECT COUNT(*) as count FROM scores")
        total_scores = cur.fetchone()['count']
        conn.close()
        st.metric("Total Scores", total_scores)


if __name__ == "__main__":
    main()

