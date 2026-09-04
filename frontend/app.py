import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# --------------------------------------------------
# Configuration
# --------------------------------------------------

API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000"
)

st.set_page_config(
    page_title="Indian Diet AI",
    layout="wide"
)


# --------------------------------------------------
# Theme — fonts, colors, component styling
# --------------------------------------------------
# Palette is grounded in the subject: turmeric and chili are the two
# pigments that define Indian cooking, rendered as neon accents on a
# deep charcoal base. Space Grotesk carries headlines (a geometric,
# slightly technical face for the "AI" side of the product); Inter
# carries body copy for readability.

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&display=swap');

    :root {
        --bg: #0B0E14;
        --surface: #141924;
        --surface-2: #1B2230;
        --border: #262E3D;
        --text: #F2F0EA;
        --text-muted: #8E97AB;
        --turmeric: #FFB627;
        --mint: #2BFFB0;
        --chili: #FF5470;
    }

    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: var(--bg);
        color: var(--text);
        font-family: 'Inter', sans-serif;
    }
    [data-testid="stAppViewContainer"] {
        background-image:
            radial-gradient(circle at 8% -10%, rgba(255, 182, 39, 0.07), transparent 42%),
            radial-gradient(circle at 92% 10%, rgba(43, 255, 176, 0.06), transparent 40%);
        background-repeat: no-repeat;
    }
    [data-testid="stHeader"] { background-color: transparent; }
    [data-testid="stMain"] .block-container { padding-top: 2.2rem; max-width: 1180px; }

    ::-webkit-scrollbar { width: 10px; height: 10px; }
    ::-webkit-scrollbar-track { background: var(--bg); }
    ::-webkit-scrollbar-thumb {
        background: var(--surface-2);
        border: 1px solid var(--border);
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover { background: var(--border); }

    /* ---------- Typography ---------- */
    h1, h2, h3, h4 {
        font-family: 'Space Grotesk', sans-serif !important;
        color: var(--text) !important;
        letter-spacing: -0.01em;
    }
    h2 {
        margin-top: 1.3rem !important;
        margin-bottom: 0.7rem !important;
        padding-bottom: 0.6rem;
        border-bottom: 1px solid var(--border);
    }
    p, span, label, div { font-family: 'Inter', sans-serif; }

    /* ---------- Hero ---------- */
    .hero-wrap {
        padding: 1.4rem 0 1.9rem 0;
        border-bottom: 1px solid var(--border);
        margin-bottom: 2rem;
        position: relative;
    }
    .hero-title {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 2.9rem;
        line-height: 1.08;
        margin: 0;
        background: linear-gradient(100deg, var(--turmeric) 0%, var(--mint) 65%);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
    }
    .hero-sub {
        color: var(--text-muted);
        font-size: 1.06rem;
        line-height: 1.6;
        margin-top: 0.6rem;
        max-width: 600px;
    }

    /* ---------- Sidebar ---------- */
    [data-testid="stSidebar"] {
        background-color: var(--surface);
        border-right: 1px solid var(--border);
    }
    [data-testid="stSidebar"] h1 {
        font-size: 1.25rem !important;
        padding: 1.2rem 0 0.4rem 0;
        margin: 0 !important;
    }
    [data-testid="stSidebar"] input[type="radio"] {
        accent-color: var(--turmeric);
    }
    [data-testid="stSidebar"] [role="radiogroup"] {
        gap: 0.45rem;
    }
    [data-testid="stSidebar"] [role="radiogroup"] label {
        background-color: var(--surface-2);
        border: 1px solid var(--border);
        border-left: 3px solid transparent;
        border-radius: 8px;
        padding: 0.6rem 0.9rem;
        transition: border-color 0.15s ease, background-color 0.15s ease;
        min-height: 4rem;
        display: flex;
        align-items: center;
        width: 100%;
        box-sizing: border-box;
    }
    [data-testid="stSidebar"] [role="radiogroup"] label:hover {
        border-color: var(--turmeric);
        border-left-color: var(--turmeric);
        background-color: rgba(255, 182, 39, 0.06);
    }
    [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
        border-left-color: var(--mint);
        background-color: rgba(43, 255, 176, 0.07);
    }
    [data-testid="stSidebar"] [role="radiogroup"] label p {
        font-weight: 500;
        font-size: 0.94rem;
    }
    .sidebar-meta {
        background-color: var(--surface-2);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 0.9rem 1rem;
        font-size: 0.85rem;
        color: var(--text-muted);
        line-height: 1.7;
    }
    .sidebar-meta b { color: var(--text); }

    /* ---------- Forms & inputs ---------- */
    [data-testid="stForm"] {
        background-color: var(--surface);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.6rem 1.6rem 0.6rem 1.6rem;
    }
    [data-testid="stNumberInput"] input,
    [data-testid="stTextInput"] input,
    [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        background-color: var(--surface-2) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        color: var(--text) !important;
    }
    [data-testid="stNumberInput"] input:focus,
    [data-testid="stTextInput"] input:focus {
        border-color: var(--turmeric) !important;
        box-shadow: 0 0 0 2px rgba(255, 182, 39, 0.15) !important;
    }

    /* ---------- Buttons ---------- */
    .stButton > button, .stFormSubmitButton > button {
        background: linear-gradient(110deg, var(--turmeric), var(--chili));
        color: #0B0E14;
        font-weight: 600;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.1rem;
        transition: box-shadow 0.15s ease, transform 0.15s ease;
    }
    .stButton > button:hover, .stFormSubmitButton > button:hover {
        box-shadow: 0 0 22px rgba(255, 182, 39, 0.35);
        transform: translateY(-1px);
        color: #0B0E14;
    }

    /* ---------- Metrics ---------- */
    [data-testid="stMetric"] {
        background-color: var(--surface);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 1rem 1.1rem;
        transition: box-shadow 0.2s ease;
    }
    [data-testid="stMetric"]:hover {
        box-shadow: 0 0 20px rgba(43, 255, 176, 0.12);
        border-color: var(--mint);
    }
    [data-testid="stMetricValue"] {
        font-family: 'Space Grotesk', sans-serif !important;
        color: var(--mint) !important;
        font-size: 1.7rem !important;
    }
    [data-testid="stMetricLabel"] {
        color: var(--text-muted) !important;
    }

    /* ---------- Alerts ---------- */
    [data-testid="stAlertContainer"] {
        background-color: var(--surface) !important;
        border-radius: 10px !important;
        border: 1px solid var(--border) !important;
    }

    /* ---------- Chat ---------- */
    [data-testid="stChatMessage"] {
        background-color: var(--surface);
        border: 1px solid var(--border);
        border-radius: 14px;
    }
    [data-testid="stChatInput"] textarea {
        background-color: var(--surface-2) !important;
        border: 1px solid var(--border) !important;
        color: var(--text) !important;
    }
    /* Un-pin the chat input from the viewport bottom so it sits
       right after the message list instead of floating far below
       on pages with little chat history. */
    [data-testid="stBottom"] {
        position: relative !important;
        background-color: transparent !important;
    }
    [data-testid="stBottom"] > div {
        padding-top: 0.5rem !important;
        padding-bottom: 0 !important;
    }
    [data-testid="stMain"] .block-container {
        padding-bottom: 2.5rem !important;
    }

    /* ---------- Dividers ---------- */
    hr { border-color: var(--border) !important; }

    /* ---------- Tech chips (About page) ---------- */
    .chip-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 0.6rem;
        margin: 1rem 0 1.6rem 0;
    }
    .chip {
        background-color: var(--surface);
        border: 1px solid var(--border);
        border-radius: 999px;
        padding: 0.45rem 1rem;
        font-size: 0.88rem;
        color: var(--text);
        transition: border-color 0.15s ease, color 0.15s ease;
    }
    .chip:hover {
        border-color: var(--mint);
        color: var(--mint);
    }
    .flow-card {
        background-color: var(--surface);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 1.1rem 1.3rem;
        margin-bottom: 0.6rem;
    }
    .flow-arrow {
        color: var(--text-muted);
        margin: 0.1rem 0 0.1rem 1.6rem;
        font-family: 'Space Grotesk', sans-serif;
    }

    /* ---------- Food search results ---------- */
    .food-card {
        background-color: var(--surface);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 1.2rem 1.3rem;
        margin-bottom: 1rem;
    }
    .food-card-title {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        font-size: 1.15rem;
        color: var(--text);
        margin-bottom: 0.6rem;
    }
    .food-tag-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-bottom: 0.8rem;
    }
    .food-tag {
        background-color: var(--surface-2);
        border: 1px solid var(--border);
        border-radius: 999px;
        padding: 0.25rem 0.75rem;
        font-size: 0.8rem;
        color: var(--text-muted);
    }
    .food-tag b { color: var(--text); }
    .food-tag.score { color: var(--mint); border-color: var(--mint); }
    .food-tag.score b { color: var(--mint); }
    .food-nutrition {
        background-color: var(--surface-2);
        border: 1px solid var(--border);
        border-left: 3px solid var(--turmeric);
        border-radius: 8px;
        padding: 0.8rem 1rem;
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        color: var(--text);
        white-space: pre-wrap;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# Helper Functions
# --------------------------------------------------

def calculate_calories(data):
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/calorie/calculate",
            json=data,
            timeout=120
        )

        if response.status_code == 200:
            return response.json()

        st.error(response.json().get("detail", "Calculation failed."))
        return None

    except requests.exceptions.ConnectionError:
        st.error(
            "Cannot connect to FastAPI. "
            "Make sure the backend is running."
        )
        return None

    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {e}")
        return None


