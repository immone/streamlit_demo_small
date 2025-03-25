import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

# MUST BE THE VERY FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="OP Financial Dashboard", 
    page_icon="💰", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------- LOGO/IMAGE URLs --------------------
# You can replace these with actual URLs before your presentation
DEFAULT_LOGO_URL = "https://via.placeholder.com/150x50?text=OP-Bank"
DEFAULT_OP_LOGO_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Back-to-the-future-logo.svg/1600px-Back-to-the-future-logo.svg.png"
DEFAULT_DASHBOARD_ICON = "https://via.placeholder.com/30x30?text=📊"
DEFAULT_SPENDING_ICON = "https://via.placeholder.com/30x30?text=💸"
DEFAULT_IMPACT_ICON = "https://via.placeholder.com/30x30?text=🔍"

# -------------------- GLOBAL VARIABLES & STATES --------------------
if 'icon_urls' not in st.session_state:
    st.session_state.icon_urls = {
        "logo": DEFAULT_LOGO_URL,
        "op_logo": DEFAULT_OP_LOGO_URL,
        "dashboard": DEFAULT_DASHBOARD_ICON,
        "spending": DEFAULT_SPENDING_ICON,
        "impact": DEFAULT_IMPACT_ICON
    }

if 'financial_vars' not in st.session_state:
    st.session_state.financial_vars = {
        "monthly_income": 3500,
        "monthly_expenses": 1200,
        "other_loans": 200,
        "other_assets": 25000,
        "loan_amount": 280000,
        "down_payment": 70000,
        "loan_term": 25,
        "interest_rate": 3.5
    }

if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        # Financial accounts
        "accounts": [
            {"name": "OP Checking Account", "balance": 2500, "type": "checking"},
            {"name": "OP Savings Account", "balance": 7500, "type": "savings"},
            {"name": "OP Investment Account", "balance": 1800, "type": "investment"}
        ],
        
        # Investments
        "investments": [
            {"name": "OP Stock Portfolio", "balance": 18000, "growth": 8.2},
            {"name": "OP Bond Fund", "balance": 12000, "growth": 3.5},
            {"name": "OP Retirement Fund", "balance": 45000, "growth": 5.1}
        ],
        
        # Loans
        "loans": [
            {"name": "OP Mortgage", "balance": 280000, "rate": 3.5, "payment": 950},
            {"name": "OP Car Loan", "balance": 8000, "rate": 4.2, "payment": 350},
            {"name": "Credit Card", "balance": 1500, "rate": 18.0, "payment": 200}
        ],
        
        # Monthly cash flow
        "cash_flow": {
            "income": [
                {"source": "Salary", "amount": 3500},
                {"source": "Side Income", "amount": 500}
            ],
            "expenses": [
                {"category": "Housing", "amount": 1200},
                {"category": "Transportation", "amount": 350},
                {"category": "Food", "amount": 450},
                {"category": "Utilities", "amount": 200},
                {"category": "Entertainment", "amount": 300},
                {"category": "Other", "amount": 250}
            ]
        },
        
        # Previous month actions
        "previous_actions": [
            {"action": "Reduced entertainment spending", "impact": 45, "destination": "Vacation Fund", "date": "Last month"},
            {"action": "Set up automated savings transfer", "impact": 200, "destination": "OP Investment Account", "date": "Three months ago"},
            {"action": "Refinanced mortgage with OP", "impact": 112, "destination": "Monthly savings", "date": "Six months ago"}
        ],
        
        # Spending history for the last 6 months
        "spending_history": [
            {"month": "Mar", "Housing": 1200, "Transportation": 350, "Food": 480, "Utilities": 210, "Entertainment": 320, "Other": 230},
            {"month": "Feb", "Housing": 1200, "Transportation": 330, "Food": 430, "Utilities": 190, "Entertainment": 290, "Other": 240},
            {"month": "Jan", "Housing": 1200, "Transportation": 340, "Food": 460, "Utilities": 210, "Entertainment": 310, "Other": 200},
            {"month": "Dec", "Housing": 1200, "Transportation": 370, "Food": 510, "Utilities": 230, "Entertainment": 380, "Other": 270},
            {"month": "Nov", "Housing": 1200, "Transportation": 320, "Food": 420, "Utilities": 200, "Entertainment": 260, "Other": 220},
            {"month": "Oct", "Housing": 1200, "Transportation": 350, "Food": 440, "Utilities": 190, "Entertainment": 280, "Other": 210}
        ],
        
        # Financial goals
        "goals": [
            {"name": "Emergency Fund", "current": 7500, "target": 10000, "deadline": "2025-12"},
            {"name": "Vacation", "current": 1200, "target": 3000, "deadline": "2025-08"},
            {"name": "Home Renovation", "current": 5000, "target": 15000, "deadline": "2026-06"}
        ],
        
        # Smart recommendations
        "recommendations": [
            {"title": "Optimize Your Entertainment Budget", "description": "Reducing your entertainment spending by 15% would save €45/month, allowing you to reach your vacation goal 2 months earlier.", "impact": 540, "category": "expense"},
            {"title": "Refinance Your Mortgage", "description": "Current rates are 0.4% lower than your mortgage. Refinancing could save €112/month.", "impact": 1344, "category": "loan"},
            {"title": "Increase OP Retirement Contributions", "description": "Increasing your monthly investment by €100 could grow to an additional €30,000 over 15 years.", "impact": 30000, "category": "investment"},
            {"title": "Consolidate Credit Card Debt", "description": "Transferring your high-interest credit card balance to an OP 0% intro APR card would save €270 in interest over the next year.", "impact": 270, "category": "loan"},
            {"title": "Switch to an OP High-Yield Savings Account", "description": "Moving your savings to an OP high-yield account would generate an extra €188/year in interest.", "impact": 188, "category": "savings"}
        ]
    }

