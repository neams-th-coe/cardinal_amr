#----------------------------------------------------------------------------------------
# Assembly geometrical information
#----------------------------------------------------------------------------------------
pitch        = 1.25984
height       = 300.0
r_fuel       = 0.4715
t_gap        = 0.0150
r_clad_inner = 0.4865
t_clad       = 0.05
edge_length  =12.1705
#----------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------
# Meshing parameters
#----------------------------------------------------------------------------------------
NUM_SECTORS              = 6
FUEL_RADIAL_DIVISIONS    = 5  #how many radial segmentation of the fuel (UO2 will be )
BACKGROUND_DIVISIONS     = 3
AXIAL_DIVISIONS          = 6
#----------------------------------------------------------------------------------------


[Mesh]
    [Pin]
      type = PolygonConcentricCircleMeshGenerator
      num_sides = 6 #determine if that will be a square or hexagon=6  
      num_sectors_per_side = '${NUM_SECTORS} ${NUM_SECTORS} ${NUM_SECTORS} ${NUM_SECTORS} ${NUM_SECTORS} ${NUM_SECTORS}' #how many segmentation in one quadrant 
      ring_radii = '${r_fuel} ${fparse r_fuel + t_gap} ${fparse r_fuel + t_gap + t_clad}'  #fparse --> to the function  ' assigns the radius '
      ring_intervals = '${FUEL_RADIAL_DIVISIONS} 1 1'                                      #FUEL_RADIAL_DIVISION-->UO2 1 FOR GAS GAP 1 FOR CLADDING 
      polygon_size = ${fparse pitch / 2.0}
  
      ring_block_ids = '0 1 2 3'
      ring_block_names = 'fuel_center fuel gap cladding'
      
  
      flat_side_up = false
      quad_center_elements = false
      preserve_volumes = true
  
      create_outward_interface_boundaries = true
    []
    [Assembly_2D]
        type = PatternedHexMeshGenerator
        inputs = 'Pin'
        pattern ='0  0  0  0  0  0  0  0  0 ;
                0  0  0  0  0  0  0  0  0  0 ;
              0  0  0  0  0  0  0  0  0  0  0 ;
            0  0  0  0  0  0  0  0  0  0  0  0 ;
          0  0  0  0  0  0  0  0  0  0  0  0  0 ;
        0  0  0  0  0  0  0  0  0  0  0  0  0  0 ;
       0  0  0  0  0  0  0  0  0  0  0  0  0  0  0 ;
      0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0 ;
      0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0 ;
       0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0 ;
         0  0  0  0  0  0  0  0  0  0  0  0  0  0  0 ;
          0  0  0  0  0  0  0  0  0  0  0  0  0  0 ;
           0  0  0  0  0  0  0  0  0  0  0  0  0 ;
            0  0  0  0  0  0  0  0  0  0  0  0 ;
             0  0  0  0  0  0  0  0  0  0  0 ;
              0  0  0  0  0  0  0  0  0  0 ;
                0  0  0  0  0  0  0  0  0 '

         hexagon_size = '${fparse edge_length}'
    []
    [Assembly_3D]
        type = AdvancedExtruderGenerator
        input = 'Assembly_2D'
        heights = '${fparse height}'
        num_layers = '${AXIAL_DIVISIONS}'
        direction = '0.0 0.0 1.0'
    
        bottom_boundary = '10001'
        top_boundary = '10000'
      []
      [To_Origin]
        type = TransformGenerator
        input = 'Assembly_3D'
        transform = TRANSLATE_CENTER_ORIGIN
      []
      [Down]
        type = TransformGenerator
        input = 'To_Origin'
        transform = TRANSLATE
        vector_value = '0.0 0.0 ${fparse height / 2.0}'
      []
      
[]
