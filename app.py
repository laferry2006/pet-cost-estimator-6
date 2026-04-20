"""
Pet Cost Estimator - Streamlit App
==================================
Interactive pet cost estimator with card-based selection and popup results
"""

import streamlit as st
import pandas as pd
import json
import plotly.graph_objects as go

# ============ PAGE CONFIG ============
st.set_page_config(
    page_title="Pet Cost Estimator",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============ CSS ============
st.markdown("""
<style>
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Header */
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 0.3rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #888;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Pet Cards */
    .pet-card {
        background: linear-gradient(135deg, #fff 0%, #f8f9ff 100%);
        border: 2px solid #e8e8f0;
        border-radius: 20px;
        padding: 2rem 1rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        height: 100%;
    }
    .pet-card:hover {
        border-color: #667eea;
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(102,126,234,0.2);
    }
    .pet-card.selected {
        border-color: #667eea;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    .pet-emoji {
        font-size: 4rem;
        margin-bottom: 0.5rem;
    }
    .pet-name {
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 0.3rem;
    }
    .pet-sub {
        font-size: 0.85rem;
        color: #888;
    }
    .pet-card.selected .pet-sub {
        color: rgba(255,255,255,0.8);
    }
    
    /* Sub-type Cards */
    .subtype-card {
        background: #fff;
        border: 2px solid #eee;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s;
    }
    .subtype-card:hover {
        border-color: #FF6B6B;
        transform: scale(1.03);
        box-shadow: 0 8px 20px rgba(255,107,107,0.15);
    }
    .subtype-card.selected {
        border-color: #FF6B6B;
        background: linear-gradient(135deg, #FF6B6B 0%, #ee5a5a 100%);
        color: white;
    }
    
    /* Region Cards */
    .region-card {
        background: #fff;
        border: 2px solid #eee;
        border-radius: 16px;
        padding: 1.2rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s;
    }
    .region-card:hover {
        border-color: #4ECDC4;
        transform: scale(1.03);
        box-shadow: 0 8px 20px rgba(78,205,196,0.15);
    }
    .region-card.selected {
        border-color: #4ECDC4;
        background: linear-gradient(135deg, #4ECDC4 0%, #44b3ab 100%);
        color: white;
    }
    
    /* Step Title */
    .step-title {
        font-size: 1.4rem;
        font-weight: bold;
        color: #333;
        margin: 2rem 0 1rem 0;
        text-align: center;
    }
    .step-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        width: 32px;
        height: 32px;
        border-radius: 50%;
        text-align: center;
        line-height: 32px;
        font-size: 0.9rem;
        margin-right: 0.5rem;
    }
    
    /* Back Button */
    .back-btn {
        color: #667eea;
        cursor: pointer;
        font-size: 0.95rem;
        margin-bottom: 1rem;
    }
    .back-btn:hover {
        color: #764ba2;
    }
    
    /* Result Popup */
    .result-overlay {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 24px;
        padding: 3rem;
        color: white;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 20px 60px rgba(102,126,234,0.35);
        animation: slideDown 0.5s ease;
    }
    @keyframes slideDown {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Advice Cards */
    .advice-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #eef0f3 100%);
        padding: 1.3rem;
        border-radius: 14px;
        border-top: 4px solid #667eea;
        margin: 0.4rem 0;
    }
    .advice-card h4 {
        margin-bottom: 0.5rem;
        color: #333;
    }
    
    /* Section divider */
    .section-line {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #ddd, transparent);
        margin: 2rem 0;
    }
    
    /* Sliders */
    .slider-box {
        background: #fff;
        border: 1px solid #e8e8f0;
        border-radius: 14px;
        padding: 1rem 1.5rem;
        text-align: center;
    }
    
    /* Calculate Button */
    .stButton > button {
        background: linear-gradient(135deg, #FF6B6B 0%, #ee5a5a 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 1rem 3rem !important;
        font-size: 1.3rem !important;
        font-weight: bold !important;
        box-shadow: 0 8px 25px rgba(255,107,107,0.35) !important;
    }
    .stButton > button:hover {
        transform: scale(1.03) !important;
        box-shadow: 0 12px 35px rgba(255,107,107,0.45) !important;
    }
    
    /* Pet name input */
    .name-input {
        max-width: 400px;
        margin: 0 auto;
    }
</style>
""", unsafe_allow_html=True)

# ============ DATA ============
@st.cache_data
def load_data():
    with open('pet_price_data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

data = load_data()

PET_DATA = {
    'Cat': {
        'emoji': '🐱',
        'color': '#FF9F43',
        'sub': {'Short-haired Cat': 'British, Siamese', 'Long-haired Cat': 'Ragdoll, Persian'}
    },
    'Dog': {
        'emoji': '🐶',
        'color': '#FF6B6B',
        'sub': {'Small Dog': 'Poodle, Chihuahua', 'Medium Dog': 'Corgi, Shiba', 'Large Dog': 'Golden, Husky'}
    },
    'Fish': {
        'emoji': '🐠',
        'color': '#4ECDC4',
        'sub': {'fish': 'Tropical, Goldfish'}
    },
    'Bird': {
        'emoji': '🦜',
        'color': '#45B7D1',
        'sub': {'bird': 'Parrot, Finch'}
    },
    'Hamster': {
        'emoji': '🐹',
        'color': '#96CEB4',
        'sub': {'hamster': 'Syrian, Dwarf'}
    },
    'Rabbit': {
        'emoji': '🐰',
        'color': '#DDA0DD',
        'sub': {'rabbit': 'Lop, Dwarf'}
    },
    'Reptile': {
        'emoji': '🦎',
        'color': '#8FBC8F',
        'sub': {'Reptile': 'Gecko, Snake'}
    }
}

REGIONS = {
    'North America': {'emoji': '🌎', 'desc': 'High cost', 'mult': 1.35},
    'Europe': {'emoji': '🌍', 'desc': 'High cost', 'mult': 1.25},
    'Oceania': {'emoji': '🌏', 'desc': 'High cost', 'mult': 1.30},
    'Asia': {'emoji': '🌏', 'desc': 'Medium cost', 'mult': 0.85},
    'South America': {'emoji': '🌎', 'desc': 'Lower cost', 'mult': 0.75},
    'Africa': {'emoji': '🌍', 'desc': 'Lower cost', 'mult': 0.65},
    'Antarctica': {'emoji': '🧊', 'desc': 'Extreme cost', 'mult': 2.00}
}

CATEGORY_ICONS = {'Grooming': '🛁', 'Food': '🍖', 'Toys & Supplies': '🎾', 'Medical': '💊'}

PET_TIPS = {
    'Short-haired Cat': {
        'grooming': 'Low-maintenance! Weekly brushing is enough. Bathing rarely needed.',
        'food': 'High-protein diet essential. Consider wet food for hydration.',
        'supplies': 'Quality scratching post, interactive toys, cat tree.',
        'medical': 'Regular vaccinations. Watch for dental issues.'
    },
    'Long-haired Cat': {
        'grooming': 'Daily brushing to prevent matting. Professional groom every 6-8 weeks.',
        'food': 'Omega fatty acids for coat health. Watch for hairballs.',
        'supplies': 'Detangling brushes, multiple scratching posts.',
        'medical': 'Watch for skin issues under fur. Regular dental care.'
    },
    'Small Dog': {
        'grooming': 'Professional grooming every 4-6 weeks.',
        'food': 'Small breed kibble. Dental chews recommended.',
        'supplies': 'Harness for walks, small toys, cozy bed.',
        'medical': 'Watch for dental disease, patellar issues.'
    },
    'Medium Dog': {
        'grooming': 'Brush 2-3x/week. Professional groom for long-haired.',
        'food': 'Balanced diet matching activity level.',
        'supplies': 'Durable toys, outdoor gear for exercise.',
        'medical': 'Hip dysplasia screening. Keep vaccinations current.'
    },
    'Large Dog': {
        'grooming': 'Regular brushing, especially shedding season.',
        'food': 'Large breed formula for joint health. Budget for higher food intake.',
        'supplies': 'Heavy-duty toys, large bed, sturdy leash.',
        'medical': 'Hip/elbow screening essential. Bloat prevention with slow feeders.'
    },
    'fish': {
        'grooming': 'Weekly water changes, filter cleaning, algae control.',
        'food': 'Species-specific flakes/pellets. Avoid overfeeding!',
        'supplies': 'Quality filter, heater, water testing kit.',
        'medical': 'Quarantine new fish. Monitor pH and ammonia levels.'
    },
    'bird': {
        'grooming': 'Regular wing/nail trims. Bathing via mist or shallow dish.',
        'food': 'Pelleted diet + fresh fruits/veg. No avocado (toxic)!',
        'supplies': 'Large cage, varied perches, foraging toys.',
        'medical': 'Annual avian vet visit. Watch for respiratory issues.'
    },
    'hamster': {
        'grooming': 'Minimal grooming. Sand bath for dwarfs. Clean cage weekly.',
        'food': 'Hamster pellets + occasional treats. They hoard food!',
        'supplies': 'Spacious cage, exercise wheel, deep bedding, hideouts.',
        'medical': '2-3 year lifespan. Watch for wet tail (stress illness).'
    },
    'rabbit': {
        'grooming': 'Regular brushing. Nail trims every 4-6 weeks.',
        'food': 'Unlimited hay essential! Fresh veg daily. No iceberg lettuce.',
        'supplies': 'Large enclosure, litter box, chew toys.',
        'medical': 'Spay/neuter recommended. Watch for GI stasis - critical!'
    },
    'Reptile': {
        'grooming': 'Enclosure cleaning. UVB light replacement every 6-12 months.',
        'food': 'Live insects/rodents/veg + calcium supplements.',
        'supplies': 'Heating gradient, UVB lighting, hides, humidity control.',
        'medical': 'Find exotic vet first. Prevent metabolic bone disease with UVB.'
    }
}

# ============ SESSION STATE ============
def init_state():
    defaults = {
        'step': 1,
        'pet_category': None,
        'pet_type': None,
        'region': None,
        'pet_name': '',
        'show_result': False,
        'multipliers': {'Grooming': 1.0, 'Food': 1.0, 'Toys & Supplies': 1.0, 'Medical': 1.0}
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ============ HEADER ============
st.markdown('<p class="main-header">🐾 Pet Cost Estimator</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Pick a pet, choose your region, and see your annual cost instantly!</p>', unsafe_allow_html=True)

# ============ RESULT POPUP (at top) ============
if st.session_state.show_result and st.session_state.pet_type:
    pet = st.session_state.pet_type
    region = st.session_state.region
    name = st.session_state.pet_name.strip() or pet
    
    region_data = data['region_data'].get(region, {})
    pet_data = region_data.get(pet, {})
    if not pet_data:
        pet_data = data['global_data'].get(pet, {})
    
    monthly = {}
    for cat in ['Grooming', 'Food', 'Toys & Supplies', 'Medical']:
        base = pet_data.get(cat, {}).get('avg_price', 30)
        monthly[cat] = round(base * st.session_state.multipliers[cat], 2)
    
    monthly_total = sum(monthly.values())
    annual = monthly_total * 12
    
    # ===== RESULT OVERLAY =====
    st.markdown(f"""
    <div class="result-overlay">
        <div style="font-size: 5rem; margin-bottom: 0.5rem;">{PET_DATA.get(st.session_state.pet_category, {}).get('emoji', '🐾')}</div>
        <h2 style="margin: 0;">💝 {name}'s Annual Cost</h2>
        <h1 style="font-size: 5rem; margin: 0.5rem 0; color: #FFD93D;">${annual:,.0f}</h1>
        <p style="font-size: 1.1rem; opacity: 0.9;">
            {REGIONS[region]['emoji']} {region} | ${monthly_total:,.0f}/month
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Charts
    c1, c2 = st.columns([1, 1])
    with c1:
        df_cost = pd.DataFrame({
            'Category': list(monthly.keys()),
            'Monthly': [f"${v:,.0f}" for v in monthly.values()],
            'Level': [f"{st.session_state.multipliers[k]:.1f}x" for k in monthly.keys()]
        })
        st.dataframe(df_cost, hide_index=True, use_container_width=True)
    
    with c2:
        fig = go.Figure(data=[go.Pie(
            labels=list(monthly.keys()), values=list(monthly.values()),
            hole=0.45, marker_colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'],
            textinfo='label+percent', textfont_size=12
        )])
        fig.update_layout(showlegend=False, margin=dict(t=5,b=5,l=5,r=5), height=250)
        st.plotly_chart(fig, use_container_width=True)
    
    # Personalized Tips
    st.markdown("<hr class='section-line'>", unsafe_allow_html=True)
    st.markdown(f"<p class='step-title'>💡 Tips for {name} ({pet})</p>", unsafe_allow_html=True)
    
    tips = PET_TIPS.get(pet, PET_TIPS['Short-haired Cat'])
    t1, t2 = st.columns(2)
    with t1:
        for icon, key in [('🛁', 'grooming'), ('🍖', 'food')]:
            st.markdown(f"""
            <div class="advice-card">
                <h4>{icon} {key.title()}</h4>
                <p style="font-size:0.9rem;">{tips[key]}</p>
            </div>
            """, unsafe_allow_html=True)
    with t2:
        for icon, key in [('🎾', 'supplies'), ('💊', 'medical')]:
            st.markdown(f"""
            <div class="advice-card">
                <h4>{icon} {key.title()}</h4>
                <p style="font-size:0.9rem;">{tips[key]}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Recalculate / Start Over
    st.markdown("<hr class='section-line'>", unsafe_allow_html=True)
    if st.button("🔄 Start Over", use_container_width=True):
        st.session_state.step = 1
        st.session_state.show_result = False
        st.session_state.pet_category = None
        st.session_state.pet_type = None
        st.session_state.region = None
        st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)

# ============ STEP 1: PET NAME ============
st.markdown("<hr class='section-line'>", unsafe_allow_html=True)
st.markdown("<p class='step-title'><span class='step-badge'>1</span> Name Your Pet (Optional)</p>", unsafe_allow_html=True)

name_col, _ = st.columns([2, 3])
with name_col:
    st.session_state.pet_name = st.text_input("Pet name", value=st.session_state.pet_name, 
                                               placeholder="e.g. Luna, Max...", label_visibility="collapsed")

# ============ STEP 2: PET CATEGORY CARDS ============
st.markdown("<hr class='section-line'>", unsafe_allow_html=True)
st.markdown("<p class='step-title'><span class='step-badge'>2</span> Choose Your Pet</p>", unsafe_allow_html=True)

# Show pet category cards in grid
cols = st.columns(4)
for idx, (key, info) in enumerate(PET_DATA.items()):
    with cols[idx % 4]:
        is_selected = st.session_state.pet_category == key
        card_class = "pet-card selected" if is_selected else "pet-card"
        
        # Use a container to make the whole area clickable
        with st.container():
            st.markdown(f"""
            <div class="{card_class}" id="pet-{key}">
                <div class="pet-emoji">{info['emoji']}</div>
                <div class="pet-name">{key}</div>
                <div class="pet-sub">{len(info['sub'])} type{'s' if len(info['sub']) > 1 else ''}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Hidden button for click handling
            if st.button(f"Select {key}", key=f"btn_cat_{key}", use_container_width=True):
                st.session_state.pet_category = key
                st.session_state.pet_type = None
                st.session_state.show_result = False
                st.rerun()

# ============ STEP 2B: SUBTYPE SELECTION ============
if st.session_state.pet_category:
    cat = st.session_state.pet_category
    subs = PET_DATA[cat]['sub']
    
    if len(subs) > 1:
        st.markdown(f"<p style='text-align:center;color:#666;margin:1rem 0;'>👆 Select a {cat} type:</p>", unsafe_allow_html=True)
        sub_cols = st.columns(len(subs))
        for idx, (sub_key, sub_desc) in enumerate(subs.items()):
            with sub_cols[idx]:
                is_sub_sel = st.session_state.pet_type == sub_key
                sc = "subtype-card selected" if is_sub_sel else "subtype-card"
                
                st.markdown(f"""
                <div class="{sc}">
                    <div style="font-size:2.5rem;margin-bottom:0.3rem;">{PET_DATA[cat]['emoji']}</div>
                    <div style="font-weight:bold;">{sub_key}</div>
                    <div style="font-size:0.8rem;color:#888;">{sub_desc}</div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Pick {sub_key}", key=f"btn_sub_{sub_key}", use_container_width=True):
                    st.session_state.pet_type = sub_key
                    st.session_state.show_result = False
                    st.rerun()
    else:
        # Auto-select if only one option
        only_sub = list(subs.keys())[0]
        if st.session_state.pet_type != only_sub:
            st.session_state.pet_type = only_sub

# ============ STEP 3: REGION CARDS ============
if st.session_state.pet_type:
    st.markdown("<hr class='section-line'>", unsafe_allow_html=True)
    st.markdown("<p class='step-title'><span class='step-badge'>3</span> Choose Your Continent</p>", unsafe_allow_html=True)
    
    reg_cols = st.columns(4)
    for idx, (reg_key, reg_info) in enumerate(REGIONS.items()):
        with reg_cols[idx % 4]:
            is_reg_sel = st.session_state.region == reg_key
            rc = "region-card selected" if is_reg_sel else "region-card"
            
            st.markdown(f"""
            <div class="{rc}">
                <div style="font-size:2.5rem;margin-bottom:0.3rem;">{reg_info['emoji']}</div>
                <div style="font-weight:bold;">{reg_key}</div>
                <div style="font-size:0.75rem;">{reg_info['desc']}</div>
                <div style="font-size:0.8rem;margin-top:0.3rem;">{reg_info['mult']}x</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Pick {reg_key}", key=f"btn_reg_{reg_key}", use_container_width=True):
                st.session_state.region = reg_key
                st.session_state.show_result = False
                st.rerun()

# ============ STEP 4: SLIDERS ============
if st.session_state.region:
    st.markdown("<hr class='section-line'>", unsafe_allow_html=True)
    st.markdown("<p class='step-title'><span class='step-badge'>4</span> Adjust Spending</p>", unsafe_allow_html=True)
    
    slider_cols = st.columns(4)
    for idx, cat in enumerate(['Grooming', 'Food', 'Toys & Supplies', 'Medical']):
        with slider_cols[idx]:
            st.markdown(f"<div class='slider-box'>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:2rem;'>{CATEGORY_ICONS[cat]}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-weight:bold;font-size:0.95rem;'>{cat}</div>", unsafe_allow_html=True)
            
            val = st.slider(cat, 0.5, 2.0, st.session_state.multipliers[cat], 0.1, 
                           key=f"sl_{cat}", label_visibility="collapsed")
            st.session_state.multipliers[cat] = val
            
            if val < 0.8:
                badge = "🟢 Basic"
            elif val < 1.2:
                badge = "🔵 Standard"
            else:
                badge = "🔴 Premium"
            st.markdown(f"<div style='font-size:0.8rem;color:#888;'>{badge} ({val:.1f}x)</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
    
    # ============ CALCULATE BUTTON ============
    st.markdown("<br>", unsafe_allow_html=True)
    calc_col, _ = st.columns([2, 3])
    with calc_col:
        if st.button("💰 Calculate Annual Cost!", use_container_width=True):
            st.session_state.show_result = True
            st.rerun()

# ============ DEFAULT VIEW (no selections yet) ============
if not st.session_state.pet_category:
    st.markdown("<hr class='section-line'>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center;padding:2rem;color:#888;">
        <div style="font-size:3rem;margin-bottom:1rem;">👆</div>
        <p style="font-size:1.1rem;">Tap a pet card above to get started!</p>
    </div>
    """, unsafe_allow_html=True)

# ============ FOOTER ============
st.markdown("<hr class='section-line'>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;color:#bbb;padding:1rem;font-size:0.85rem;">
    🐾 Pet Cost Estimator | Data: Kaggle Pet Store Records 2020 | 💵 USD | 🌍 7 Continents
</div>
""", unsafe_allow_html=True)