def ask_ai(query, context_query=None, top_k=5):
    try:
        payload = {"query": query, "top_k": top_k}
        if context_query:
            payload["context_query"] = context_query
            
        response = requests.post(
            f"{API_BASE_URL}/api/chat",
            json=payload,
            timeout=120
        )

        if response.status_code == 200:
            return response.json().get("answer")

        st.error(response.json().get("detail", "AI request failed."))
        return None

    except requests.exceptions.ConnectionError:
        st.error(
            "Cannot connect to FastAPI. "
            "Start the backend first."
        )
        return None

    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {e}")
        return None


def search_food_api(query, top_k):
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/food/search",
            params={"query": query, "top_k": top_k},
            timeout=60
        )

        if response.status_code == 200:
            return response.json()

        st.error(response.json().get("detail", "Search failed."))
        return None

    except requests.exceptions.ConnectionError:
        st.error(
            "Cannot connect to FastAPI. "
            "Make sure the backend is running."
        )
        return None

    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {e}")
        return None





# --------------------------------------------------
# Sidebar
# --------------------------------------------------

st.sidebar.markdown("# Indian Diet AI")

page = st.sidebar.radio(
    "Navigate",
    [
        "Calorie Calculator",
        "Food Calorie Search",
        "AI Nutrition Assistant",
        "Diet Recommendation",
        "About"
    ],
    label_visibility="collapsed"
)

