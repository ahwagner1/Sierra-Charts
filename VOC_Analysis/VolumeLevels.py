from VolDeltaLevelsLibrary import (plot_vol_and_delta, get_delta_levels, get_volume_levels)

#input paths
es_data = ""
nq_data = ""
cl_data = ""
gc_data = ""

# output paths
es_vol_path = ""
es_delta_path = ""

nq_vol_path = ""
nq_delta_path = ""

cl_vol_path = ""
cl_delta_path = ""

gc_vol_path = ""
gc_delta_path = ""



plot_vol_and_delta(es_data, "ES")
es_vol_threshold = int(input("Enter threshold for ES volume level: "))
es_delta_threshold = int(input("Enter threshold for ES delta level: "))

plot_vol_and_delta(nq_data, "NQ")
nq_vol_threshold = int(input("Enter threshold for NQ volume level: "))
nq_delta_threshold = int(input("Enter threshold for NQ delta level: "))

plot_vol_and_delta(cl_data, "CL")
cl_vol_threshold = int(input("Enter threshold for CL volume level: "))
cl_delta_threshold = int(input("Enter threshold for CL delta level: "))

plot_vol_and_delta(gc_data, "GC")
gc_vol_threshold = int(input("Enter threshold for GC volume level: "))
gc_delta_threshold = int(input("Enter threshold for GC delta level: "))

get_volume_levels(es_data, es_vol_path, es_vol_threshold)
get_delta_levels(es_data, es_delta_path, es_delta_threshold)

get_volume_levels(nq_data, nq_vol_path, nq_vol_threshold)
get_delta_levels(nq_data, nq_delta_path, nq_delta_threshold)

get_volume_levels(cl_data, cl_vol_path, cl_vol_threshold)
get_delta_levels(cl_data, cl_delta_path, cl_delta_threshold)

get_volume_levels(gc_data, gc_vol_path, gc_vol_threshold)
get_delta_levels(gc_data, gc_delta_path, gc_delta_threshold)

