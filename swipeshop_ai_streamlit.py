# swipeshop_ai_streamlit.py
import streamlit as st
import requests
import random
import webbrowser
from typing import List, Dict

API_URL = "https://fakestoreapi.com/products"

@st.cache_data
def fetch_products() -> List[Dict]:
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        return [
            {
                "id": p["id"],
                "name": p["title"],
                "category": p["category"],
                "price": float(p["price"]),
                "image": p["image"],
                "checkout_url": f"https://fakestoreapi.com/cart/{p['id']}"
            }
            for p in data
        ]
    except Exception as e:
        st.error(f"Failed to fetch products: {e}")
        return []

def recommend_products(likes: List[Dict], all_products: List[Dict]) -> List[Dict]:
    if not likes:
        return random.sample(all_products, 3) if len(all_products) >= 3 else all_products
    
    cat_count = {}
    prices = []
    for p in likes:
        cat_count[p["category"]] = cat_count.get(p["category"], 0) + 1
        prices.append(p["price"])

    top_category = max(cat_count, key=cat_count.get)
    avg_price = sum(prices) / len(prices)

    filtered = [p for p in all_products if p["category"] == top_category and abs(p["price"] - avg_price) < 50]
    return filtered[:3] if filtered else random.sample(all_products, 3)

# Streamlit UI Setup
st.set_page_config(page_title="🛍️ SwipeShop AI", layout="centered")
st.title("🛍️ SwipeShop AI")
st.caption("Swipe to like or buy amazing products. Smart AI learns your taste!")

if "products" not in st.session_state:
    st.session_state.products = fetch_products()
    random.shuffle(st.session_state.products)

if "index" not in st.session_state:
    st.session_state.index = 0

if "likes" not in st.session_state:
    st.session_state.likes = []

if "purchases" not in st.session_state:
    st.session_state.purchases = []

# Show current product
if st.session_state.index < len(st.session_state.products):
    p = st.session_state.products[st.session_state.index]

    st.image(p["image"], width=300)
    st.subheader(p["name"])
    st.write(f"**Category**: {p['category']}")
    st.write(f"**Price**: ${p['price']}")

    cols = st.columns([1, 1, 1])
    with cols[0]:
        if st.button("❌ Skip"):
            st.session_state.index += 1
            st.experimental_rerun()
    with cols[1]:
        if st.button("❤️ Like"):
            st.session_state.likes.append(p)
            st.session_state.index += 1
            st.experimental_rerun()
    with cols[2]:
        if st.button("🛒 Buy Now"):
            st.session_state.purchases.append(p)
            webbrowser.open_new_tab(p["checkout_url"])

else:
    st.success("🎉 You're done swiping!")
    st.subheader("❤️ Liked Items")
    for p in st.session_state.likes:
        st.markdown(f"**{p['name']}** - ${p['price']}")
        st.image(p["image"], width=120)

    st.subheader("🛒 Purchases")
    for p in st.session_state.purchases:
        st.markdown(f"**{p['name']}** - ${p['price']}")
        st.image(p["image"], width=120)

    st.subheader("🤖 AI Recommendations")
    recs = recommend_products(st.session_state.likes, st.session_state.products)
    for r in recs:
        st.markdown(f"**{r['name']}** - ${r['price']}")
        st.image(r["image"], width=120)
        st.markdown(f"[Buy Now]({r['checkout_url']})", unsafe_allow_html=True)