st.sidebar.divider()

st.sidebar.markdown(
    """
    <div class="sidebar-meta">
        <b>Backend</b> — FastAPI<br>
        <b>LLM</b> — Gemini<br>
        <b>RAG</b> — Qdrant
    </div>
    """,
    unsafe_allow_html=True
)


# ==================================================
# PAGE 1 — CALORIE CALCULATOR
# ==================================================

if page == "Calorie Calculator":

    st.markdown(
        """
        <div class="hero-wrap">
            <p class="hero-title">Indian Diet AI</p>
            <p class="hero-sub">
                An LLM + RAG assistant that calculates your calorie needs and
                builds personalized Indian diet plans from a real nutrition
                knowledge base.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.header("Calorie Calculator")

    st.write(
        "Enter your details to calculate BMR, TDEE, "
        "BMI and your estimated daily calorie target."
    )

    with st.form("calorie_form"):

        col1, col2 = st.columns(2)

        with col1:

            age = st.number_input(
                "Age",
                min_value=0,
                max_value=120,
                value=0,
                help="Your age in years",
                key="calc_age"
            )

            gender = st.selectbox(
                "Gender",
                ["female", "male"],
                key="calc_gender"
            )

            height = st.number_input(
                "Height (cm)",
                min_value=0.0,
                max_value=250.0,
                value=0.0,
                key="calc_height"
            )

        with col2:

            weight = st.number_input(
                "Weight (kg)",
                min_value=0.0,
                max_value=300.0,
                value=0.0,
                key="calc_weight"
            )

            activity = st.selectbox(
                "Activity Level",
                [
                    "Sedentary",
                    "Lightly Active",
                    "Moderate",
                    "Highly Active",
                    "Extremely Active"
                ],
                key="calc_activity"
            )

            goal = st.selectbox(
                "Goal",
                [
                    "Weight Loss",
                    "Maintenance",
                    "Weight Gain"
                ],
                key="calc_goal"
            )

        submitted = st.form_submit_button(
            "Calculate",
            use_container_width=True
        )

    if submitted:

        user_data = {
            "age": age,
            "gender": gender,
            "height_cm": height,
            "weight_kg": weight,
            "activity_level": activity,
            "goal": goal
        }

        result = calculate_calories(user_data)

        if result:

            st.success("Calculation completed")

            st.divider()

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(
                "BMR",
                f"{result['bmr']} kcal"
            )

            col2.metric(
                "TDEE",
                f"{result['tdee']} kcal"
            )

            col3.metric(
                "BMI",
                result["bmi"]
            )

            col4.metric(
                "Daily Target",
                f"{result['daily_calorie_target']} kcal"
            )

            st.divider()

            st.subheader("Your Results")

            result_col1, result_col2 = st.columns(2)

            with result_col1:

                st.write("**Goal:**")

                st.info(
                    result["goal"].replace("_", " ").title()
                )

            with result_col2:

                st.write("**Recommended Daily Calories:**")

                st.success(
                    f"{result['daily_calorie_target']} kcal/day"
                )


# ==================================================
# PAGE 2 — FOOD CALORIE SEARCH
# ==================================================

elif page == "Food Calorie Search":

    st.header("Indian Food Calorie Search")

    st.write(
        "Search the nutrition database for Indian foods."
    )

    query = st.text_input(
        "Search food",
        placeholder="e.g. paneer, dal, roti, biryani"
    )

    top_k = st.slider(
        "Number of results",
        min_value=1,
        max_value=10,
        value=5
    )

    if st.button(
        "Search Food",
        use_container_width=True
    ):

        if not query.strip():
            st.warning(
                "Please enter a food name."
            )

        else:

            with st.spinner(
                "Searching nutrition database..."
            ):

                data = search_food_api(
                    query,
                    top_k
                )

            if data and data["results"]:

                st.success(
                    f"Found {len(data['results'])} results."
                )

                for item in data["results"]:

                    st.markdown(
                        f"""
                        <div class="food-card">
                            <div class="food-card-title">{item['food']}</div>
                            <div class="food-tag-row">
                                <span class="food-tag"><b>Calories</b> — {item.get('calories', 'N/A')}</span>
                                <span class="food-tag"><b>Protein</b> — {item.get('protein', 'N/A')}</span>
                                <span class="food-tag"><b>Carbs</b> — {item.get('carbohydrates', 'N/A')}</span>
                                <span class="food-tag"><b>Fat</b> — {item.get('fat', 'N/A')}</span>
                                <span class="food-tag"><b>Fibre</b> — {item.get('fibre', 'N/A')}</span>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            else:
                st.warning(
                    "No matching food found."
                )


# ==================================================
# PAGE 3 — AI NUTRITION ASSISTANT
# ==================================================

elif page == "AI Nutrition Assistant":

    st.header("AI Nutrition Assistant")

    st.write(
        "Ask questions about Indian foods, calories, "
        "protein, carbohydrates, fats and nutrition."
    )

    # Container for the input
    input_container = st.container()
    
    st.write("") # some spacing

    # Container for messages below input
    messages_container = st.container()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    with messages_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    query = input_container.chat_input(
        "Ask something like: How many calories are in paneer?"
    )

    if query:
        st.session_state.messages.append(
            {
                "role": "user",
                "content": query
            }
        )

        with messages_container:
            with st.chat_message("user"):
                st.markdown(query)

            with st.chat_message("assistant"):
                with st.spinner("Searching nutrition knowledge..."):
                    answer = ask_ai(query)

                if answer:
                    st.markdown(answer)
                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": answer
                        }
                    )


