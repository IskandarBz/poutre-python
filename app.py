import streamlit as st
from backend import analyze_beam
import matplotlib.pyplot as plt
import sys
import planesections as ps

# This MUST be the first Streamlit command
st.set_page_config(page_title="Outil d'Analyse de Poutre 2D", layout="wide")
# Initialisation de l'état de session
if 'forces' not in st.session_state:
    st.session_state.forces = []

if 'supports' not in st.session_state:
    st.session_state.supports = []

if 'distributed_loads' not in st.session_state:
    st.session_state.distributed_loads = []

# Configuration de la page

st.title("Outil d'Analyse de Poutre 2D")

# Disposition verticale principale
with st.container():
    # Entrée de la longueur de la poutre
    beam_length = st.number_input(
        "📏 Longueur de la poutre (m)",
        min_value=1.0,
        value=5.0,
        step=0.1,
        help="Longueur totale de la poutre entre les appuis"
    )

    # Colonnes d'entrée parallèles
    col_forces, col_supports = st.columns(2, gap="large")

    # Colonne des forces
    with col_forces:
        with st.expander("🔽 Charges verticales", expanded=True):
            # Contrôles d'ajout de force
            new_force_mag = st.number_input(
                "Intensité de la charge (kN)",
                value=-10.0,
                help="Les valeurs négatives représentent des charges vers le bas",
                key="new_force_mag"
            )
            new_force_loc = st.number_input(
                "Position de la charge (m)",
                0.0, beam_length, 2.0 if beam_length >= 2.0 else beam_length,
                key="new_force_loc"
            )

            if st.button("➕ Ajouter une charge", key="add_force"):
                st.session_state.forces.append({
                    'strength': new_force_mag,
                    'location': new_force_loc
                })

            # Affichage des charges actuelles
            st.markdown("**Charges ponctuelles**")
            for i, force in enumerate(st.session_state.forces):
                cols = st.columns([1, 3, 1])
                cols[0].markdown(f"F{i+1}:")
                cols[1].metric(
                    label="Intensité et position",
                    value=f"{abs(force['strength'])} kN {'↓' if force['strength']<0 else '↑'} à {force['location']}m"
                )
                cols[2].button(
                    "❌",
                    key=f"remove_force_{i}",
                    on_click=lambda i=i: st.session_state.forces.pop(i),
                    help="Supprimer cette charge"
                )

            # Section des charges réparties
            st.markdown("---")
            st.markdown("**Charges réparties**")

            col1, col2 = st.columns(2)
            with col1:
                x1 = st.number_input(
                    "Position de début (m)",
                    0.0, beam_length, 0.0,
                    key="dist_x1"
                )
                q_start = st.number_input(
                    "Intensité initiale (kN/m)",
                    value=-5.0,
                    key="dist_qstart"
                )
            with col2:
                x2 = st.number_input(
                    "Position de fin (m)",
                    x1, beam_length, beam_length,
                    key="dist_x2"
                )
                q_end = st.number_input(
                    "Intensité finale (kN/m)",
                    value=-5.0,
                    key="dist_qend"
                )

            if st.button("➕ Ajouter une charge répartie"):
                st.session_state.distributed_loads.append({
                    'x1': x1,
                    'x2': x2,
                    'q_start': q_start,
                    'q_end': q_end
                })

            # Affichage des charges réparties
            st.markdown("**Charges réparties actuelles**")
            for i, load in enumerate(st.session_state.distributed_loads):
                cols = st.columns([1, 3, 1])
                cols[0].markdown(f"CR{i+1}:")
                cols[1].metric(
                    label="Répartition",
                    value=f"{load['x1']}m à {load['x2']}m",
                    delta=f"{load['q_start']} → {load['q_end']} kN/m"
                )
                cols[2].button(
                    "❌",
                    key=f"remove_dist_{i}",
                    on_click=lambda i=i: st.session_state.distributed_loads.pop(i),
                    help="Supprimer cette charge répartie"
                )

    # Colonne des appuis
    with col_supports:
        with st.expander("🏗️ Appuis", expanded=True):
            # Contrôles d'ajout d'appui
            new_supp_type = st.selectbox(
                "Type d'appui",
                ['pinned', 'roller', 'fixed'],
                key="new_supp_type",
                help="Un seul appui doit être de type fixe. Les appuis multiples peuvent être combinés."
            )
            new_supp_loc = st.number_input(
                "Position de l'appui (m)",
                min_value=0.0,
                max_value=beam_length,  # Bloque les valeurs > longueur poutre
                value=0.0,
                key="new_supp_loc"
            )

            if st.button("➕ Add Support", key="add_support"):
                if any(s['location'] == new_supp_loc for s in st.session_state.supports):
                    st.warning("Un appui existe déja à cette position!")
                elif new_supp_loc > beam_length:
                    st.warning("❌ La position de l'appui ne peut pas dépasser la longueur de la poutre !")
                else:
                    st.session_state.supports.append({
                        'type': new_supp_type,
                        'location': new_supp_loc
                    })

            # Affichage des appuis actuels
            st.markdown("**Appuis actuels**")
            for i, support in enumerate(st.session_state.supports):
                cols = st.columns([1, 3, 1])
                cols[0].markdown(f"A{i+1}:")
                cols[1].metric(
                    label="Type et position",
                    value=f"{support['type'].title()} à {support['location']}m"
                )
                cols[2].button(
                    "❌",
                    key=f"remove_support_{i}",
                    on_click=lambda i=i: st.session_state.supports.pop(i),
                    help="Supprimer cet appui"
                )

    # Contrôles d'analyse
    st.markdown("---")
    analyze_cols = st.columns([1, 2, 1])
    with analyze_cols[1]:
        analyze_btn = st.button(
            "🚀 Lancer l'analyse structurelle",
            type="primary",
            use_container_width=True
        )

    # Bouton de réinitialisation
    st.markdown("---")
    reset_cols = st.columns([1, 2, 1])
    with reset_cols[1]:
        if st.button("♻️ Réinitialiser toutes les entrées", use_container_width=True):
            st.session_state.forces = []
            st.session_state.supports = []
            st.session_state.distributed_loads = []
            st.rerun()

