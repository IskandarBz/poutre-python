import planesections as ps
import matplotlib.pyplot as plt
from planesections.analysis import PyNiteAnalyzer2D

def analyze_beam(beam_length, forces_data, supports_data, distributed_loads):
    plt.close('all')
    
    try:

        beam = ps.newEulerBeam(beam_length)
        

        for force in forces_data:
            beam.addVerticalLoad(force['location'], force['strength'])
 

        for support in supports_data:
            beam.setFixity(support['location'], support['type'])


        for dl in distributed_loads:
            beam.addLinLoad(
                dl['x1'], 
                dl['x2'], 
                [[0.0, 0.0], [dl['q_start'], dl['q_end']]]
            )

        # Analyse
        analyzer = PyNiteAnalyzer2D(beam)
        analyzer.runAnalysis()
        
        # Creation des diagrammes
        plt.figure(figsize=(10, 4))
        ps.plotBeamDiagram(beam)
        plt.title('Configuration de la poutre')
        beam_fig = plt.gcf()
        
        plt.figure(figsize=(10, 4))
        ps.plotMoment(beam,labelPOI=True)
        plt.title('Moment fléchissant')
        moment_fig = plt.gcf()
        
        plt.figure(figsize=(10, 4))
        ps.plotShear(beam,labelPOI=True)
        plt.title('Effort tranchant')
        shear_fig = plt.gcf()
        
        return beam_fig, moment_fig, shear_fig

    except Exception as e:
        plt.close('all')
        raise e