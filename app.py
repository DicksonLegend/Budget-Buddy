import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from uuid import uuid4
import psycopg2
from sqlalchemy import create_engine, text
import numpy as np
import os 

# Page config
st.set_page_config(
    page_title="Budget Buddy - Finance Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS for better styling and mobile responsiveness
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        animation: fadeInDown 0.8s ease-out;
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        text-align: center;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
        animation: slideIn 0.6s ease-out;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
    }
    
    .balance-positive {
        color: #10b981;
        font-weight: 600;
        font-size: 1.2rem;
    }
    
    .balance-negative {
        color: #ef4444;
        font-weight: 600;
        font-size: 1.2rem;
    }
    
    .income-metric {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .expense-metric {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .balance-metric {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .insight-card {
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
        color: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .alert-card {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .success-card {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
        border-radius: 10px;
    }
    
    .stSelectbox > div > div {
        border-radius: 10px;
        border: 2px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .stButton > button {
        border-radius: 12px;
        border: none;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    }
    
    .transaction-item {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    .transaction-item:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .chart-container {
        background: white;
        border-radius: 15px;
        padding: 1rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        margin: 1rem 0;
    }
    
    .spending-card {
        background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
        color: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .spending-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }
        
        .metric-card {
            padding: 1rem;
            margin: 0.25rem 0;
        }
        
        .stButton > button {
            width: 100%;
            margin: 0.25rem 0;
        }
    }
    
    /* Dark mode support */
    @media (prefers-color-scheme: dark) {
        .metric-card {
            background: linear-gradient(135deg, #1f2937 0%, #374151 100%);
            color: white;
        }
    }
</style>
""", unsafe_allow_html=True)
@st.cache_resource
def get_database_connection():
    """Create database connection with timeout and better error handling for Railway deployment"""
    try:
        # Get DATABASE_URL from environment
        database_url = os.environ.get("DATABASE_URL")
        
        if not database_url:
            print("❌ DATABASE_URL not found!")
            return None
        
        # Clean up the URL and ensure SSL
        if "?sslmode=" not in database_url and "sslmode=" not in database_url:
            database_url += "?sslmode=require"
        
        print(f"🔗 Connecting to database...")
        
        # Create engine with optimized settings
        engine = create_engine(
            database_url,
            connect_args={
                "connect_timeout": 30,
                "application_name": "budget_buddy_railway"
            },
            pool_size=3,
            max_overflow=5,
            pool_timeout=30,
            pool_recycle=3600,
            pool_pre_ping=True,
            echo=False
        )
        
        # Test the connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1 as test"))
            test_result = result.fetchone()
            if test_result and test_result[0] == 1:
                print("✅ Database connection successful!")
                return engine
            else:
                raise Exception("Connection test failed")
        
    except Exception as e:
        print(f"❌ Database connection error: {str(e)}")
        return None

def initialize_database():
    """Initialize database tables with better error handling"""
    print("🔄 Initializing database...")
    
    engine = get_database_connection()
    if engine is None:
        return False
    
    try:
        with engine.connect() as conn:
            # Create transactions table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id SERIAL PRIMARY KEY,
                    user_id VARCHAR(255) NOT NULL,
                    type VARCHAR(50) NOT NULL,
                    category VARCHAR(255) NOT NULL,
                    amount DECIMAL(10,2) NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            # Create indexes
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_transactions_user_id 
                ON transactions(user_id)
            """))
            
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_transactions_date 
                ON transactions(created_at)
            """))
            
            conn.commit()
            print("✅ Database initialized successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Database initialization error: {str(e)}")
        return False

def initialize_session_state():
    """Initialize session state variables"""
    if 'user_id' not in st.session_state:
        st.session_state.user_id = str(uuid4())
    
    if 'db_initialized' not in st.session_state:
        st.session_state.db_initialized = initialize_database()
        
def clear_data_cache():
    """Clear all cached data"""
    try:
        # Clear specific cache functions
        if 'get_transactions' in globals():
            get_transactions.clear()
        if 'get_summary' in globals():
            get_summary.clear()
        if 'get_category_summary' in globals():
            get_category_summary.clear()
        if 'get_daily_summary' in globals():
            get_daily_summary.clear()
    except Exception as e:
        print(f"Warning: Could not clear cache: {str(e)}")

def refresh_data_from_db():
    """Refresh all data from database"""
    clear_data_cache()
    # Force rerun to refresh the UI
    st.rerun()

def add_transaction(transaction_type, category, amount, description=""):
    """Add a new transaction to database"""
    engine = get_database_connection()
    if engine is None:
        return False
    
    try:
        with engine.connect() as conn:
            conn.execute(text("""
                INSERT INTO transactions (user_id, type, category, amount, description)
                VALUES (:user_id, :type, :category, :amount, :description)
            """), {
                'user_id': st.session_state.user_id,
                'type': transaction_type,
                'category': category,
                'amount': float(amount),
                'description': description
            })
            conn.commit()
        
        # Clear cache immediately after adding
        clear_data_cache()
        
        return True
    except Exception as e:
        st.error(f"Error adding transaction: {str(e)}")
        return False

def clear_data_cache():
    """Clear all cached data"""
    try:
        get_transactions.clear()
        get_summary.clear()
        get_category_summary.clear()
        get_daily_summary.clear()
    except Exception as e:
        st.error(f"Error clearing cache: {str(e)}")

@st.cache_data(ttl=10)  # Cache for 10 seconds
def get_transactions():
    """Get all transactions from database"""
    engine = get_database_connection()
    if engine is None:
        return []
    
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT id, type, category, amount, description, created_at
                FROM transactions
                WHERE user_id = :user_id
                ORDER BY created_at DESC
            """), {'user_id': st.session_state.user_id})
            
            transactions = []
            for row in result:
                transactions.append({
                    'id': row[0],
                    'type': row[1],
                    'category': row[2],
                    'amount': float(row[3]),
                    'description': row[4],
                    'created_at': row[5]
                })
            
            return transactions
    except Exception as e:
        st.error(f"Error fetching transactions: {str(e)}")
        return []

@st.cache_data(ttl=10)  # Cache for 10 seconds
def get_summary():
    """Get income and expense summary"""
    engine = get_database_connection()
    if engine is None:
        return 0, 0
    
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT 
                    SUM(CASE WHEN type = 'Income' THEN amount ELSE 0 END) as income,
                    SUM(CASE WHEN type = 'Expense' THEN amount ELSE 0 END) as expense
                FROM transactions
                WHERE user_id = :user_id
            """), {'user_id': st.session_state.user_id}).fetchone()
            
            income = float(result[0] or 0)
            expense = float(result[1] or 0)
            return income, expense
    except Exception as e:
        st.error(f"Error getting summary: {str(e)}")
        return 0, 0

@st.cache_data(ttl=10)  # Cache for 10 seconds
def get_category_summary():
    """Get summary by category"""
    engine = get_database_connection()
    if engine is None:
        return []
    
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT category, type, SUM(amount) as total_amount
                FROM transactions
                WHERE user_id = :user_id
                GROUP BY category, type
                ORDER BY total_amount DESC
            """), {'user_id': st.session_state.user_id})
            
            categories = []
            for row in result:
                categories.append((row[0], row[1], float(row[2])))
            
            return categories
    except Exception as e:
        st.error(f"Error getting category summary: {str(e)}")
        return []

@st.cache_data(ttl=10)  # Cache for 10 seconds
def get_daily_summary():
    """Get daily transaction summary for the last 30 days"""
    engine = get_database_connection()
    if engine is None:
        return []
    
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT 
                    DATE(created_at) as date,
                    type,
                    SUM(amount) as total_amount
                FROM transactions
                WHERE user_id = :user_id 
                    AND created_at >= NOW() - INTERVAL '30 days'
                GROUP BY DATE(created_at), type
                ORDER BY date DESC
            """), {'user_id': st.session_state.user_id})
            
            daily_data = []
            for row in result:
                daily_data.append({
                    'date': row[0],
                    'type': row[1],
                    'amount': float(row[2])
                })
            
            return daily_data
    except Exception as e:
        st.error(f"Error getting daily summary: {str(e)}")
        return []

def clear_all_data():
    """Clear all user data"""
    engine = get_database_connection()
    if engine is None:
        return False
    
    try:
        with engine.connect() as conn:
            conn.execute(text("""
                DELETE FROM transactions WHERE user_id = :user_id
            """), {'user_id': st.session_state.user_id})
            conn.commit()
        
        # Clear cache after clearing data
        clear_data_cache()
        
        return True
    except Exception as e:
        st.error(f"Error clearing data: {str(e)}")
        return False



def format_currency(amount):
    """Format amount as Indian Rupees"""
    return f"₹{amount:,.2f}"

def get_spending_insights():
    """Get spending insights and alerts"""
    transactions = get_transactions()
    if not transactions:
        return []
    
    df = pd.DataFrame(transactions)
    df['created_at'] = pd.to_datetime(df['created_at'])
    
    insights = []
    
    # This month vs last month spending
    current_month = datetime.now().replace(day=1)
    last_month = (current_month - timedelta(days=1)).replace(day=1)
    
    current_month_expenses = df[
        (df['type'] == 'Expense') & 
        (df['created_at'] >= current_month)
    ]['amount'].sum()
    
    last_month_expenses = df[
        (df['type'] == 'Expense') & 
        (df['created_at'] >= last_month) & 
        (df['created_at'] < current_month)
    ]['amount'].sum()
    
    if last_month_expenses > 0:
        change = ((current_month_expenses - last_month_expenses) / last_month_expenses) * 100
        if change > 20:
            insights.append({
                'type': 'alert',
                'title': '🚨 High Spending Alert!',
                'message': f'Your spending increased by {change:.1f}% this month compared to last month.'
            })
        elif change < -20:
            insights.append({
                'type': 'success',
                'title': '🎉 Great Savings!',
                'message': f'You reduced spending by {abs(change):.1f}% this month. Keep it up!'
            })
    
    # Top spending category
    expense_df = df[df['type'] == 'Expense']
    if not expense_df.empty:
        top_category = expense_df.groupby('category')['amount'].sum().idxmax()
        top_amount = expense_df.groupby('category')['amount'].sum().max()
        total_expenses = expense_df['amount'].sum()
        
        if total_expenses > 0:
            percentage = (top_amount / total_expenses) * 100
            if percentage > 40:
                insights.append({
                    'type': 'insight',
                    'title': f'💡 Top Spending: {top_category}',
                    'message': f'{percentage:.1f}% of your expenses go to {top_category}. Consider budgeting for this category.'
                })
    
    # Savings rate
    income, expense = get_summary()
    if income > 0:
        savings_rate = ((income - expense) / income) * 100
        if savings_rate > 20:
            insights.append({
                'type': 'success',
                'title': '💰 Excellent Savings Rate!',
                'message': f'You\'re saving {savings_rate:.1f}% of your income. Financial experts recommend 20%+.'
            })
        elif savings_rate < 10:
            insights.append({
                'type': 'alert',
                'title': '⚠️ Low Savings Rate',
                'message': f'Your savings rate is {savings_rate:.1f}%. Try to aim for at least 20% of your income.'
            })
    
    return insights

def main():
    initialize_session_state()
    
    # Check database connection
    if not st.session_state.db_initialized:
        st.error("🚨 Database Connection Failed")
        st.error("Please check your Railway PostgreSQL service and try refreshing the page.")
        
        # Add a retry button
        if st.button("🔄 Retry Database Connection"):
            # Clear the initialization flag and retry
            if 'db_initialized' in st.session_state:
                del st.session_state['db_initialized']
            st.rerun()
        return

    # Fixed refresh button
    if st.sidebar.button("🔄 Refresh Data"):
        with st.spinner("Refreshing data..."):
            try:
                refresh_data_from_db()
                st.sidebar.success("✅ Data refreshed!")
            except Exception as e:
                st.sidebar.error(f"Error refreshing: {str(e)}")
    
    # Header with animation
    st.markdown('<h1 class="main-header">💰 Budget Buddy - Finance Tracker</h1>', unsafe_allow_html=True)
    
    # Sidebar navigation with icons
    st.sidebar.title("📊 Navigation")
    
    # Navigation options with icons
    nav_options = {
        "🏠 Dashboard": "Dashboard",
        "💰 Add Income": "Add Income", 
        "💸 Add Expense": "Add Expense",
        "📋 Transactions": "View Transactions",
        "🎯 Insights": "Insights",
        "📈 Analytics": "Analytics"
    }
    
    selected_nav = st.sidebar.selectbox("Choose a page", list(nav_options.keys()))
    page = nav_options[selected_nav]
    
    # Get current summary
    income, expense = get_summary()
    balance = income - expense
    
    # Enhanced sidebar summary
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Summary")
    
    # Sidebar metrics with better styling
    st.sidebar.markdown(f'''
    <div class="income-metric">
        <div style="font-size: 0.9rem; opacity: 0.9;">💰 Total Income</div>
        <div style="font-size: 1.5rem; font-weight: 700;">{format_currency(income)}</div>
    </div>
    ''', unsafe_allow_html=True)
    
    st.sidebar.markdown(f'''
    <div class="expense-metric">
        <div style="font-size: 0.9rem; opacity: 0.9;">💸 Total Expenses</div>
        <div style="font-size: 1.5rem; font-weight: 700;">{format_currency(expense)}</div>
    </div>
    ''', unsafe_allow_html=True)
    
    balance_color = "balance-positive" if balance >= 0 else "balance-negative"
    balance_icon = "📈" if balance >= 0 else "📉"
    
    st.sidebar.markdown(f'''
    <div class="balance-metric">
        <div style="font-size: 0.9rem; opacity: 0.9;">{balance_icon} Balance</div>
        <div style="font-size: 1.5rem; font-weight: 700;">{format_currency(balance)}</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Data management section
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🛠️ Data Management")
    
    if st.sidebar.button("🗑️ Clear All Data"):
        if st.sidebar.button("⚠️ Confirm Delete", key="confirm_delete"):
            if clear_all_data():
                st.success("All data cleared successfully!")
                st.rerun()
            else:
                st.error("Failed to clear data.")
    
    # Download functionality
    transactions = get_transactions()
    if transactions:
        df = pd.DataFrame(transactions)
        csv = df.to_csv(index=False)
        st.sidebar.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"budget_buddy_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    # Route to different pages
    if page == "Dashboard":
        show_dashboard(income, expense, balance)
    elif page == "Add Income":
        show_add_income()
    elif page == "Add Expense":
        show_add_expense()
    elif page == "View Transactions":
        show_transactions()
    elif page == "Insights":
        show_insights()
    elif page == "Analytics":
        show_analytics()

def show_dashboard(income, expense, balance):
    st.header("🏠 Dashboard")
    
    # Enhanced metrics with animations
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f'''
        <div class="metric-card">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">💰</div>
            <div style="font-size: 0.9rem; color: #6b7280; margin-bottom: 0.5rem;">Total Income</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #10b981;">{format_currency(income)}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="metric-card">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">💸</div>
            <div style="font-size: 0.9rem; color: #6b7280; margin-bottom: 0.5rem;">Total Expenses</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #ef4444;">{format_currency(expense)}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        balance_color = "#10b981" if balance >= 0 else "#ef4444"
        balance_icon = "📈" if balance >= 0 else "📉"
        st.markdown(f'''
        <div class="metric-card">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">{balance_icon}</div>
            <div style="font-size: 0.9rem; color: #6b7280; margin-bottom: 0.5rem;">Balance</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: {balance_color};">{format_currency(balance)}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Charts section
    if income > 0 or expense > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            # Daily balance trend (last 30 days)
            daily_data = get_daily_summary()
            if daily_data:
                df_daily = pd.DataFrame(daily_data)
                df_pivot = df_daily.pivot(index='date', columns='type', values='amount').fillna(0)
                df_pivot['balance'] = df_pivot.get('Income', 0) - df_pivot.get('Expense', 0)
                df_pivot['cumulative_balance'] = df_pivot['balance'].cumsum()
                
                fig_trend = px.line(
                    x=df_pivot.index,
                    y=df_pivot['cumulative_balance'],
                    title='💹 Daily Balance Trend (Last 30 Days)',
                    labels={'x': 'Date', 'y': 'Balance (₹)'}
                )
                fig_trend.update_layout(
                    height=400,
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                fig_trend.update_traces(line_color='#667eea', line_width=3)
                st.plotly_chart(fig_trend, use_container_width=True)
            else:
                st.info("📊 Add more transactions to see the trend chart.")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            # Enhanced income vs expenses pie chart
            if income > 0 and expense > 0:
                fig_pie = px.pie(
                    values=[income, expense],
                    names=['Income', 'Expenses'],
                    title='📊 Income vs Expenses',
                    color_discrete_map={'Income': '#10b981', 'Expenses': '#ef4444'}
                )
                fig_pie.update_layout(
                    height=400,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.info("📊 Add both income and expenses to see the chart.")
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Recent transactions with better styling
    st.markdown("### 📋 Recent Transactions")
    transactions = get_transactions()
    
    if transactions:
        recent_transactions = transactions[:5]
        for transaction in recent_transactions:
            icon = "💰" if transaction['type'] == 'Income' else "💸"
            color = "#10b981" if transaction['type'] == 'Income' else "#ef4444"
            date_str = transaction['created_at'].strftime('%d %b %Y')
            
            st.markdown(f'''
            <div class="transaction-item">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="display: flex; align-items: center;">
                        <div style="font-size: 1.5rem; margin-right: 0.5rem;">{icon}</div>
                        <div>
                            <div style="font-weight: 600; color: #1f2937;">{transaction['category']}</div>
                            <div style="font-size: 0.8rem; color: #6b7280;">{date_str}</div>
                        </div>
                    </div>
                    <div style="font-size: 1.2rem; font-weight: 700; color: {color};">
                        {format_currency(transaction['amount'])}
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
    else:
        st.info("📝 No transactions yet. Add some income or expenses to get started!")
                    

def show_add_income():
    st.header("💰 Add Income")
    
    # Pre-defined income categories
    income_categories = [
        "Salary", "Freelance", "Business", "Investment", "Rental", 
        "Bonus", "Commission", "Dividend", "Interest", "Other"
    ]
    
    with st.form("income_form"):
        st.subheader("📝 Enter Income Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            category = st.selectbox("Category", income_categories)
            custom_category = st.text_input("Custom Category (optional)")
        
        with col2:
            amount = st.number_input("Amount (₹)", min_value=0.01, value=100.00, step=0.01)
        
        description = st.text_area("Description (Optional)", placeholder="Additional details...")
        
        submitted = st.form_submit_button("💰 Add Income", use_container_width=True)
        
        if submitted:
            final_category = custom_category if custom_category else category
            
            if final_category and amount > 0:
                transaction_key = f"income_{final_category}_{amount}_{description}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
                
                if st.session_state.get('last_income_key') != transaction_key:
                    if add_transaction('Income', final_category, amount, description):
                        st.success(f"✅ Successfully added income: {final_category} - {format_currency(amount)}")
                        st.session_state.last_income_key = transaction_key
                        st.balloons()
                    else:
                        st.error("❌ Failed to add income. Please try again.")
                else:
                    st.warning("⚠️ This income was already added.")
            else:
                st.error("❌ Please enter a valid category and amount.")

def show_add_expense():
    st.header("💸 Add Expense")
    
    # Pre-defined expense categories
    expense_categories = [
        "Food", "Transportation", "Utilities", "Healthcare", "Education",
        "Entertainment", "Shopping", "Rent", "Insurance", "Groceries",
        "Fuel", "Bills", "Travel", "Subscription", "Other"
    ]
    
    with st.form("expense_form"):
        st.subheader("📝 Enter Expense Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            category = st.selectbox("Category", expense_categories)
            custom_category = st.text_input("Custom Category (optional)")
        
        with col2:
            amount = st.number_input("Amount (₹)", min_value=0.01, value=100.00, step=0.01)
        
        description = st.text_area("Description (Optional)", placeholder="Additional details...")
        
        submitted = st.form_submit_button("💸 Add Expense", use_container_width=True)
        
        if submitted:
            final_category = custom_category if custom_category else category
            
            if final_category and amount > 0:
                transaction_key = f"expense_{final_category}_{amount}_{description}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
                
                if st.session_state.get('last_expense_key') != transaction_key:
                    if add_transaction('Expense', final_category, amount, description):
                        st.success(f"✅ Successfully added expense: {final_category} - {format_currency(amount)}")
                        st.session_state.last_expense_key = transaction_key
                    else:
                        st.error("❌ Failed to add expense. Please try again.")
                else:
                    st.warning("⚠️ This expense was already added.")
            else:
                st.error("❌ Please enter a valid category and amount.")

def delete_transaction(transaction_id):
    """Delete a transaction"""
    engine = get_database_connection()
    if engine is None:
        return False
    
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                DELETE FROM transactions 
                WHERE id = :id AND user_id = :user_id
            """), {
                'id': transaction_id,
                'user_id': st.session_state.user_id
            })
            conn.commit()
            
            if result.rowcount == 0:
                st.warning("Transaction not found or already deleted.")
                return False
        
        # Clear cache after deletion
        clear_data_cache()
        
        return True
    except Exception as e:
        st.error(f"Error deleting transaction: {str(e)}")
        return False
        
        # Clear cache and force refresh
        clear_data_cache()
        if 'data_loaded' in st.session_state:
            del st.session_state['data_loaded']
        st.session_state.data_loaded = True
        
        return True
    except Exception as e:
        st.error(f"Error deleting transaction: {str(e)}")
        return False

