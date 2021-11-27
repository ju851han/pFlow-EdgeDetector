# pFlow-Map-Creator

## About
The pFlowMapCreator is a lightweight, python-based editor for creating maps 
for pFlow.

## Developed under versions
- Python 3.8.8
- [PyGimli 1.2.1](https://www.pygimli.org)

### To get PyGimli
`conda create -n pg -c gimli -c conda-forge pygimli=1.2.1`

`conda activate pg`

## Performance test pipeline
- main.py - Draw a map, generate a mesh and export it
- point generator - Three files will be created
    - **middle_points.txt** A file with the coordinates of one point per 
      one triangle in the meshing. Given point will always be in the
      middle of the triangle.
    - **random-points.txt** Same as above but the points are in a random
      location inside the triangle and not in the middle anymore
    - **random_points_random_triangles.txt** A defined amount of points
      in a randomly chosen triangle. Define in **point_generator.py**
       `amount_of_random_generated_triangles`
      