import planesections as ps
import matplotlib.pyplot as plt

def analyze_beam(beam_length, forces_data, supports_data, distributed_loads):
    """Performs beam analysis and returns exactly two figures."""
    plt.close('all')  # Clean up any existing figures

    try:
        # Initialize beam
        beam = ps.newEulerBeam(beam_length)

        # Add loads
        for force in forces_data:
            beam.addVerticalLoad(force['location'], force['strength'])

        # Add supports
        support_mapping = {'free': 'free', 'roller': 'roller',
                          'pinned': 'pinned', 'fixed': 'fixed'}
        for support in supports_data:
            beam.setFixity(support['location'], support_mapping[support['type']])

        # Add distributed loads
        for dl in distributed_loads:
            beam.addLinLoad(
                dl['x1'],
                dl['x2'],
                [[0.0, 0.0], [dl['q_start'], dl['q_end']]]
            )

        # Create beam diagram
        fig_beam, ax_beam = plt.subplots()
        ps.plotBeamDiagram(beam, ax=ax_beam)
        ax_beam.set_title('Configuration de la poutre')

        # Run analysis
        analysis = ps.OpenSeesAnalyzer2D(beam)
        analysis.runAnalysis()

        # Create moment diagram
        fig_moment, ax_moment = plt.subplots()
        ps.plotMoment(beam, ax=ax_moment)
        ax_moment.set_title('Moment fléchissant')

        # Create shear diagram
        fig_shear, ax_shear = plt.subplots()
        ps.plotShear(beam, ax=ax_shear, labelPOI=True)
        ax_shear.set_title('Effort tranchant')

        return fig_beam, fig_moment, fig_shear

    except Exception as e:
        print(f"Analysis error: {e}")
        return None, None, None
