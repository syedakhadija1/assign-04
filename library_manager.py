import streamlit as st
import json
import os
import pandas as pd 


DB_FILE = "library.json"


st.set_page_config(page_title="Personal Library Manager", layout="wide")


st.markdown(
    """
    <style>
    /* Global Styles */
    :root {
        --primary-color: #1E88E5;
        --secondary-color: #43A047;
        --accent-color: #FFC107;
        --text-color: #333333;
        --light-bg: #FFFFFF;
        --dark-bg: #121212;
        --dark-text: #E0E0E0;
        --border-radius: 10px;
        --card-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }

    body {
        font-family: 'Roboto', sans-serif;
        transition: background-color 0.3s ease;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif;
    }

    /* Light Mode */
    .light-mode {
        background-color: var(--light-bg);
        color: var(--text-color);
    }

    /* Dark Mode */
    .dark-mode {
        background-color: var(--dark-bg);
        color: var(--dark-text);
    }

    /* Card Styling */
    .book-card {
        border-radius: var(--border-radius);
        box-shadow: var(--card-shadow);
        padding: 20px;
        margin: 10px 0;
        transition: transform 0.2s;
    }

    .book-card:hover {
        transform: translateY(-5px);
    }

    /* Button Styling */
    .primary-button button {
        background-color: var(--primary-color) !important;
        color: white !important;
    }

    .secondary-button button {
        background-color: var(--secondary-color) !important;
        color: white !important;
    }

    .accent-button button {
        background-color: var(--accent-color) !important;
        color: var(--text-color) !important;
    }

    /* Status Colors */
    .status-read {
        color: var(--secondary-color);
    }

    .status-reading {
        color: var(--primary-color);
    }

    .status-to-read {
        color: var(--accent-color);
    }

    /* Sidebar button styles */
    [data-testid="stSidebar"] .stButton > button {
        background-color: #4361EE !important;
        color: white !important;
        width: 100%;
        margin: 4px 0;
    }

    /* Button styles */
    .stButton > button {
        background: #3949AB !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 500 !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 5px rgba(57, 73, 171, 0.2) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }

    /* Metric styles */
    [data-testid="stMetricValue"] {
        color: #4361EE !important;
    }

    /* Main heading style with animated icon */
    h1:first-of-type {
        position: relative !important;
        color: #2C3E50 !important;
        font-family: 'Poppins', sans-serif !important;
        font-size: 2.8rem !important;
        font-weight: 700 !important;
        text-align: center !important;
        margin-top: 3rem !important;
        margin-bottom: 2rem !important;
        padding: 1rem 0 !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        background: linear-gradient(120deg, #6A11CB, #2575FC) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        border-bottom: 3px solid #2575FC !important;
        text-shadow: 0 2px 4px rgba(106, 17, 203, 0.1) !important;
    }

    /* Add floating book icon before heading */
    h1:first-of-type::before {
        content: "\1F4DA" !important;
        position: absolute !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        top: -3rem !important;
        font-size: 3.5rem !important;
        background: none !important;
        -webkit-background-clip: initial !important;
        -webkit-text-fill-color: initial !important;
        animation: float 3s ease-in-out infinite !important;
        filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.1)) !important;
    }

    /* Add shine effect after heading */
    h1:first-of-type::after {
        content: "" !important;
        position: absolute !important;
        top: 0 !important;
        left: -100% !important;
        width: 100% !important;
        height: 100% !important;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(255, 255, 255, 0.2),
            transparent
        ) !important;
        animation: shine 3s infinite !important;
    }

    /* Float animation for icon */
    @keyframes float {
        0% {
            transform: translateX(-50%) translateY(0px);
        }
        50% {
            transform: translateX(-50%) translateY(-10px);
        }
        100% {
            transform: translateX(-50%) translateY(0px);
        }
    }

    /* Shine animation */
    @keyframes shine {
        0% {
            left: -100%;
        }
        50% {
            left: 100%;
        }
        100% {
            left: 100%;
        }
    }

    /* Other headings remain unchanged */
    h1:not(:first-of-type), h2, h3 {
        color: #1E1E1E !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* Container styles */
    [data-testid="stContainer"] {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }

    /* Header styles */
    .stButton > button:hover {
        background: #283593 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 10px rgba(57, 73, 171, 0.3) !important;
    }

    /* Hide default Streamlit navigation */
    [data-testid="stSidebarNav"],
    .stSidebarNav {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        width: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
    }

    /* Form Styling */
    .stTextInput > div > div > input {
        border-radius: var(--border-radius);
    }

    .stSelectbox > div > div > div {
        border-radius: var(--border-radius);
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #f5f5f5;
        border-right: 1px solid #e0e0e0;
    }

    .dark-mode section[data-testid="stSidebar"] {
        background-color: #1e1e1e;
        border-right: 1px solid #333;
    }

    /* Login/Register Form Styling */
    .auth-form {
        max-width: 500px;
        margin: 0 auto;
        padding: 20px;
        border-radius: var(--border-radius);
        box-shadow: var(--card-shadow);
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        .book-card {
            padding: 15px;
        }
    }

    /* Sidebar button styles */
    [data-testid="stSidebar"] .stButton > button {
        background: #303F9F !important;
        width: 100% !important;
        margin: 4px 0 !important;
        padding: 0.8rem !important;
        border-radius: 6px !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
    }

    /* Sidebar button hover */
    [data-testid="stSidebar"] .stButton > button:hover {
        background: #283593 !important;
        transform: translateY(-2px) !important;
    }

    /* Edit button style */
    button:has(span:contains("Edit")) {
        background: #1976D2 !important;
    }

    /* Edit button hover */
    button:has(span:contains("Edit")):hover {
        background: #1565C0 !important;
    }

    /* Delete button style */
    .stButton > button[kind="secondary"] {
        background: #E53935 !important;
    }

    /* Delete button hover */
    .stButton > button[kind="secondary"]:hover {
        background: #D32F2F !important;
    }

    /* Active/Click state for all buttons */
    .stButton > button:active {
        transform: translateY(1px) !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1) !important;
    }

    /* Metric styles */
    [data-testid="stMetricValue"] {
        color: #2980B9 !important;
        font-weight: 600 !important;
    }

    /* Container styles with subtle gradient border */
    [data-testid="stContainer"] {
        border: 2px solid #ECF0F1 !important;
        border-radius: 12px !important;
        padding: 1.2rem !important;
        margin: 0.7rem 0 !important;
        background: white !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
        transition: all 0.3s ease !important;
    }

    [data-testid="stContainer"]:hover {
        border-color: #BDC3C7 !important;
        box-shadow: 0 6px 20px rgba(41,128,185,0.1) !important;
    }

    /* Other headings */
    h1:not(:first-of-type), h2, h3 {
        color: #1E1E1E !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* Add smooth scrolling to whole page */
    * {
        scroll-behavior: smooth !important;
    }

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px !important;
    }

    ::-webkit-scrollbar-track {
        background: #ECF0F1 !important;
    }

    ::-webkit-scrollbar-thumb {
        background: #2980B9 !important;
        border-radius: 4px !important;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #2C3E50 !important;
    }

    /* Regular Button Styles */
    .stButton > button {
        background: linear-gradient(120deg, #6A11CB, #2575FC) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.7rem 1.5rem !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        font-size: 0.9rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(106, 17, 203, 0.2) !important;
    }

    /* Button hover effect */
    .stButton > button:hover {
        background: linear-gradient(120deg, #2575FC, #6A11CB) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(106, 17, 203, 0.3) !important;
    }

    /* Sidebar button styles */
    [data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(120deg, #6A11CB, #2575FC) !important;
        width: 100% !important;
        margin: 4px 0 !important;
        padding: 0.8rem !important;
    }

    /* Edit button style */
    button:has(span:contains("Edit")) {
        background: linear-gradient(120deg, #6A11CB, #2575FC) !important;
    }

    /* Delete button style */
    .stButton > button[kind="secondary"] {
        background: linear-gradient(120deg, #6A11CB, #2575FC) !important;
    }

    /* Button click effect */
    .stButton > button:active {
        transform: translateY(1px) !important;
        box-shadow: 0 2px 10px rgba(106, 17, 203, 0.2) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 📌 Function to Load Data from JSON
def load_data():
    try:
        if os.path.exists(DB_FILE):
            with open(DB_FILE, "r") as file:
                return json.load(file)
        else:
            return []
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return []

# 📌 Function to Save Data to JSON
def save_data(data):
    try:
        with open(DB_FILE, "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        st.error(f"Error saving data: {e}")

# 📌 Function to Add Book
def add_book(title, author, genre, year, status):
    books = load_data()
    new_id = str(len(books) + 1) if books else "1"
    new_book = {
        "id": new_id,
        "title": title,
        "author": author,
        "genre": genre,
        "year": year,
        "status": status,
    }
    books.append(new_book)
    save_data(books)


def delete_book(book_id):
    books = load_data()
    books = [book for book in books if book["id"] != book_id]
    save_data(books)


def update_book(book_id, title, author, genre, year, status):
    books = load_data()
    for book in books:
        if book["id"] == book_id:
            book.update({"title": title, "author": author, "genre": genre, "year": year, "status": status})
            save_data(books)
            return True
    return False


def search_book(query):
    books = load_data()
    return [book for book in books if query.lower() in book["title"].lower() or query.lower() in book["author"].lower()]

# Title
st.markdown('<p class="stTitle">📚 Personal Library Management System</p>', unsafe_allow_html=True)

# Sidebar Menu
menu = st.sidebar.selectbox("Menu", ["🏠 Home", "➕ Add Book", "🔍 Search Book", "✏️ Edit Book", "🗑️ Remove Book"])

if menu == "🏠 Home":
    st.markdown('<p class="stHeader">🏠 Home</p>', unsafe_allow_html=True)
    books = load_data()

    # Quick Overview Section
    st.markdown('<div class="quick-overview">', unsafe_allow_html=True)
    st.markdown("### Quick Overview")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Total Books:** {len(books)}")
        st.write(f"**Read:** {len([book for book in books if book['status'] == 'Read'])}")
        st.write(f"**Reading:** {len([book for book in books if book['status'] == 'Reading'])}")
        st.write(f"**To Read:** {len([book for book in books if book['status'] == 'To Read'])}")
        st.write(f"**Wishlist:** {len([book for book in books if book['status'] == 'Wishlist'])}")
    with col2:
        st.write("### Library Analytics")
        st.markdown(
            """
            <table class="analytics-table">
                <tr>
                    <th>Read</th>
                    <th>To Read</th>
                    <th>Reading</th>
                </tr>
                <tr>
                    <td>33.3%</td>
                    <td>33.3%</td>
                    <td>33.3%</td>
                </tr>
            </table>
            """,
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)

    # Top Genres Section
    st.markdown("### Top Genres")
    if books:
        genres = [book["genre"] for book in books]
        genre_counts = {genre: genres.count(genre) for genre in set(genres)}
        st.table(pd.DataFrame(list(genre_counts.items()), columns=["Genre", "Number of Books"]))
    else:
        st.warning("No genres found!")

elif menu == "➕ Add Book":
    st.markdown('<p class="stHeader">➕ Add a New Book</p>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        title = st.text_input("Book Title", max_chars=100)
        author = st.text_input("Author Name", max_chars=50)
    with col2:
        genre = st.text_input("Genre", max_chars=50)
        year = st.text_input("Year of Publication", max_chars=4)
    status = st.selectbox("Status", ["Read", "Reading", "To Read", "Wishlist"])
    if st.button("Add Book", key="add_book"):
        if title and author and genre and year:
            if year.isdigit() and len(year) == 4:
                add_book(title, author, genre, year, status)
                st.success("✅ Book added successfully!")
            else:
                st.error("❌ Please enter a valid year (e.g., 2023).")
        else:
            st.error("❌ Please fill in all fields.")

elif menu == "🔍 Search Book":
    st.markdown('<p class="stHeader">🔍 Search a Book</p>', unsafe_allow_html=True)
    query = st.text_input("Enter Book Title or Author Name")
    if st.button("Search", key="search_book"):
        if query:
            results = search_book(query)
            if results:
                st.table(pd.DataFrame(results))  # Use pandas DataFrame to display results
            else:
                st.warning("❌ No matching books found!")
        else:
            st.error("❌ Please enter a search query.")

elif menu == "✏️ Edit Book":
    st.markdown('<p class="stHeader">✏️ Edit Book</p>', unsafe_allow_html=True)
    book_id = st.text_input("Enter Book ID to Edit")
    if book_id:
        books = load_data()
        book_to_edit = next((book for book in books if book["id"] == book_id), None)
        if book_to_edit:
            col1, col2 = st.columns(2)
            with col1:
                title = st.text_input("Title", value=book_to_edit["title"], max_chars=100)
                author = st.text_input("Author", value=book_to_edit["author"], max_chars=50)
            with col2:
                genre = st.text_input("Genre", value=book_to_edit["genre"], max_chars=50)
                year = st.text_input("Year", value=book_to_edit["year"], max_chars=4)
            status = st.selectbox("Status", ["Read", "Reading", "To Read", "Wishlist"], index=["Read", "Reading", "To Read", "Wishlist"].index(book_to_edit["status"]))
            if st.button("Update Book", key="update_book"):
                if title and author and genre and year:
                    if year.isdigit() and len(year) == 4:
                        if update_book(book_id, title, author, genre, year, status):
                            st.success("✅ Book updated successfully!")
                        else:
                            st.error("❌ Failed to update book.")
                    else:
                        st.error("❌ Please enter a valid year (e.g., 2023).")
                else:
                    st.error("❌ Please fill in all fields.")
        else:
            st.error("❌ Book ID not found!")

elif menu == "🗑️ Remove Book":
    st.markdown('<p class="stHeader">🗑️ Remove Book</p>', unsafe_allow_html=True)
    book_id = st.text_input("Enter Book ID to Remove")
    if st.button("Remove Book", key="remove_book"):
        if book_id:
            delete_book(book_id)
            st.success("✅ Book removed successfully!")
        else:
            st.error("❌ Please enter a Book ID.")