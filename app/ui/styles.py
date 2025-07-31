# styles.py

def get_custom_css():
    """Return modern CSS styling for the AutoEDA landing page and UI"""
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;500;600;700&display=swap');

    body, .stApp {
        font-family: 'Inter', sans-serif;
        background-color: #0f172a;
        color: #f8fafc;
    }

    /* Container for hero title and subtitle */
    .hero-container {
        max-width: 900px;
        margin: 0 auto;
        text-align: center;
    }

    .hero-title {
        font-size: 3.25rem;
        font-weight: 700;
        color: #22c55e;
        line-height: 1.2;
    }

    .hero-subtitle {
        font-size: 1.125rem;
        color: #cbd5e1;
        font-weight: 400;
        line-height: 1.6;
        max-width: 800px;
        margin: 0 auto 2.5rem auto;
    }

    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 2rem;
        padding: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }

    .feature-card {
        background: #1e293b;
        border-radius: 1.25rem;
        padding: 2rem;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        border: 1px solid #334155;
    }

    .feature-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 20px 45px rgba(0, 0, 0, 0.2);
        border-color: #22c55e;
    }

    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1.5rem;
        color: #22c55e;
    }

    .feature-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #f1f5f9;
        margin-bottom: 0.5rem;
    }

    .feature-description {
        font-size: 1rem;
        color: #94a3b8;
        line-height: 1.6;
    }

    /* Floating background shapes */
    .floating-shapes {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        overflow: hidden;
        z-index: -1;
        pointer-events: none;
    }

    .shape {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.03);
        animation: float 8s ease-in-out infinite;
    }

    .shape-1 {
        top: 10%;
        left: 10%;
        width: 80px;
        height: 80px;
        animation-delay: 0s;
    }

    .shape-2 {
        top: 35%;
        right: 15%;
        width: 120px;
        height: 120px;
        animation-delay: 2s;
    }

    .shape-3 {
        bottom: 20%;
        left: 30%;
        width: 100px;
        height: 100px;
        animation-delay: 4s;
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(180deg); }
    }

    /* Responsive tweaks */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.25rem;
        }

        .hero-subtitle {
            font-size: 1rem;
        }

        .feature-card {
            padding: 1.5rem;
        }
    }

    div.stButton > button {
        background-color: #1e293b;
        color: white;
        font-weight: 500;
        border-radius: 0.75rem;
        padding: 0.6rem 1.5rem;
        border: none;
        transition: background-color 0.3s ease;
    }

    div.stButton > button:hover {
        background-color: #22c55e;
        color: #ffffff;
    }

    .type-section {
    background-color: #1e293b;
    border-radius: 1rem;
    padding: 1.5rem;
    margin-bottom: 2rem;
    border: 1px solid #334155;
    }

    .type-badge {
        display: inline-block;
        background-color: #22c55e;
        color: white;
        padding: 0.3rem 0.7rem;
        border-radius: 999px;
        margin: 0.25rem 0.4rem 0.25rem 0;
        font-size: 0.9rem;
        font-weight: 500;
    }

    .section-card {
        background-color: #1e293b;
        border-radius: 1rem;
        padding: 1.5rem;
        margin-bottom: 2rem;
        border: 1px solid #334155;
    }
    .streamlit-expanderHeader {
        font-weight: 600;
        color: #22c55e;
        font-size: 1rem;
    }

    .null-flag-badge {
        display: inline-block;
        background-color: #f43f5e;
        color: white;
        font-weight: 500;
        font-size: 0.9rem;
        padding: 0.3rem 0.7rem;
        border-radius: 999px;
        margin: 0.25rem 0.4rem 0.25rem 0;
    }


    /* Hide Streamlit native UI */
    #MainMenu, header, footer { visibility: hidden; }
    </style>
    """

def feature_card(icon, title, description):
    """Generate one feature card"""
    return f"""
    <div class='feature-card'>
        <div class='feature-icon'>{icon}</div>
        <div class='feature-title'>{title}</div>
        <div class='feature-description'>{description}</div>
    </div>
    """


def get_floating_shapes():
    """Return floating decorative background shapes"""
    return """
    <div class='floating-shapes'>
        <div class='shape shape-1'></div>
        <div class='shape shape-2'></div>
        <div class='shape shape-3'></div>
    </div>
    """


def section_block(title):
    """Styled section title block"""
    return f"""
    <h3 style='
        margin-top: 3rem;
        margin-bottom: 1rem;
        font-size: 1.5rem;
        font-weight: 600;
        color: #22c55e;
    '>{title}</h3>
    """