def show_transactions():
    st.header("📋 All Transactions")
    
    transactions = get_transactions()
    
    if not transactions:
        st.info("📝 No transactions found. Add some income or expenses to get started.")
        return
    
    df = pd.DataFrame(transactions)
    df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%d %b %Y %H:%M')
    
    # Enhanced filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        transaction_type = st.selectbox("🔍 Filter by Type", ["All", "Income", "Expense"])
    
    with col2:
        categories = ["All"] + sorted(list(df['category'].unique()))
        selected_category = st.selectbox("📂 Filter by Category", categories)
    
    with col3:
        date_range = st.selectbox("📅 Filter by Date", ["All Time", "Last 7 Days", "Last 30 Days", "This Month"])
    
    # Apply filters
    filtered_df = df.copy()
    
    if transaction_type != "All":
        filtered_df = filtered_df[filtered_df['type'] == transaction_type]
    
    if selected_category != "All":
        filtered_df = filtered_df[filtered_df['category'] == selected_category]
    
    # Date filtering - FIXED: Convert back to datetime for filtering
    if date_range != "All Time":
        # Get original datetime data for filtering
        original_df = pd.DataFrame(transactions)
        original_df['created_at'] = pd.to_datetime(original_df['created_at'])
        
        now = datetime.now()
        
        if date_range == "Last 7 Days":
            cutoff = now - timedelta(days=7)
        elif date_range == "Last 30 Days":
            cutoff = now - timedelta(days=30)
        elif date_range == "This Month":
            cutoff = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        # Filter original data and get IDs
        filtered_ids = original_df[original_df['created_at'] >= cutoff]['id'].tolist()
        filtered_df = filtered_df[filtered_df['id'].isin(filtered_ids)]
    
    # Display results
    st.subheader(f"📊 Transactions ({len(filtered_df)} found)")
    
    if not filtered_df.empty:
        # Create a more readable display with consistent currency formatting
        display_df = filtered_df[['type', 'category', 'amount', 'created_at']].copy()
        display_df['amount'] = display_df['amount'].apply(lambda x: format_currency(x))
        display_df.columns = ['Type', 'Category', 'Amount', 'Date']
        
        st.dataframe(display_df, use_container_width=True)
        
        # Delete transaction option - FIXED: Better handling
        st.subheader("🗑️ Delete Transaction")
        transaction_options = [f"{row['id']}: {row['category']} - {format_currency(row['amount'])} ({row['type']})" 
                             for _, row in filtered_df.iterrows()]
        
        if transaction_options:
            selected_transaction = st.selectbox("Select transaction to delete", [""] + transaction_options)
            
            if selected_transaction:
                col1, col2 = st.columns([1, 4])
                with col1:
                    if st.button("🗑️ Delete", type="secondary"):
                        try:
                            transaction_id = int(selected_transaction.split(':')[0])
                            if delete_transaction(transaction_id):
                                st.success("✅ Transaction deleted successfully!")
                                st.rerun()
                            else:
                                st.error("❌ Failed to delete transaction.")
                        except ValueError:
                            st.error("❌ Invalid transaction selection.")
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
    else:
        st.info("No transactions match the selected filters.")
