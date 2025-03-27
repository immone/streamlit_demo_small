import streamlit as st
import pandas as pd
import streamlit_shadcn_ui as ui
import plotly.express as px
import plotly.graph_objects as go

# MUST BE THE VERY FIRST STREAMLIT COMMAND
st.set_page_config(page_title=None, page_icon=None, layout="wide")

# -------------------- GLOBAL VARIABLES --------------------
colors = {
    'primary': '#FF9500',
    'secondary': '#FF5A00',
    'success': '#4DAA57',
    'warning': '#FF5A00',
    'light': '#FFF4E6',
    'white': '#FFFFFF',
    'text': '#333333',
    'slate': '#708090',
    'positive': '#4DAA57',
    'negative': '#E63946'
}

# Default financial values
financial_vars = {
    "monthly_income": 3500,
    "monthly_expenses": 1200,
    "other_loans": 200,
    "existing_student_debt": 7000,
    "monthly_student_payment": 150,
    "other_assets": 25000,
    "loan_amount": 280000,
    "down_payment": 70000,
    "loan_term": 25,
    "interest_rate": 3.5,
    "maintenance_fee": 245,
    "renovation_cost_monthly": 50  # Added default value
}

# -------------------- CUSTOM THEME --------------------
banking_css = f"""
<style>
/* Base styles */
@import url('https://fonts.googleapis.com/css2?family=Calibri:wght@300;400;700&display=swap');

.stApp {{
    background-color: {colors['white']};
    color: {colors['text']};
    font-family: 'Calibri Light', 'Calibri', sans-serif;
    font-weight: 300;
}}

.block-container {{
    padding-top: 1rem;
}}

h1, h2, h3 {{
    color: {colors['primary']};
    font-family: 'Calibri Light', 'Calibri', sans-serif;
    font-weight: 300;
}}

.stButton button {{
    background-color: {colors['primary']};
    color: {colors['white']};
    font-family: 'Calibri Light', 'Calibri', sans-serif;
    font-weight: 300;
}}

/* Bank-like UI components */
.bank-card {{
    background-color: white;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}}

.bank-card-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
}}

.bank-card-title {{
    color: #333333;
    font-size: 18px;
    font-weight: 500;
}}

.bank-card-arrow {{
    color: {colors['primary']};
    font-size: 18px;
}}

.bank-widget {{
    background-color: #f8f9fa;
    border-radius: 5px;
    padding: 10px;
    margin-bottom: 10px;
}}

.bank-item {{
    display: flex;
    align-items: center;
    padding: 12px 0;
    border-bottom: 1px solid #f0f0f0;
}}

.bank-item-label {{
    flex-grow: 1;
    font-size: 14px;
}}

.bank-item-value {{
    font-weight: 500;
    font-size: 14px;
}}

.bank-item-arrow {{
    width: 15px;
    text-align: right;
    color: {colors['primary']};
}}

.bank-notice {{
    background-color: {colors['light']};
    border-left: 4px solid {colors['primary']};
    border-radius: 4px;
    padding: 10px;
    margin-top: 15px;
    font-size: 13px;
}}

.positive-value {{
    color: {colors['positive']};
}}

.negative-value {{
    color: {colors['negative']};
}}

.bank-progress-bar {{
    background-color: #f0f0f0;
    border-radius: 10px;
    height: 8px;
    position: relative;
    overflow: hidden;
}}

.bank-progress-fill {{
    position: absolute;
    height: 100%;
    border-radius: 10px;
}}

.bank-metric {{
    flex: 1; 
    background-color: white; 
    border-radius: 10px; 
    box-shadow: 0 1px 3px rgba(0,0,0,0.1); 
    margin: 0 5px; 
    padding: 15px; 
    text-align: center;
}}

.bank-metric-label {{
    font-size: 14px;
    color: #555;
    margin-bottom: 8px;
}}

.bank-metric-value {{
    font-size: 22px;
    font-weight: 500;
}}
</style>
"""

