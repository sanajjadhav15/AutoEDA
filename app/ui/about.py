import streamlit as st
from PIL import Image

def show_about_section():
    st.markdown("---")
    with st.expander("👨‍💻 About Me"):
        col1, col2 = st.columns([1, 3])
        #some space
        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

        with col1:
            try:
                image = Image.open("app/profile.png")
                st.image(image, caption="", use_container_width=True)
            except FileNotFoundError:
                st.warning("Upload 'profile.png' in the project root to show your picture.")

        with col2:
            st.markdown("""
            <div style="font-size: 17px; line-height: 1.6; color: #e5e7eb;">
                <p>Hi there! 👋 I’m <span style="color:#22c55e; font-weight:bold;">Sanaj Jadhav</span> — a data analyst who loves turning messy data into clean, insight-packed dashboards.</p>
                <p>I specialize in exploratory data analysis, smart automation, and building tools that make data look good and make sense — fast.</p>
                <p>From streaming service trends to AutoEDA magic, I mix clean Python code 🐍, storytelling 📊, and a sprinkle of creativity ✨ to make data actually mean something.</p>
                <p>My mission? Turn data confusion into clarity — one dashboard at a time. 🚀</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div style="margin-top: 20px;">
                <h4 style="color:#f3f4f6;">🛠️ Tech Stack</h4>
                <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px;">
                    <span style="background-color:#1f2937; padding:6px 12px; border-radius:20px;">Python</span>
                    <span style="background-color:#1f2937; padding:6px 12px; border-radius:20px;">Pandas</span>
                    <span style="background-color:#1f2937; padding:6px 12px; border-radius:20px;">Numpy</span>
                    <span style="background-color:#1f2937; padding:6px 12px; border-radius:20px;">MySQL</span>
                    <span style="background-color:#1f2937; padding:6px 12px; border-radius:20px;">C++</span>
                    <span style="background-color:#1f2937; padding:6px 12px; border-radius:20px;">Matplotlib</span>
                    <span style="background-color:#1f2937; padding:6px 12px; border-radius:20px;">Seaborn</span>
                    <span style="background-color:#1f2937; padding:6px 12px; border-radius:20px;">Plotly</span>
                    <span style="background-color:#1f2937; padding:6px 12px; border-radius:20px;">Tableau</span>
                    <span style="background-color:#1f2937; padding:6px 12px; border-radius:20px;">Power BI</span>
                    <span style="background-color:#1f2937; padding:6px 12px; border-radius:20px;">Streamlit</span>
                    <span style="background-color:#1f2937; padding:6px 12px; border-radius:20px;">Excel</span>
                    <span style="background-color:#1f2937; padding:6px 12px; border-radius:20px;">HTML</span>
                    <span style="background-color:#1f2937; padding:6px 12px; border-radius:20px;">CSS</span>
                    <span style="background-color:#1f2937; padding:6px 12px; border-radius:20px;">JavaScript</span>
                    <span style="background-color:#1f2937; padding:6px 12px; border-radius:20px;">React</span>
                    <span style="background-color:#1f2937; padding:6px 12px; border-radius:20px;">Git</span>
                    <span style="background-color:#1f2937; padding:6px 12px; border-radius:20px;">Github</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            #icons for linkedin github and email
            st.markdown("""
            <style>
                .connect-container {
                    margin-top: 30px;
                }
                .connect-heading {
                    color: #f3f4f6;
                    font-size: 20px;
                    margin-bottom: 12px;
                }
                .social-icons {
                    display: flex;
                    gap: 18px;
                    flex-wrap: wrap;
                }
                .social-icons a img {
                    transition: transform 0.2s ease, box-shadow 0.2s ease;
                    border-radius: 8px;
                }
                .social-icons a img:hover {
                    transform: scale(1.08);
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
                }
            </style>

            <div class="connect-container">
                <h4 class="connect-heading">🤝 Let's Connect</h4>
                <div class="social-icons">
                    <a href="https://www.linkedin.com/in/sanaj-jadhav/" target="_blank">
                        <img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white">
                    </a>
                    <a href="https://github.com/sanajjadhav" target="_blank">
                        <img src="https://img.shields.io/badge/GitHub-171717?style=for-the-badge&logo=github&logoColor=white">
                    </a>
                    <a href="mailto:sanajjadhav77@gmail.com">
                        <img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white">
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True)


    # Inspirational Quote (outside the expander)
        # Inspirational Quote (center aligned)
    st.markdown("""
    <div style="margin-top: 25px; padding: 15px; text-align: center;">
        <p style="color:#d1d5db; font-style: italic; font-size: 16px;">
            “I tell data to sit up straight, look sharp, and say something meaningful.”
        </p>
    </div>
    """, unsafe_allow_html=True)