def show_insights():
    st.header("🎯 Financial Insights")
    
    insights = get_spending_insights()
    
    if not insights:
        st.info("📊 Add more transactions to get personalized insights!")
        return
    
    for insight in insights:
        if insight['type'] == 'alert':
            st.markdown(f'''
            <div class="alert-card">
                <h3>{insight['title']}</h3>
                <p>{insight['message']}</p>
            </div>
            ''', unsafe_allow_html=True)
        elif insight['type'] == 'success':
            st.markdown(f'''
            <div class="success-card">
                <h3>{insight['title']}</h3>
                <p>{insight['message']}</p>
            </div>
            ''', unsafe_allow_html=True)
        else:  # insight type
            st.markdown(f'''
            <div class="insight-card">
                <h3>{insight['title']}</h3>
                <p>{insight['message']}</p>
            </div>
            ''', unsafe_allow_html=True)
    
    # Additional insights section
    st.subheader("📈 Spending Pattern Analysis")
    
    # Get category summary for spending patterns
    category_summary = get_category_summary()
    
    if category_summary:
        # Separate income and expense categories
        expense_categories = [(cat, amount) for cat, type_, amount in category_summary if type_ == 'Expense']
        income_categories = [(cat, amount) for cat, type_, amount in category_summary if type_ == 'Income']
        
        col1, col2 = st.columns(2)
        
        with col1:
            if expense_categories:
                st.markdown("### 💸 Top Expense Categories")
                for i, (category, amount) in enumerate(expense_categories[:5], 1):
                    st.markdown(f'''
                    <div class="spending-card">
                        <div style="font-size: 1.2rem; font-weight: 600;">{i}. {category}</div>
                        <div style="font-size: 1.5rem; font-weight: 700;">{format_currency(amount)}</div>
                    </div>
                    ''', unsafe_allow_html=True)
        
        with col2:
            if income_categories:
                st.markdown("### 💰 Top Income Sources")
                for i, (category, amount) in enumerate(income_categories[:5], 1):
                    st.markdown(f'''
                    <div class="spending-card" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%);">
                        <div style="font-size: 1.2rem; font-weight: 600;">{i}. {category}</div>
                        <div style="font-size: 1.5rem; font-weight: 700;">{format_currency(amount)}</div>
                    </div>
                    ''', unsafe_allow_html=True)

