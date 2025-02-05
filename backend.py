import planesections as ps
import matplotlib.pyplot as plt
import sys
import traceback

def analyze_beam(beam_length, forces_data, supports_data, distributed_loads):
    """Performs beam analysis and returns three figures and debug info."""
    debug_info = []  # List to collect debug information
    plt.close('all')
    
    try:
        debug_info.append("Starting beam analysis...")
        
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
        # Run analysis
        analysis = ps.OpenSeesAnalyzer2D(beam)
        analysis.runAnalysis()
        debug_info.append("Analysis completed")
        
        # Create beam diagram
        debug_info.append("Creating beam diagram...")
        plt.figure(figsize=(10, 4))
        ps.plotBeamDiagram(beam)
        plt.title('Configuration de la poutre')
        beam_fig = plt.gcf()
        debug_info.append(f"Beam figure created: {beam_fig.get_size_inches()}")
        
        # Create moment diagram
        debug_info.append("Creating moment diagram...")
        plt.figure(figsize=(10, 4))
        ps.plotMoment(beam)
        plt.title('Moment fléchissant')
        moment_fig = plt.gcf()
        debug_info.append(f"Moment figure created: {moment_fig.get_size_inches()}")
        
        # Create shear diagram
        debug_info.append("Creating shear diagram...")
        plt.figure(figsize=(10, 4))
        ps.plotShear(beam)
        plt.title('Effort tranchant')
        shear_fig = plt.gcf()
        debug_info.append(f"Shear figure created: {shear_fig.get_size_inches()}")
        
        return beam_fig, moment_fig, shear_fig, debug_info, None

    except Exception as e:
        error_info = {
            'error_type': str(type(e).__name__),
            'error_message': str(e),
            'traceback': traceback.format_exc()
        }
        debug_info.append(f"Error occurred: {error_info['error_type']}")
        debug_info.append(f"Error message: {error_info['error_message']}")
        plt.close('all')
        return None, None, None, debug_info, error_info