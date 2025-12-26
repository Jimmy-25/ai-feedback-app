"""
AI Feedback Form App - Streamlit Version
Run this with: streamlit run app.py
"""

import streamlit as st
import json
import os
from datetime import datetime
import qrcode
from io import BytesIO
import base64

# Page configuration
st.set_page_config(
    page_title="AI Feedback System",
    page_icon="",
    layout="wide"
)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'feedbacks' not in st.session_state:
    st.session_state.feedbacks = []
if 'company_info' not in st.session_state:
    st.session_state.company_info = None
if 'feedback_url' not in st.session_state:
    st.session_state.feedback_url = "http://localhost:8501"

# Load/Save feedbacks to file
FEEDBACK_FILE = 'feedbacks.json'

def load_feedbacks():
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, 'r') as f:
            return json.load(f)
    return []

def save_feedbacks(feedbacks):
    with open(FEEDBACK_FILE, 'w') as f:
        json.dump(feedbacks, f, indent=2)

# Load feedbacks on startup
if not st.session_state.feedbacks:
    st.session_state.feedbacks = load_feedbacks()

# AI Processing Function
def process_feedback_with_ai(feedback_text, category, company_context=""):
    """
    Simulates AI processing of feedback
    In production, this would call an actual AI API
    """
    
    improved = feedback_text
    solution = ""
    
    # Check feedback length and improve clarity
    if len(feedback_text) < 20:
        improved = f"Customer feedback indicates: {feedback_text}. Additional context would be helpful."
    
    lower_feedback = feedback_text.lower()
    
    # Generate solutions based on keywords and company context
    if 'slow' in lower_feedback or 'wait' in lower_feedback:
        solution = f"Recommendation: Increase staff during peak hours. Consider implementing a queue management system. {company_context}"
    elif 'dirty' in lower_feedback or 'clean' in lower_feedback:
        solution = "Recommendation: Implement more frequent cleaning schedules and conduct regular hygiene inspections."
    elif 'rude' in lower_feedback or 'unfriendly' in lower_feedback or 'staff' in lower_feedback:
        solution = "Recommendation: Provide customer service training for staff and establish clear communication guidelines."
    elif 'price' in lower_feedback or 'expensive' in lower_feedback or 'cheap' in lower_feedback:
        solution = "Recommendation: Review pricing strategy and consider offering value packages or loyalty programs."
    elif 'food' in lower_feedback or 'meal' in lower_feedback or 'taste' in lower_feedback:
        solution = "Recommendation: Gather specific feedback about menu items and consider taste testing with focus groups."
    elif 'long' in lower_feedback or 'boring' in lower_feedback:
        solution = "Recommendation: Break sessions into shorter segments with interactive elements and regular breaks."
    elif 'good' in lower_feedback or 'great' in lower_feedback or 'excellent' in lower_feedback:
        solution = "Positive feedback received! Continue maintaining these high standards and consider what's working well."
    else:
        solution = f"Recommendation: Follow up with customer for more specific details. {company_context if company_context else 'Consider implementing regular feedback sessions.'}"
    
    return improved, solution

# Generate QR Code
def generate_qr_code(url):
    """Generate QR code for the feedback form"""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to bytes
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf

# Navigation
def navigate_to(page):
    st.session_state.page = page
    st.rerun()

# ===== HOME PAGE =====
def show_home():
    st.title(" AI Feedback System")
    st.markdown("### Welcome to the Intelligent Feedback Management Platform")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### For Companies")
        st.info("Set up your custom feedback form and get AI-powered insights")
        if st.button("Company Setup", use_container_width=True, type="primary"):
            navigate_to('setup')
    
    with col2:
        st.markdown("#### View Dashboard")
        st.info("Access your feedback dashboard and AI recommendations")
        if st.button("Staff Dashboard", use_container_width=True):
            navigate_to('login')
    
    st.markdown("---")
    st.markdown("#### Submit Feedback")
    st.success("Customers can scan the QR code or click below to submit feedback")
    if st.button("Go to Feedback Form", use_container_width=True):
        navigate_to('feedback')