# Apply the CSS
st.markdown(banking_css, unsafe_allow_html=True)
# -------------------- FUNCTIONS --------------------
def calculate_financial_metrics(vars):
    """Calculate all financial metrics based on input variables"""
    # Extract variables for readability
    mi = vars["monthly_income"]
    me = vars["monthly_expenses"]
    sd = vars["existing_student_debt"]
    ms = vars["monthly_student_payment"]
    ol = vars["other_loans"]
    oa = vars["other_assets"]
    la = vars["loan_amount"]
    dp = vars["down_payment"]
    lt = vars["loan_term"]
    ir = vars["interest_rate"]
    maintenance = vars["maintenance_fee"]
    renovation_cost = vars["renovation_cost_monthly"]
    
    # Calculate key metrics
    monthly_payment = (la * (ir/100/12) * (1 + ir/100/12)**(lt*12)) / ((1 + ir/100/12)**(lt*12) - 1)
    loan_to_value = (la / (la + dp)) * 100
    debt_to_income = ((monthly_payment + ol) / mi) * 100
    disposable_income = mi - me - monthly_payment - ol
    asset_to_loan_ratio = (oa / la) * 100
    
    total_monthly_housing_cost = monthly_payment + maintenance + renovation_cost
    total_housing_ratio = (total_monthly_housing_cost / mi) * 100
    
    risk_score = (debt_to_income * 0.4 + loan_to_value * 0.4 - (disposable_income/mi)*20 - (asset_to_loan_ratio*0.1))
    risk_category = "Low Risk" if risk_score < 20 else "Moderate Risk" if risk_score < 35 else "High Risk"
    risk_color = colors['success'] if risk_score < 20 else colors['primary'] if risk_score < 35 else colors['warning']
    
    return {
        "monthly_payment": monthly_payment,
        "loan_to_value": loan_to_value,
        "debt_to_income": debt_to_income,
        "disposable_income": disposable_income,
        "asset_to_loan_ratio": asset_to_loan_ratio,
        "total_monthly_housing_cost": total_monthly_housing_cost,
        "total_housing_ratio": total_housing_ratio,
        "risk_score": risk_score,
        "risk_category": risk_category,
        "risk_color": risk_color
    }

