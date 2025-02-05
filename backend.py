import planesections as ps
import matplotlib.pyplot as plt

def analyze_beam(beam_length, forces_data, supports_data, distributed_loads):
    plt.close('all')
    
    try:
        # Initialize beam
        beam = ps.newEulerBeam(beam_length)
        
        # Create explicit figures for each plot
        beam_fig, beam_ax = plt.subplots()
        moment_fig, moment_ax = plt.subplots()
        shear_fig, shear_ax = plt.subplots()
        
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
        
        # Create beam diagram with explicit figure
        ps.plotBeamDiagram(beam, ax=beam_ax)
        beam_fig.suptitle('Configuration de la poutre')
        
        # Run analysis
        analysis = ps.OpenSeesAnalyzer2D(beam)
        analysis.runAnalysis()
        
        # Create moment diagram with explicit figure
        ps.plotMoment(beam, ax=moment_ax)
        moment_fig.suptitle('Moment fléchissant')
        
        # Create shear diagram with explicit figure
        ps.plotShear(beam, ax=shear_ax)
        shear_fig.suptitle('Effort tranchant')
        
        return beam_fig, moment_fig, shear_fig

    except Exception as e:
        print(f"Analysis error: {e}")
        return None, None, None