# ===== COMPANY SETUP PAGE =====
def show_setup():
    st.title(" Company Setup")
    
    if st.button("← Back to Home"):
        navigate_to('home')
    
    st.markdown("### Configure Your Feedback System")
    
    with st.form("company_setup"):
        company_name = st.text_input("Company Name *", placeholder="e.g., Sunset Restaurant")
        
        company_type = st.selectbox(
            "Business Type *",
            ["Restaurant", "School", "Hotel", "Retail Store", "Healthcare", "Other"]
        )
        
        company_description = st.text_area(
            "Company Description *",
            placeholder="Describe your business, services, and what makes you unique...",
            height=150
        )
        
        focus_areas = st.multiselect(
            "Key Focus Areas",
            ["Customer Service", "Product Quality", "Cleanliness", "Speed", "Value for Money", "Ambiance", "Communication"],
            default=["Customer Service", "Product Quality"]
        )
        
        st.markdown("### Feedback Form Customization")
        
        custom_categories = st.text_input(
            "Custom Categories (comma-separated)",
            placeholder="e.g., Food Quality, Service, Ambiance, Pricing",
            value="General, Service, Quality, Environment"
        )
        
        enable_rating = st.checkbox("Enable Star Rating", value=True)
        
        submitted = st.form_submit_button("Generate Feedback System", type="primary", use_container_width=True)
        
        if submitted:
            if company_name and company_description:
                company_info = {
                    'name': company_name,
                    'type': company_type,
                    'description': company_description,
                    'focus_areas': focus_areas,
                    'categories': [cat.strip() for cat in custom_categories.split(',')],
                    'enable_rating': enable_rating,
                    'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                st.session_state.company_info = company_info
                st.success("✅ Feedback system generated successfully!")
                
                # Generate QR Code
                st.markdown("---")
                st.markdown("### QR Code for Customer Access")
                st.info("Print this QR code and place it where customers can scan it")
                
                qr_buf = generate_qr_code(st.session_state.feedback_url)
                st.image(qr_buf, caption="Scan to Submit Feedback", width=300)
                
                
                if st.button("View Feedback Form", type="primary"):
                    navigate_to('feedback')
            else:
                st.error("Please fill in all required fields (*)")

# ===== FEEDBACK FORM PAGE =====
def show_feedback_form():
    # Check if company is set up
    if not st.session_state.company_info:
        st.warning(" No company setup found. Using default settings.")
        company_name = "Our Company"
        categories = ["General", "Service", "Quality", "Environment"]
        enable_rating = True
    else:
        company_name = st.session_state.company_info['name']
        categories = st.session_state.company_info['categories']
        enable_rating = st.session_state.company_info['enable_rating']
    
    st.title(f" Feedback Form - {company_name}")
    st.markdown("### We Value Your Opinion!")
    st.info("Your feedback helps us improve our service")
    
    with st.form("feedback_form"):
        category = st.selectbox("Category", categories)
        
        if enable_rating:
            rating = st.slider("Rating (1-5 stars)", 1, 5, 3)
        else:
            rating = 0
        
        feedback_text = st.text_area(
            "Your Feedback *",
            placeholder="Share your experience, suggestions, or concerns...",
            height=150
        )
        
        submitted = st.form_submit_button("Submit Feedback", type="primary", use_container_width=True)
        
        if submitted:
            if feedback_text.strip():
                # Process with AI
                with st.spinner("Processing your feedback with AI..."):
                    company_context = ""
                    if st.session_state.company_info:
                        company_context = f"Company context: {st.session_state.company_info['description']}"
                    
                    improved, solution = process_feedback_with_ai(
                        feedback_text, 
                        category, 
                        company_context
                    )
                    
                    # Save feedback
                    feedback_entry = {
                        'id': len(st.session_state.feedbacks) + 1,
                        'company': company_name,
                        'category': category,
                        'rating': rating,
                        'original': feedback_text,
                        'improved': improved,
                        'solution': solution,
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                    st.session_state.feedbacks.insert(0, feedback_entry)
                    save_feedbacks(st.session_state.feedbacks)
                    
                    st.success("✅ Thank you! Your feedback has been submitted successfully.")
                    st.balloons()
            else:
                st.error("Please enter your feedback before submitting.")
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Home"):
            navigate_to('home')
    with col2:
        if st.button("Submit Another Feedback"):
            st.rerun()

# ===== LOGIN PAGE =====
def show_login():
    st.title(" Staff Login")
    
    if st.button("← Back to Home"):
        navigate_to('home')
    
    st.markdown("### Access Dashboard")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        login_btn = st.form_submit_button("Login", type="primary", use_container_width=True)
        
        if login_btn:
            # Simple authentication (for demo)
            if username == "admin" and password == "admin123":
                st.session_state.logged_in = True
                navigate_to('dashboard')
            else:
                st.error("Invalid credentials. Try username: admin, password: admin123")
    
    st.info("**Demo Credentials:**\n\nUsername: `admin`\n\nPassword: `admin123`")

# ===== DASHBOARD PAGE =====
def show_dashboard():
    if not st.session_state.get('logged_in', False):
        navigate_to('login')
        return
    
    st.title(" Feedback Dashboard")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown("### All Feedback Submissions")
    with col2:
        if st.button(" Home"):
            navigate_to('home')
    with col3:
        if st.button(" Logout"):
            st.session_state.logged_in = False
            navigate_to('home')
    
    # Statistics
    total_feedbacks = len(st.session_state.feedbacks)
    if total_feedbacks > 0:
        avg_rating = sum(f['rating'] for f in st.session_state.feedbacks if f['rating'] > 0) / max(1, sum(1 for f in st.session_state.feedbacks if f['rating'] > 0))
    else:
        avg_rating = 0
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Feedback", total_feedbacks)
    col2.metric("Average Rating", f"{avg_rating:.1f}/5.0" if avg_rating > 0 else "N/A")
    col3.metric("Recent (24h)", sum(1 for f in st.session_state.feedbacks))
    
    st.markdown("---")
    
    # Filters
    if st.session_state.feedbacks:
        categories = list(set(f['category'] for f in st.session_state.feedbacks))
        filter_category = st.selectbox("Filter by Category", ["All"] + categories)
        
        # Filter feedbacks
        filtered_feedbacks = st.session_state.feedbacks
        if filter_category != "All":
            filtered_feedbacks = [f for f in st.session_state.feedbacks if f['category'] == filter_category]
        
        st.markdown(f"**Showing {len(filtered_feedbacks)} feedback(s)**")
        
        # Display feedbacks
        for feedback in filtered_feedbacks:
            with st.expander(f"#{feedback['id']} - {feedback['category']} - {feedback['timestamp']}"):
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    st.markdown("**Rating:**")
                    if feedback['rating'] > 0:
                        st.markdown(str(feedback['rating']))

                    else:
                        st.markdown("No rating")
                    
                    st.markdown(f"**Category:** {feedback['category']}")
                    st.markdown(f"**Date:** {feedback['timestamp']}")
                
                with col2:
                    st.markdown("**Original Feedback:**")
                    st.text_area("", feedback['original'], height=80, disabled=True, key=f"orig_{feedback['id']}")
                    
                    st.markdown("** AI-Improved Feedback:**")
                    st.info(feedback['improved'])
                    
                    st.markdown("** AI-Suggested Solution:**")
                    st.success(feedback['solution'])
    else:
        st.info("No feedback submitted yet. Go to the feedback form to submit one!")
        if st.button("Go to Feedback Form"):
            navigate_to('feedback')

# ===== MAIN APP LOGIC =====
def main():
    # Sidebar
    with st.sidebar:
        st.markdown("## Navigation")
        st.markdown("---")
        
        if st.button(" Home", use_container_width=True):
            navigate_to('home')
        
        if st.button(" Company Setup", use_container_width=True):
            navigate_to('setup')
        
        if st.button(" Feedback Form", use_container_width=True):
            navigate_to('feedback')
        
        if st.button(" Dashboard", use_container_width=True):
            navigate_to('login')
        
        st.markdown("---")
        st.markdown("###  Quick Info")
        if st.session_state.company_info:
            st.success(f" Setup: {st.session_state.company_info['name']}")
        else:
            st.warning(" No company setup")
        
        st.metric("Total Feedback", len(st.session_state.feedbacks))
        
        st.markdown("---")
        st.markdown("**Demo Login:**")
        st.code("admin / admin123")
    
    # Main content based on current page
    if st.session_state.page == 'home':
        show_home()
    elif st.session_state.page == 'setup':
        show_setup()
    elif st.session_state.page == 'feedback':
        show_feedback_form()
    elif st.session_state.page == 'login':
        show_login()
    elif st.session_state.page == 'dashboard':
        show_dashboard()

if __name__ == "__main__":

    main()