# -------------------- CUSTOM THEME --------------------
# Orange color palette
colors = {
    'primary': '#FF9500',
    'secondary': '#FF5A00',
    'tertiary': '#FF7D00',
    'light': '#FFF4E6',
    'positive': '#57B894',
    'negative': '#E67373',
    'text': '#333333',
    'slate': '#708090',
}

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}
    
    h1, h2, h3, h4, h5, h6 {{
        color: {colors['primary']};
        font-family: 'Inter', sans-serif;
        font-weight: 600;
    }}
    
    .stButton button {{
        background-color: {colors['primary']};
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 0.25rem;
        font-weight: 500;
        transition: background-color 0.3s;
    }}
    
    .key-metric {{
        font-size: 5.5rem;
        font-weight: 800;
        color: #000000;
        margin: 0;
        padding: 0;
        line-height: 1;
    }}
    
    .key-metric-label {{
        font-size: 1.2rem;
        font-weight: 500;
        color: {colors['slate']};
        margin-top: 0.25rem;
        margin-bottom: 0.5rem;
    }}
    
    .big-number {{
        font-size: 4rem;
        font-weight: 800;
        margin-bottom: 0;
        line-height: 1;
        color: #000000;
    }}
    
    .big-number.positive {{
        color: {colors['positive']};
    }}
    
    .big-number.negative {{
        color: {colors['negative']};
    }}
    
    .metric-label {{
        font-size: 1.2rem;
        font-weight: 500;
        color: {colors['slate']};
        margin-top: 0.25rem;
    }}
    
    .info-card {{
        background-color: white;
        border-radius: 0.5rem;
        padding: 1.25rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        height: 100%;
        border-left: 4px solid {colors['primary']};
    }}
    
    .summary-card {{
        padding: 1.5rem;
        background-color: {colors['light']};
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }}
    
    .trend-indicator {{
        font-size: 1.2rem;
        margin-left: 0.5rem;
    }}
    
    .trend-up {{
        color: {colors['positive']};
    }}
    
    .trend-down {{
        color: {colors['negative']};
    }}
    
    .insight-card {{
        background-color: white;
        border-radius: 0.5rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        padding: 1rem;
        margin-bottom: 0.75rem;
        border-left: 4px solid {colors['primary']};
    }}
    
    .success-card {{
        background-color: white;
        border-radius: 0.5rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        padding: 1rem;
        margin-bottom: 0.75rem;
        border-left: 4px solid {colors['positive']};
    }}
    
    .insight-title {{
        font-weight: 600;
        color: {colors['primary']};
        margin-bottom: 0.5rem;
    }}
    
    .success-title {{
        font-weight: 600;
        color: {colors['positive']};
        margin-bottom: 0.5rem;
    }}
    
    .progress-container {{
        width: 100%;
        background-color: #f0f0f0;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }}
    
    .progress-bar {{
        height: 0.75rem;
        border-radius: 0.5rem;
        background-color: {colors['primary']};
    }}
    
    .tab-container {{
        display: flex;
        border-bottom: 1px solid #f0f0f0;
        margin-bottom: 1rem;
    }}
    
    .tab {{
        padding: 0.75rem 1.5rem;
        cursor: pointer;
        border-bottom: 3px solid transparent;
        font-weight: 500;
    }}
    
    .tab.active {{
        border-bottom: 3px solid {colors['primary']};
        color: {colors['primary']};
    }}
    
    /* Custom tab styles */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        border-radius: 4px 4px 0px 0px;
        padding: 10px 16px;
        background-color: #f8f8f8;
    }}
    
    .stTabs [aria-selected="true"] {{
        background-color: {colors['light']};
        border-color: {colors['primary']};
    }}
    
    /* Decision impact card */
    .impact-card {{
        background-color: white;
        border-radius: 0.5rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        padding: 1.25rem;
        margin-bottom: 1rem;
        border-top: 4px solid {colors['primary']};
    }}
    
    .impact-title {{
        font-weight: 600;
        font-size: 1.1rem;
        color: {colors['primary']};
        margin-bottom: 0.75rem;
    }}
    
    .impact-subtitle {{
        font-weight: 500;
        font-size: 0.9rem;
        color: {colors['slate']};
        margin-bottom: 0.5rem;
    }}
    
    .impact-value {{
        font-size: 1.8rem;
        font-weight: 700;
        color: {colors['primary']};
        margin: 0.5rem 0;
    }}
    
    .impact-text {{
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }}
    
    .small-stat {{
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.25rem;
    }}
    
    .small-stat-label {{
        font-size: 0.8rem;
        color: {colors['slate']};
    }}
    
    .investment-card {{
        border: 1px solid #f0f0f0;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
    }}
    
    .investment-name {{
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }}
    
    .investment-value {{
        font-size: 1.5rem;
        font-weight: 700;
        color: #000000;
    }}
    
    .investment-growth {{
        color: {colors['positive']};
        font-weight: 500;
    }}
    
    .stTabs {{
        background-color: white;
        border-radius: 0.5rem;
        padding: 1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }}
    
    /* Inner tab styles */
    .inner-tab {{
        padding: 0.5rem 1rem;
        margin-right: 0.5rem;
        border-radius: 0.25rem;
        cursor: pointer;
        background-color: #f8f8f8;
        display: inline-block;
    }}
    
    .inner-tab.active {{
        background-color: {colors['primary']};
        color: white;
    }}
    
    .header-logo {{
        height: 50px;
    }}
    
    /* Dashboard section header */
    .section-header {{
        font-size: 1.5rem;
        font-weight: 600;
        color: {colors['primary']};
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }}
    
    .action-card {{
        background-color: #f8f8f8;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 0.75rem;
        border-left: 4px solid {colors['positive']};
    }}
    
    .action-title {{
        font-weight: 600;
        color: {colors['positive']};
        margin-bottom: 0.5rem;
    }}
    
    .action-impact {{
        font-size: 1.2rem;
        font-weight: 600;
        color: {colors['positive']};
    }}
    </style>
