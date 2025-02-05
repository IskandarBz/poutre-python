import planesections as ps
import matplotlib.pyplot as plt
from planesections.analysis import PyNiteAnalyzer2D
import traceback

def analyze_beam(beam_length, forces_data, supports_data, distributed_loads):
    """Analyzes a 2D beam and returns the beam, moment, and shear diagrams."""
    plt.close('all')
    debug_info = []
    
    try:
        debug_info.append("Starting analysis...")
        
        # Initialize beam
        beam = ps.newEulerBeam(beam_length)
        debug_info.append(f"Beam initialized with length: {beam_length}")
        
        # Add loads
        for force in forces_data:
            beam.addVerticalLoad(force['location'], force['strength'])
            debug_info.append(f"Added force: {force['strength']} at {force['location']}")
 
        # Add supports
        for support in supports_data:
            beam.setFixity(support['location'], support['type'])
            debug_info.append(f"Added support: {support['type']} at {support['location']}")

        # Add distributed loads
        for dl in distributed_loads:
            beam.addLinLoad(
                dl['x1'], 
                dl['x2'], 
                [[0.0, 0.0], [dl['q_start'], dl['q_end']]]
            )
            debug_info.append(f"Added distributed load from {dl['x1']} to {dl['x2']}")

        debug_info.append("Running analysis...")
        # Analysis
        analyzer = PyNiteAnalyzer2D(beam)
        analyzer.runAnalysis()
        debug_info.append("Analysis completed")
        
        # Create diagrams with safe POI handling
        plt.figure(figsize=(10, 4))
        ps.plotBeamDiagram(beam)
        plt.title('Configuration de la poutre')
        beam_fig = plt.gcf()
        debug_info.append("Beam diagram created")
        
        # Create moment diagram with safe POI handling
        plt.figure(figsize=(10, 4))
        try:
            ps.plotMoment(beam, labelPOI=False)  # First try without POI labels
            debug_info.append("Basic moment diagram created")
            # If successful, try with POI labels
            plt.close()
            plt.figure(figsize=(10, 4))
            ps.plotMoment(beam, labelPOI=True)
        except:
            debug_info.append("Using fallback moment diagram without POI")
        plt.title('Moment fléchissant')
        moment_fig = plt.gcf()
        debug_info.append("Moment diagram created")
        
        # Create shear diagram with safe POI handling
        plt.figure(figsize=(10, 4))
        try:
            ps.plotShear(beam, labelPOI=False)  # First try without POI labels
            debug_info.append("Basic shear diagram created")
            # If successful, try with POI labels
            plt.close()
            plt.figure(figsize=(10, 4))
            ps.plotShear(beam, labelPOI=True)
        except:
            debug_info.append("Using fallback shear diagram without POI")
        plt.title('Effort tranchant')
        shear_fig = plt.gcf()
        debug_info.append("Shear diagram created")
        
        return beam_fig, moment_fig, shear_fig, debug_info, None

    except Exception as e:
        error_info = {
            'type': str(type(e).__name__),
            'message': str(e),
            'traceback': traceback.format_exc()
        }
        debug_info.append(f"Error occurred: {error_info['type']}")
        debug_info.append(f"Error message: {error_info['message']}")
        plt.close('all')
        return None, None, None, debug_info, error_info