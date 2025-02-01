import streamlit as st
from backend import analyze_beam
import matplotlib.pyplot as plt

# Initialize session state
if 'forces' not in st.session_state:
    st.session_state.forces = []

if 'supports' not in st.session_state:
    st.session_state.supports = []

if 'distributed_loads' not in st.session_state:  # New for distributed loads
    st.session_state.distributed_loads = []

# Page Configuration
st.set_page_config(page_title="Beam Analysis", layout="wide")
st.title("2D Beam Analysis Tool")

# Main Vertical Layout
with st.container():
    # Beam Length Input
    beam_length = st.number_input(
        "📏 Beam Length (m)",
        min_value=1.0,
        value=5.0,
        step=0.1,
        help="Total length of the beam between supports"
    )

    # Parallel Input Columns
    col_forces, col_supports = st.columns(2, gap="large")

    # Forces Input Column - Modified to include distributed loads
    with col_forces:
        with st.expander("🔽 Vertical Loads", expanded=True):
            # Point Loads Section
            st.markdown("**Point Loads**")
            # ... (keep existing point load inputs same)
            new_force_mag = st.number_input(
                "Force Magnitude (kN)", 
                value=-10.0,
                help="Negative values = downward forces",
                key="new_force_mag"
            )
            new_force_loc = st.number_input(
                "Force Location (m)", 
                0.0, beam_length, 2.0,
                key="new_force_loc"
            )
            
            if st.button("➕ Add Force", key="add_force"):
                st.session_state.forces.append({
                    'strength': new_force_mag,
                    'location': new_force_loc
                })
            
            # Current Forces Display
            st.markdown("**Current Forces**")
            for i, force in enumerate(st.session_state.forces):
                cols = st.columns([1, 3, 1])
                cols[0].markdown(f"F{i+1}:")
                cols[1].metric(
                    label="Magnitude & Location",
                    value=f"{abs(force['strength'])} kN {'↓' if force['strength']<0 else '↑'} @ {force['location']}m"
                )
                cols[2].button(
                    "❌", 
                    key=f"remove_force_{i}",
                    on_click=lambda i=i: st.session_state.forces.pop(i),
                    help="Remove this force"
                )
            
            # Distributed Loads Section
            st.markdown("---")
            st.markdown("**Distributed Loads**")
            
            col1, col2 = st.columns(2)
            with col1:
                x1 = st.number_input(
                    "Start Position (m)",
                    0.0, beam_length, 0.0,
                    key="dist_x1"
                )
                q_start = st.number_input(
                    "Start Magnitude (kN/m)",
                    value=-5.0,
                    key="dist_qstart"
                )
            with col2:
                x2 = st.number_input(
                    "End Position (m)",
                    x1, beam_length, beam_length,
                    key="dist_x2"
                )
                q_end = st.number_input(
                    "End Magnitude (kN/m)",
                    value=-5.0,
                    key="dist_qend"
                )
            
            if st.button("➕ Add Distributed Load"):
                st.session_state.distributed_loads.append({
                    'x1': x1,
                    'x2': x2,
                    'q_start': q_start,
                    'q_end': q_end
                })
            
            # Display current distributed loads
            st.markdown("**Current Distributed Loads**")
            for i, load in enumerate(st.session_state.distributed_loads):
                cols = st.columns([1, 3, 1])
                cols[0].markdown(f"DL{i+1}:")
                cols[1].metric(
                    label="Distribution",
                    value=f"{load['x1']}m to {load['x2']}m",
                    delta=f"{load['q_start']} → {load['q_end']} kN/m"
                )
                cols[2].button(
                    "❌", 
                    key=f"remove_dist_{i}",
                    on_click=lambda i=i: st.session_state.distributed_loads.pop(i),
                    help="Remove this distributed load"
                )


    # Supports Input Column
    with col_supports:
        with st.expander("🏗️ Supports", expanded=True):
            # Add Support Controls
            new_supp_type = st.selectbox(
                "Support Type", 
                ['pinned', 'roller', 'fixed'],
                key="new_supp_type",
                help="Single support must be 'fixed' type. Multiple supports can be any combination."
            )
            new_supp_loc = st.number_input(
                "Support Location (m)", 
                0.0, beam_length, 0.0,
                key="new_supp_loc"
            )
            
            if st.button("➕ Add Support", key="add_support"):
                st.session_state.supports.append({
                    'type': new_supp_type,
                    'location': new_supp_loc
                })
            
            # Current Supports Display
            st.markdown("**Current Supports**")
            for i, support in enumerate(st.session_state.supports):
                cols = st.columns([1, 3, 1])
                cols[0].markdown(f"S{i+1}:")
                cols[1].metric(
                    label="Type & Location",
                    value=f"{support['type'].title()} @ {support['location']}m"
                )
                cols[2].button(
                    "❌", 
                    key=f"remove_support_{i}",
                    on_click=lambda i=i: st.session_state.supports.pop(i),
                    help="Remove this support"
                )

    # Analysis Controls
    st.markdown("---")
    analyze_cols = st.columns([1, 2, 1])
    with analyze_cols[1]:
        analyze_btn = st.button(
            "🚀 Run Structural Analysis",
            type="primary",
            use_container_width=True
        )

    # Reset Button
    st.markdown("---")
    reset_cols = st.columns([1, 2, 1])
    with reset_cols[1]:
        if st.button("♻️ Reset All Inputs", use_container_width=True):
            st.session_state.forces = []
            st.session_state.supports = []
            st.session_state.distributed_loads = []  # Add this line
            st.rerun()

# Results Display
if analyze_btn:
    # New validation checks
    supports = st.session_state.supports
    if len(supports) == 1 and supports[0]['type'] != 'fixed':
        st.error("❌ Single support must be a fixed type!")
        st.stop()
    elif len(supports) == 0:
        st.error("❌ At least one support required!")
        st.stop()

    with st.spinner("Analyzing beam structure..."):
        try:
            beam_fig, moment_fig = analyze_beam(
                beam_length,
                st.session_state.forces,
                st.session_state.supports,
                st.session_state.distributed_loads
            )
            
            # Display Results
            result_col1, result_col2 = st.columns(2)
            
            with result_col1:
                with st.container(border=True):
                    st.markdown("### Beam Configuration")
                    st.pyplot(beam_fig)
                    plt.close(beam_fig)
                    st.caption("Shows applied loads and support conditions")
            
            with result_col2:
                with st.container(border=True):
                    st.markdown("### Bending Moment Diagram")
                    st.pyplot(moment_fig)
                    plt.close(moment_fig)
                    st.caption("Shows internal moment distribution along the beam")
            
            st.success("Analysis completed successfully!")

        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")
            plt.close('all')