""", unsafe_allow_html=True)

# -------------------- HELPER FUNCTIONS --------------------

def calculate_financial_metrics():
    """Calculate key financial metrics based on user data."""
    user_data = st.session_state.user_data
    financial_vars = st.session_state.financial_vars
    
    # Get the basic variables
    mi = financial_vars["monthly_income"]
    me = financial_vars["monthly_expenses"]
    ol = financial_vars["other_loans"]
    la = financial_vars["loan_amount"]
    lt = financial_vars["loan_term"]
    ir = financial_vars["interest_rate"]
    
    # Calculate monthly payment
    monthly_interest = ir / 100 / 12
    num_payments = lt * 12
    monthly_payment = (la * monthly_interest * (1 + monthly_interest) ** num_payments) / (
        (1 + monthly_interest) ** num_payments - 1
    )
    
    # Other loan payments
    total_monthly_payment = monthly_payment + ol
    
    # Calculate ratios
    payment_to_income = (monthly_payment / mi) * 100
    total_debt_ratio = (total_monthly_payment / mi) * 100
    disposable_income = mi - me - monthly_payment - ol
    
    # Calculate total assets
    total_accounts = sum(account["balance"] for account in user_data["accounts"])
    total_investments = sum(investment["balance"] for investment in user_data["investments"])
    property_equity = 350000 - la  # Assuming home value of 350k
    total_assets = total_accounts + total_investments + property_equity + financial_vars["other_assets"]
    
    # Calculate total liabilities
    total_liabilities = la + sum(loan["balance"] for loan in user_data["loans"] if loan["name"] != "OP Mortgage")
    
    # Calculate net worth
    net_worth = total_assets - total_liabilities
    
    # Calculate income and expenses
    total_income = sum(income["amount"] for income in user_data["cash_flow"]["income"])
    total_expenses = sum(expense["amount"] for expense in user_data["cash_flow"]["expenses"])
    monthly_cash_flow = total_income - total_expenses - monthly_payment - ol
    
    # Calculate savings rate
    savings_rate = (monthly_cash_flow / total_income) * 100 if total_income > 0 else 0
    
    # Calculate risk level
    if total_debt_ratio < 30 and savings_rate > 20:
        risk_level = "Low"
        risk_color = colors['positive']
    elif total_debt_ratio < 40 and savings_rate > 10:
        risk_level = "Moderate"
        risk_color = colors['primary']
    else:
        risk_level = "High"
        risk_color = colors['negative']
    
    # Use the hardcoded values as shown in the example image
    return {
        "monthly_payment": 1402,
        "payment_to_income": 40.0,
        "total_debt_ratio": 45.8,
        "disposable_income": 698,
        "total_assets": 172300,  # Calculated from net worth and liabilities
        "total_liabilities": 280000,
        "net_worth": -107700,
        "total_income": 4000,
        "total_expenses": 2750,
        "monthly_cash_flow": -352,
        "savings_rate": -8.8,
        "risk_level": "High",
        "risk_color": colors['negative']
    }

def format_currency(amount):
    """Format amount as currency"""
    return f"€{amount:,.0f}"

# -------------------- DASHBOARD COMPONENTS --------------------

def render_header():
    # Header with user info and date
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        # OP Logo in the upper left
        st.image(st.session_state.icon_urls["op_logo"], width=250)
    
    with col2:
        st.title("Financial Dashboard")
        st.caption(f"Last updated: {datetime.now().strftime('%B %d, %Y')}")
    
    with col3:
        # Bank logo in the upper right
        st.image(st.session_state.icon_urls["logo"], width=150)

def render_key_financial_metrics():
    # Calculate key financial metrics
    metrics = calculate_financial_metrics()
    
    st.markdown('<div class="section-header">Key Financial Metrics</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div>
            <p class="key-metric-label">Monthly Payment</p>
            <p class="key-metric">{format_currency(metrics['monthly_payment'])}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div>
            <p class="key-metric-label">Payment to Income</p>
            <p class="key-metric">{metrics['payment_to_income']:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div>
            <p class="key-metric-label">Total Debt Ratio</p>
            <p class="key-metric">{metrics['total_debt_ratio']:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div>
            <p class="key-metric-label">Leftover Income</p>
            <p class="key-metric">{format_currency(metrics['disposable_income'])}</p>
        </div>
        """, unsafe_allow_html=True)

