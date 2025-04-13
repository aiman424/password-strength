import streamlit as st
import re

# Set page config
st.set_page_config(
    page_title="🔒 Password Strength Checker",
    page_icon="🔒",
    layout="centered"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stTextInput>div>div>input {
        border-radius: 8px;
        padding: 10px;
    }
    .password-strength-bar {
        height: 10px;
        border-radius: 5px;
        margin: 10px 0;
        background-color: #e9ecef;
    }
    .strength-0 {
        background-color: #dc3545;
        width: 20%;
    }
    .strength-1 {
        background-color: #fd7e14;
        width: 40%;
    }
    .strength-2 {
        background-color: #ffc107;
        width: 60%;
    }
    .strength-3 {
        background-color: #28a745;
        width: 80%;
    }
    .strength-4 {
        background-color: #28a745;
        width: 100%;
        animation: pulse 2s infinite;
    }
    .feedback-box {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    .suggestions {
        color: #6c757d;
        font-size: 0.9rem;
    }
    </style>
    """, unsafe_allow_html=True)

def check_password_strength(password):
    if not password:
        return 0, "Enter a password to check its strength", []
    
    # Initialize score
    score = 0
    
    # Length check
    length = len(password)
    if length >= 12:
        score += 2
    elif length >= 8:
        score += 1
    
    # Character diversity checks
    has_lower = bool(re.search(r'[a-z]', password))
    has_upper = bool(re.search(r'[A-Z]', password))
    has_digit = bool(re.search(r'[0-9]', password))
    has_special = bool(re.search(r'[^A-Za-z0-9]', password))
    
    # Add to score based on character diversity
    score += sum([has_lower, has_upper, has_digit, has_special])
    
    # Cap score at 4
    score = min(score, 4)
    
    # Strength feedback
    feedback = {
        0: "Very Weak - Easily guessable",
        1: "Weak - Vulnerable to simple attacks",
        2: "Moderate - Can resist basic attacks",
        3: "Strong - Can resist most attacks",
        4: "Very Strong - Highly resistant to attacks"
    }
    
    # Suggestions
    suggestions = []
    if length < 12:
        suggestions.append("Use at least 12 characters")
    if not has_upper:
        suggestions.append("Add uppercase letters")
    if not has_lower:
        suggestions.append("Add lowercase letters")
    if not has_digit:
        suggestions.append("Add numbers")
    if not has_special:
        suggestions.append("Add special characters (!@#$% etc.)")
    if password.lower() in ['password', '123456', 'qwerty', 'letmein']:
        suggestions.append("Avoid common passwords")
    
    return score, feedback.get(score, "Unknown"), suggestions

# App layout
st.title("🔒 Password Strength Checker")
st.markdown("Check how strong your password is and get improvement suggestions")

# Password input
password = st.text_input(
    "Enter your password", 
    type="password",
    placeholder="Type your password here...",
    help="We don't store your password anywhere"
)

# Check strength when password is entered
if password:
    score, strength_text, suggestions = check_password_strength(password)
    
    # Display strength meter
    st.markdown(f"**Strength:** {strength_text}")
    st.markdown(f'<div class="password-strength-bar"><div class="strength-{score}"></div></div>', unsafe_allow_html=True)
    
    # Display feedback box
    with st.container():
        st.markdown('<div class="feedback-box">', unsafe_allow_html=True)
        st.subheader("Password Analysis")
        
        # Crack time estimation (simplified)
        crack_time = {
            0: "less than a second",
            1: "a few seconds to minutes",
            2: "hours to days",
            3: "months to years",
            4: "centuries"
        }.get(score, "unknown")
        
        st.write(f"⏱️ **Estimated time to crack:** {crack_time}")
        
        # Suggestions for improvement
        if suggestions:
            st.write("💡 **Suggestions to improve:**")
            for suggestion in suggestions:
                st.write(f"- {suggestion}")
        else:
            st.write("🎉 Great job! Your password meets all security recommendations.")
        st.markdown('</div>', unsafe_allow_html=True)
        
    # Password requirements checklist
    st.subheader("Password Requirements")
    col1, col2 = st.columns(2)
    
    with col1:
        st.checkbox("At least 8 characters", value=len(password) >= 8, disabled=True)
        st.checkbox("Contains uppercase letter", value=bool(re.search(r'[A-Z]', password)), disabled=True)
        st.checkbox("Contains number", value=bool(re.search(r'[0-9]', password)), disabled=True)
        
    with col2:
        st.checkbox("Contains lowercase letter", value=bool(re.search(r'[a-z]', password)), disabled=True)
        st.checkbox("Contains special character", value=bool(re.search(r'[^A-Za-z0-9]', password)), disabled=True)
        st.checkbox("At least 12 characters", value=len(password) >= 12, disabled=True)

# Sidebar with info
with st.markdown("---"):
    st.write("💡 **Tips for strong passwords:**")
    st.write("- Use at least 12 characters")
    st.write("- Combine letters, numbers, and symbols")
    st.write("- Avoid common words and personal info")
    st.write("- Consider using a passphrase")
    st.markdown("---")
    st.write("Made by Aiman Rizwan ❤️")