# Affichage des résultats
if analyze_btn:
    with st.expander("Environment Information", expanded=False):
        st.write(f"Python version: {sys.version}")
        # Get package version safely
        try:
            from importlib.metadata import version
            ps_version = version('planesections')
            st.write(f"Planesections version: {ps_version}")
        except:
            st.write("Planesections version: Unknown")
    # Vérifications de validation
    supports = st.session_state.supports

    invalid_supports = [s for s in supports if s['location'] > beam_length]
    if invalid_supports:
        st.error("❌ Appuis invalides détectés :")
        for supp in invalid_supports:
            st.markdown(f"- {supp['type'].title()} à {supp['location']}m (max autorisé : {beam_length}m)")
        st.stop()

    if len(supports) == 1 and supports[0]['type'] != 'fixed':
        st.error("❌ Un seul appui doit être de type encastré !")
        st.stop()
    elif len(supports) == 0:
        st.error("❌ Au moins un appui est requis !")
        st.stop()

    invalid_forces = [f for f in st.session_state.forces if f['location'] > beam_length]
    if invalid_forces:
        st.error("❌ Charges invalides détectées :")
        for force in invalid_forces:
            st.markdown(f"- {force['strength']} kN à {force['location']}m (max autorisé : {beam_length}m)")
        st.stop()

    invalid_distributed_loads = [dl for dl in st.session_state.distributed_loads if dl['x1'] > beam_length or dl['x2'] > beam_length]
    if invalid_distributed_loads:
        st.error("❌ Charges réparties invalides détectées :")
        for load in invalid_distributed_loads:
            st.markdown(f"- De {load['x1']}m à {load['x2']}m (max autorisé : {beam_length}m)")
        st.stop()

    with st.spinner("Analyse de la structure de la poutre..."):
        try:
            beam_fig, moment_fig, shear_fig, debug_info, error_info = analyze_beam(
                beam_length,
                st.session_state.forces,
                st.session_state.supports,
                st.session_state.distributed_loads
            )

            # Display debug information in an expander
            with st.expander("Debug Information", expanded=error_info is not None):
                st.write("### Debug Log")
                for info in debug_info:
                    st.text(info)
                
                if error_info:
                    st.error("### Error Details")
                    st.code(error_info['traceback'])

            if all(fig is not None for fig in [beam_fig, moment_fig, shear_fig]):
                result_col1, result_col2, result_col3 = st.columns(3)

                with result_col1:
                    with st.container(border=True):
                        st.markdown("### Configuration de la poutre")
                        st.pyplot(beam_fig)

                with result_col2:
                    with st.container(border=True):
                        st.markdown("### Moment fléchissant")
                        st.pyplot(moment_fig)

                with result_col3:
                    with st.container(border=True):
                        st.markdown("### Effort tranchant")
                        st.pyplot(shear_fig)

                st.success("Analyse terminée avec succès !")

            else:
                st.error("Erreur lors de la génération des diagrammes")

        except Exception as e:
            st.error(f"Échec de l'analyse : {str(e)}")
        finally:
            plt.close('all')