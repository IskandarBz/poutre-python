import planesections as ps
import matplotlib.pyplot as plt

def analyze_beam(beam_length, forces_data, supports_data, distributed_loads):
    """Performs beam analysis and returns three figures."""
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

        # Run analysis first
        analysis = ps.OpenSeesAnalyzer2D(beam)
        analysis.runAnalysis()
        
        # Create beam diagram
        plt.figure(figsize=(10, 4))
        ps.plotBeamDiagram(beam)
        plt.title('Configuration de la poutre')
        beam_fig = plt.gcf()
        
        print("Beam diagram created")
        print(f"Beam figure size: {beam_fig.get_size_inches()}")
        print(f"Number of axes: {len(beam_fig.axes)}")

        # Create moment diagram
        plt.figure(figsize=(10, 4))
        ps.plotMoment(beam)
        plt.title('Moment fléchissant')
        moment_fig = plt.gcf()
        print("Beam diagram created")
        print(f"Beam figure size: {moment_fig.get_size_inches()}")
        print(f"Number of axes: {len(moment_fig.axes)}")
        # Create shear diagram
        plt.figure(figsize=(10, 4))
        ps.plotShear(beam)
        plt.title('Effort tranchant')
        shear_fig = plt.gcf()
        print("Beam diagram created")
        print(f"Beam figure size: {shear_fig.get_size_inches()}")
        print(f"Number of axes: {len(shear_fig.axes)}")
        return beam_fig, moment_fig, shear_fig

    except Exception as e:
        print(f"Analysis error: {e}")
        plt.close('all')
        return None, None, None