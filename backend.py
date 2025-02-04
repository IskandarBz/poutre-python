import planesections as ps
import matplotlib.pyplot as plt

def analyze_beam(beam_length, forces_data, supports_data, distributed_loads):
    plt.close('all')
    try:
        beam = ps.newEulerBeam(beam_length)
        
        # Ajout des charges
        for force in forces_data:
            beam.addVerticalLoad(force['location'], force['strength'])
        
        # Ajout des charges réparties
        for dl in distributed_loads:
            beam.addLinLoad(dl['x1'], dl['x2'], [[0.0, 0.0], [dl['q_start'], dl['q_end']]])
        
        # Conversion des appuis français vers anglais
        support_mapping = {'Articulé': 'pinned', 'Rouleau': 'roller', 'Encastré': 'fixed'}
        for support in supports_data:
            beam.setFixity(support['location'], support_mapping[support['type']])
        
        # Création des figures
        # Create Matplotlib figures explicitly
        fig_beam, ax_beam = plt.subplots()
        fig_moment, ax_moment = plt.subplots()
        fig_shear, ax_shear = plt.subplots()

        # Plot beam diagram
        ax_beam.set_title("Configuration de la poutre")
        ax_beam.set_xlabel("Position (m)")
        ax_beam.set_ylabel("Charge (kN)")
        # Add your beam plotting logic here
        # Example: ax_beam.plot([0, beam_length], [0, 0], color="black")

        # Plot moment diagram
        ax_moment.set_title("Moment fléchissant")
        ax_moment.set_xlabel("Position (m)")
        ax_moment.set_ylabel("Moment (kNm)")
        # Add your moment plotting logic here
        # Example: ax_moment.plot(x_values, moment_values)

        # Plot shear diagram
        ax_shear.set_title("Effort tranchant")
        ax_shear.set_xlabel("Position (m)")
        ax_shear.set_ylabel("Effort (kN)")
        # Add your shear plotting logic here
        # Example: ax_shear.plot(x_values, shear_values)

        # Return the figures
        return fig_beam, fig_moment, fig_shear

    except Exception as e:
        print(f"Erreur backend : {str(e)}")
        return None, None, None