def render_financial_summary(vars, metrics):
    """Render the financial summary section"""
    # Extract metrics for readability
    mi = vars["monthly_income"]
    me = vars["monthly_expenses"]
    sd = vars["existing_student_debt"]
    ms = vars["monthly_student_payment"]
    ol = vars["other_loans"]
    oa = vars["other_assets"]
    la = vars["loan_amount"]
    dp = vars["down_payment"]
    maintenance = vars["maintenance_fee"]
    renovation_cost = vars["renovation_cost_monthly"]
    
    monthly_payment = metrics["monthly_payment"]
    loan_to_value = metrics["loan_to_value"]
    debt_to_income = metrics["debt_to_income"]
    total_housing_ratio = metrics["total_housing_ratio"]
    risk_score = metrics["risk_score"]
    risk_category = metrics["risk_category"]
    
    # Pre-loan wealth (status quo)
    debt_amount_pre = sd  # Student debt only
    assets_amount_pre = oa  # Savings only
    total_amount_pre = debt_amount_pre + assets_amount_pre
    debt_percentage_pre = (debt_amount_pre / total_amount_pre) * 100 if total_amount_pre > 0 else 0
    assets_percentage_pre = 100 - debt_percentage_pre
    
    # Post-loan wealth
    property_value = la + dp
    debt_amount_post = sd + la  # Student debt + housing loan
    assets_amount_post = oa - dp + property_value  # Remaining savings + property
    total_amount_post = debt_amount_post + assets_amount_post
    debt_percentage_post = (debt_amount_post / total_amount_post) * 100 if total_amount_post > 0 else 0
    assets_percentage_post = 100 - debt_percentage_post
    
    # Post-loan expenses
    total_expenses = me - 900 + monthly_payment + ms + maintenance + renovation_cost  # Subtract rent, add housing costs
    monthly_balance = mi - total_expenses
    
    # Display key metrics    
    st.write("#")
    col1, col2 = st.columns([2, 1])
    with col1:
        with st.container(border=True):
            kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
            with kpi_col1:
                ui.metric_card(title="Loan-to-Value", content=f"{loan_to_value:.1f}%", description=f"{'Good' if loan_to_value < 80 else 'Moderate' if loan_to_value < 90 else 'High'}")
            with kpi_col2:
                ui.metric_card(title="Debt-to-Income", content=f"{debt_to_income:.1f}%", description=f"{'Good' if debt_to_income < 35 else 'Moderate' if debt_to_income < 45 else 'High'}")
            with kpi_col3:
                ui.metric_card(title="Housing Costs to Income", content=f"{total_housing_ratio:.1f}%", description=f"{'Good' if total_housing_ratio < 35 else 'Moderate' if total_housing_ratio < 45 else 'High'}")
            with kpi_col4:
                ui.metric_card(title="Overall Risk Score", content=f"{risk_score:.1f}", description=risk_category)
            
            # Wealth section (show pre- and post-loan)
            wealth_html = f"""
            <div class="bank-card">
                <div class="bank-card-header">
                    <span class="bank-card-title">Wealth</span>
                    <span class="bank-card-arrow">›</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <div style="flex: 1; padding-right: 10px;">
                        <h4>Before Loan</h4>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                            <div style="color: #555; font-size: 14px;">Debt</div>
                            <div style="color: #555; font-size: 14px;">Assets</div>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                            <div style="font-weight: 500; font-size: 14px;">-{debt_amount_pre:,.2f} €</div>
                            <div style="font-weight: 500; font-size: 14px;">{assets_amount_pre:,.2f} €</div>
                        </div>
                        <div style="height: 10px; background-color: #e0e0e0; border-radius: 5px; margin: 15px 0; position: relative;">
                            <div style="position: absolute; width: 1px; height: 16px; background-color: #333; top: -3px; left: {assets_percentage_pre}%;"></div>
                            <div style="position: absolute; height: 100%; left: 0; width: {debt_percentage_pre}%; background-color: #555; border-radius: 5px 0 0 5px;"></div>
                            <div style="position: absolute; height: 100%; right: 0; width: {assets_percentage_pre}%; background-color: #FF9500; border-radius: 0 5px 5px 0;"></div>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 3px;">
                            <div style="font-size: 13px; color: #555;">Existing student debt</div>
                            <div style="font-size: 13px; font-weight: 500;">{sd:,.2f} €</div>
                        </div>
                    </div>
                    <div style="flex: 1; padding-left: 10px;">
                        <h4>After Loan</h4>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                            <div style="color: #555; font-size: 14px;">Debt</div>
                            <div style="color: #555; font-size: 14px;">Assets</div>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                            <div style="font-weight: 500; font-size: 14px;">-{debt_amount_post:,.2f} €</div>
                            <div style="font-weight: 500; font-size: 14px;">{assets_amount_post:,.2f} €</div>
                        </div>
                        <div style="height: 10px; background-color: #e0e0e0; border-radius: 5px; margin: 15px 0; position: relative;">
                            <div style="position: absolute; width: 1px; height: 16px; background-color: #333; top: -3px; left: {assets_percentage_post}%;"></div>
                            <div style="position: absolute; height: 100%; left: 0; width: {debt_percentage_post}%; background-color: #555; border-radius: 5px 0 0 5px;"></div>
                            <div style="position: absolute; height: 100%; right: 0; width: {assets_percentage_post}%; background-color: #FF9500; border-radius: 0 5px 5px 0;"></div>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 3px;">
                            <div style="font-size: 13px; color: #555;">Loan {vars["loan_term"]}-year fixed</div>
                            <div style="font-size: 13px; font-weight: 500;">{la:,.2f} €</div>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 3px;">
                            <div style="font-size: 13px; color: #555;">Existing student debt</div>
                            <div style="font-size: 13px; font-weight: 500;">{sd:,.2f} €</div>
                        </div>
                    </div>
                </div>
            </div>
            """

            # Everyday finance section
            necessaries = (me - 900) * 0.6  # Adjust for rent removal
            loan_repayment = monthly_payment + ms
            fun_benefits = (me - 900) * 0.4
            
            finance_html = f"""
            <div class="bank-card">
                <div class="bank-card-header">
                    <span class="bank-card-title">Everyday Finance</span>
                    <span class="bank-card-arrow">›</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-top: 20px;">
                    <div style="text-align: center; flex: 1;">
                        <div style="font-size: 14px; color: #555; margin-bottom: 8px;">Income</div>
                        <div style="font-size: 22px; font-weight: 500; color: #4DAA57;">{mi:,.2f} €</div>
                    </div>
                    <div style="text-align: center; flex: 1;">
                        <div style="font-size: 14px; color: #555; margin-bottom: 8px;">Expenditure</div>
                        <div style="font-size: 22px; font-weight: 500; color: #E63946;">-{total_expenses:,.2f} €</div>
                    </div>
                </div>
                <div style="height: 1px; background-color: #f0f0f0; margin: 15px 0;"></div>
                <div class="bank-item">
                    <div class="bank-item-label">Necessaries</div>
                    <div class="bank-item-value negative-value">-{necessaries:,.2f} €</div>
                    <div class="bank-item-arrow">›</div>
                </div>
                <div class="bank-item">
                    <div class="bank-item-label">Loan repayment</div>
                    <div class="bank-item-value negative-value">-{loan_repayment:,.2f} €</div>
                    <div class="bank-item-arrow">›</div>
                </div>
                <div class="bank-item" style="border-bottom: none;">
                    <div class="bank-item-label">Fun and benefits</div>
                    <div class="bank-item-value negative-value">-{fun_benefits:,.2f} €</div>
                    <div class="bank-item-arrow">›</div>
                </div>
            </div>
            """

            # Loan impact section
            payment_to_income_ratio = (monthly_payment / mi) * 100
            loan_html = f"""
            <div class="bank-card">
                <div class="bank-card-header">
                    <span class="bank-card-title">Loan Impact</span>
                    <span class="bank-card-arrow">›</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <div style="color: #555; font-size: 14px;">Monthly Payment</div>
                    <div style="font-weight: 500; font-size: 14px;">{monthly_payment:,.2f} €</div>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <div style="color: #555; font-size: 14px;">Payment-to-Income Ratio</div>
                    <div style="font-weight: 500; font-size: 14px;">{payment_to_income_ratio:.1f}%</div>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <div style="color: #555; font-size: 14px;">Loan-to-Value Ratio</div>
                    <div style="font-weight: 500; font-size: 14px;">{loan_to_value:.1f}%</div>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 15px;">
                    <div style="color: #555; font-size: 14px;">Monthly Balance After Expenses</div>
                    <div style="font-weight: 500; font-size: 14px; color: {'#4DAA57' if monthly_balance > 0 else '#E63946'};">{monthly_balance:,.2f} €</div>
                </div>
                <div class="bank-notice">
                    <strong>Note:</strong> Loan service costs in relation to net income must not exceed 60%. 
                    Current ratio: <span style="color: {'#4DAA57' if payment_to_income_ratio < 40 else '#FF9500' if payment_to_income_ratio < 60 else '#E63946'};">{payment_to_income_ratio:.1f}%</span>
                </div>
            </div>
            """
            st.html(finance_html)
            st.html(wealth_html)
            st.html(loan_html)



# -------------------- FINANCIAL PARAMETER INPUTS --------------------
# Calculate financial metrics
metrics = calculate_financial_metrics(financial_vars)

# Render the financial summary section
render_financial_summary(financial_vars, metrics)