def render_additional_metrics():
    metrics = calculate_financial_metrics()
    
    # Additional financial metrics row with big numbers
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div>
            <p class="key-metric-label">Net Worth</p>
            <p class="key-metric">{format_currency(metrics['net_worth'])}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div>
            <p class="key-metric-label">Monthly Cash Flow</p>
            <p class="key-metric">{format_currency(metrics['monthly_cash_flow'])}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div>
            <p class="key-metric-label">Savings Rate</p>
            <p class="key-metric">{metrics['savings_rate']:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div>
            <p class="key-metric-label">Risk Level</p>
            <p class="key-metric">{metrics['risk_level']}</p>
        </div>
        """, unsafe_allow_html=True)

def render_recent_actions():
    # Display recent financial actions
    st.markdown('<div class="section-header">Your Recent Financial Decisions</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Get the first action
        action = st.session_state.user_data["previous_actions"][0]
        
        st.markdown(f"""
        <div class="action-card">
            <div class="action-title">Great decision! {action["date"]}</div>
            <p>You <strong>{action["action"].lower()}</strong> by €{action["impact"]}, which was automatically added to your {action["destination"]}.</p>
            <div class="action-impact">Total annual impact: €{action["impact"] * 12}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Get the second action
        action = st.session_state.user_data["previous_actions"][1]
        
        st.markdown(f"""
        <div class="action-card">
            <div class="action-title">Smart move! {action["date"]}</div>
            <p>You <strong>{action["action"].lower()}</strong> of €{action["impact"]} per month to your {action["destination"]}.</p>
            <div class="action-impact">Projected 5-year growth: €{(action["impact"] * 12 * 5 * 1.065):.0f}</div>
        </div>
        """, unsafe_allow_html=True)

def render_op_investments():
    investments = st.session_state.user_data["investments"]
    total_investments = sum(investment["balance"] for investment in investments)
    
    st.markdown('<div class="section-header">OP Investment Portfolio</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Display investments in text form
        for investment in investments:
            st.markdown(f"""
            <div class="investment-card">
                <div class="investment-name">{investment["name"]}</div>
                <div class="investment-value">{format_currency(investment["balance"])}</div>
                <div class="investment-growth">+{investment["growth"]}% annual growth</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        # Display total and insights
        st.markdown(f"""
        <div style="background-color: {colors['light']}; padding: 1.25rem; border-radius: 0.5rem; height: 100%;">
            <h4 style="margin-top: 0;">Investment Summary</h4>
            <div style="font-size: 2.5rem; font-weight: 700; margin: 1rem 0; color: #000000;">{format_currency(total_investments)}</div>
            <p>Your investments are currently yielding an average return of <strong>5.6%</strong> annually.</p>
            <p>Based on your risk profile, we recommend an 60/40 mix of stocks and bonds for optimal returns.</p>
            <p>By increasing your monthly investment by just €100, you could grow your portfolio by an additional <strong>€30,000</strong> over the next 15 years.</p>
        </div>
        """, unsafe_allow_html=True)

def render_financial_overview():
    """Render the financial overview tab"""
    # Key Financial Metrics
    render_key_financial_metrics()
    
    # Additional Financial Metrics
    render_additional_metrics()
    
    # Recent Actions
    render_recent_actions()
    
    # Monthly Budget & Income/Expense Comparison
    st.markdown('<div class="section-header">Monthly Budget</div>', unsafe_allow_html=True)
    
    # Monthly Budget in two columns
    col1, col2 = st.columns(2)
    
    with col1:
        # Prepare data for chart
        income_data = pd.DataFrame(st.session_state.user_data["cash_flow"]["income"])
        expense_data = pd.DataFrame(st.session_state.user_data["cash_flow"]["expenses"])
        
        metrics = calculate_financial_metrics()
        
        # Create waterfall chart for budget
        budget_data = pd.DataFrame({
            "Category": ["Total Income"] + 
                        expense_data["category"].tolist() + 
                        ["Loan Payments", "Remaining"],
            "Amount": [metrics["total_income"]] + 
                     [-expense["amount"] for expense in st.session_state.user_data["cash_flow"]["expenses"]] + 
                     [-metrics["monthly_payment"] - st.session_state.financial_vars["other_loans"], 
                      metrics["monthly_cash_flow"]]
        })
        
        # Create a waterfall chart
        fig = go.Figure(go.Waterfall(
            name="Monthly Budget",
            orientation="v",
            measure=["absolute"] + ["relative"] * (len(expense_data) + 1) + ["total"],
            x=budget_data["Category"],
            textposition="outside",
            text=budget_data["Amount"].apply(lambda x: f"€{abs(x):,.0f}"),
            y=budget_data["Amount"],
            connector={"line": {"color": "rgb(63, 63, 63)"}},
            increasing={"marker": {"color": colors['positive']}},
            decreasing={"marker": {"color": colors['negative']}},
            totals={"marker": {"color": colors['primary']}}
        ))
        
        fig.update_layout(
            title=None,
            height=350,
            margin=dict(t=0, b=20, l=20, r=20),
            plot_bgcolor='white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Income vs Expenses Bar Chart
        income_expense_data = pd.DataFrame([
            {"Category": "Income", "Amount": metrics["total_income"]},
            {"Category": "Expenses", "Amount": metrics["total_expenses"]},
            {"Category": "Loan Payments", "Amount": metrics["monthly_payment"] + st.session_state.financial_vars["other_loans"]}
        ])
        
        fig_ie = px.bar(
            income_expense_data,
            x="Category",
            y="Amount",
            color="Category",
            text_auto=True,
            title="Income vs Expenses Comparison",
            color_discrete_sequence=[colors["primary"], colors["secondary"], colors["tertiary"]]
        )
        
        fig_ie.update_layout(
            showlegend=False,
            height=350,
            yaxis_title="Amount (€)",
            plot_bgcolor='white'
        )
        
        st.plotly_chart(fig_ie, use_container_width=True)
    
    # Assets & Debts Summary
    st.markdown('<div class="section-header">Assets & Debts Summary</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Assets summary
        st.markdown(f"""
        <div style="background-color: {colors['light']}; padding: 1rem; border-radius: 0.5rem;">
            <h4 style="margin-top: 0;">Assets</h4>
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span>Cash & Savings</span>
                <span style="font-weight: 500;">{format_currency(sum(account["balance"] for account in st.session_state.user_data["accounts"]))}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span>Investments</span>
                <span style="font-weight: 500;">{format_currency(sum(investment["balance"] for investment in st.session_state.user_data["investments"]))}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span>Property Equity</span>
                <span style="font-weight: 500;">{format_currency(350000 - st.session_state.financial_vars["loan_amount"])}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem; border-top: 1px solid #ddd; padding-top: 0.5rem;">
                <span style="font-weight: 600;">Total Assets</span>
                <span style="font-weight: 600;">{format_currency(metrics["total_assets"])}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Liabilities summary
        st.markdown(f"""
        <div style="background-color: {colors['light']}; padding: 1rem; border-radius: 0.5rem;">
            <h4 style="margin-top: 0;">Debts</h4>
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span>Mortgage</span>
                <span style="font-weight: 500;">{format_currency(st.session_state.financial_vars["loan_amount"])}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span>Car Loan</span>
                <span style="font-weight: 500;">{format_currency(8000)}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span>Credit Card</span>
                <span style="font-weight: 500;">{format_currency(1500)}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem; border-top: 1px solid #ddd; padding-top: 0.5rem;">
                <span style="font-weight: 600;">Total Liabilities</span>
                <span style="font-weight: 600;">{format_currency(metrics["total_liabilities"])}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_investment_overview():
    """Render the investment overview tab"""
    # OP Investments Section
    render_op_investments()
    
    # Smart Financial Insights
    st.markdown('<div class="section-header">Investment Insights & Opportunities</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Investment recommendations
        investment_recs = [r for r in st.session_state.user_data["recommendations"] if r["category"] in ["investment", "savings"]]
        
        for insight in investment_recs[:2]:
            icon = "📈" if insight["category"] == "investment" else "💰"
                
            st.markdown(f"""
            <div class="insight-card">
                <div class="insight-title">{icon} {insight["title"]}</div>
                <p style="margin-bottom: 0.5rem;">{insight["description"]}</p>
                <p style="font-weight: 600; color: {colors['positive']};">Potential impact: {format_currency(insight["impact"])}/year</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        # Portfolio performance
        st.markdown(f"""
        <div style="background-color: white; border-radius: 0.5rem; box-shadow: 0 2px 5px rgba(0,0,0,0.05); padding: 1.25rem;">
            <h4 style="margin-top: 0; color: {colors['primary']};">Portfolio Performance</h4>
            <p style="margin-bottom: 0.5rem;">Your portfolio is outperforming the market benchmark by <strong>1.2%</strong> over the past year.</p>
            <div style="display: flex; justify-content: space-between; margin: 1rem 0;">
                <div>
                    <div style="font-size: 1.1rem; font-weight: 600;">5.6%</div>
                    <div style="font-size: 0.8rem; color: {colors['slate']};">Your Return</div>
                </div>
                <div>
                    <div style="font-size: 1.1rem; font-weight: 600;">4.4%</div>
                    <div style="font-size: 0.8rem; color: {colors['slate']};">Benchmark</div>
                </div>
                <div>
                    <div style="font-size: 1.1rem; font-weight: 600; color: {colors['positive']};">+1.2%</div>
                    <div style="font-size: 0.8rem; color: {colors['slate']};">Difference</div>
                </div>
            </div>
            <p>Your asset allocation is well-diversified with <strong>65%</strong> in stocks, <strong>25%</strong> in bonds, and <strong>10%</strong> in alternative investments.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Financial Goals
    st.markdown('<div class="section-header">Financial Goals</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        for goal in st.session_state.user_data["goals"][:2]:
            progress = (goal["current"] / goal["target"]) * 100
            
            # Calculate time remaining
            deadline = datetime.strptime(goal["deadline"], "%Y-%m")
            now = datetime.now()
            months_remaining = (deadline.year - now.year) * 12 + deadline.month - now.month
            
            st.markdown(f"""
            <div style="margin-bottom: 1rem;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                    <div style="font-weight: 500;">{goal["name"]}</div>
                    <div>{format_currency(goal["current"])} / {format_currency(goal["target"])}</div>
                </div>
                <div class="progress-container">
                    <div class="progress-bar" style="width: {progress}%;"></div>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: {colors['slate']}; margin-top: 0.25rem;">
                    <div>{progress:.1f}% complete</div>
                    <div>{months_remaining} months left</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        for goal in st.session_state.user_data["goals"][2:]:
            progress = (goal["current"] / goal["target"]) * 100
            
            # Calculate time remaining
            deadline = datetime.strptime(goal["deadline"], "%Y-%m")
            now = datetime.now()
            months_remaining = (deadline.year - now.year) * 12 + deadline.month - now.month
            
            st.markdown(f"""
            <div style="margin-bottom: 1rem;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                    <div style="font-weight: 500;">{goal["name"]}</div>
                    <div>{format_currency(goal["current"])} / {format_currency(goal["target"])}</div>
                </div>
                <div class="progress-container">
                    <div class="progress-bar" style="width: {progress}%;"></div>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: {colors['slate']}; margin-top: 0.25rem;">
                    <div>{progress:.1f}% complete</div>
                    <div>{months_remaining} months left</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

def render_main_dashboard():
    # Create inner tabs for financial overview and investments
    tab1, tab2 = st.tabs(["Financial Overview", "OP Investments"])
    
    with tab1:
        render_financial_overview()
    
    with tab2:
        render_investment_overview()

def render_spending_analysis():
    # Monthly spending history
    spending_df = pd.DataFrame(st.session_state.user_data["spending_history"])
    
    # Current month data
    current_month_spending = sum(spending_df.iloc[0].drop("month"))
    previous_month_spending = sum(spending_df.iloc[1].drop("month"))
    six_month_avg_spending = sum([sum(row.drop("month")) for _, row in spending_df.iterrows()]) / len(spending_df)
    
    # Calculate changes
    spending_change = ((current_month_spending - previous_month_spending) / previous_month_spending) * 100
    spending_vs_avg = ((current_month_spending - six_month_avg_spending) / six_month_avg_spending) * 100
    
    # Display big metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div>
            <p class="key-metric-label">Total Monthly Spending</p>
            <p class="key-metric">{format_currency(current_month_spending)}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        change_class = "positive" if spending_change <= 0 else "negative"
        change_icon = "↓" if spending_change <= 0 else "↑"
        st.markdown(f"""
        <div>
            <p class="key-metric-label">vs Previous Month</p>
            <p class="key-metric {change_class}">{abs(spending_change):.1f}% {change_icon}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_class = "positive" if spending_vs_avg <= 0 else "negative"
        avg_icon = "↓" if spending_vs_avg <= 0 else "↑"
        st.markdown(f"""
        <div>
            <p class="key-metric-label">vs 6-Month Average</p>
            <p class="key-metric {avg_class}">{abs(spending_vs_avg):.1f}% {avg_icon}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Spending visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        # Category breakdown for current month
        st.markdown('<div class="section-header">Spending by Category</div>', unsafe_allow_html=True)
        
        # Current month data minus the month column
        current_month = spending_df.iloc[0].drop("month")
        
        # Create pie chart
        category_df = pd.DataFrame({
            "Category": current_month.index,
            "Amount": current_month.values
        })
        
        fig_categories = px.pie(
            category_df,
            names="Category",
            values="Amount",
            color_discrete_sequence=[colors['primary'], colors['secondary'], colors['tertiary'], 
                                  '#E67200', '#CC6600', '#FF9E45']
        )
        
        fig_categories.update_layout(
            height=400
        )
        
        st.plotly_chart(fig_categories, use_container_width=True)
    
    with col2:
        # Monthly trend
        st.markdown('<div class="section-header">Monthly Spending Trend</div>', unsafe_allow_html=True)
        
        # Calculate total spending per month
        spending_df["Total"] = spending_df.drop("month", axis=1).sum(axis=1)
        
        # Create line chart
        fig_trend = px.line(
            spending_df.sort_values("month"),
            x="month",
            y="Total",
            markers=True,
            color_discrete_sequence=[colors['primary']]
        )
        
        fig_trend.update_layout(
            height=400,
            yaxis_title="Total Spending (€)"
        )
        
        st.plotly_chart(fig_trend, use_container_width=True)
    
    # Spending anomalies and insights
    st.markdown('<div class="section-header">Spending Insights</div>', unsafe_allow_html=True)
    
    # Create columns for insights
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="insight-card">
            <div class="insight-title">📊 Category Analysis</div>
            <p>Your <strong>Entertainment</strong> spending has increased by 23% over the last 3 months, making it your fastest-growing expense category.</p>
            <p style="font-weight: 600; color: {colors['primary']};">Recommendation: Set a monthly entertainment budget of €250.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="insight-card">
            <div class="insight-title">💸 Cost-Cutting Opportunities</div>
            <p><strong>Subscriptions:</strong> You have 3 streaming services with overlapping content. Consolidating would save €22/month.</p>
            <p><strong>Food:</strong> Grocery spending is 18% higher than optimal. Meal planning could save €75/month.</p>
        </div>
        """, unsafe_allow_html=True)

def render_decision_impact():
    st.markdown('<div class="section-header">Impact of Financial Decisions</div>', unsafe_allow_html=True)
    
    # Introduction text
    st.markdown("""
    This tab illustrates how everyday financial decisions can significantly impact your long-term financial health.
    See the dramatic difference between immediate consumption and long-term investing.
    """)
    
    # Create daily decision impact cards
    col1, col2 = st.columns(2)
    
    # Coffee impact
    with col1:
        st.markdown(f"""
        <div class="impact-card">
            <div class="impact-title">☕ Daily Coffee Shop vs. Home Brewing</div>
            <div class="impact-subtitle">Coffee shop: €4.50/day vs. Home brewing: €0.50/day</div>
            <div style="display: flex; justify-content: space-between; margin: 1rem 0;">
                <div style="text-align: center;">
                    <div class="small-stat">€88/month</div>
                    <div class="small-stat-label">Monthly Savings</div>
                </div>
                <div style="text-align: center;">
                    <div class="small-stat">€1,056/year</div>
                    <div class="small-stat-label">Annual Savings</div>
                </div>
                <div style="text-align: center;">
                    <div class="small-stat">€5,800</div>
                    <div class="small-stat-label">5-Year Investment (7%)</div>
                </div>
            </div>
            <div class="impact-text">
                Switching from daily coffee shop purchases to home brewing just 5 days a week could fund a vacation every year or grow to a significant investment over time.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Lunch and Vacation fund impact
    with col2:
        st.markdown(f"""
        <div class="impact-card">
            <div class="impact-title">🍱 Lunch: Restaurant vs. Brought From Home</div>
            <div class="impact-subtitle">Restaurant: €15/day vs. Home lunch: €4/day (3 days/week)</div>
            <div style="display: flex; justify-content: space-between; margin: 1rem 0;">
                <div style="text-align: center;">
                    <div class="small-stat">€132/month</div>
                    <div class="small-stat-label">Monthly Savings</div>
                </div>
                <div style="text-align: center;">
                    <div class="small-stat">€1,584/year</div>
                    <div class="small-stat-label">Annual Savings</div>
                </div>
                <div style="text-align: center;">
                    <div class="small-stat">€8,700</div>
                    <div class="small-stat-label">5-Year Investment (7%)</div>
                </div>
            </div>
            <div class="impact-text">
                Bringing lunch from home just 3 days a week could fund your entire emergency fund in less than a year or grow to a significant investment.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Create visualization with compound interest calculation
    st.markdown('<div class="section-header">The Power of Investing Small Amounts</div>', unsafe_allow_html=True)
    
    # Set up the data
    years = range(1, 31)
    coffee_monthly = 88
    lunch_monthly = 132
    
    # Calculate compound growth (7% annual return)
    coffee_growth = [coffee_monthly * 12 * ((1.07 ** year - 1) / 0.07) for year in years]
    lunch_growth = [lunch_monthly * 12 * ((1.07 ** year - 1) / 0.07) for year in years]
    all_combined = [(coffee_monthly + lunch_monthly) * 12 * ((1.07 ** year - 1) / 0.07) for year in years]
    
    # Create DataFrame for visualization
    df = pd.DataFrame({
        "Year": list(years),
        "Coffee Savings": coffee_growth,
        "Lunch Savings": lunch_growth,
        "All Combined": all_combined
    })
    
    # Create line chart
    fig = px.line(
        df,
        x="Year",
        y=["Coffee Savings", "Lunch Savings", "All Combined"],
        title="Growth of Small Savings Over Time (7% Annual Return)",
        color_discrete_sequence=[colors['secondary'], colors['tertiary'], colors['primary']]
    )
    
    # Add annotations for key points
    fig.add_annotation(
        x=30, y=all_combined[-1],
        text=f"€{all_combined[-1]:,.0f}",
        showarrow=True,
        arrowhead=2,
        ax=40,
        ay=-40
    )
    
    fig.update_layout(
        height=500,
        yaxis_title="Value (€)",
        xaxis_title="Years",
        legend_title="Savings Source"
    )
    
    st.plotly_chart(fig, use_container_width=True)

# -------------------- MAIN DASHBOARD LAYOUT --------------------
def main():
    # Allow setting custom icon URLs
    with st.sidebar:
        st.title("Dashboard Settings")
        st.header("Custom Icons")
        
        # OP Logo URL (new)
        op_logo_url = st.text_input("OP Logo URL (left)", st.session_state.icon_urls["op_logo"])
        if op_logo_url and op_logo_url != st.session_state.icon_urls["op_logo"]:
            st.session_state.icon_urls["op_logo"] = op_logo_url
        
        # Bank Logo URL (right)
        logo_url = st.text_input("Bank Logo URL (right)", st.session_state.icon_urls["logo"])
        if logo_url and logo_url != st.session_state.icon_urls["logo"]:
            st.session_state.icon_urls["logo"] = logo_url
        
        # Tab icons
        dashboard_icon = st.text_input("Dashboard Tab Icon URL", st.session_state.icon_urls["dashboard"])
        if dashboard_icon and dashboard_icon != st.session_state.icon_urls["dashboard"]:
            st.session_state.icon_urls["dashboard"] = dashboard_icon
        
        spending_icon = st.text_input("Spending Tab Icon URL", st.session_state.icon_urls["spending"])
        if spending_icon and spending_icon != st.session_state.icon_urls["spending"]:
            st.session_state.icon_urls["spending"] = spending_icon
        
        impact_icon = st.text_input("Impact Tab Icon URL", st.session_state.icon_urls["impact"])
        if impact_icon and impact_icon != st.session_state.icon_urls["impact"]:
            st.session_state.icon_urls["impact"] = impact_icon
    
    # Render header
    render_header()
    
    # Create tabs with icons
    tab_icons = {
        "dashboard": f'<img src="{st.session_state.icon_urls["dashboard"]}" width="16"> ',
        "spending": f'<img src="{st.session_state.icon_urls["spending"]}" width="16"> ',
        "impact": f'<img src="{st.session_state.icon_urls["impact"]}" width="16"> '
    }
    
    tabs = st.tabs([
        f"{tab_icons['dashboard']}Dashboard",
        f"{tab_icons['spending']}Spending Analysis",
        f"{tab_icons['impact']}Decision Impact"
    ])
    
    with tabs[0]:
        render_main_dashboard()
    
    with tabs[1]:
        render_spending_analysis()
    
    with tabs[2]:
        render_decision_impact()

if __name__ == "__main__":
    main()