# ==================================================
# PAGE 4 — DIET RECOMMENDATION
# ==================================================

elif page == "Diet Recommendation":

    st.header("Personalized Diet Recommendation")

    st.write(
        "Generate a diet recommendation based on "
        "your profile and fitness goal."
    )

    col1, col2 = st.columns(2)

    with col1:

        age = st.number_input(
            "Age",
            min_value=0,
            max_value=120,
            value=0,
            key="diet_age"
        )

        gender = st.selectbox(
            "Gender",
            ["female", "male"],
            key="diet_gender"
        )

        height = st.number_input(
            "Height (cm)",
            min_value=0.0,
            max_value=250.0,
            value=0.0,
            key="diet_height"
        )

        weight = st.number_input(
            "Weight (kg)",
            min_value=0.0,
            max_value=300.0,
            value=0.0,
            key="diet_weight"
        )

    with col2:

        activity = st.selectbox(
            "Activity Level",
            [
                "Sedentary",
                "Lightly Active",
                "Moderate",
                "Highly Active",
                "Extremely Active"
            ],
            key="diet_activity"
        )

        goal = st.selectbox(
            "Goal",
            [
                "Weight Loss",
                "Maintenance",
                "Weight Gain"
            ],
            key="diet_goal"
        )

        food_preference = st.selectbox(
            "Food Preference",
            [
                "Vegetarian",
                "Non-Vegetarian",
                "Eggetarian"
            ]
        )

        meals = st.selectbox(
            "Meals Per Day",
            [2, 3, 4, 5, 6]
        )

        sugar_free = st.checkbox(
            "Sugar-Free Options Only"
        )

    if st.button(
        "Generate Diet Plan",
        use_container_width=True
    ):

        with st.spinner(
            "Calculating calories and generating your plan..."
        ):

            calorie_data = {
                "age": age,
                "gender": gender,
                "height_cm": height,
                "weight_kg": weight,
                "activity_level": activity,
                "goal": goal
            }

            calorie_result = calculate_calories(
                calorie_data
            )

            if calorie_result:

                target = calorie_result[
                    "daily_calorie_target"
                ]
                
                protein_target = calorie_result.get(
                    "daily_protein_target", "N/A"
                )

                query = f"""
Create a personalized Indian diet recommendation.

User Profile:
- Age: {age}
- Gender: {gender}
- Height: {height} cm
- Weight: {weight} kg
- Activity Level: {activity}
- Goal: {goal}
- Food Preference: {food_preference}
- Meals per day: {meals}
- Sugar-Free Preference: {'Yes' if sugar_free else 'No'} (If Yes, strictly avoid sugary foods and sweets)

Estimated targets:
- Calories: {target} kcal/day
- Protein: {protein_target} g/day

Use Indian foods from the nutrition knowledge base.

Provide:
1. A brief 1-sentence summary of the plan.
2. The Meal Plan in a clean, highly structured Markdown table with columns: [Meal Time] | [Food Item(s)] | [Calories] | [Protein (g)]
3. Approximate total daily calories and protein summary below the table. (Write this as normal sized text, do NOT use markdown headers like # or ## for this point).
4. Protein-rich food choices (highlight specific foods to meet daily protein needs)
5. Practical Indian food substitutions

CRITICAL RULES:
- Format the meal plan strictly as a single Markdown table for a clean, defined look. DO NOT use HTML tags like <br> in the table; use commas to separate multiple food items.
- ABSOLUTELY NO MATH OR CALCULATIONS. You are strictly forbidden from showing calculations anywhere in the output (e.g., avoid "149 + 105 = 254"). Output ONLY the final total numeric values. Keep all text clean and composed.
- If nutritional information for an item (like salad or plain roti) is missing from the context, invent a reasonable approximation or just leave the calories/protein blank. DO NOT write any notes, footnotes, disclaimers, or apologies about missing nutritional information or missed targets anywhere in the output. Keep the entire response perfectly clean.
- MUST include exactly 5 meals: Breakfast, Mid-morning snack, Lunch, Evening snack, and Dinner.
- Prioritize a variety of HEALTHY and nutritious options. The two snack options must be completely different from each other. DO NOT serve salads for snacks (e.g., no fruit salads or paneer salads for snacks). Salads MUST ONLY be included in Lunch and Dinner.
- If the user selects Eggetarian or Non-Vegetarian, DO NOT serve eggs or meat in every single meal. You MUST make at least 2 or 3 of the 5 meals vegetarian (without any egg or meat) to provide a realistic, balanced, and highly varied diet.
- Ensure high variety. DO NOT repeat the same food item across different meals.
- Pair foods logically! Keep food options together that traditionally complement each other in Indian cuisine (e.g., Roti + Dal + Green Salad). DO NOT create random, weird, or unnecessary food combinations.
- For Lunch and Dinner, you MUST explicitly include at least one type of bread (roti, parantha, poori, naan) OR rice, AND a savory salad (like green salad or cucumber salad, NOT fruit salad), alongside the main curry or dal. Mix and match these logically to create a complete meal.
- MACRO TARGETING & PORTIONS: You MUST adjust the quantity of food items to get as close to the target {target} kcal and {protein_target} g as possible, BUT you must ONLY use realistic, human-readable portion sizes (e.g., "2 Rotis", "1 Bowl of Dal", "1 Cup of Curd", "1/2 Portion of Halwa", "2 Pieces of Burfi"). DO NOT use absurd mathematical decimals like "1.13 servings" or "5.11 servings". Stick to whole numbers or simple halves (0.5). It is okay if the final totals are slightly off in order to keep the portions realistic. Multiply the base nutrition by your chosen portion and output only the final numbers.
- Do not invent exact nutrition values when they are not available in the knowledge base.
"""

                recommendation = ask_ai(
                    query=query,
                    context_query=f"healthy Indian {food_preference} breakfast lunch dinner snacks roti parantha rice salad high protein",
                    top_k=40
                )

                if recommendation:

                    st.success(
                        "Your personalized recommendation "
                        "has been generated!"
                    )
                    
                    metric_col1, metric_col2 = st.columns(2)
                    
                    with metric_col1:
                        st.metric(
                            "Daily Calorie Target",
                            f"{target} kcal"
                        )
                        
                    with metric_col2:
                        st.metric(
                            "Daily Protein Target",
                            f"{protein_target} g"
                        )

                    st.divider()

                    st.subheader("Recommended Diet Plan")

                    st.markdown(recommendation)


