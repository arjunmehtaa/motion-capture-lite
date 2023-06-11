# Refer to https://math.stackexchange.com/questions/1725790/calculate-third-point-of-triangle-from-two-points-and-angles

import math

def get_tag_location(beamer_angles, beamer_positions):
  
  # Check if data is valid
  if len(beamer_angles) < 2:
    print("Data from atleast 2 beamers required. Aborting...")
    return

  # 2D location
  elif len(beamer_angles) == 2:
    
    # Extract angles of known beamers
    angle_b1 = beamer_angles[0]
    angle_b2 = beamer_angles[1]
    
    # Extract positions of known beamers
    pos_b1 = beamer_positions[0]
    pos_b2 = beamer_positions[1]
    
    # Compute the two possible solutions 
    res1 = compute_2d_coordinates(angle_b1, angle_b2, pos_b1, pos_b2)
    res2 = compute_2d_coordinates(angle_b2, angle_b1, pos_b2, pos_b1)
    
    return [res1, res2]
    
  # 3D location
  else:
    print("TODO")

def compute_2d_coordinates(angle_b1, angle_b2, pos_b1, pos_b2):
  
  # Extract coordinates of known points
  x1, y1 = pos_b1
  x2, y2 = pos_b2
  
  # Compute x and y offset
  u = x2 - x1
  v = y2 - y1
  
  # Compute distance between given points
  distance = math.sqrt(u**2 + v**2)
  
  # Convert angles to radians and find 3rd angle
  a1 = math.radians(angle_b1)
  a2 = math.radians(angle_b2)
  a3 = math.pi - a1 - a2
  
  # Set up equations
  l = distance * (math.sin(a2) / math.sin(a3))
  RHS1 = (x1 * u) + (y1 * v) + (l * distance * math.cos(a1))
  RHS2 = (y2 * u) - (x2 * v) - (l * distance * math.sin(a1))
  
  # Calculate coordinates of third point
  x3 = (1 / distance**2) * ((u * RHS1) - (v * RHS2))
  y3 = (1 / distance**2) * ((v * RHS1) + (u * RHS2))
  
  return (x3, y3)
