import planesections as ps
import matplotlib.pyplot as plt

def analyze_beam(beam_length, forces_data, supports_data,distributed_loads):
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
        ps.plotBeamDiagram(beam)
        beam_fig = plt.gcf()
        #beam_fig.set_size_inches(10, 4)
        plt.title('Configuration de la poutre')

        # Run analysis
        analysis = ps.OpenSeesAnalyzer2D(beam)
        analysis.runAnalysis()
        
        # Create moment diagram
        plt.figure()  # Explicit new figure
        ps.plotMoment(beam)
        moment_fig = plt.gcf()
        #moment_fig.set_size_inches(10, 4)
        plt.title('Moment fléchissant')
        # Create shear diagram
        plt.figure()  # New figure for shear
        ps.plotShear(beam)
        shear_diagram_fig = plt.gcf()
        plt.title('Effort tranchant')
        
        return beam_fig, moment_fig, shear_diagram_fig

    except Exception as e:
        print(f"Analysis error: {e}")
        return None, None, None