# ==================================================
# PAGE 5 — ABOUT
# ==================================================

elif page == "About":

    st.header("About Indian Diet AI")

    st.write(
        "An AI-powered nutrition application combining a calorie engine, "
        "retrieval-augmented generation over an Indian food knowledge base, "
        "and a conversational assistant."
    )

    st.markdown(
        """
        <div class="chip-grid">
            <span class="chip">Streamlit — Frontend</span>
            <span class="chip">FastAPI — Backend API</span>
            <span class="chip">Gemini / Groq — LLM</span>
            <span class="chip">LangChain — Orchestration</span>
            <span class="chip">Qdrant — Vector database</span>
            <span class="chip">Sentence Transformers — Embeddings</span>
            <span class="chip">RAG — Nutrition retrieval</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("Architecture")

    st.markdown(
        """
        <div class="flow-card">Streamlit — collects your profile and questions</div>
        <div class="flow-arrow">↓</div>
        <div class="flow-card">FastAPI — routes requests to the right engine</div>
        <div class="flow-arrow">↓</div>
        <div class="flow-card">Calorie Engine — computes BMR, TDEE, BMI</div>
        <div class="flow-arrow">↓</div>
        <div class="flow-card">RAG + Qdrant — retrieves relevant Indian foods</div>
        <div class="flow-arrow">↓</div>
        <div class="flow-card">Gemini / Groq — generates the personalized response</div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.subheader("Disclaimer")

    st.info(
        "This application is intended for educational and informational "
        "purposes. Calorie estimates and diet recommendations should not "
        "be considered medical advice. Consult a qualified nutrition "
        "professional for individualized medical or dietary guidance."
    )