def show_analytics():
    st.header("📈 Analytics")
    
    transactions = get_transactions()
    
    if not transactions:
        st.info("📊 No transactions found. Add some income or expenses to see analytics.")
        return
    
    # Convert to DataFrame
    df = pd.DataFrame(transactions)
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['date'] = df['created_at'].dt.date
    df['month'] = df['created_at'].dt.strftime('%Y-%m')
    
    # Monthly trends
    st.subheader("📊 Monthly Trends")
    monthly_data = df.groupby(['month', 'type'])['amount'].sum().reset_index()
    
    if not monthly_data.empty:
        fig_monthly = px.line(
            monthly_data, 
            x='month', 
            y='amount', 
            color='type',
            title='Monthly Income vs Expenses Trend',
            color_discrete_map={'Income': '#10b981', 'Expense': '#ef4444'},
            labels={'amount': 'Amount (₹)', 'month': 'Month'}
        )
        fig_monthly.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_monthly, use_container_width=True)
    
    # Category analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💸 Expense Categories")
        expense_data = df[df['type'] == 'Expense'].groupby('category')['amount'].sum().reset_index()
        
        if not expense_data.empty:
            fig_expense = px.pie(
                expense_data, 
                values='amount', 
                names='category',
                title='Expenses by Category',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_expense.update_layout(
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_expense, use_container_width=True)
        else:
            st.info("No expense data available for chart.")
    
    with col2:
        st.subheader("💰 Income Categories")
        income_data = df[df['type'] == 'Income'].groupby('category')['amount'].sum().reset_index()
        
        if not income_data.empty:
            fig_income = px.pie(
                income_data, 
                values='amount', 
                names='category',
                title='Income by Category',
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig_income.update_layout(
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_income, use_container_width=True)
        else:
            st.info("No income data available for chart.")
    
    # Additional analytics
    st.subheader("📊 Transaction Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Transactions", len(df))
    
    with col2:
        avg_transaction = df['amount'].mean()
        st.metric("Average Transaction", format_currency(avg_transaction))
    
    with col3:
        if not df.empty:
            largest_transaction = df.loc[df['amount'].idxmax()]
            st.metric("Largest Transaction", format_currency(largest_transaction['amount']))
            st.caption(f"{largest_transaction['category']} ({largest_transaction['type']})")
        else:
            st.metric("Largest Transaction", "N/A")

if __name__ == "__main__":
    main()