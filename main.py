import numpy as np
import io_process
import checking_shapes
import make_curve
import regularization
import symmetry

polylines = []
polylines = io_process.read_csv("problems/isolated.csv")
# polylines = io_process.read_csv("problems/occlusion1.csv")
# polylines = io_process.read_csv("problems/occlusion2.csv")
# polylines = io_process.read_csv("problems/frag1.csv")
# polylines = io_process.read_csv("problems/frag2.csv")


# creating the model 
shape_operations = checking_shapes.Shapes() 





regularized_polylines =[]
for polyline_i in polylines:
    temp_polyline =[]
    for sub_polyline_j in polyline_i:
        sub_polyline_j = regularization.remove_outliers(sub_polyline_j)
        p = shape_operations.check_shape(polyline=sub_polyline_j) 
        print(p) 
        if p!="unknown":
            sub_polyline_j = make_curve.make_curve(p,sub_polyline_j) 
            sub_polyline_j = regularization.regularize(sub_polyline_j,1)
        else :
            sub_polyline_j = regularization.regularize(sub_polyline_j,1)

            # TODO 1: Now check the symmetry 
            # sub_polyline_j = symmetry.process_points(sub_polyline_j) 
            # TODO 2: after symmetry check do complete the shape this is the last task
            sub_polyline_j = regularization.regularize(sub_polyline_j,1)

        temp_polyline.append(sub_polyline_j) 
    
    # TODO 3:check if polyline collectively form something or not

    regularized_polylines.append(temp_polyline) 
io_process.plot_two_sets(regularized_polylines,polylines)
        