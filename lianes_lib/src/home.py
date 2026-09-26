import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from read_books import load_books
from insert_books import insert_book
from insert_copies import insert_copy
from delete_copies import delete_copy
from update_copies import update_copy, get_copy_details
from read_friends import load_friends
from insert_friends import insert_friend
from update_friends import update_friend, get_friend_details
from delete_friends import delete_friend
from read_loans import load_loans
from insert_loans import insert_loan
from update_loans import update_loan
from dashboard_stats import get_book_statistics, get_loans_per_month, get_spending_per_month,get_overdue_loans, get_top_books, get_top_friends, get_top_authors

st.set_page_config(
    page_title="Lianes Library",
    layout="wide"
)


# ─────────────────────────────────────
# CSS
# ─────────────────────────────────────

st.markdown("""
<style>

    /* ============================= */
    /* Sidebar                       */
    /* ============================= */

    /* Library title */
    [data-testid="stSidebar"] h1 {
        font-size: 35px !important;
        color: #222222 !important;
        font-weight: 700 !important;
        margin-bottom: 40px !important;
    }

    /* Navigation title */
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        font-size: 23px !important;
        color: #555555 !important;
        font-weight: 600 !important;
        margin-bottom: 25px !important;
    }

    /* Navigation items */
    [data-testid="stSidebar"] div[role="radiogroup"] label {
        font-size: 21px !important;
        margin-bottom: 18px !important;
        padding: 12px 8px !important;
    }

    /* Navigation text */
    [data-testid="stSidebar"] div[role="radiogroup"] label p {
        font-size: 21px !important;
        color: #333333 !important;
        font-weight: 500 !important;
    }

    /* Space between navigation items */
    [data-testid="stSidebar"] div[role="radiogroup"] label + label {
        margin-top: 12px !important;
    }

    /* Sidebar width */
    [data-testid="stSidebar"] {
        min-width: 340px;
        max-width: 340px;
    }

    /* Library title */
    [data-testid="stSidebar"] h1 {
        font-size: 20px;
        margin-bottom: 35px;
    }

    /* Navigation title */
    [data-testid="stSidebar"] p {
        font-size: 18px;
    }

    /* Navigation items */
    [data-testid="stSidebar"] div[role="radiogroup"] label {
        padding: 12px 8px;
        margin-bottom: 8px;
        font-size: 19px;
    }

    /* Text inside navigation items */
    [data-testid="stSidebar"] div[role="radiogroup"] label p {
        font-size: 19px;
    }

    /* Book columns */
    [data-testid="column"] {
        padding: 0 12px;
    }

    [data-testid="column"] p {
        margin-bottom: 18px;
        line-height: 1.5;
    }

    [data-testid="column"] h3 {
        margin-bottom: 20px;
    }

    /* Add new Book button */
    div.stButton > button {
        background-color: #28a745;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 22px;
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 50px;
    }

    div.stButton > button:hover {
        background-color: #218838;
        color: white;
    }


    /* Edit buttons */
    [class*="st-key-edit_button_"] button {
        background-color: #ffc107 !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }

    [class*="st-key-edit_button_"] button:hover {
        background-color: #e0a800 !important;
        color: #000000 !important;
    }


    /* Delete buttons */
    [class*="st-key-delete_button_"] button {
        background-color: #dc3545 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }

    [class*="st-key-delete_button_"] button:hover {
        background-color: #bb2d3b !important;
        color: white !important;
    }
    [class*="st-key-edit_friend_button_"] button {
    background-color: #ffc107 !important;
    color: #000000 !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}

[class*="st-key-edit_friend_button_"] button:hover {
    background-color: #e0a800 !important;
    color: #000000 !important;
}

[class*="st-key-delete_friend_button_"] button {
    background-color: #dc3545 !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}

[class*="st-key-delete_friend_button_"] button:hover {
    background-color: #bb2d3b !important;
    color: white !important;
}
[class*="st-key-edit_loan_button_"] button {
    background-color: #ffc107 !important;
    color: #000000 !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}

[class*="st-key-edit_loan_button_"] button:hover {
    background-color: #e0a800 !important;
    color: #000000 !important;
}
/* Dashboard cards */
.dashboard-card {
    background: white;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
    border: 1px solid #eeeeee;
    min-height: 150px;
    margin-bottom: 25px;
}

.dashboard-card .card-icon {
    font-size: 32px;
    margin-bottom: 12px;
}

.dashboard-card .card-title {
    font-size: 20px;
    font-weight: 600;
    color: #666666;
    margin-bottom: 8px;
}

.dashboard-card .card-value {
    font-size: 36px;
    font-weight: 700;
    color: #222222;
}
/* Dashboard date filter */
[class*="st-key-dashboard_date_filter"] {
    margin-top: 45px;
    padding: 22px 24px;
    background-color: #f8f9fa;
    border: 1px solid #e9ecef;
    border-radius: 14px;
}

/* Date filter title */
[class*="st-key-dashboard_date_filter"] h2,
[class*="st-key-dashboard_date_filter"] h3 {
    margin-bottom: 18px;
}

/* Date input fields */
[class*="st-key-dashboard_date_filter"] [data-testid="stDateInput"] {
    margin-bottom: 5px;
}

/* Date input label */
[class*="st-key-dashboard_date_filter"] [data-testid="stDateInput"] label {
    font-weight: 600;
    font-size: 15px;
}
/* Dashboard table */
.dashboard-table {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #e5e7eb;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.06);
}

.dashboard-table th {
    background-color: #f3f4f6;
    color: #222222;
    font-weight: 700;
    padding: 12px;
}

.dashboard-table td {
    padding: 10px 12px;
}

.dashboard-table tr:hover {
    background-color: #f8f9fa;
}
/* Dashboard table */
.dashboard-table {
    width: 100%;
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #e5e7eb;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.06);
    margin-top: 10px;
}

.dashboard-table table {
    width: 100%;
    border-collapse: collapse;
    background: white;
}

.dashboard-table th {
    background-color: #f3f4f6;
    color: #222222;
    font-weight: 700;
    padding: 14px 12px;
    text-align: left;
    border-bottom: 2px solid #e5e7eb;
}

.dashboard-table td {
    padding: 12px;
    color: #333333;
    border-bottom: 1px solid #eeeeee;
}

.dashboard-table tbody tr:hover {
    background-color: #f8f9fa;
}

.dashboard-table tbody tr:last-child td {
    border-bottom: none;
}

.days-positive {
    color: #198754;
    font-weight: 700;
    text-align: center;
}

.days-negative {
    color: #dc3545;
    font-weight: 700;
    text-align: center;
}

.days-today {
    color: #fd7e14;
    font-weight: 700;
    text-align: center;
}
.dashboard-table td.days-positive {
    color: #198754;
    font-weight: 700;
    text-align: center;
}

.dashboard-table td.days-negative {
    color: #dc3545;
    font-weight: 700;
    text-align: center;
}

.dashboard-table td.days-today {
    color: #fd7e14;
    font-weight: 700;
    text-align: center;
}
/* Top 5 Cards */

.top-card {
    background: white;
    border-radius: 16px;
    padding: 20px;
    border: 1px solid #eeeeee;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
    min-height: 280px;
}

.top-card-title {
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 18px;
    color: #222222;
}

.top-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 11px 0;
    border-bottom: 1px solid #eeeeee;
}

.top-row:last-child {
    border-bottom: none;
}

.top-name {
    font-size: 16px;
    color: #333333;
}

.top-count {
    font-size: 16px;
    font-weight: 700;
    color: #555555;
    margin-left: 10px;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────
# Sidebar
# ─────────────────────────────────────

st.sidebar.title("📚 Lianes Library")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "📚 Books",
        "👥 Friends",
        "🔄 Borrowing",
    ]
)


# ─────────────────────────────────────
# Books
# ─────────────────────────────────────

if page == "📚 Books":

    # ─────────────────────────────────
    # Add new Book button
    # ─────────────────────────────────

    if st.button(
        "Add new Book",
        key="add_book"
    ):
        st.session_state["show_add_book"] = True


    # ─────────────────────────────────
    # Add Book Form
    # ─────────────────────────────────

    if st.session_state.get("show_add_book", False):

        with st.form(
            "add_book_form",
            clear_on_submit=True
        ):

            st.subheader("📚 Add New Book")

            title = st.text_input(
                "📚 Titel"
            )

            author = st.text_input(
                "👤 Autor"
            )

            genre = st.text_input(
                "🏷️ Genre"
            )

            isbn = st.text_input(
                "🔢 ISBN"
            )
            copy_status = st.selectbox(
                "🔄 Copy Status",
                [
                    "Available",
                    "Borrowed",
                    "Lost",
                    "Not available for borrowing",
                    "Worn out"
                ]
            )
            pub_year = st.number_input(
                "📅 Publication Year",
                min_value=0,
                step=1
            )

            book_price = st.number_input(
                "💰 Book Price",
                min_value=0.0,
                step=0.1
            )

            copies_num = st.slider(
                "📦 Number Of Copies",
                min_value=1,
                max_value=10,
                step=1
            )

            submitted = st.form_submit_button(
                "➕ Add Book"
            )


            # ─────────────────────────
            # Insert Book
            # ─────────────────────────

            if submitted:

                if title and author and copies_num > 0:

                    insert_book(
                        title,
                        author,
                        genre,
                        isbn,
                        pub_year
                    )

                    copy = 0

                    while copy < copies_num:

                        insert_copy(
                            book_price,
                            copy_status
                        )

                        copy += 1

                    st.success(
                        "✅ Buch wurde erfolgreich hinzugefügt!"
                    )

                    st.session_state["show_add_book"] = False

                    st.rerun()

                else:

                    st.warning(
                        "⚠️ Bitte alle Felder ausfüllen."
                    )
    # ─────────────────────────────────
    # Load Books
    # ─────────────────────────────────

    books_df = load_books()

    # ─────────────────────────────────
    # Newest Books First
    # ─────────────────────────────────

    books_df = books_df.sort_values(
        by="copy_id",
        ascending=False
    )

    # ─────────────────────────────────
    # Filters
    # ─────────────────────────────────

    st.subheader("🔎 Filter")

    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)


    with filter_col1:

        author_filter = st.selectbox(
            "👤 Autor",
            ["All"] + sorted(
                books_df["author"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )
        )
    st.markdown(
        """
        <div style="margin-bottom: 70px;"></div>
        """,
        unsafe_allow_html=True
    )

    with filter_col2:

        title_filter = st.text_input(
            "📚 Titel",
            placeholder="Buchtitel suchen..."
        )


    with filter_col3:

        genre_filter = st.selectbox(
            "🏷️ Genre",
            ["All"] + sorted(
                books_df["genre"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )
        )


    with filter_col4:

        status_filter = st.selectbox(
            "🔄 Status",
            [
                "All",
                "Available",
                "Borrowed",
                "Lost",
                "Not available for borrowing",
                "Worn out"
            ]
        )


    # ─────────────────────────────────
    # Apply Filters
    # ─────────────────────────────────

    filtered_books = books_df.copy()


    if author_filter != "All":

        filtered_books = filtered_books[
            filtered_books["author"].astype(str) == author_filter
        ]


    if title_filter.strip():

        filtered_books = filtered_books[
            filtered_books["title"]
            .astype(str)
            .str.contains(
                title_filter.strip(),
                case=False,
                na=False
            )
        ]


    if genre_filter != "All":

        filtered_books = filtered_books[
            filtered_books["genre"].astype(str) == genre_filter
        ]


    if status_filter != "All":

        filtered_books = filtered_books[
            filtered_books["copy_status"].astype(str) == status_filter
        ]
    # ─────────────────────────────────
    # Pagination
    # ─────────────────────────────────

    books_per_page = 100

    total_books = len(filtered_books)

    total_pages = max(
        1,
        (total_books + books_per_page - 1) // books_per_page
    )

    if "books_page" not in st.session_state:

        st.session_state["books_page"] = 1


    current_page = st.session_state["books_page"]


    # Safety check
    if current_page > total_pages and total_pages > 0:

        current_page = total_pages

        st.session_state["books_page"] = total_pages


    start_index = (
        current_page - 1
    ) * books_per_page

    end_index = (
        start_index + books_per_page
    )


    page_books = filtered_books.iloc[
        start_index:end_index
    ]


    # ─────────────────────────────────
    # Display Books
    # ─────────────────────────────────

    for start in range(
        0,
        len(page_books),
        4
    ):

        row_books = page_books.iloc[
            start:start + 4
        ]


        cols = st.columns(
            4,
            gap="large"
        )


        for col, (_, book) in zip(
            cols,
            row_books.iterrows()
        ):

            with col:

                # st.write(
                #     f"📦 Copy ID: {book['copy_id']}"
                # )

                st.subheader(
                    f"📚 {book['title']}"
                )

                st.image(
                    "../images/cover.jpeg"
                )

                st.write(
                    f"👤 Autor: {book['author']}"
                )

                st.write(
                    f"🏷️ Genre: {book['genre']}"
                )

                st.write(
                    f"🔄 Status: {book['copy_status']}"
                )

                st.write(
                    f"💰 Preis: {book['purchase_price']} €"
                )


                # ─────────────────
                # Edit / Delete
                # ─────────────────

                edit_col, delete_col = st.columns(2)


                # ─────────────────
                # Edit Button
                # ─────────────────

                with edit_col:

                    with st.container(
                        key=f"edit_button_{book['copy_id']}"
                    ):

                        if st.button(
                            "✏️ Update",
                            key=f"edit_{book['copy_id']}"
                        ):

                            st.session_state[
                                "edit_copy_id"
                            ] = book["copy_id"]


                    # ─────────────────
                    # Edit Form
                    # ─────────────────

                    if st.session_state.get(
                        "edit_copy_id"
                    ) == book["copy_id"]:

                        copy_id = book["copy_id"]

                        copy_data = get_copy_details(
                            copy_id
                        )


                        if copy_data:

                            st.subheader(
                                f"✏️ Buch Update – Copy ID {copy_id}"
                            )


                            with st.form(
                                f"edit_form_{copy_id}"
                            ):

                                title = st.text_input(
                                    "📚 Titel",
                                    value=copy_data["title"]
                                )


                                author = st.text_input(
                                    "👤 Autor",
                                    value=copy_data["author"] or ""
                                )


                                genre = st.text_input(
                                    "🏷️ Genre",
                                    value=copy_data["genre"] or ""
                                )


                                isbn = st.text_input(
                                    "🔢 ISBN",
                                    value=copy_data["isbn"] or ""
                                )


                                publicationyear = st.number_input(
                                    "📅 Publication Year",
                                    min_value=0,
                                    value=int(
                                        copy_data["publicationyear"] or 0
                                    ),
                                    step=1
                                )


                                st.write(
                                    f"🔄 Status: {copy_data['copy_status']}"
                                )

                                copy_status = copy_data["copy_status"]


                                purchase_price = st.number_input(
                                    "💰 Preis",
                                    min_value=0.0,
                                    value=float(
                                        copy_data["purchase_price"] or 0
                                    ),
                                    step=0.1
                                )


                                purchase_date = st.date_input(
                                    "📅 Kaufdatum",
                                    value=copy_data["purchase_date"]
                                )


                                submitted = st.form_submit_button(
                                    "💾 Änderungen speichern"
                                )


                                if submitted:

                                    result = update_copy(
                                        copy_id,
                                        title,
                                        author,
                                        genre,
                                        isbn,
                                        publicationyear,
                                        copy_status,
                                        purchase_price,
                                        purchase_date
                                    )


                                    if result == "updated":

                                        st.success(
                                            "✅ Änderungen wurden gespeichert."
                                        )

                                        del st.session_state[
                                            "edit_copy_id"
                                        ]

                                        st.rerun()


                # ─────────────────
                # Delete Button
                # ─────────────────

                with delete_col:

                    with st.container(
                        key=f"delete_button_{book['copy_id']}"
                    ):

                        if st.button(
                            "🗑️ Delete",
                            key=f"delete_{book['copy_id']}"
                        ):

                            result = delete_copy(
                                book["copy_id"]
                            )

                            if result == "not_found":

                                st.error(
                                    "❌ Die Kopie wurde nicht gefunden."
                                )


                            elif result == "has_loans":

                                st.warning(
                                    "⚠️ Diese Kopie kann nicht gelöscht werden, "
                                    "weil sie aktuell bereits ausgeliehen wurde."
                                )


                            elif result == "copy_deleted":

                                st.success(
                                    "✅ Die Kopie wurde erfolgreich gelöscht."
                                )

                                st.rerun()


                            elif result == "copy_and_book_deleted":

                                st.success(
                                    "✅ Die letzte Kopie und das Buch wurden gelöscht."
                                )

                                st.rerun()


                            st.session_state[
                                "delete_copy_id"
                            ] = book["copy_id"]


    # ─────────────────────────────────
    # Pagination Buttons
    # ─────────────────────────────────

    col1, col2, col3 = st.columns(
        [1, 2, 1]
    )


    with col1:

        if st.button(
            "⬅️ Previous",
            disabled=current_page == 1
        ):

            st.session_state[
                "books_page"
            ] -= 1

            st.rerun()


    with col2:

        st.write(
            f"Page {current_page} of {total_pages}"
        )


    with col3:

        if st.button(
            "Next ➡️",
            disabled=current_page == total_pages
        ):

            st.session_state[
                "books_page"
            ] += 1

            st.rerun()
elif page == "👥 Friends":

    if st.button("➕ Add Friend", key="add_friend"):
        st.session_state["show_add_friend"] = True


    if st.session_state.get("show_add_friend", False):

        with st.form("add_friend_form", clear_on_submit=True):

            st.subheader("👤 Add New Friend")

            f_name = st.text_input("👤 First Name")
            l_name = st.text_input("👤 Last Name")
            email = st.text_input("📧 Email")
            phone = st.text_input("📞 Phone")
            adress = st.text_input("🏠 Address")

            max_loans = st.number_input(
                "📚 Maximum Loans",
                min_value=1,
                value=3,
                step=1
            )

            is_trusted = st.checkbox(
                "⭐ Trusted Friend",
                value=True
            )

            friend_notes = st.text_area(
                "📝 Notes"
            )

            submitted = st.form_submit_button(
                "➕ Add Friend"
            )

            if submitted:

                if f_name and l_name:

                    insert_friend(
                        f_name,
                        l_name,
                        email,
                        phone,
                        adress,
                        max_loans,
                        is_trusted,
                        friend_notes
                    )

                    st.success(
                        "✅ Friend wurde erfolgreich hinzugefügt!"
                    )

                    st.session_state["show_add_friend"] = False
                    st.rerun()

                else:

                    st.warning(
                        "⚠️ First Name und Last Name sind erforderlich."
                    )


    friends_df = load_friends()

    # ─────────────────────────────────
    # Search Friends
    # ─────────────────────────────────

    st.subheader("🔎 Search Friends")

    search_col1, search_col2, search_col3 = st.columns(3)


    with search_col1:

        first_name_filter = st.text_input(
            "👤 First Name",
            placeholder="Search first name..."
        )


    with search_col2:

        last_name_filter = st.text_input(
            "👥 Last Name",
            placeholder="Search last name..."
        )


    with search_col3:

        trust_filter = st.selectbox(
            "⭐ Trust",
            [
                "All",
                "Trusted",
                "Not Trusted"
            ]
        )


    filtered_friends = friends_df.copy()


    # ─────────────────────────────────
    # First Name Filter
    # ─────────────────────────────────

    if first_name_filter.strip():

        filtered_friends = filtered_friends[
            filtered_friends["f_name"]
            .astype(str)
            .str.contains(
                first_name_filter.strip(),
                case=False,
                na=False
            )
        ]


    # ─────────────────────────────────
    # Last Name Filter
    # ─────────────────────────────────

    if last_name_filter.strip():

        filtered_friends = filtered_friends[
            filtered_friends["l_name"]
            .astype(str)
            .str.contains(
                last_name_filter.strip(),
                case=False,
                na=False
            )
        ]


    # ─────────────────────────────────
    # Trust Filter
    # ─────────────────────────────────

    if trust_filter == "Trusted":

        filtered_friends = filtered_friends[
            filtered_friends["is_trusted"] == 1
        ]

    elif trust_filter == "Not Trusted":

        filtered_friends = filtered_friends[
            filtered_friends["is_trusted"] == 0
        ]
    # ─────────────────────────────────
    # Friends Cards
    # ─────────────────────────────────

    for start in range(0, len(filtered_friends), 4):

        row_friends = filtered_friends.iloc[start:start + 4]

        cols = st.columns(4, gap="large")

        for col, (_, friend) in zip(
            cols,
            row_friends.iterrows()
        ):

            with col:

                st.container(border=True)

                st.write(
                    f"🪪 Friend ID: {friend['friend_id']}"
                )

                st.subheader(
                    f"👤 {friend['f_name']} {friend['l_name']}"
                )

                st.write(
                    f"📧 Email: {friend['email']}"
                )

                st.write(
                    f"📞 Phone: {friend['phone']}"
                )

                st.write(
                    f"🏠 Address: {friend['adress']}"
                )

                st.write(
                    f"📚 Max Loans: {friend['max_loans']}"
                )

                if friend["is_trusted"]:

                    st.write("⭐ Trusted: Yes")

                else:

                    st.write("⭐ Trusted: No")


                # ─────────────────────────
                # Edit / Delete Buttons
                # ─────────────────────────

                edit_col, delete_col = st.columns(2)


                with edit_col:

                    with st.container(
                        key=f"edit_friend_button_{friend['friend_id']}"
                    ):

                        if st.button(
                            "✏️ Update",
                            key=f"edit_friend_{friend['friend_id']}"
                        ):

                            st.session_state["edit_friend_id"] = (
                                friend["friend_id"]
                            )
                            st.rerun()


                with delete_col:

                    with st.container(
                        key=f"delete_friend_button_{friend['friend_id']}"
                    ):

                        if st.button(
                            "🗑️ Delete",
                            key=f"delete_friend_{friend['friend_id']}"
                        ):

                            result = delete_friend(
                                friend["friend_id"]
                            )

                            if result == "not_found":

                                st.error(
                                    "❌ Der Freund wurde nicht gefunden."
                                )

                            elif result == "has_loans":

                                st.warning(
                                    "⚠️ Dieser Freund kann nicht gelöscht "
                                    "werden, weil er bereits Bücher "
                                    "ausgeliehen hat."
                                )

                            elif result == "deleted":

                                st.success(
                                    "✅ Der Freund wurde erfolgreich gelöscht."
                                )

                                st.rerun()


                # ─────────────────────────
                # Edit Friend
                # ─────────────────────────

                if st.session_state.get(
                    "edit_friend_id"
                ) == friend["friend_id"]:


                    friend_details = get_friend_details(
                        friend["friend_id"]
                    )

                    if friend_details:

                        st.write("### ✏️ Update")

                        with st.form(
                            f"edit_friend_form_{friend['friend_id']}"
                        ):

                            f_name = st.text_input(
                                "👤 First Name",
                                value=friend_details["f_name"]
                            )

                            l_name = st.text_input(
                                "👤 Last Name",
                                value=friend_details["l_name"]
                            )

                            email = st.text_input(
                                "📧 Email",
                                value=friend_details["email"] or ""
                            )

                            phone = st.text_input(
                                "📞 Phone",
                                value=friend_details["phone"] or ""
                            )

                            adress = st.text_input(
                                "🏠 Address",
                                value=friend_details["adress"] or ""
                            )

                            max_loans = st.number_input(
                                "📚 Maximum Loans",
                                min_value=1,
                                value=int(friend_details["max_loans"]),
                                step=1
                            )

                            is_trusted = st.checkbox(
                                "⭐ Trusted Friend",
                                value=bool(friend_details["is_trusted"])
                            )

                            friend_notes = st.text_area(
                                "📝 Notes",
                                value=friend_details["friend_notes"] or ""
                            )

                            submitted = st.form_submit_button(
                                "💾 Save Changes"
                            )

                            if submitted:

                                if f_name and l_name:

                                    result = update_friend(
                                        friend["friend_id"],
                                        f_name,
                                        l_name,
                                        email,
                                        phone,
                                        adress,
                                        max_loans,
                                        is_trusted,
                                        friend_notes
                                    )

                                    if result == "updated":

                                        st.success(
                                            "✅ Friend wurde erfolgreich aktualisiert."
                                        )

                                        st.session_state.pop(
                                            "edit_friend_id",
                                            None
                                        )

                                        st.rerun()

                                    elif result == "not_found":

                                        st.error(
                                            "❌ Der Freund wurde nicht gefunden."
                                        )

                                else:

                                    st.warning(
                                        "⚠️ First Name und Last Name sind erforderlich."
                                    )
elif page == "🔄 Borrowing" :
    loans_df = load_loans()

     # ─────────────────────────────────
    # Add New Loan
    # ─────────────────────────────────

    if st.button(
        "➕ Add New Borrowing",
        key="add_loan"
    ):
        st.session_state["show_add_loan"] = True


    if st.session_state.get(
        "show_add_loan",
        False
    ):

        available_copies = load_books()

        available_copies = available_copies[
            available_copies["copy_status"] == "Available"
        ]

        friends_df = load_friends()

        with st.form(
            "add_loan_form"
        ):

            st.subheader(
                "➕ New Borrowing"
            )

            # Friend selection

            friend_options = friends_df.apply(
                lambda row:
                f"{row['friend_id']} - "
                f"{row['f_name']} {row['l_name']}",
                axis=1
            ).tolist()

            selected_friend = st.selectbox(
                "👤 Friend",
                friend_options
            )


            # Copy selection

            copy_options = available_copies.apply(
                lambda row:
                f"Copy {row['copy_id']} - "
                f"{row['title']}",
                axis=1
            ).tolist()

            selected_copy = st.selectbox(
                "📚 Available Copy",
                copy_options
            )


            submitted = st.form_submit_button(
                "💾 Ausleihen"
            )


            if submitted:

                selected_friend_id = friends_df.loc[
                    friends_df.apply(
                        lambda row:
                        f"{row['friend_id']} - "
                        f"{row['f_name']} {row['l_name']}",
                        axis=1
                    ) == selected_friend,
                    "friend_id"
                ].iloc[0]

                selected_copy_id = available_copies.loc[
                    available_copies.apply(
                        lambda row:
                        f"Copy {row['copy_id']} - "
                        f"{row['title']}",
                        axis=1
                    ) == selected_copy,
                    "copy_id"
                ].iloc[0]


                result = insert_loan(
                    int(selected_copy_id),
                    int(selected_friend_id)
                )


                if result == "friend_not_trusted":

                    # st.warning(
                    #     "⚠️ Dieser Freund ist nicht vertrauenswürdig."
                    # )

                    st.session_state["pending_loan"] = {
                        "copy_id": int(selected_copy_id),
                        "friend_id": int(selected_friend_id)
                    }


                elif result == "copy_not_found":

                    st.error(
                        "❌ Die Kopie wurde nicht gefunden."
                    )


                elif result == "copy_not_available":

                    st.warning(
                        "⚠️ Diese Kopie ist nicht verfügbar."
                    )


                elif result == "friend_not_found":

                    st.error(
                        "❌ Der Freund wurde nicht gefunden."
                    )


                elif result == "max_loans_reached":

                    st.session_state["pending_loan"] = {
                        "copy_id": int(selected_copy_id),
                        "friend_id": int(selected_friend_id),
                        "reason": "max_loans"
                    }

                    st.rerun()


                elif result == "created":

                    st.success(
                        "✅ Die Ausleihe wurde erfolgreich erstellt."
                    )

                    st.session_state["show_add_loan"] = False

                    st.rerun()

            # ─────────────────────────────────
            # Confirm Loan for Untrusted Friend
            # ─────────────────────────────────

            if "pending_loan" in st.session_state:

                pending_loan = st.session_state["pending_loan"]

                if pending_loan.get("reason") == "max_loans":

                    st.warning(
                        "⚠️ Der Freund hat bereits die maximale Anzahl "
                        "an Ausleihen erreicht. "
                        "Möchten Sie die Ausleihe trotzdem durchführen?"
                    )

                else:

                    st.warning(
                        "⚠️ Der Freund ist nicht vertrauenswürdig. "
                        "Möchten Sie die Ausleihe trotzdem durchführen?"
                    )

                if st.form_submit_button(
                    "⚠️ Trotzdem ausleihen",
                    key="confirm_pending_loan"
                ):

                    pending_loan = st.session_state["pending_loan"]

                    result = insert_loan(
                        pending_loan["copy_id"],
                        pending_loan["friend_id"],
                        confirmed=True
                    )

                    if result == "created":

                        st.success(
                            "✅ Die Ausleihe wurde erfolgreich erstellt."
                        )

                        st.session_state.pop(
                            "pending_loan",
                            None
                        )

                        st.session_state["show_add_loan"] = False

                        st.rerun()

                    elif result == "copy_not_available":

                        st.warning(
                            "⚠️ Diese Kopie ist nicht mehr verfügbar."
                        )

                        st.session_state.pop(
                            "pending_loan",
                            None
                        )

                    # elif result == "max_loans_reached":

                    #     st.session_state["pending_loan"] = {
                    #         "copy_id": int(selected_copy_id),
                    #         "friend_id": int(selected_friend_id)
                    #     }

                    #     st.session_state["max_loans_warning"] = True

    # ─────────────────────────────────
    # Loan Filters
    # ─────────────────────────────────

    st.subheader("🔎 Filter")

    filter_col1, filter_col2, filter_col3 = st.columns(3)


    # ─────────────────────────────────
    # Friend Filter
    # ─────────────────────────────────

    with filter_col1:

        friend_options = ["All"] + sorted(
            loans_df.apply(
                lambda row:
                f"{row['friend_id']} - "
                f"{row['f_name']} {row['l_name']}",
                axis=1
            ).unique().tolist()
        )

        friend_filter = st.selectbox(
            "👤 Friend",
            friend_options
        )


    # ─────────────────────────────────
    # Loan Type Filter
    # ─────────────────────────────────

    with filter_col2:

        loan_type_filter = st.selectbox(
            "🔄 Loan Type",
            [
                "All",
                "Open",
                "Closed"
            ]
        )


    # ─────────────────────────────────
    # Book Filter
    # ─────────────────────────────────

    with filter_col3:

        book_filter = st.selectbox(
            "📚 Book",
            ["All"] + sorted(
                loans_df["title"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )
        )


    # ─────────────────────────────────
    # Apply Filters
    # ─────────────────────────────────

    filtered_loans = loans_df.copy()


    # Friend

    if friend_filter != "All":

        filtered_loans = filtered_loans[
            filtered_loans.apply(
                lambda row:
                f"{row['friend_id']} - "
                f"{row['f_name']} {row['l_name']}"
                == friend_filter,
                axis=1
            )
        ]


    # Loan Type

    if loan_type_filter == "Open":

        filtered_loans = filtered_loans[
            filtered_loans["return_date"].isna()
        ]

    elif loan_type_filter == "Closed":

        filtered_loans = filtered_loans[
            filtered_loans["return_date"].notna()
        ]


    # Book

    if book_filter != "All":

        filtered_loans = filtered_loans[
            filtered_loans["title"] == book_filter
        ]

    # ─────────────────────────────────
    # Loan Cards
    # ─────────────────────────────────

    for start in range(0, len(loans_df), 4):

        row_loans = filtered_loans.iloc[start:start + 4]

        cols = st.columns(4, gap="large")

        for col, (_, loan) in zip(
            cols,
            row_loans.iterrows()
        ):

            with col:

                st.container(border=True)

                st.write(
                    f"🪪 Loan ID: {loan['loan_id']}"
                )

                st.subheader(
                    f"📚 {loan['title']}"
                )

                st.write(
                    f"📦 Copy ID: {loan['copy_id']}"
                )

                st.write(
                    f"👤 Friend: {loan['f_name']} {loan['l_name']}"
                )

                st.write(
                    f"📅 Loan Date: {loan['loan_date']}"
                )

                st.write(
                    f"📅 Due Date: {loan['due_date']}"
                )

                if pd.isna(loan["return_date"]):

                    st.write(
                        "🔄 Status: Open"
                    )

                else:

                    st.write(
                        f"🔄 Status: Closed"
                    )

                    st.write(
                        f"📅 Return Date: {loan['return_date']}"
                    )

                st.write(
                    f"📦 Copy Status: {loan['copy_status']}"
                )

                if pd.isna(loan["return_date"]):

                    with st.container(
                        key=f"edit_loan_button_{loan['loan_id']}"
                    ):

                        if st.button(
                            "✏️ Update",
                            key=f"edit_loan_{loan['loan_id']}"
                        ):

                            st.session_state["edit_loan_id"] = loan["loan_id"]

                            st.rerun()
                        # ─────────────────────────────────
                        # Edit Loan
                        # ─────────────────────────────────

                        if st.session_state.get(
                            "edit_loan_id"
                        ) == loan["loan_id"]:

                            st.write("### ✏️ Update")

                            with st.form(
                                f"edit_loan_form_{loan['loan_id']}"
                            ):

                                st.write(
                                    f"🪪 Loan ID: {loan['loan_id']}"
                                )

                                st.write(
                                    f"📚 Book: {loan['title']}"
                                )

                                st.write(
                                    f"📦 Copy ID: {loan['copy_id']}"
                                )

                                st.write(
                                    f"👤 Friend: {loan['f_name']} {loan['l_name']}"
                                )

                                copy_status = st.selectbox(
                                    "📦 Copy Status",
                                    [
                                        "Available",
                                        "Lost"
                                    ]
                                )

                                submitted = st.form_submit_button(
                                    "💾 Finish Loan"
                                )

                                if submitted:

                                    result = update_loan(
                                        loan["loan_id"],
                                        copy_status
                                    )

                                    if result == "not_found":

                                        st.error(
                                            "❌ Die Ausleihe wurde nicht gefunden."
                                        )

                                    elif result == "already_closed":

                                        st.warning(
                                            "⚠️ Diese Ausleihe wurde bereits beendet."
                                        )

                                    elif result == "updated":

                                        st.success(
                                            "✅ Die Ausleihe wurde erfolgreich beendet."
                                        )

                                        st.session_state.pop(
                                            "edit_loan_id",
                                            None
                                        )

                                        st.rerun()
else:
    total_books, status_counts = get_book_statistics()

    card_col1, card_col2, card_col3, card_col4 = st.columns(4)

    with card_col1:
        st.markdown(
            f"""
            <div class="dashboard-card">
                <div class="card-icon">📚</div>
                <div class="card-title">Total Books</div>
                <div class="card-value">{total_books}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with card_col2:
        st.markdown(
            f"""
            <div class="dashboard-card">
                <div class="card-icon">🟢</div>
                <div class="card-title">Available Copies</div>
                <div class="card-value">{status_counts["Available"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with card_col3:
        st.markdown(
            f"""
            <div class="dashboard-card">
                <div class="card-icon">🔄</div>
                <div class="card-title">Borrowed Copies</div>
                <div class="card-value">{status_counts["Borrowed"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with card_col4:
        st.markdown(
            f"""
            <div class="dashboard-card">
                <div class="card-icon">🔴</div>
                <div class="card-title">Lost Copies</div>
                <div class="card-value">{status_counts["Lost"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


    card_col5, card_col6 = st.columns(2)

    with card_col5:
        st.markdown(
            f"""
            <div class="dashboard-card">
                <div class="card-icon">🚫</div>
                <div class="card-title">Not Available for Borrowing</div>
                <div class="card-value">{status_counts["Not available for borrowing"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with card_col6:
        st.markdown(
            f"""
            <div class="dashboard-card">
                <div class="card-icon">📕</div>
                <div class="card-title">Worn Out Copies</div>
                <div class="card-value">{status_counts["Worn out"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with st.container(key="dashboard_date_filter"):

        st.subheader("📅 Date Range")

        date_col1, date_col2 = st.columns(2)

        with date_col1:
            start_date = st.date_input(
                "From",
                value=pd.Timestamp("2026-01-01").date()
            )

        with date_col2:
            end_date = st.date_input(
                "To",
                value=pd.Timestamp.today().date()
            )
        loans_per_month = get_loans_per_month(
        start_date,
        end_date)
        loans_df = pd.DataFrame(loans_per_month)
        st.subheader("📚 Books Borrowed per Month")
        st.line_chart(
            loans_df,
            x="month",
            y="loan_count"
        )
        spending_per_month = get_spending_per_month(
            start_date,
            end_date
        )

        spending_df = pd.DataFrame(spending_per_month)
        st.subheader("💰 Monthly Spending")

        fig, ax = plt.subplots(figsize=(12, 5))

        bars = ax.bar(
            spending_df["month"],
            spending_df["spending"],
            color=[
                "#4E79A7",
                "#F28E2B",
                "#E15759",
                "#76B7B2",
                "#59A14F",
                "#EDC948",
                "#B07AA1",
                "#FF9DA7",
                "#9C755F"
            ]
        )

        for bar in bars:
            value = bar.get_height()

            ax.text(
                bar.get_x() + bar.get_width() / 2,
                value + 0.15,
                f"{value:.2f} €",
                ha="center",
                va="bottom",
                fontsize=10,
                fontweight="bold"
            )

        ax.set_xlabel("Month")
        ax.set_ylabel("Spending (€)")
        ax.set_title("Monthly Spending")

        plt.xticks(rotation=45)
        plt.tight_layout()

        st.pyplot(fig)
    overdue_loans = get_overdue_loans()

    overdue_df = pd.DataFrame(overdue_loans)
    st.subheader("🔄 Open Loans")
    # def color_days_remaining(value):
    #     if value > 0:
    #         return "color: green; font-weight: bold;"
    #     elif value < 0:
    #         return "color: red; font-weight: bold;"
    #     else:
    #         return "color: orange; font-weight: bold;"


    # Rename columns
    display_df = overdue_df.rename(
        columns={
            "title": "Book",
            "friend": "Friend",
            "loan_date": "Loan Date",
            "due_date": "Due Date",
            "days_remaining": "Days Remaining"
        }
    )

    # Build HTML table
    table_html = """
    <div class="dashboard-table">
    <table>
        <thead>
            <tr>
                <th>Book</th>
                <th>Friend</th>
                <th>Loan Date</th>
                <th>Due Date</th>
                <th>Days Remaining</th>
            </tr>
        </thead>
        <tbody>
    """

    for _, row in display_df.iterrows():

        days = int(row["Days Remaining"])

        if days > 0:
            days_class = "days-positive"
        elif days < 0:
            days_class = "days-negative"
        else:
            days_class = "days-today"
        table_html += f"""
            <tr>
                <td>{row["Book"]}</td>
                <td>{row["Friend"]}</td>
                <td>{row["Loan Date"]}</td>
                <td>{row["Due Date"]}</td>
                <td class="{days_class}">{days}</td>
            </tr>
        """

    table_html += """
        </tbody>
    </table>
    </div>
    """

    st.html(table_html)


    top_books = get_top_books()
    top_friends = get_top_friends()
    top_authors = get_top_authors()

    st.subheader("🏆 Top 5")

    top_col1, top_col2, top_col3 = st.columns(3)

    with top_col1:

        books_html = """
        <div class="top-card">
            <div class="top-card-title">📚 Top 5 Books</div>
        """

        medals = ["🥇", "🥈", "🥉", "4.", "5."]

        for position, book in enumerate(top_books):
            books_html += f"""
            <div class="top-row">
                <span class="top-name">
                    {medals[position]} {book['title']}
                </span>
                <span class="top-count">
                    {book['loan_count']}
                </span>
            </div>
            """

        books_html += "</div>"

        st.html(books_html)

    with top_col2:

        friends_html = """
        <div class="top-card">
            <div class="top-card-title">👥 Top 5 Friends</div>
        """

        for position, friend in enumerate(top_friends):
            friends_html += f"""
            <div class="top-row">
                <span class="top-name">
                    {medals[position]} {friend['friend']}
                </span>
                <span class="top-count">
                    {friend['loan_count']}
                </span>
            </div>
            """

        friends_html += "</div>"

        st.html(friends_html)

    with top_col3:

        authors_html = """
        <div class="top-card">
            <div class="top-card-title">✍️ Top 5 Authors</div>
        """

        for position, author in enumerate(top_authors):
            authors_html += f"""
            <div class="top-row">
                <span class="top-name">
                    {medals[position]} {author['author']}
                </span>
                <span class="top-count">
                    {author['loan_count']}
                </span>
            </div>
            """

        authors_html += "</div>"

        st.html(authors_html)


